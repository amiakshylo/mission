import json
import os
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np

from goal_task_management.models import GoalSuggestionLog, Goal

MODEL_PATH = "trained_models/goal_prediction_model.pth"
OUTPUT_SIZE_PATH = "trained_models/output_size.json"


class GoalPredictionModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(GoalPredictionModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.dropout1 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.dropout2 = nn.Dropout(0.5)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.dropout1(x)
        x = torch.relu(self.fc2(x))
        x = self.dropout2(x)
        x = self.fc3(x)
        return x


def validate_model_output_size():
    current_goal_count = Goal.objects.count()
    output_size = get_output_size()  # This should be the number of classes the model was trained on

    if current_goal_count != output_size:
        print(f"Number of goals has changed from {output_size} to {current_goal_count}. Retraining the model.")
        train_pytorch_model()  # Retrain the model with the new goal count
        model = load_trained_model()  # Reload the model
        return model
    else:
        print("Model output size is consistent with current goals.")
        return load_trained_model()


def reverse_goal_mapping(predicted_idx):
    """
    Reverse map the predicted index to the actual goal ID.
    """
    unique_goals = list(Goal.objects.values_list('id', flat=True).order_by('id'))
    if predicted_idx < len(unique_goals):
        return unique_goals[predicted_idx]
    else:
        print(f"Predicted index {predicted_idx} is out of bounds for goal list size {len(unique_goals)}.")
        return None


def get_output_size():
    """
    Retrieve the output size from the saved model configuration.
    """
    if os.path.exists(OUTPUT_SIZE_PATH):
        with open(OUTPUT_SIZE_PATH, 'r') as f:
            config = json.load(f)
            return config.get('output_size', None)
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
        gender_map = {'M': 1, 'F': 2, 'O': 3, 'PNS': 4}
        gender = gender_map.get(log.user_profile.gender, -1)
        roles = [role.id for role in log.user_profile.roles.all()]
        if not roles:
            continue
        row = {'age': age, 'gender': gender, 'goal_id': log.goal.id if log.goal else None,
               'age_gender_interaction': age * gender}
        for i, role_id in enumerate(roles):
            row[f'role_{i + 1}'] = role_id
        data.append(row)

    df = pd.DataFrame(data)
    df = df.dropna(subset=['goal_id'])
    return df


def init_weights(m):
    if isinstance(m, nn.Linear):
        nn.init.kaiming_normal_(m.weight, nonlinearity='relu')
        if m.bias is not None:
            nn.init.constant_(m.bias, 0)


def train_pytorch_model(model_path=MODEL_PATH):
    logs = GoalSuggestionLog.objects.all()

    data = preprocess_logs(logs)

    if data.empty:
        print("No data available to train the model.")
        return None

    X = data.drop('goal_id', axis=1).values
    y = data['goal_id'].values

    unique_goals = np.unique(y)
    goal_mapping = {goal_id: idx for idx, goal_id in enumerate(unique_goals)}
    y_mapped = np.array([goal_mapping[goal_id] for goal_id in y])

    model = GoalPredictionModel(input_size=X.shape[1], hidden_size=128, output_size=len(unique_goals))

    # Initialize weights carefully
    model.apply(init_weights)

    # Define the optimizer with a lower learning rate
    optimizer = optim.Adam(model.parameters(), lr=0.0001)

    criterion = nn.CrossEntropyLoss()

    X_tensor = torch.tensor(X, dtype=torch.float32)
    y_tensor = torch.tensor(y_mapped, dtype=torch.long)

    epochs = 100
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(X_tensor)
        loss = criterion(outputs, y_tensor)

        if torch.isnan(loss):
            print("Encountered NaN loss at epoch:", epoch)
            break  # Stop training if nan loss is encountered

        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)  # Clip gradients
        optimizer.step()

        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}')

    torch.save(model.state_dict(), model_path)
    print(f'Model saved to {model_path}')

    # Save the output size (number of unique goals)
    with open(OUTPUT_SIZE_PATH, 'w') as f:
        json.dump({'output_size': len(unique_goals)}, f)

    return model


def load_trained_model():
    """
    Load the trained PyTorch model from disk.
    """
    if os.path.exists(OUTPUT_SIZE_PATH):
        with open(OUTPUT_SIZE_PATH, 'r') as f:
            config = json.load(f)
            output_size = config['output_size']
    else:
        print(f"No configuration file found at {OUTPUT_SIZE_PATH}.")
        return None

    input_size = 13  # This should match the input size during training
    hidden_size = 128
    model = GoalPredictionModel(input_size=input_size, hidden_size=hidden_size, output_size=output_size)

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


def preprocess_user_data(user_profile, role):
    """
    Prepare the user's data for prediction.

    Returns:
    - torch.Tensor: Processed data ready for model prediction.
    """
    age = user_profile.get_age()
    gender_map = {'M': 1, 'F': 2, 'O': 3, 'PNS': 4}
    gender = gender_map.get(user_profile.gender, -1)

    # Collect the user's roles as a list of role IDs (integers)
    roles = [r.id for r in user_profile.roles.all()]

    # Define the input size expected by the model
    expected_input_size = 13  # Update this to match your model's expected input size

    # Calculate the number of padding needed
    padding_needed = max(0, expected_input_size - 2 - len(roles))  # Subtract 2 for age and gender

    # Pad the roles with zeros if fewer than the expected number, or trim if too many
    roles_padded = roles[:expected_input_size - 2] + [0] * padding_needed

    # Combine all features
    user_data = [age, gender] + roles_padded

    # Ensure the length matches the expected input size
    if len(user_data) > expected_input_size:
        user_data = user_data[:expected_input_size]
    elif len(user_data) < expected_input_size:
        user_data += [0] * (expected_input_size - len(user_data))

    # Convert list to tensor
    user_data_tensor = torch.tensor([user_data], dtype=torch.float32)

    return user_data_tensor
