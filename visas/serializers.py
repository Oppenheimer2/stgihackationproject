from rest_framework import serializers
from .models import amrika

class amrikaSerializer(serializers.ModelSerializer):
    class Meta:
        model = amrika
        fields = '__all__'