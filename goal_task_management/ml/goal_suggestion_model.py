import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MultiLabelBinarizer
from goal_task_management.models import GoalSuggestionLog


def preprocess_logs(logs):
    """
    Convert GoalSuggestionLog queryset into a pandas DataFrame for model training,
    with Multi-Hot Encoding for user roles and direct age handling.
    """
    data = []

    for log in logs:
        print(f"Processing log: {log}")
        age = log.user_profile.get_age()
        gender = log.user_profile.gender_encoded

        # Collect all roles for Multi-Hot Encoding
        roles = [role.name for role in log.user_profile.roles.all()]
        print(f"Roles for user: {roles}")

        data.append({
            'age': age,
            'gender': gender,
            'roles': roles,
            'goal_id': log.goal.id
        })

    df = pd.DataFrame(data)
    print("DataFrame before encoding:", df.head())  # Add this line

    if not df.empty:
        mlb = MultiLabelBinarizer()
        roles_encoded = mlb.fit_transform(df['roles'])
        roles_encoded_df = pd.DataFrame(roles_encoded, columns=mlb.classes_)
        df = pd.concat([df.drop(columns=['roles']), roles_encoded_df], axis=1)
    else:
        print("No data available for encoding.")

    print("DataFrame after encoding:", df.head())  # Add this line
    return df


def train_model():
    """
    Train a logistic regression model on the goal suggestion data.
    """
    # Fetch data from GoalSuggestionLog
    logs = GoalSuggestionLog.objects.all()
    data = preprocess_logs(logs)

    if data.empty:
        print("No data available to train the model.")
        return None

    # Prepare the data
    X = data.drop('goal_id', axis=1)
    y = data['goal_id']

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f'Model Accuracy: {accuracy * 100:.2f}%')

    return model


def predict_goal(model, user_profile):
    """
    Predict a goal for a user based on their profile using a trained model.
    """
    # Get the user's age directly
    age = user_profile.get_age()

    # Prepare user data for prediction
    user_data = {
        'age': age,
        'gender': user_profile.gender_encoded,
        'roles': [role.name for role in user_profile.roles.all()]
    }

    # Convert user data to DataFrame for prediction
    user_data_df = pd.DataFrame([user_data])

    # Multi-Hot Encode the roles for the prediction data
    mlb = MultiLabelBinarizer()
    roles_encoded = mlb.fit_transform([user_data['roles']])
    roles_encoded_df = pd.DataFrame(roles_encoded, columns=mlb.classes_)

    # Combine with other user data
    user_data_df = pd.concat([user_data_df.drop(columns=['roles']), roles_encoded_df], axis=1)

    # Predict the goal based on user data
    prediction = model.predict(user_data_df)
    return prediction
