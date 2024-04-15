from typing import Any

from django.db.models import QuerySet
from rest_framework import mixins, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from yourballot.api.core.response import ballot_response
from yourballot.api.serializers.guest.matches import (GuestCandidateMatchRequestSerializer,
                                                      GuestCandidateMatchResponseSerializer)
from yourballot.candidate.models.candidate import Candidate
from yourballot.locality.models.zipcode_locality import ZipcodeLocality


class GuestMatchViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Candidate.objects.all()
    serializer_class = GuestCandidateMatchResponseSerializer
    ordering = ["id"]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = GuestCandidateMatchRequestSerializer(data=request.data)
        if serializer.is_valid():
            candidate_match_qs = self.build_candidate_match_qs(serializer.validated_data)
            paginated_queryset = self.paginate_queryset(candidate_match_qs)
            serializer_context = self.build_serializer_context(serializer.validated_data)
            if paginated_queryset is not None:
                candidate_serializer = self.serializer_class(paginated_queryset, many=True, context=serializer_context)
                return self.get_paginated_response(candidate_serializer.data)
            else:
                candidate_serializer = self.serializer_class(candidate_match_qs, many=True, context=serializer_context)
                return ballot_response(candidate_serializer.data, many=True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def build_candidate_match_qs(self, validated_data: dict[str, Any]) -> QuerySet:
        zipcode = validated_data["zipcode"]
        return Candidate.objects.filter(
            position__locality__in=ZipcodeLocality.objects.filter(zipcode=zipcode).values("political_locality")
        )

    def build_serializer_context(self, validated_data: dict[str, Any]) -> dict[str, Any]:
        issue_views = validated_data["issue_views"]
        context = {"issue_views": issue_views}
        return context
