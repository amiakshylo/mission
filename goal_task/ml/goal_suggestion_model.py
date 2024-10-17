import json
import os

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim

from goal_task.models import GoalSuggestionLog, Goal

MODEL_PATH = "trained_models/goal_prediction_model.pth"
OUTPUT_SIZE_PATH = "trained_models/output_size.json"


class GoalPredictionModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(GoalPredictionModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def reverse_goal_mapping(predicted_idx):
    """
    Reverse map the predicted index to the actual goal ID.
    This assumes that the goals are indexed in the order they were loaded into the model.
    """
    # Get the list of unique goal IDs in the order they were indexed
    unique_goals = list(Goal.objects.values_list("id", flat=True).order_by("id"))

    if predicted_idx < len(unique_goals):
        return unique_goals[predicted_idx]
    else:
        print(
            f"Predicted index {predicted_idx} is out of bounds for goal list size {len(unique_goals)}."
        )
        return None


def get_output_size():
    """
    Retrieve the output size from the saved model configuration.
    """
    if os.path.exists(OUTPUT_SIZE_PATH):
        with open(OUTPUT_SIZE_PATH, "r") as f:
            config = json.load(f)
            return config.get("output_size", None)
    else:
        print(f"No configuration file found at {OUTPUT_SIZE_PATH}.")
        return None


def preprocess_logs(logs):
    """
    Convert logs into a structured DataFrame suitable for model training.
    """
    data = []
    for log in logs:
        age = log.user_profile.get_age()
        gender_map = {"M": 1, "F": 2, "O": 3, "PNS": 4}
        gender = gender_map.get(log.user_profile.gender, -1)
        roles = [role.id for role in log.user_profile.roles.all()]
        if not roles:
            continue
        row = {
            "age": age,
            "gender": gender,
            "goal_id": log.goal.id if log.goal else None,
            "age_gender_interaction": age * gender,
        }
        for i, role_id in enumerate(roles):
            row[f"role_{i + 1}"] = role_id
        data.append(row)

    df = pd.DataFrame(data)
    df = df.dropna(subset=["goal_id"])
    return df


def train_pytorch_model():
    logs = GoalSuggestionLog.objects.all()

    data = preprocess_logs(logs)

    if data.empty:
        print("No data available to train the model.")
        return None

    X = data.drop("goal_id", axis=1).values
    y = data["goal_id"].values

    unique_goals = np.unique(y)
    goal_mapping = {goal_id: idx for idx, goal_id in enumerate(unique_goals)}
    y_mapped = np.array([goal_mapping[goal_id] for goal_id in y])

    input_size = X.shape[1]
    output_size = len(unique_goals)

    model = GoalPredictionModel(
        input_size=input_size, hidden_size=128, output_size=output_size
    )

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    X_tensor = torch.tensor(X, dtype=torch.float32)
    y_tensor = torch.tensor(y_mapped, dtype=torch.long)

    epochs = 100
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(X_tensor)
        loss = criterion(outputs, y_tensor)
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}")

    torch.save(model.state_dict(), MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    # Save the output size (number of unique goals)
    with open(OUTPUT_SIZE_PATH, "w") as f:
        json.dump({"output_size": output_size}, f)

    return model


def load_trained_model():
    """
    Load the trained PyTorch model from disk.
    """
    if os.path.exists(OUTPUT_SIZE_PATH):
        with open(OUTPUT_SIZE_PATH, "r") as f:
            config = json.load(f)
            output_size = config["output_size"]
    else:
        print(f"No configuration file found at {OUTPUT_SIZE_PATH}.")
        return None

    input_size = 13  # This should match the input size during training
    hidden_size = 128
    model = GoalPredictionModel(
        input_size=input_size, hidden_size=hidden_size, output_size=output_size
    )

    if os.path.exists(MODEL_PATH):
        try:
            model.load_state_dict(torch.load(MODEL_PATH))
            print(f"Model loaded from {MODEL_PATH} with output size {output_size}")
            model.eval()  # Set the model to evaluation mode
            return model
        except Exception as e:
            print(f"Failed to load model: {e}")
            return None
    else:
        print(f"No model found at {MODEL_PATH}. You need to train and save it first.")
        return None


def preprocess_user_data(user_profile, expected_role_count=10):
    """
    Preprocess user data to ensure it has a consistent number of features.
    """
    age = user_profile.get_age()
    gender_map = {"M": 1, "F": 2, "O": 3, "PNS": 4}
    gender = gender_map.get(user_profile.gender, -1)

    # Collect the user's roles
    roles = [role.id for role in user_profile.roles.all()]

    # Pad the roles list to ensure it has exactly `expected_role_count` roles
    if len(roles) < expected_role_count:
        roles += [0] * (expected_role_count - len(roles))  # Pad with zeros
    else:
        roles = roles[:expected_role_count]  # Truncate if more than expected

    # Prepare user data
    user_data = [age, gender, age * gender] + roles

    # Convert list to tensor
    user_data_tensor = torch.tensor([user_data], dtype=torch.float32)

    return user_data_tensor
