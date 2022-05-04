from rest_framework import serializers  
from src.address.models import Address

class AddressSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    address_type = serializers.SerializerMethodField()
    address_line_1 = serializers.SerializerMethodField()
    address_line_2 = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    postal_code = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = [
            'name',
            'address_type',
            'address_line_1',
            'address_line_2',
            'city',
            'country',
            'state',
            'postal_code'
        ]

    def get_name(self, obj):
        return obj.name
    
    def get_address_type(self, obj):
        return obj.address_type

    def get_address_line_1(self, obj):
        return obj.address_line_1

    def get_address_line_2(self, obj):
        return obj.address_line_2

    def get_city(self, obj):
        return obj.city

    def get_country(self, obj):
        return obj.country

    def get_state(self, obj):
        return obj.state

    def get_postal_code(self, obj):
        return obj.postal_code
