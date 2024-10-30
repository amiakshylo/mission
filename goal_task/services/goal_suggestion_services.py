from goal_task.ai.goal_suggestion_openai import generate_goal_with_openai
from goal_task.models import Goal, GoalSuggestionLog
from goal_task.services.text_utils import lemmatize_title, normalize_text, are_titles_similar


class GoalSuggestionService:
    def __init__(self, user_profile, role):
        self.user_profile = user_profile
        self.role = role

    def suggest_goals(self):
        """
        Suggest goals for a user based on their profile and selected role.
        """
        existing_goals = Goal.objects.filter(role=self.role)
        if not existing_goals.exists():
            self._generate_goals_with_ai()

        return Goal.objects.filter(role=self.role)

    def _generate_goals_with_ai(self):
        """
        Generate goals using AI and save them.
        """
        generated_goals = generate_goal_with_openai(self.user_profile, selected_role=self.role.title)
        print('done')
        # if generated_goals:
        #     self.save_generated_goals(generated_goals)

    def save_generated_goals(self, generated_goals):
        """
        Save generated goals to the database.
        """
        created_goals = []
        logged_goals = []
        print(type(generated_goals))

        for goal in generated_goals:
            try:

                lemmatized_title = lemmatize_title(normalize_text(goal[0]))
                existing_goals = Goal.objects.filter(role=self.role)
                is_duplicate = False

                for existing_goal in existing_goals:
                    existing_lemmatized_title = lemmatize_title(normalize_text(existing_goal.title))

                    if lemmatized_title == existing_lemmatized_title or are_titles_similar(lemmatized_title,
                                                                                           existing_lemmatized_title):
                        created_goals.append(existing_goal)
                        logged_goals.append(existing_goal)
                        is_duplicate = True
                        break

                if not is_duplicate:
                    new_goal = Goal(
                        title=goal[0],
                        description=goal[1],
                        is_custom=True,
                    )
                    new_goal.save()
                    new_goal.role.set([self.role])

                    created_goals.append(new_goal)
                    logged_goals.append(new_goal)
            except Exception as e:
                # Log the error and continue with the next goal
                print(f"Error saving goal: {e}")

        try:
            GoalSuggestionLog.objects.bulk_create(
                [
                    GoalSuggestionLog(
                        user_profile=self.user_profile,
                        goal=logged_goal,
                        suggestion_source="ai",
                        role=self.role,
                    )
                    for logged_goal in logged_goals
                ]
            )
        except Exception as e:
            # Log the error
            print(f"Error creating goal suggestion logs: {e}")

        return created_goals
