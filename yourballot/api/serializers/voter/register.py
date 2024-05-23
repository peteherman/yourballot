from django.core.validators import MinValueValidator, RegexValidator
from rest_framework import serializers

from yourballot.party import PoliticalParty
from yourballot.voter.models.voter import Ethnicity, Gender, Race


class VoterRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    age = serializers.IntegerField(
        validators=[MinValueValidator(limit_value=0, message="Minimum age is 0 year(s) old")],
        required=False,
        allow_null=True,
    )
    ethnicity = serializers.ChoiceField(choices=Ethnicity.choices, required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=Gender.choices, required=False, allow_null=True)
    race = serializers.ChoiceField(choices=Race.choices, required=False, allow_null=True)
    political_identity = serializers.CharField(max_length=1024, allow_blank=True)
    political_party = serializers.ChoiceField(choices=PoliticalParty.choices, required=False, allow_null=True)
    zipcode = serializers.CharField(
        max_length=10, validators=[RegexValidator(regex=r"^\d{5}$", message="Zip code must be in the format XXXXX")]
    )
    password = serializers.CharField(max_length=100, min_length=6)
