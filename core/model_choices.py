class UserProfileChoices:
    GENDER_MALE = "Male"
    GENDER_FEMALE = "Female"
    GENDER_OTHER = "Other"
    GENDER_NON_BINARY = "Non-binary"
    GENDER_NOT_TO_SAY = "Prefer not to say"
    GENDER_SELF_DESCRIBE = "Self describe"

    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
        (GENDER_NOT_TO_SAY, "Prefer not to say"),
        (GENDER_NON_BINARY, "Non-binary"),
        (GENDER_SELF_DESCRIBE, "Prefer to self-describe"),
    ]

    ASSISTANT_MODEL_CHOICES = [
        ("spouse", "Spouse"),
        ("friend", "Friend"),
        ("coach", "Coach"),
        ("therapist", "Therapist"),
    ]

    AGE_RANGE_UNDER_13 = 0
    AGE_RANGE_13_17 = 1
    AGE_RANGE_18_24 = 2
    AGE_RANGE_25_34 = 3
    AGE_RANGE_35_44 = 4
    AGE_RANGE_45_54 = 5
    AGE_RANGE_55_64 = 6
    AGE_RANGE_65_ABOVE = 7
    AGE_RANGE_PREFER_NOT_TO_SAY = 8

    AGE_RANGE_CHOICES = [
        (AGE_RANGE_UNDER_13, "Under 13"),
        (AGE_RANGE_13_17, "13-17"),
        (AGE_RANGE_18_24, "18-24"),
        (AGE_RANGE_25_34, "25-34"),
        (AGE_RANGE_35_44, "35-44"),
        (AGE_RANGE_45_54, "45-54"),
        (AGE_RANGE_55_64, "55-64"),
        (AGE_RANGE_65_ABOVE, "65 and above"),
        (AGE_RANGE_PREFER_NOT_TO_SAY, "Prefer not to say"),
    ]


class GoalTypeChoices:
    TYPE_LONG_TERM = (
        "long_term"  # Long-term goals are goals that take a long time to achieve
    )
    TYPE_SHORT_TERM = "short_term"  # Short-term goals are goals that can be achieved in a short period of time

    GOAL_TYPE_CHOICES = ((TYPE_SHORT_TERM, "Short-term"), (TYPE_LONG_TERM, "Long-term"))


class RoleChoices:
    PROFESSIONAL = "Professional Roles"
    PERSONAL = "Personal Roles"
    SELF_IMPROVEMENT = "Self-Improvement Roles"
    COMMUNITY_SOCIAL_IMPACT = "Community and Social Impact Roles"
    WELLNESS_SPIRITUAL = "Wellness and Spiritual Roles"

    ROLE_TYPE_CHOICES = [
        (PROFESSIONAL, "Professional Roles"),
        (PERSONAL, "Personal Roles"),
        (SELF_IMPROVEMENT, "Self-Improvement Roles"),
        (COMMUNITY_SOCIAL_IMPACT, "Community and Social Impact Roles"),
        (WELLNESS_SPIRITUAL, "Wellness and Spiritual Roles"),
    ]
