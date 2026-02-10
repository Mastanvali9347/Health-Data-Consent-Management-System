from rest_framework import serializers
from .models import Consent

class ConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consent
        fields = '__all__'
        read_only_fields = ('patient',)
