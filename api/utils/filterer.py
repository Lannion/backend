from rest_framework.exceptions import NotFound

class QuerysetFilter:
    """Handles queryset filtering logic."""
    @staticmethod
    def filter_queryset(model, query_params):
        filters = {}
        for key in query_params:
            values = query_params.getlist(key)
            if len(values) > 1:
                filters[f"{key}__in"] = values
            else:
                filters[key] = values[0]

        if not filters:
            return model.objects.all()

        try:
            queryset = model.objects.filter(**filters)
            if not queryset.exists():
                raise NotFound(detail=f"No {model.__name__}s found matching the provided filters.")
            return queryset
        except Exception as e:
            raise NotFound(detail=f"Invalid filters provided: {e}")