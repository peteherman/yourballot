from rest_framework import serializers

from yourballot.locality.models.political_locality import PoliticalLocality


class PoliticalLocalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliticalLocality
        fields = ["id", "geo_json_id", "created", "updated", "name", "type"]
