from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramSimilarity, SearchRank
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from goal_task_management.models import Goal
from goal_task_management.serializers import GoalSuggestionInputSerializer, GoalSerializer



class GoalSuggestionsViewset(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSuggestionInputSerializer
    queryset = Goal.objects.all()

    def create(self, request, *args, **kwargs):
        # Fetch the roles associated with the user profile
        user_profile = request.user.user_profile
        roles_queryset = user_profile.roles.all()

        # Initialize the serializer with the filtered queryset directly
        suggestion_serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )

        # Set the queryset directly after initialization
        suggestion_serializer.fields['role'].queryset = roles_queryset

        if suggestion_serializer.is_valid():
            role = suggestion_serializer.validated_data['role']
            suggested_goals = Goal.objects.filter(role=role)

            search_query = request.data.get('search', None)
            if search_query:
                # Creating a custom search vector for title and description
                vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')

                # Create a SearchQuery with a custom weighting
                query = SearchQuery(search_query, search_type='websearch')

                # Annotate the queryset with rank and trigram similarity
                suggested_goals = Goal.objects.annotate(
                    rank=SearchRank(vector, query),
                    trigram_similarity=TrigramSimilarity('title', search_query)
                ).filter(
                    Q(rank__gte=0.2) | Q(trigram_similarity__gt=0.2)  # Lowered threshold to catch more matches
                ).distinct().order_by('-rank', '-trigram_similarity')

                if not suggested_goals.exists():
                    return Response({'detail': 'No goals found'}, status=status.HTTP_404_NOT_FOUND)

            return Response(GoalSerializer(suggested_goals, many=True).data)

        return Response(suggestion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
