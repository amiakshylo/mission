from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import CharField
from django.db.models.functions import Greatest
from rest_framework.filters import SearchFilter


class TrigramSimilaritySearchFilter(SearchFilter):
    search_param = 'search'

    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'search_fields', [])
        search_terms = self.get_search_terms(request)
        search_term = ' '.join(search_terms)

        if not search_fields or not search_term:
            return queryset

        similarity_annotations = {}

        for idx, field in enumerate(search_fields):
            if '__' in field:
                field_name = field.replace('__', '_')
                queryset = queryset.annotate(
                    **{f'{field_name}_agg': StringAgg(field, delimiter=' ', output_field=CharField())}
                )
                similarity_annotations[f'similarity_{field_name}'] = TrigramSimilarity(f'{field_name}_agg',
                                                                                       search_term)
            else:
                similarity_annotations[f'similarity_{idx}'] = TrigramSimilarity(field, search_term)

        queryset = queryset.annotate(**similarity_annotations)
        similarity_fields = list(similarity_annotations.keys())

        if len(similarity_fields) == 1:
            similarity_score = list(similarity_annotations.values())[0]
            queryset = queryset.annotate(similarity=similarity_score)
        else:
            queryset = queryset.annotate(similarity=Greatest(*similarity_annotations.values()))

        queryset = queryset.filter(similarity__gt=0.2).order_by('-similarity')

        return queryset.distinct()
