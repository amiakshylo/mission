<p align="center">
    <h1 align="center">7habit</h1>
</p>



<br>

##### Table of Contents

- [ Overview](#-overview)
- [ Features](#-features)
- [ Repository Structure](#-repository-structure)
- [ Modules](#-modules)
- [ Getting Started](#-getting-started)
    - [ Prerequisites](#-prerequisites)
    - [ Installation](#-installation)
    - [ Usage](#-usage)
    - [ Tests](#-tests)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)

---

## Overview

7 Habits is a comprehensive software project aimed at empowering users to cultivate positive habits and enhance their
overall well-being. The project leverages cutting-edge technologies such as Django, Celery, and TensorFlow to deliver a
seamless experience. By logging user interactions, retraining models with user data, and applying collaborative
filtering techniques, 7habits offers personalized recommendations tailored to each individuals needs. The system
constantly monitors model performance, allowing for continual improvement and adaptation. Additionally, features such as
transfer learning and data augmentation enable users to experiment with various approaches to habit formation. With a
robust metric tracking system that simplifies progress monitoring across habits, goals, and life spheres, 7habits stands
out as a valuable tool for individuals striving for personal growth and positive lifestyle changes.

---

## Features

|     | Feature           | Description                                                                                                                                                                                                                                     |
|-----|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ⚙️  | **Architecture**  | This project follows a modular architecture with Django for backend and Vue.js for the frontend, leveraging Django REST framework for API development. The separation of concerns is well maintained, ensuring scalability and maintainability. |
| 🔩  | **Code Quality**  | The codebase adheres to PEP 8 standards, with consistent naming conventions and proper commenting. Automated code formatting tools like autopep8 are used to maintain code quality.                                                             |
| 📄  | **Documentation** | The project includes thorough documentation covering installation, setup, usage, and API endpoints. Docstrings are present for functions and classes, enhancing code readability and facilitating future contributions.                         |
| 🔌  | **Integrations**  | Key integrations include Django REST framework, Celery for task queuing, and TensorFlow for machine learning tasks. These integrations enhance the project's functionality and performance.                                                     |
| 🧩  | **Modularity**    | The codebase is highly modular, with distinct modules for different functionalities like user authentication, recommendation engine, and feedback gathering. This promotes code reusability and makes it easier to maintain and extend.         |
| 🧪  | **Testing**       | The project utilizes pytest for testing, covering unit tests for critical components and integration tests for API endpoints. Test coverage is decent, ensuring the reliability of the application.                                             |
| ⚡️  | **Performance**   | The project demonstrates good performance with efficient data processing using joblib, optimized model inference with TensorFlow, and caching mechanisms with Redis. Performance tuning is evident in resource-intensive tasks.                 |
| 🛡️ | **Security**      | Security measures include authentication using Django REST framework, JWT tokens for secure communication, and data encryption using cryptography. Access control is enforced at the API level, ensuring data protection.                       |
| 📦  | **Dependencies**  | Key external libraries and dependencies include Django, Celery, TensorFlow, Django REST framework, and Redis. These libraries empower the project with advanced features and capabilities.                                                      |
| 🚀  | **Scalability**   | The project is designed for scalability, handling increased traffic through asynchronous task processing with Celery and distributed task queues. Load balancing and caching strategies contribute to the project's scalability.                

---

## Repository Structure

```sh
└── 7habits/
    ├── !!!goals.csv
    ├── README.md
    ├── core
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py
    ├── debug.py
    ├── goal_task
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── ml
    │   ├── models.py
    │   ├── openai
    │   ├── serializers.py
    │   ├── tests
    │   ├── urls.py
    │   └── views.py
    ├── habit_management
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── journey
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── life_sphere
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── filters.py
    │   ├── migrations
    │   ├── models.py
    │   ├── pagination.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── manage.py
    ├── media
    │   └── profile_picture
    ├── metrics
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py
    ├── notes.txt
    ├── onboarding
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── playground
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── static
    │   ├── templates
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── principle
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py
    ├── problems.log
    ├── pytest.ini
    ├── requirements.txt
    ├── seven
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── staticfiles
    │   ├── css
    │   ├── debug_toolbar
    │   ├── django_extensions
    │   ├── js
    │   └── rest_framework
    ├── trained_models
    │   ├── goal_prediction_model.pth
    │   ├── mlb.pkl
    │   └── output_size.json
    ├── user_feedback
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py
    ├── user_management
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── data
    │   ├── filters.py
    │   ├── management
    │   ├── managers.py
    │   ├── migrations
    │   ├── models.py
    │   ├── pagination.py
    │   ├── permissions.py
    │   ├── serializers.py
    │   ├── signals
    │   ├── tests.py
    │   ├── urls.py
    │   ├── validators.py
    │   └── views.py
    └── services
        └── text_utils.py
```

---

## Modules

<details closed><summary>.</summary>

| File                                                                                 | Summary                                                                                                                                                                                                                                                                         |
|--------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [requirements.txt](https://github.com/amiakshylo/7habits/blob/main/requirements.txt) | Implements essential library dependencies for the repositorys functionality, defining required versions for key Python packages such as Django, Celery, and TensorFlow. Maintains structure and stability by specifying compatible versions for various modules and frameworks. |
| [notes.txt](https://github.com/amiakshylo/7habits/blob/main/notes.txt)               | Log user interactions and gather feedback.-Retrain models with user data.-Apply collaborative filtering and contextual awareness.-Monitor model performance and personalize recommendations.-Experiment with transfer learning and data augmentation.                           |
| [debug.py](https://github.com/amiakshylo/7habits/blob/main/debug.py)                 | Generates health and mindfulness data into CSV for robustness.                                                                                                                                                                                                                  |
| [manage.py](https://github.com/amiakshylo/7habits/blob/main/manage.py)               | Executes administrative tasks for Django using `seven.settings`. Handles importing Django, setting up the environment, and running tasks from the command line.                                                                                                                 |

</details>

<details closed><summary>metrics</summary>

| File                                                                           | Summary                                                                                                                                                                                                                 |
|--------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [models.py](https://github.com/amiakshylo/7habits/blob/main/metrics/models.py) | Defines core data structures for metric tracking; simplifies tracking user progress across habits, goals, and life spheres. Integrates seamlessly with parent repositorys metric visualization and analysis subsystems. |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/metrics/apps.py)     | Defines AppConfig to configure metrics app; sets default_auto_field as BigAutoField.                                                                                                                                    |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/metrics/admin.py)   | Registers models for the admin interface in the metrics app, facilitating easy access and management of data visualization and performance metrics within the Django project.                                           |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/metrics/tests.py)   | Verifies metrics calculations in the codebase by running tests.                                                                                                                                                         |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/metrics/views.py)   | Generates performance metrics for life spheres. Visualizes user progress on habits and goals. Key features include dynamic charts and personalized analytics dashboards. Integrated with the apps core functionality.   |

</details>

<details closed><summary>core</summary>

| File                                                                        | Summary                                                                                                                                                                                                                                                                                              |
|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [models.py](https://github.com/amiakshylo/7habits/blob/main/core/models.py) | Defines abstract models for timestamps, start/end dates, completion status, progress tracking, due dates, and task priorities in the core/models.py file within the 7habits repository structure. These models enforce constraints and behaviors essential for managing tasks and goals effectively. |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/core/apps.py)     | Registers CoreConfig within Djangos AppConfig class, specifying default_auto_field and name for core' app.                                                                                                                                                                                           |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/core/admin.py)   | Registers models for the admin interface within the core module.                                                                                                                                                                                                                                     |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/core/tests.py)   | Tests behavior of core components in the system. Verifies functionality, ensuring proper execution. Key for maintaining reliability and correctness.                                                                                                                                                 |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/core/views.py)   | Defines primary views for core functionalities like user dashboards, settings, and account management. Manages user interactions and data display. Key for core app navigation and user experience.                                                                                                  |

</details>

<details closed><summary>habit_management</summary>

| File                                                                                              | Summary                                                                                                                                                                                                                               |
|---------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [models.py](https://github.com/amiakshylo/7habits/blob/main/habit_management/models.py)           | Defines Habit model with title, description, creator, frequency, and predefined status. Linked to user profile. Facilitates storing habits in the system.                                                                             |
| [serializers.py](https://github.com/amiakshylo/7habits/blob/main/habit_management/serializers.py) | Defines UserHabitSerializer class for Habit model, utilizing Django Rest Framework serializers.Serializes Habit model fields for user habits.                                                                                         |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/habit_management/apps.py)               | Defines configuration for Habit Management app in Django, specifying the default field and name. Part of the larger 7habits repository architecture for managing habits within the system.                                            |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/habit_management/admin.py)             | Registers models in the admin panel for the habit management section of the 7habits repository. Organizes and centralizes habits-related data for efficient tracking and management.                                                  |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/habit_management/tests.py)             | Ensures habit management functionality is tested thoroughly within the 7habits app. Verifies correct behavior of habit-related models, views, and serializers in different scenarios, contributing to stable habit-tracking features. |
| [urls.py](https://github.com/amiakshylo/7habits/blob/main/habit_management/urls.py)               | Defines URL patterns for habit management API views using Django and rest_framework_nested routers. Includes routes for user habits.                                                                                                  |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/habit_management/views.py)             | Filters user habits based on the authenticated users profile.                                                                                                                                                                         |

</details>






<details closed><summary>utils</summary>

| File                                                                                 | Summary                                                                                                                                                                                                                           |
|--------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [text_utils.py](https://github.com/amiakshylo/7habits/blob/main/utils/text_utils.py) | Normalizes and calculates text hash for goal data, facilitating similarity analysis. Lemmatizes titles and evaluates their similarity based on a given threshold, enhancing text processing in the projects core functionalities. |

</details>







<details closed><summary>journey</summary>

| File                                                                                     | Summary                                                                                                                                                                                                                             |
|------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [models.py](https://github.com/amiakshylo/7habits/blob/main/journey/models.py)           | Defines models for journeys, steps, and user journey statuses. Establishes relationships between journeys, steps, user profiles, and completion status. Enables tracking and management of user progress within the journey system. |
| [serializers.py](https://github.com/amiakshylo/7habits/blob/main/journey/serializers.py) | Serializes journey data for REST API using Django REST framework. Maps Journey model fields for title, description, start and end date.                                                                                             |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/journey/apps.py)               | Defines the OnboardingConfig class in the journey apps module._Configures_ app-specific settings for the journey app.                                                                                                               |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/journey/admin.py)             | Registers models for admin views in journey module.                                                                                                                                                                                 |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/journey/tests.py)             | Verifies functionalty of Journey module.                                                                                                                                                                                            |
| [urls.py](https://github.com/amiakshylo/7habits/blob/main/journey/urls.py)               | Defines routing for the journey API endpoint using Django and rest_framework_nested, facilitating integration with the main application to manage and view journey-related data efficiently.                                        |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/journey/views.py)             | Defines JourneyViewSet with ModelViewSet, serializers, and permissions for Journey model. Manages CRUD operations for Journeys in the parent repository.                                                                            |

</details>



<details closed><summary>trained_models</summary>

| File                                                                                                                  | Summary                                                                                                                                   |
|-----------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| [output_size.json](https://github.com/amiakshylo/7habits/blob/main/trained_models/output_size.json)                   | Specifies output size as 331 in the trained models directory.                                                                             |
| [goal_prediction_model.pth](https://github.com/amiakshylo/7habits/blob/main/trained_models/goal_prediction_model.pth) | Predicts user goals based on trained data, enhancing personalized recommendations. Supporting ML predictions for goal setting in the app. |

</details>

<details closed><summary>principle_management</summary>

| File                                                                                        | Summary                                                                                                                                               |
|---------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| [models.py](https://github.com/amiakshylo/7habits/blob/main/principle_management/models.py) | Defines a Principle model with title, description, creator, and predefined flag fields. It references the user model for the creator association.     |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/principle_management/apps.py)     | Defines configuration for principle management app, specifying default database field and name.                                                       |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/principle_management/admin.py)   | Registers models for the Principle Management feature within the admin interface for easy management and visualization of principles-related data.    |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/principle_management/tests.py)   | Validates adherence to core principles through unit tests for the Principle Management module.                                                        |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/principle_management/views.py)   | Implements CRUD operations for managing principles within the application, serving as a key component in maintaining user-defined guiding principles. |

</details>



<details closed><summary>seven</summary>

| File                                                                             | Summary                                                                                                                                                                                                                                                                                                  |
|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [asgi.py](https://github.com/amiakshylo/7habits/blob/main/seven/asgi.py)         | Exposes ASGI callable for seamless Django project deployment.Clarifies how to access `application` variable and set DJANGO settings module. Ensure smooth ASGI configuration per Django best practices.                                                                                                  |
| [settings.py](https://github.com/amiakshylo/7habits/blob/main/seven/settings.py) | Defines Django settings for the entire repository. Specifies installed apps, authentication settings, middleware, database configuration, user management, logging settings, and other essential configurations. Orchestrates the functionality and behavior of different components within the project. |
| [urls.py](https://github.com/amiakshylo/7habits/blob/main/seven/urls.py)         | Defines API routes and documentation views for user, habit, life sphere, goal task, journey, and onboarding functionalities. Includes admin panel, debug toolbar, and Django REST framework settings with permissions and Swagger UI integration.                                                        |
| [wsgi.py](https://github.com/amiakshylo/7habits/blob/main/seven/wsgi.py)         | Enables Django WSGI configuration for the seven project, exposing the WSGI callable as application. Sets the Django settings module and retrieves the WSGI application for deployment.                                                                                                                   |

</details>

<details closed><summary>goal_task_management</summary>

| File                                                                                                  | Summary                                                                                                                                                                                                                                                  |
|-------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [models.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/models.py)           | Defines models for goals, suggestions, tasks, and subtasks, linking with user profiles, roles, and habits. Differentiates between long/short-term goals and allows for custom and predefined tasks. Tracks suggestions from AI models and user feedback. |
| [serializers.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/serializers.py) | Defines serializers for Goal and Role model data. GoalSerializer includes fields for goal details, while GoalSuggestionInputSerializer handles role suggestions based on user context.                                                                   |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/apps.py)               | Defines the configuration for the Goal Task Management app within the Django framework. It sets up the apps default auto field and specifies the app name.                                                                                               |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/admin.py)             | Manages admin functionality for goal tasks, leveraging Djangos built-in admin interface. Registers the GoalTask model for easy management and visibility within the Django admin dashboard, ensuring seamless interaction with goal tasks.               |
| [urls.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/urls.py)               | Defines routing for goal suggestions using a nested router in the projects goal task management module. Integrates with Django URLs and REST framework for seamless navigation to goal suggestions views.                                                |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/views.py)             | Generates and suggests custom goals based on user data. Utilizes AI for goal generation and ML model for recommendations. Handles duplicate prevention. Logs and returns suggested goals. Fallbacks to OpenAI if data is insufficient.                   |

</details>



<details closed><summary>goal_task_management.ml</summary>

| File                                                                                                                         | Summary                                                                                                                                                                                                                                                                                    |
|------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [goal_suggestion_ml.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/ml/goal_suggestion_ml.py)       | Enables training a PyTorch model for predicting user goals. Validates model output size consistency with goal count, handles reverse goal mapping, and preprocesses user data for prediction. Supports model training with carefully initialized weights and optimized cross-entropy loss. |
| [goal_suggestion_model.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/ml/goal_suggestion_model.py) | Trains and loads a PyTorch neural network model to predict user goals based on historical logs. Maps goal IDs, retrieves model configuration, preprocesses user data, and handles model training and saving within the goal_task_management modules context.                               |

</details>

<details closed><summary>goal_task_management.openai</summary>

| File                                                                                                                       | Summary                                                                                                                                                                                     |
|----------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [goal_suggestion_ai.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/openai/goal_suggestion_ai.py) | Generates tailored goals leveraging OpenAI API based on user profile and role. Parses AI-generated responses to extract goal title and description, ensuring alignment with user specifics. |

</details>

<details closed><summary>life_sphere</summary>

| File                                                                                         | Summary                                                                                                                                                                                                                                    |
|----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [models.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/models.py)           | Defines models for life spheres, areas of interest, progress tracking, and completion status, linked to user profiles. Facilitates categorization, tracking, and completion of personal life spheres in the application.                   |
| [serializers.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/serializers.py) | Defines serializers for LifeSphere and Area models in the life_sphere app. Serializes data fields like ID, title, description, and related LifeSphere.                                                                                     |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/apps.py)               | Defines CategoriesConfig for life_sphere module, specifying the default database field as BigAutoField.                                                                                                                                    |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/admin.py)             | Defines Django admin configuration for the Life Sphere category model. Registers the Life Sphere model with custom display and search fields.                                                                                              |
| [pagination.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/pagination.py)   | Defines default pagination settings using PageNumberPagination from rest_framework.                                                                                                                                                        |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/tests.py)             | Tests various functionalities related to life spheres.                                                                                                                                                                                     |
| [urls.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/urls.py)               | Defines URL patterns for life sphere features using Django and rest_framework_nested routers. Includes views for LifeSphereViewSet and AreaViewSet, offering structured access to life sphere and area resources in the parent repository. |
| [filters.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/filters.py)         | Defines custom filter for `Area` model based on `life_sphere_id` in the parent repository architecture.                                                                                                                                    |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/views.py)             | Implements viewsets for Life Sphere and Area models with authentication, filtering, and pagination. Supports search on title and description. References related models.                                                                   |

</details>



<details closed><summary>user_feedback</summary>

| File                                                                                 | Summary                                                                                                                                                                                                                                                      |
|--------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [models.py](https://github.com/amiakshylo/7habits/blob/main/user_feedback/models.py) | Defines user feedback models enhancing interaction and data insights.                                                                                                                                                                                        |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/user_feedback/apps.py)     | Defines AppConfig for UserFeedback, utilizing Djangos BigAutoField.                                                                                                                                                                                          |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/user_feedback/admin.py)   | Registers models for admin view access control and customization in user feedback section.                                                                                                                                                                   |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/user_feedback/tests.py)   | Tests user feedback functionality ensuring robustness through comprehensive test cases within the user_feedback module of the 7habits repository.                                                                                                            |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/user_feedback/views.py)   | Manages user feedback creation and display for enhancing user experience within the 7habits platform. Collaborates with user management and core modules to implement feedback-related functionalities, contributing to a user-centric development approach. |

</details>

<details closed><summary>user_management</summary>

| File                                                                                             | Summary                                                                                                                                                                                                                                                                                                                                        |
|--------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [models.py](https://github.com/amiakshylo/7habits/blob/main/user_management/models.py)           | Defines user-related models linked to user profiles, roles, goals, tasks, habits, principles, and balance within the system. Manages user details, goal types, notifications, and AI assistance. Supports customized user roles and tailored missions. Achieves complete user profile information, task management, and life balance tracking. |
| [validators.py](https://github.com/amiakshylo/7habits/blob/main/user_management/validators.py)   | Validates profile image size, dimensions, and format in the user management module. Limits size to 5MB, dimensions to 2000x2000 pixels, and accepts.jpg,.jpeg,.png extensions.                                                                                                                                                                 |
| [serializers.py](https://github.com/amiakshylo/7habits/blob/main/user_management/serializers.py) | Defines serializers for user roles, areas, goals, and profiles. Validates and creates user-related objects with specific business logic. Manages user data relationships within the repositorys user management module.                                                                                                                        |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/user_management/apps.py)               | Registers signal handlers for user management module. Configures Django app with default auto field and module name.                                                                                                                                                                                                                           |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/user_management/admin.py)             | Defines custom admin views for User, UserProfile, and Role models in Django, enhancing admin interface with key user management functionalities. Enriches visibility and management of user-related information and roles through customized admin display and search features.                                                                |
| [permissions.py](https://github.com/amiakshylo/7habits/blob/main/user_management/permissions.py) | Implements custom permissions to restrict access based on user roles. Validates user_profile_pk as an integer and confirms user is an admin or the owner of the profile. Facilitates secure user profile viewing and manipulation within the system.                                                                                           |
| [pagination.py](https://github.com/amiakshylo/7habits/blob/main/user_management/pagination.py)   | Enables default pagination with a page size of 10 using rest_framework in user_management of the parent repository.                                                                                                                                                                                                                            |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/user_management/tests.py)             | Tests user-related functionality ensuring data integrity and operations in user management, including permissions, signals, and validators. Verifies user model, serializers, and views for robustness in managing user data.                                                                                                                  |
| [urls.py](https://github.com/amiakshylo/7habits/blob/main/user_management/urls.py)               | Defines URL patterns for user management features using Django REST Framework routers. Includes endpoints for user profiles, roles, goals, areas, and balances. Integrated within the user management module of the parent repositorys architecture.                                                                                           |
| [filters.py](https://github.com/amiakshylo/7habits/blob/main/user_management/filters.py)         | Filters user roles by type using a RoleFilter class in user_management/models.py.                                                                                                                                                                                                                                                              |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/user_management/views.py)             | Retrieves and updates the current users profile information.-Manages roles with CRUD operations.-Handles user goal creation and customization.-Manages user areas of focus and balance tracking.                                                                                                                                               |
| [managers.py](https://github.com/amiakshylo/7habits/blob/main/user_management/managers.py)       | Enables custom user creation and superuser creation with specified attributes, ensuring essential fields are set and handling password encryption. Maintains user integrity and authentication for the application.                                                                                                                            |

</details>



<details closed><summary>user_management.signals</summary>

| File                                                                                               | Summary                                                                                                                                                                     |
|----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [handlers.py](https://github.com/amiakshylo/7habits/blob/main/user_management/signals/handlers.py) | Creates user profile upon new user creation, linking it to the user instance. Incorporated into Django signals, this handler reacts to post-save events for the user model. |

</details>

<details closed><summary>user_management.management.commands</summary>

| File                                                                                                                 | Summary                                                                                                                                                                                                                     |
|----------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [populate_db.py](https://github.com/amiakshylo/7habits/blob/main/user_management/management/commands/populate_db.py) | Populate database with goals from a CSV file. Reads CSV containing goal data, creates Goal objects, assigns roles, and saves to database. Maintains data integrity while populating the database with relevant information. |

</details>

<details closed><summary>onboarding</summary>

| File                                                                                        | Summary                                                                                                                                                                                                                                                                                                                             |
|---------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [models.py](https://github.com/amiakshylo/7habits/blob/main/onboarding/models.py)           | Defines models for onboarding questions, responses, and user progress. Establishes relationships with LifeSphere and UserProfile. Tracks user progress with completed and skipped questions. Encapsulates user responses with predefined choices for clarity. Organizes onboarding process components for seamless user experience. |
| [serializers.py](https://github.com/amiakshylo/7habits/blob/main/onboarding/serializers.py) | Manages serialization of onboarding questions and responses. Enables updating existing onboarding responses or creating new ones based on user profile and question ID contexts.                                                                                                                                                    |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/onboarding/apps.py)               | Defines the configuration for the Onboarding app in the Django project, specifying default fields. The purpose is to provide structured app-specific settings for the Onboarding functionality within the larger system.                                                                                                            |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/onboarding/admin.py)             | Registers models with the Django admin interface to manage onboarding-related data.                                                                                                                                                                                                                                                 |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/onboarding/tests.py)             | Verifies onboarding functionalities by importing TestCase class and creating tests within the Django framework.                                                                                                                                                                                                                     |
| [urls.py](https://github.com/amiakshylo/7habits/blob/main/onboarding/urls.py)               | Defines URL routing for onboarding questions using Django and Rest Framework Nested routers. Includes the OnboardingViewSet within the DefaultRouter for endpoint access.                                                                                                                                                           |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/onboarding/views.py)             | Manages onboarding progress by filtering and presenting questions based on user status. Updates progress and transitions to the next life sphere upon completion.                                                                                                                                                                   |

</details>



---

## Getting Started

### Prerequisites

**Python**: `version x.y.z`

### Installation

Build the project from source:

1. Clone the 7habits repository:

```sh
❯ git clone https://github.com/amiakshylo/7habits
```

2. Navigate to the project directory:

```sh
❯ cd 7habits
```

3. Install the required dependencies:

```sh
❯ pip install -r requirements.txt
```

### Usage

To run the project, execute the following command:

```sh
❯ python main.py
```

### Tests

Execute the test suite using the following command:

```sh
❯ pytest
```

---

## Project Roadmap

- [X] **`Task 1`**: <strike>Implement feature one.</strike>
- [ ] **`Task 2`**: Implement feature two.
- [ ] **`Task 3`**: Implement feature three.

---

## Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Report Issues](https://github.com/amiakshylo/7habits/issues)**: Submit bugs found or log feature requests for
  the `7habits` project.
- **[Submit Pull Requests](https://github.com/amiakshylo/7habits/blob/main/CONTRIBUTING.md)**: Review open PRs, and
  submit your own PRs.
- **[Join the Discussions](https://github.com/amiakshylo/7habits/discussions)**: Share your insights, provide feedback,
  or ask questions.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/amiakshylo/7habits
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and
   their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your
   contribution!

</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/amiakshylo/7habits/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=amiakshylo/7habits">
   </a>
</p>
</details>

---

## License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details,
refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

## Acknowledgments

- List any resources, contributors, inspiration, etc. here.

---
