from rest_framework import serializers
from .models import DesignSubmission

class DesignSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignSubmission
        fields = '__all__'
