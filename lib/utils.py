from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email
from django.db import transaction
from rest_framework.utils import model_meta

from rest_framework import filters
import traceback
import json

from core_api.models import Status

def get_statuses(ids):
    statuses = []

    for id in ids:
        data = StatusSerializer(instance=Status.objects.get(id=id))
        statuses.append(data.data)
    return statuses

class FilterJSON(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        if 'search' in request.GET:
            search = request.GET['search']
        else:
            return queryset

        filtered_queryset = list()

        for item in queryset:
            data = json.loads(item.data.replace('\'','\"'))
            for field in data:
                if search in data[field]:
                    filtered_queryset.append(item)

        return filtered_queryset

def validate_email(value):
    """Validate a single email."""
    if not value:
        return False
    # Check the regex, using the validate_email from django.
    try:
        django_validate_email(value)
    except ValidationError:
        return False
