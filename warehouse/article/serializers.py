from rest_framework import serializers

import config
from warehouse.article.models import Article
from warehouse.article.services.article_manager import ArticleManager
from warehouse.inventory.services.inventory_manager import InventoryManager


class ArticleSerializer(serializers.ModelSerializer):
    current_availability = serializers.SerializerMethodField(method_name='get_current_availability', read_only=True)
    class Meta:
        model = Article
        fields = '__all__'

    def get_current_availability(self, obj):
        return InventoryManager().get_current_quantity_for_article(obj.barcode)


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.reorder_threshold = validated_data.get('reorder_threshold', instance.reorder_threshold)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    def create(self, validated_data):
        if validated_data.get('barcode') == '-1':

            generated_barcode = ArticleManager.generate_unique_barcode(length=config.ARTICLE_BARCODE_LENGTH)

            while Article.objects.filter(barcode=generated_barcode).exists():
                generated_barcode = ArticleManager.generate_unique_barcode(length=10)

            article = Article.objects.create(barcode=generated_barcode,
                                             name=validated_data.get('name'),
                                             description=validated_data.get('description'),
                                             reorder_threshold=validated_data.get('reorder_threshold'),
                                             is_active=validated_data.get('is_active'))
        else:
            article = Article.objects.create(**validated_data)
        return article
