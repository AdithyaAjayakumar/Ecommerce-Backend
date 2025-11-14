from rest_framework import serializers
from .models import Category, Tag, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','slug']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),many=True, required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields= [
            'id', 'name', 'description', 'price', 'stock',
            'category', 'tags', 'images', 'is_active',
            'created_at', 'updated_at'
        ]
    
    def create(self, validate_data):
        images_data = validate_data.pop('images',[]) # remove many-to-many before saving
        tags = validate_data.pop('tags',[]) # remove FK before saving
        validate_data.pop('created_by', None)  # ✅ Remove if already present
        user = self.context['request'].user # get logged-in user
        

        product = Product.objects.create(created_by = user,**validate_data)
        # Save Many-to-Many tags
        product.tags.set(tags)


        for img in images_data:
            ProductImage.objects.create(product=product, **img)

        return product

        def update(self, instance, validate_data):
            images_data = validate_data.pop('images', None)
            tags = validate_data.pop('tags', None)

            #update product basic fields
            for attr, value in validate_data.items():
                setattr(instance, attr, value)
            instance.save()

            #updates tags if provided
            if tags is not   None:
                instance.tags.set()

            #update product images if provided
            if images_data is not None:
                for img in images_data:
                    ProductImage.objects.create(product=instance, **img)

            return instance
