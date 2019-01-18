from rest_framework.serializers import ModelSerializer
from .models import BloodGroup


class BloodGroupSerializer(ModelSerializer):

    class Meta:
        model = BloodGroup
        fields = ("a_positive", "o_positive", "b_positive", "ab_positive", "a_negative",
                  "o_negative", "b_negative", "ab_negative")
