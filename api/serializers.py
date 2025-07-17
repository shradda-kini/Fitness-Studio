from rest_framework import serializers
from .models import *

class FitnessClassSerializer(serializers.ModelSerializer):
    available_slots = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'datetime', 'instructor', 'available_slots']

    def get_available_slots(self, obj):
        return obj.slots_remaining()



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['fitness_class', 'client_name', 'client_email']

    def validate(self, data):
        fc = data['fitness_class']
        if fc.is_full():
            raise serializers.ValidationError("Class is full.")
        return data
