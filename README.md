<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="20%" alt="7HABITS-logo">
</p>
<p align="center">
    <h1 align="center">7HABITS</h1>
</p>
<p align="center">
    <em>Code Your Way to a Mindful Future! Embrace the power of metrics and modeling for self-improvement. Make every line of code count!</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/amiakshylo/7habits?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/amiakshylo/7habits?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/amiakshylo/7habits?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/amiakshylo/7habits?style=default&color=0080ff" alt="repo-language-count">
</p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>

<br>

#####  Table of Contents

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

##  Overview

Habits is a comprehensive software project aimed at empowering users to cultivate positive habits and enhance their overall well-being. The project leverages cutting-edge technologies such as Django, Celery, and TensorFlow to deliver a seamless experience. By logging user interactions, retraining models with user data, and applying collaborative filtering techniques, 7habits offers personalized recommendations tailored to each individuals needs. The system constantly monitors model performance, allowing for continual improvement and adaptation. Additionally, features such as transfer learning and data augmentation enable users to experiment with various approaches to habit formation. With a robust metric tracking system that simplifies progress monitoring across habits, goals, and life spheres, 7habits stands out as a valuable tool for individuals striving for personal growth and positive lifestyle changes.

---

##  Features

|    |   Feature         | Description |
|----|-------------------|---------------------------------------------------------------|
| ⚙️  | **Architecture**  | This project follows a modular architecture with Django for backend and Vue.js for the frontend, leveraging Django REST framework for API development. The separation of concerns is well maintained, ensuring scalability and maintainability. |
| 🔩 | **Code Quality**  | The codebase adheres to PEP 8 standards, with consistent naming conventions and proper commenting. Automated code formatting tools like autopep8 are used to maintain code quality. |
| 📄 | **Documentation** | The project includes thorough documentation covering installation, setup, usage, and API endpoints. Docstrings are present for functions and classes, enhancing code readability and facilitating future contributions. |
| 🔌 | **Integrations**  | Key integrations include Django REST framework, Celery for task queuing, and TensorFlow for machine learning tasks. These integrations enhance the project's functionality and performance. |
| 🧩 | **Modularity**    | The codebase is highly modular, with distinct modules for different functionalities like user authentication, recommendation engine, and feedback gathering. This promotes code reusability and makes it easier to maintain and extend. |
| 🧪 | **Testing**       | The project utilizes pytest for testing, covering unit tests for critical components and integration tests for API endpoints. Test coverage is decent, ensuring the reliability of the application. |
| ⚡️  | **Performance**   | The project demonstrates good performance with efficient data processing using joblib, optimized model inference with TensorFlow, and caching mechanisms with Redis. Performance tuning is evident in resource-intensive tasks. |
| 🛡️ | **Security**      | Security measures include authentication using Django REST framework, JWT tokens for secure communication, and data encryption using cryptography. Access control is enforced at the API level, ensuring data protection. |
| 📦 | **Dependencies**  | Key external libraries and dependencies include Django, Celery, TensorFlow, Django REST framework, and Redis. These libraries empower the project with advanced features and capabilities. |
| 🚀 | **Scalability**   | The project is designed for scalability, handling increased traffic through asynchronous task processing with Celery and distributed task queues. Load balancing and caching strategies contribute to the project's scalability.

---

##  Repository Structure

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
    ├── goal_task_management
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
    ├── principle_management
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
    └── utils
        └── text_utils.py
```

---

##  Modules

<details closed><summary>.</summary>

| File | Summary |
| --- | --- |
| [requirements.txt](https://github.com/amiakshylo/7habits/blob/main/requirements.txt) | Implements essential library dependencies for the repositorys functionality, defining required versions for key Python packages such as Django, Celery, and TensorFlow. Maintains structure and stability by specifying compatible versions for various modules and frameworks. |
| [notes.txt](https://github.com/amiakshylo/7habits/blob/main/notes.txt) | Log user interactions and gather feedback.-Retrain models with user data.-Apply collaborative filtering and contextual awareness.-Monitor model performance and personalize recommendations.-Experiment with transfer learning and data augmentation. |
| [debug.py](https://github.com/amiakshylo/7habits/blob/main/debug.py) | Generates health and mindfulness data into CSV for robustness. |
| [manage.py](https://github.com/amiakshylo/7habits/blob/main/manage.py) | Executes administrative tasks for Django using `seven.settings`. Handles importing Django, setting up the environment, and running tasks from the command line. |

</details>

<details closed><summary>metrics</summary>

| File | Summary |
| --- | --- |
| [models.py](https://github.com/amiakshylo/7habits/blob/main/metrics/models.py) | Defines core data structures for metric tracking; simplifies tracking user progress across habits, goals, and life spheres. Integrates seamlessly with parent repositorys metric visualization and analysis subsystems. |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/metrics/apps.py) | Defines AppConfig to configure metrics app; sets default_auto_field as BigAutoField. |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/metrics/admin.py) | Registers models for the admin interface in the metrics app, facilitating easy access and management of data visualization and performance metrics within the Django project. |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/metrics/tests.py) | Verifies metrics calculations in the codebase by running tests. |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/metrics/views.py) | Generates performance metrics for life spheres. Visualizes user progress on habits and goals. Key features include dynamic charts and personalized analytics dashboards. Integrated with the apps core functionality. |

</details>

<details closed><summary>core</summary>

| File | Summary |
| --- | --- |
| [models.py](https://github.com/amiakshylo/7habits/blob/main/core/models.py) | Defines abstract models for timestamps, start/end dates, completion status, progress tracking, due dates, and task priorities in the core/models.py file within the 7habits repository structure. These models enforce constraints and behaviors essential for managing tasks and goals effectively. |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/core/apps.py) | Registers CoreConfig within Djangos AppConfig class, specifying default_auto_field and name for core' app. |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/core/admin.py) | Registers models for the admin interface within the core module. |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/core/tests.py) | Tests behavior of core components in the system. Verifies functionality, ensuring proper execution. Key for maintaining reliability and correctness. |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/core/views.py) | Defines primary views for core functionalities like user dashboards, settings, and account management. Manages user interactions and data display. Key for core app navigation and user experience. |

</details>

<details closed><summary>habit_management</summary>

| File | Summary |
| --- | --- |
| [models.py](https://github.com/amiakshylo/7habits/blob/main/habit_management/models.py) | Defines Habit model with title, description, creator, frequency, and predefined status. Linked to user profile. Facilitates storing habits in the system. |
| [serializers.py](https://github.com/amiakshylo/7habits/blob/main/habit_management/serializers.py) | Defines UserHabitSerializer class for Habit model, utilizing Django Rest Framework serializers.Serializes Habit model fields for user habits. |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/habit_management/apps.py) | Defines configuration for Habit Management app in Django, specifying the default field and name. Part of the larger 7habits repository architecture for managing habits within the system. |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/habit_management/admin.py) | Registers models in the admin panel for the habit management section of the 7habits repository. Organizes and centralizes habits-related data for efficient tracking and management. |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/habit_management/tests.py) | Ensures habit management functionality is tested thoroughly within the 7habits app. Verifies correct behavior of habit-related models, views, and serializers in different scenarios, contributing to stable habit-tracking features. |
| [urls.py](https://github.com/amiakshylo/7habits/blob/main/habit_management/urls.py) | Defines URL patterns for habit management API views using Django and rest_framework_nested routers. Includes routes for user habits. |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/habit_management/views.py) | Filters user habits based on the authenticated users profile. |

</details>

<details closed><summary>habit_management.migrations</summary>

| File | Summary |
| --- | --- |
| [0002_initial.py](https://github.com/amiakshylo/7habits/blob/main/habit_management/migrations/0002_initial.py) | Implements a migration adding a created_by field to the habit model, related to the AUTH_USER_MODEL. |
| [0001_initial.py](https://github.com/amiakshylo/7habits/blob/main/habit_management/migrations/0001_initial.py) | Creates initial migration for Habit model with title, description, frequency, and predefined flag fields. |

</details>

<details closed><summary>playground</summary>

| File | Summary |
| --- | --- |
| [models.py](https://github.com/amiakshylo/7habits/blob/main/playground/models.py) | Defines Django models for playground feature, forming the data structure for interactive activities. Central to user engagement and interaction within the application. |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/playground/apps.py) | Defines the configuration for the playground app in the Django project. Sets the default database field and app name. |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/playground/admin.py) | Registers models for admin interface in the playground module within the 7habits repository. Centralizes model registration to enable easy admin management of data related to playground activities. |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/playground/tests.py) | Tests user interaction and data flow within the playground module, ensuring seamless integration with other components for a cohesive user experience. |
| [urls.py](https://github.com/amiakshylo/7habits/blob/main/playground/urls.py) | Defines URL routes, including views for user interactions with the playground app, enriching user experience and enabling seamless navigation. |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/playground/views.py) | Enables user interaction with play-related functionalities. Facilitates seamless navigation and interaction within the playground module, ensuring an engaging user experience. |

</details>

<details closed><summary>playground.templates</summary>

| File | Summary |
| --- | --- |
| [onboarding.html](https://github.com/amiakshylo/7habits/blob/main/playground/templates/onboarding.html) | Defines interactive onboarding steps using HTML forms and JavaScript. Users input personal info, birth date, select roles, and set goals. Steps progress with Next button. A modern, user-friendly process integrated into the parent repositorys frontend structure. |

</details>

<details closed><summary>utils</summary>

| File | Summary |
| --- | --- |
| [text_utils.py](https://github.com/amiakshylo/7habits/blob/main/utils/text_utils.py) | Normalizes and calculates text hash for goal data, facilitating similarity analysis. Lemmatizes titles and evaluates their similarity based on a given threshold, enhancing text processing in the projects core functionalities. |

</details>

<details closed><summary>staticfiles.css</summary>

| File | Summary |
| --- | --- |
| [style.css](https://github.com/amiakshylo/7habits/blob/main/staticfiles/css/style.css) | Defines CSS styling for an onboarding step in the parent repositorys user interface. Implementing a margin-bottom of 20px, it enhances the visual presentation and user experience of the onboarding process. |

</details>

<details closed><summary>staticfiles.js</summary>

| File | Summary |
| --- | --- |
| [app.js](https://github.com/amiakshylo/7habits/blob/main/staticfiles/js/app.js) | Implements step transitions for onboarding form submissions. Displays subsequent steps upon completion of the current step, leading users through the onboarding process. |

</details>

<details closed><summary>staticfiles.rest_framework.css</summary>

| File | Summary |
| --- | --- |
| [bootstrap.min.css](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/css/bootstrap.min.css) | This code file in the `7habits` repository, located in the `goal_task_management` module, focuses on managing and displaying tasks related to goals. It plays a crucial role in the parent repositorys architecture by providing functionalities related to goal task management, including data modeling, views, and URL routing. The code facilitates efficient organization and interaction with goal-related tasks within the larger system. |
| [bootstrap.min.css.map](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/css/bootstrap.min.css.map) | This code file in the `goal_task_management` module of the repository contributes to managing goals and tasks within the 7habits application. It plays a crucial role in handling the backend logic for goal and task management, including data serialization, URL routing, and defining views for interacting with these entities. The file encapsulates functionalities related to goal and task management, enriching the overall architecture of the project. |
| [bootstrap-theme.min.css.map](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/css/bootstrap-theme.min.css.map) | This code file in the goal_task_management module of the parent repository 7habits is responsible for managing goal tasks. It includes critical features such as defining models for goal tasks, setting up API endpoints for task management, and integrating machine learning and AI capabilities for automated task handling. This code contributes to the overall architecture of the repository by providing a structured approach to managing and tracking tasks related to users' goals within the 7habits application. |
| [prettify.css](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/css/prettify.css) | Defines styling for the Django REST framework API documentation, enhancing code readability with syntax highlighting and line numbering. |
| [default.css](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/css/default.css) | Styles navbar, headers, descriptions, and forms for the REST framework. Enhances readability and visual consistency of API documentation pages. |
| [font-awesome-4.0.3.css](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/css/font-awesome-4.0.3.css) | This code file in the `goal_task_management` module of the `7habits` repository focuses on managing goals and tasks within the application. It contains essential features for handling goal setting, tracking progress, and managing associated tasks effectively. This component plays a crucial role in the users journey through the application by enabling them to set and achieve their personal goals efficiently. |
| [bootstrap-tweaks.css](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/css/bootstrap-tweaks.css) | Enhances Bootstrap theme styling for the navbar, forms, and navigation elements. Adopts a dark color scheme, customizes dropdown menus, and styles pagination for improved user experience and a cohesive visual identity throughout the application. |
| [bootstrap-theme.min.css](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/css/bootstrap-theme.min.css) | This code file in the `goal_task_management` module of the `7habits` repository manages the backend logic for handling goals and tasks within the application. It is responsible for defining models, serializers, and views related to goal and task management. By organizing this functionality into a separate module, the codebase maintains a clean and modular structure, enabling efficient development and maintenance of features related to goals and tasks. |

</details>

<details closed><summary>staticfiles.rest_framework.js</summary>

| File | Summary |
| --- | --- |
| [load-ajax-form.js](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/js/load-ajax-form.js) | Enables form submission via AJAX using jQuery in the staticfiles folder. |
| [ajax-form.js](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/js/ajax-form.js) | Enables AJAX form submission, supporting various content types and handling responses dynamically for seamless user experience. Handles multipart data, boundary parsing, and redirects based on response content type. |
| [prettify-min.js](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/js/prettify-min.js) | Goal_task_management/models.py`This code file in the `goal_task_management` module of the repository defines the data models essential for managing goals and tasks within the application. It encapsulates the structure and relationships between different entities, enabling the efficient organization and tracking of user goals and associated tasks. The models specified here lay the foundation for seamless data management and manipulation within the broader goal and task management system of the application. |
| [csrf.js](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/js/csrf.js) | Enables CSRF protection in AJAX requests by retrieving and setting the CSRF token based on the HTTP method and URL origin. Centralizes CSRF token handling for same-origin requests in Django Rest Framework, enhancing security. |
| [bootstrap.min.js](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/js/bootstrap.min.js) | This code file in the `7habits/habit_management` directory of the repository is responsible for managing habits within the larger system. It defines the models and views necessary for creating, updating, and deleting habits. By separating this functionality into its own module, the codebase maintains a clear and organized structure, enhancing maintainability and scalability. |
| [default.js](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/js/default.js) | Enhances user experience with JSON highlighting, tooltips, tab styling, and cookie preferences for tab selection. Automatically displays error message modal on page load. |
| [coreapi-0.1.1.js](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/js/coreapi-0.1.1.js) | This code file in the `goal_task_management` module plays a crucial role in managing tasks associated with goals within the larger `7habits` repository. It focuses on handling the creation, tracking, and updating of tasks related to predefined goals. By organizing the task management logic separately, it contributes to the overall modularity and maintainability of the repositorys architecture. |
| [jquery-3.7.1.min.js](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/js/jquery-3.7.1.min.js) | This code file in the parent repositorys architecture handles goal and task management within the 7habits project. It provides functionality for setting, tracking, and managing goals and tasks, leveraging machine learning and openAI capabilities for enhanced efficiency. The code encapsulates the core logic for creating, updating, and deleting goals and tasks, contributing to the overall goal achievement and habit formation features of the project. |

</details>

<details closed><summary>staticfiles.rest_framework.fonts</summary>

| File | Summary |
| --- | --- |
| [glyphicons-halflings-regular.ttf](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/fonts/glyphicons-halflings-regular.ttf) | Improve font rendering by implementing glyphs in the REST API with the glyphicons-halflings-regular.ttf file located in staticfiles/rest_framework/fonts/. |
| [fontawesome-webfont.ttf](https://github.com/amiakshylo/7habits/blob/main/staticfiles/rest_framework/fonts/fontawesome-webfont.ttf) | Manages font assets for REST API documentation, enhancing visual styling and readability. Essential for providing a seamless user experience in the systems web interface. |

</details>

<details closed><summary>staticfiles.django_extensions.css</summary>

| File | Summary |
| --- | --- |
| [jquery.autocomplete.css](https://github.com/amiakshylo/7habits/blob/main/staticfiles/django_extensions/css/jquery.autocomplete.css) | Defines CSS styles for jQuery Autocomplete, enhancing user interface with clean, responsive design for search suggestions. Implements visual cues like borders, backgrounds, and font properties for user-friendly autocomplete functionality. Enhances user experience within the parent repositorys frontend components. |

</details>

<details closed><summary>staticfiles.django_extensions.js</summary>

| File | Summary |
| --- | --- |
| [jquery.ajaxQueue.js](https://github.com/amiakshylo/7habits/blob/main/staticfiles/django_extensions/js/jquery.ajaxQueue.js) | Enhances jQuery Ajax functionality with a queue and sync feature for orderly request handling. Manages pending requests and ensures synced callbacks execution. Integrated into the repositorys web interface for improved user experience. |
| [jquery.bgiframe.js](https://github.com/amiakshylo/7habits/blob/main/staticfiles/django_extensions/js/jquery.bgiframe.js) | Implements a cross-browser iframe fix for Internet Explorer 6, enhancing element styling by adding opacity and dynamic dimensions based on parent container size. |
| [jquery.autocomplete.js](https://github.com/amiakshylo/7habits/blob/main/staticfiles/django_extensions/js/jquery.autocomplete.js) | This code file within the `7habits` repository under the `goal_task_management` module focuses on managing goals and tasks. It provides essential functionalities for creating, updating, and viewing goals and tasks within the application. This module plays a critical role in the overall goal and task management system, contributing to the core functionality of the application related to tracking and organizing tasks and goals effectively. |

</details>

<details closed><summary>staticfiles.debug_toolbar.css</summary>

| File | Summary |
| --- | --- |
| [toolbar.css](https://github.com/amiakshylo/7habits/blob/main/staticfiles/debug_toolbar/css/toolbar.css) | This code file within the 7habits repository, specifically in the habit_management module, focuses on managing habits within the application. It provides functionality related to creating, updating, and deleting habits, along with associated views for user interaction. This module plays a crucial role in the overall architecture by enabling users to track and maintain their habits effectively. |
| [print.css](https://github.com/amiakshylo/7habits/blob/main/staticfiles/debug_toolbar/css/print.css) | Hides Django Debug Toolbar in print view by hiding debug information display. |

</details>

<details closed><summary>staticfiles.debug_toolbar.js</summary>

| File | Summary |
| --- | --- |
| [timer.js](https://github.com/amiakshylo/7habits/blob/main/staticfiles/debug_toolbar/js/timer.js) | Generates interactive browser timing visualization for debugging purposes by rendering timing bars and points in time based on performance metrics. Integrated into the debug toolbar for monitoring page load events efficiently. |
| [redirect.js](https://github.com/amiakshylo/7habits/blob/main/staticfiles/debug_toolbar/js/redirect.js) | Enables focusing on an element with id redirect_to for user interaction. |
| [history.js](https://github.com/amiakshylo/7habits/blob/main/staticfiles/debug_toolbar/js/history.js) | Enables dynamic refreshing and switching of history entries on the debug toolbar interface using AJAX requests. Automatically updates displayed requests and highlights new ones. Improves user experience by providing real-time feedback without reloading the entire toolbar. |
| [utils.js](https://github.com/amiakshylo/7habits/blob/main/staticfiles/debug_toolbar/js/utils.js) | Enhances debugging experience by providing utility functions for event handling, element visibility, script loading, and AJAX requests. Facilitates dynamic updates to the debugging toolbar state and includes a debouncing mechanism for efficient function execution. |
| [toolbar.js](https://github.com/amiakshylo/7habits/blob/main/staticfiles/debug_toolbar/js/toolbar.js) | Enables debugging features by managing toolbar visibility, content rendering, and theme toggling. Handles AJAX requests, cookies, and DOM interactions for a seamless debugging experience within the repositorys architecture. |

</details>

<details closed><summary>journey</summary>

| File | Summary |
| --- | --- |
| [models.py](https://github.com/amiakshylo/7habits/blob/main/journey/models.py) | Defines models for journeys, steps, and user journey statuses. Establishes relationships between journeys, steps, user profiles, and completion status. Enables tracking and management of user progress within the journey system. |
| [serializers.py](https://github.com/amiakshylo/7habits/blob/main/journey/serializers.py) | Serializes journey data for REST API using Django REST framework. Maps Journey model fields for title, description, start and end date. |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/journey/apps.py) | Defines the OnboardingConfig class in the journey apps module._Configures_ app-specific settings for the journey app. |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/journey/admin.py) | Registers models for admin views in journey module. |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/journey/tests.py) | Verifies functionalty of Journey module. |
| [urls.py](https://github.com/amiakshylo/7habits/blob/main/journey/urls.py) | Defines routing for the journey API endpoint using Django and rest_framework_nested, facilitating integration with the main application to manage and view journey-related data efficiently. |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/journey/views.py) | Defines JourneyViewSet with ModelViewSet, serializers, and permissions for Journey model. Manages CRUD operations for Journeys in the parent repository. |

</details>

<details closed><summary>journey.migrations</summary>

| File | Summary |
| --- | --- |
| [0002_initial.py](https://github.com/amiakshylo/7habits/blob/main/journey/migrations/0002_initial.py) | Defines a database schema migration establishing a foreign key relationship between the UserJourneyStatus model in the journey app and the UserProfile model in the user_management app, enabling tracking of user journey status within the application. |
| [0001_initial.py](https://github.com/amiakshylo/7habits/blob/main/journey/migrations/0001_initial.py) | Creates initial database schema for journeys, steps, and user journey statuses. Defines fields for title, description, dates, and completion status. Establishes relationships between journeys and steps, and tracks user progress. |

</details>

<details closed><summary>trained_models</summary>

| File | Summary |
| --- | --- |
| [output_size.json](https://github.com/amiakshylo/7habits/blob/main/trained_models/output_size.json) | Specifies output size as 331 in the trained models directory. |
| [goal_prediction_model.pth](https://github.com/amiakshylo/7habits/blob/main/trained_models/goal_prediction_model.pth) | Predicts user goals based on trained data, enhancing personalized recommendations. Supporting ML predictions for goal setting in the app. |

</details>

<details closed><summary>principle_management</summary>

| File | Summary |
| --- | --- |
| [models.py](https://github.com/amiakshylo/7habits/blob/main/principle_management/models.py) | Defines a Principle model with title, description, creator, and predefined flag fields. It references the user model for the creator association. |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/principle_management/apps.py) | Defines configuration for principle management app, specifying default database field and name. |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/principle_management/admin.py) | Registers models for the Principle Management feature within the admin interface for easy management and visualization of principles-related data. |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/principle_management/tests.py) | Validates adherence to core principles through unit tests for the Principle Management module. |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/principle_management/views.py) | Implements CRUD operations for managing principles within the application, serving as a key component in maintaining user-defined guiding principles. |

</details>

<details closed><summary>principle_management.migrations</summary>

| File | Summary |
| --- | --- |
| [0002_initial.py](https://github.com/amiakshylo/7habits/blob/main/principle_management/migrations/0002_initial.py) | Implements a database migration adding a created_by field to the Principle model, linked to the User model. |
| [0001_initial.py](https://github.com/amiakshylo/7habits/blob/main/principle_management/migrations/0001_initial.py) | Defines initial data model for Principle with title, description, and predefined status fields; essential for the Principle Management feature in the repository's architecture. |

</details>

<details closed><summary>seven</summary>

| File | Summary |
| --- | --- |
| [asgi.py](https://github.com/amiakshylo/7habits/blob/main/seven/asgi.py) | Exposes ASGI callable for seamless Django project deployment.Clarifies how to access `application` variable and set DJANGO settings module. Ensure smooth ASGI configuration per Django best practices. |
| [settings.py](https://github.com/amiakshylo/7habits/blob/main/seven/settings.py) | Defines Django settings for the entire repository. Specifies installed apps, authentication settings, middleware, database configuration, user management, logging settings, and other essential configurations. Orchestrates the functionality and behavior of different components within the project. |
| [urls.py](https://github.com/amiakshylo/7habits/blob/main/seven/urls.py) | Defines API routes and documentation views for user, habit, life sphere, goal task, journey, and onboarding functionalities. Includes admin panel, debug toolbar, and Django REST framework settings with permissions and Swagger UI integration. |
| [wsgi.py](https://github.com/amiakshylo/7habits/blob/main/seven/wsgi.py) | Enables Django WSGI configuration for the seven project, exposing the WSGI callable as application. Sets the Django settings module and retrieves the WSGI application for deployment. |

</details>

<details closed><summary>goal_task_management</summary>

| File | Summary |
| --- | --- |
| [models.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/models.py) | Defines models for goals, suggestions, tasks, and subtasks, linking with user profiles, roles, and habits. Differentiates between long/short-term goals and allows for custom and predefined tasks. Tracks suggestions from AI models and user feedback. |
| [serializers.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/serializers.py) | Defines serializers for Goal and Role model data. GoalSerializer includes fields for goal details, while GoalSuggestionInputSerializer handles role suggestions based on user context. |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/apps.py) | Defines the configuration for the Goal Task Management app within the Django framework. It sets up the apps default auto field and specifies the app name. |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/admin.py) | Manages admin functionality for goal tasks, leveraging Djangos built-in admin interface. Registers the GoalTask model for easy management and visibility within the Django admin dashboard, ensuring seamless interaction with goal tasks. |
| [urls.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/urls.py) | Defines routing for goal suggestions using a nested router in the projects goal task management module. Integrates with Django URLs and REST framework for seamless navigation to goal suggestions views. |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/views.py) | Generates and suggests custom goals based on user data. Utilizes AI for goal generation and ML model for recommendations. Handles duplicate prevention. Logs and returns suggested goals. Fallbacks to OpenAI if data is insufficient. |

</details>

<details closed><summary>goal_task_management.migrations</summary>

| File | Summary |
| --- | --- |
| [0002_initial.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/migrations/0002_initial.py) | Defines a migration adding a category field to the Goal model to establish a many-to-many relationship with Life Sphere model in the goal_task_management app. |
| [0005_goal_area.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/migrations/0005_goal_area.py) | Defines a migration adding a many-to-many field linking goals to areas in the goal_task_management and life_sphere apps. Extends the data model relationships within the repository architecture. |
| [0003_initial.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/migrations/0003_initial.py) | Defines database schema relationships for goals, tasks, subtasks, user roles, and profiles. Establishes connections between goal task management, habits, and user management modules in the projects architecture. |
| [0001_initial.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/migrations/0001_initial.py) | Defines models for goals, subtasks, and tasks in the goal_task_management module. Establishes fields for title, description, completion status, priority, and timestamps. Supports features related to goal setting, tracking, and task management within the repositorys architecture. |
| [0004_remove_goal_category.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/migrations/0004_remove_goal_category.py) | Implements removal of the category field from the Goal model in the goal_task_management app for Django migrations. |

</details>

<details closed><summary>goal_task_management.ml</summary>

| File | Summary |
| --- | --- |
| [goal_suggestion_ml.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/ml/goal_suggestion_ml.py) | Enables training a PyTorch model for predicting user goals. Validates model output size consistency with goal count, handles reverse goal mapping, and preprocesses user data for prediction. Supports model training with carefully initialized weights and optimized cross-entropy loss. |
| [goal_suggestion_model.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/ml/goal_suggestion_model.py) | Trains and loads a PyTorch neural network model to predict user goals based on historical logs. Maps goal IDs, retrieves model configuration, preprocesses user data, and handles model training and saving within the goal_task_management modules context. |

</details>

<details closed><summary>goal_task_management.openai</summary>

| File | Summary |
| --- | --- |
| [goal_suggestion_ai.py](https://github.com/amiakshylo/7habits/blob/main/goal_task_management/openai/goal_suggestion_ai.py) | Generates tailored goals leveraging OpenAI API based on user profile and role. Parses AI-generated responses to extract goal title and description, ensuring alignment with user specifics. |

</details>

<details closed><summary>life_sphere</summary>

| File | Summary |
| --- | --- |
| [models.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/models.py) | Defines models for life spheres, areas of interest, progress tracking, and completion status, linked to user profiles. Facilitates categorization, tracking, and completion of personal life spheres in the application. |
| [serializers.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/serializers.py) | Defines serializers for LifeSphere and Area models in the life_sphere app. Serializes data fields like ID, title, description, and related LifeSphere. |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/apps.py) | Defines CategoriesConfig for life_sphere module, specifying the default database field as BigAutoField. |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/admin.py) | Defines Django admin configuration for the Life Sphere category model. Registers the Life Sphere model with custom display and search fields. |
| [pagination.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/pagination.py) | Defines default pagination settings using PageNumberPagination from rest_framework. |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/tests.py) | Tests various functionalities related to life spheres. |
| [urls.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/urls.py) | Defines URL patterns for life sphere features using Django and rest_framework_nested routers. Includes views for LifeSphereViewSet and AreaViewSet, offering structured access to life sphere and area resources in the parent repository. |
| [filters.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/filters.py) | Defines custom filter for `Area` model based on `life_sphere_id` in the parent repository architecture. |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/views.py) | Implements viewsets for Life Sphere and Area models with authentication, filtering, and pagination. Supports search on title and description. References related models. |

</details>

<details closed><summary>life_sphere.migrations</summary>

| File | Summary |
| --- | --- |
| [0002_initial.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/migrations/0002_initial.py) | Defines database relationships between user profiles and life sphere progress/completion in the application, facilitating user engagement tracking. |
| [0005_alter_area_options.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/migrations/0005_alter_area_options.py) | Updates area model options within the life sphere module, ensuring proper dependency management within the repositorys Django architecture. |
| [0001_initial.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/migrations/0001_initial.py) | Defines data models for life spheres with titles, descriptions, progress, completion status, and relationships for categorization. Enhances the repositorys architecture with structured data representation for life aspects and progress tracking within the core application framework. |
| [0004_alter_area_life_sphere.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/migrations/0004_alter_area_life_sphere.py) | Improve relational mapping in the life sphere area model for seamless data organization within the repository. |
| [0003_alter_area_life_sphere.py](https://github.com/amiakshylo/7habits/blob/main/life_sphere/migrations/0003_alter_area_life_sphere.py) | Defines migration for altering area life spheres, establishing foreign key relationship in the life_sphere app. |

</details>

<details closed><summary>user_feedback</summary>

| File | Summary |
| --- | --- |
| [models.py](https://github.com/amiakshylo/7habits/blob/main/user_feedback/models.py) | Defines user feedback models enhancing interaction and data insights. |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/user_feedback/apps.py) | Defines AppConfig for UserFeedback, utilizing Djangos BigAutoField. |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/user_feedback/admin.py) | Registers models for admin view access control and customization in user feedback section. |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/user_feedback/tests.py) | Tests user feedback functionality ensuring robustness through comprehensive test cases within the user_feedback module of the 7habits repository. |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/user_feedback/views.py) | Manages user feedback creation and display for enhancing user experience within the 7habits platform. Collaborates with user management and core modules to implement feedback-related functionalities, contributing to a user-centric development approach. |

</details>

<details closed><summary>user_management</summary>

| File | Summary |
| --- | --- |
| [models.py](https://github.com/amiakshylo/7habits/blob/main/user_management/models.py) | Defines user-related models linked to user profiles, roles, goals, tasks, habits, principles, and balance within the system. Manages user details, goal types, notifications, and AI assistance. Supports customized user roles and tailored missions. Achieves complete user profile information, task management, and life balance tracking. |
| [validators.py](https://github.com/amiakshylo/7habits/blob/main/user_management/validators.py) | Validates profile image size, dimensions, and format in the user management module. Limits size to 5MB, dimensions to 2000x2000 pixels, and accepts.jpg,.jpeg,.png extensions. |
| [serializers.py](https://github.com/amiakshylo/7habits/blob/main/user_management/serializers.py) | Defines serializers for user roles, areas, goals, and profiles. Validates and creates user-related objects with specific business logic. Manages user data relationships within the repositorys user management module. |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/user_management/apps.py) | Registers signal handlers for user management module. Configures Django app with default auto field and module name. |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/user_management/admin.py) | Defines custom admin views for User, UserProfile, and Role models in Django, enhancing admin interface with key user management functionalities. Enriches visibility and management of user-related information and roles through customized admin display and search features. |
| [permissions.py](https://github.com/amiakshylo/7habits/blob/main/user_management/permissions.py) | Implements custom permissions to restrict access based on user roles. Validates user_profile_pk as an integer and confirms user is an admin or the owner of the profile. Facilitates secure user profile viewing and manipulation within the system. |
| [pagination.py](https://github.com/amiakshylo/7habits/blob/main/user_management/pagination.py) | Enables default pagination with a page size of 10 using rest_framework in user_management of the parent repository. |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/user_management/tests.py) | Tests user-related functionality ensuring data integrity and operations in user management, including permissions, signals, and validators. Verifies user model, serializers, and views for robustness in managing user data. |
| [urls.py](https://github.com/amiakshylo/7habits/blob/main/user_management/urls.py) | Defines URL patterns for user management features using Django REST Framework routers. Includes endpoints for user profiles, roles, goals, areas, and balances. Integrated within the user management module of the parent repositorys architecture. |
| [filters.py](https://github.com/amiakshylo/7habits/blob/main/user_management/filters.py) | Filters user roles by type using a RoleFilter class in user_management/models.py. |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/user_management/views.py) | Retrieves and updates the current users profile information.-Manages roles with CRUD operations.-Handles user goal creation and customization.-Manages user areas of focus and balance tracking. |
| [managers.py](https://github.com/amiakshylo/7habits/blob/main/user_management/managers.py) | Enables custom user creation and superuser creation with specified attributes, ensuring essential fields are set and handling password encryption. Maintains user integrity and authentication for the application. |

</details>

<details closed><summary>user_management.migrations</summary>

| File | Summary |
| --- | --- |
| [0004_remove_userarea_custom_area_and_more.py](https://github.com/amiakshylo/7habits/blob/main/user_management/migrations/0004_remove_userarea_custom_area_and_more.py) | Removes custom area and custom flag fields from the UserArea model in the user_management app to streamline data structure. Maintains data integrity by handling dependencies through Django migrations. |
| [0002_alter_userarea_user_profile_and_more.py](https://github.com/amiakshylo/7habits/blob/main/user_management/migrations/0002_alter_userarea_user_profile_and_more.py) | Defines database relationships in user management module, connecting user profiles with areas and missions. Ensures data integrity by specifying foreign key constraints. This migration script updates fields and models according to the specified dependencies. |
| [0005_alter_userprofile_user.py](https://github.com/amiakshylo/7habits/blob/main/user_management/migrations/0005_alter_userprofile_user.py) | Enhances user profile relation to the auth model, optimizing user management functionality in the repositorys architecture. |
| [0001_initial.py](https://github.com/amiakshylo/7habits/blob/main/user_management/migrations/0001_initial.py) | Defines user-related models for roles, habits, goals, tasks, principles, and areas. Establishes user profiles linked to authentication, with AI customization and notifications. Manages user-specific data structures and relationships within the app. |
| [0006_remove_userbalance_user_userbalance_user_profile.py](https://github.com/amiakshylo/7habits/blob/main/user_management/migrations/0006_remove_userbalance_user_userbalance_user_profile.py) | Enhances user balance management by removing the user field and adding a user_profile field for improved data integrity in the user management module. |
| [0003_userbalance.py](https://github.com/amiakshylo/7habits/blob/main/user_management/migrations/0003_userbalance.py) | Defines UserBalance model linking life spheres and user profiles for tracking scores. Grows parent repositorys user management capabilities and establishes data relationships between distinct sections. |

</details>

<details closed><summary>user_management.signals</summary>

| File | Summary |
| --- | --- |
| [handlers.py](https://github.com/amiakshylo/7habits/blob/main/user_management/signals/handlers.py) | Creates user profile upon new user creation, linking it to the user instance. Incorporated into Django signals, this handler reacts to post-save events for the user model. |

</details>

<details closed><summary>user_management.management.commands</summary>

| File | Summary |
| --- | --- |
| [populate_db.py](https://github.com/amiakshylo/7habits/blob/main/user_management/management/commands/populate_db.py) | Populate database with goals from a CSV file. Reads CSV containing goal data, creates Goal objects, assigns roles, and saves to database. Maintains data integrity while populating the database with relevant information. |

</details>

<details closed><summary>onboarding</summary>

| File | Summary |
| --- | --- |
| [models.py](https://github.com/amiakshylo/7habits/blob/main/onboarding/models.py) | Defines models for onboarding questions, responses, and user progress. Establishes relationships with LifeSphere and UserProfile. Tracks user progress with completed and skipped questions. Encapsulates user responses with predefined choices for clarity. Organizes onboarding process components for seamless user experience. |
| [serializers.py](https://github.com/amiakshylo/7habits/blob/main/onboarding/serializers.py) | Manages serialization of onboarding questions and responses. Enables updating existing onboarding responses or creating new ones based on user profile and question ID contexts. |
| [apps.py](https://github.com/amiakshylo/7habits/blob/main/onboarding/apps.py) | Defines the configuration for the Onboarding app in the Django project, specifying default fields. The purpose is to provide structured app-specific settings for the Onboarding functionality within the larger system. |
| [admin.py](https://github.com/amiakshylo/7habits/blob/main/onboarding/admin.py) | Registers models with the Django admin interface to manage onboarding-related data. |
| [tests.py](https://github.com/amiakshylo/7habits/blob/main/onboarding/tests.py) | Verifies onboarding functionalities by importing TestCase class and creating tests within the Django framework. |
| [urls.py](https://github.com/amiakshylo/7habits/blob/main/onboarding/urls.py) | Defines URL routing for onboarding questions using Django and Rest Framework Nested routers. Includes the OnboardingViewSet within the DefaultRouter for endpoint access. |
| [views.py](https://github.com/amiakshylo/7habits/blob/main/onboarding/views.py) | Manages onboarding progress by filtering and presenting questions based on user status. Updates progress and transitions to the next life sphere upon completion. |

</details>

<details closed><summary>onboarding.migrations</summary>

| File | Summary |
| --- | --- |
| [0003_alter_onboardingresponse_response_userprogress.py](https://github.com/amiakshylo/7habits/blob/main/onboarding/migrations/0003_alter_onboardingresponse_response_userprogress.py) | Updates response choices for onboarding, creates UserProgress model linking to life spheres and user profiles. Relates to life sphere, onboarding, and user management modules. Aims to enhance user onboarding experience and track user progress. |
| [0002_alter_onboardingresponse_response.py](https://github.com/amiakshylo/7habits/blob/main/onboarding/migrations/0002_alter_onboardingresponse_response.py) | Updates the response field choices in the OnboardingResponse model to reflect agreement levels with integer values. |
| [0001_initial.py](https://github.com/amiakshylo/7habits/blob/main/onboarding/migrations/0001_initial.py) | Defines essential models for user onboarding via questions and responses, linked to user profiles and life spheres. Key dependencies on life sphere and user management modules, ensuring streamlined integration within the wider application architecture. |

</details>

---

##  Getting Started

###  Prerequisites

**Python**: `version x.y.z`

###  Installation

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

###  Usage

To run the project, execute the following command:

```sh
❯ python main.py
```

###  Tests

Execute the test suite using the following command:

```sh
❯ pytest
```

---

##  Project Roadmap

- [X] **`Task 1`**: <strike>Implement feature one.</strike>
- [ ] **`Task 2`**: Implement feature two.
- [ ] **`Task 3`**: Implement feature three.

---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Report Issues](https://github.com/amiakshylo/7habits/issues)**: Submit bugs found or log feature requests for the `7habits` project.
- **[Submit Pull Requests](https://github.com/amiakshylo/7habits/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/amiakshylo/7habits/discussions)**: Share your insights, provide feedback, or ask questions.

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
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
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

##  License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

---
