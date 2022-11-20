from rest_framework import serializers

from warehouse.article import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.reorder_threshold = validated_data.get('reorder_threshold', instance.reorder_threshold)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
