from rest_framework import serializers
from .models import Production, Set

class ProductionListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Production
		fields = ('id', 'name', 'price', 'type_product')

class SetListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Set
		fields = ('id', 'name', 'top', 'bottom')
		depth = 2

class ResultListSerializer(serializers.Serializer):
	productions = ProductionListSerializer(many = True)
	sets = SetListSerializer(many = True)