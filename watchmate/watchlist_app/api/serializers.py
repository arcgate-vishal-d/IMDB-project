from rest_framework import serializers
from watchlist_app.models import Watchlist, StreamPlatform, Review

# # using Model Serializer  
# # It will automatically generate a set of fields for you, based on the model.
# # It will automatically generate validators for the serializer, such as unique_together validators.
# # It includes simple default implementations of .create() and .update().


class ReviewSerializer(serializers.ModelSerializer):

    # If we don't use this so it will give the review user id by default
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ('watchlist',)

class WatchlistSerializer(serializers.ModelSerializer):
    # adding new field using serializer or performing extra action on model field
    # name_length = serializers.SerializerMethodField()

    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Watchlist
        fields = '__all__'
        # exclude = ['name',]


    def get_name_length(self, object):
        # this .name is come from model
        return len(object.title)
    
# streaming platform serializer
class StreamPlatformSerializer(serializers.ModelSerializer):

    # watchlist is a related name which is defined in the model foriegn key field 
    # it can be same as defined in model

    watchlist = WatchlistSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'




# # # using Model Serializer  
# # # It will automatically generate a set of fields for you, based on the model.
# # # It will automatically generate validators for the serializer, such as unique_together validators.
# # # It includes simple default implementations of .create() and .update().

# class WatchlistSerializer(serializers.ModelSerializer):
#     # adding new field using serializer or performing extra action on model field
#     name_length = serializers.SerializerMethodField()

#     class Meta:
#         model = Watchlist
#         fields = '__all__'
#         # exclude = ['name',]


#     def get_name_length(self, object):
#         # this .name is come from model
#         return len(object.title)
    
# # streaming platform serializer
# class StreamPlatformSerializer(serializers.ModelSerializer):

#     # watchlist is a related name which is defined in the model foriegn key field 
#     # it can be same as defined in model

#     watchlist = WatchlistSerializer(many=True, read_only=True)

#     # It will show only the __str__ name (single name) which is written inside the model __str funtion
#     # watchlist = serializers.StringRelatedField(many=True)

#     # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


#     # Hyperlink 
#     # watchlist = serializers.HyperlinkedRelatedField(
#     #     many=True,
#     #     read_only=True,
#     #     view_name='movie-detail'        # which we defined in the urls.py -> name detail bcz we will redirect to the detail page
#     # )

#     class Meta:
#         model = StreamPlatform
#         fields = '__all__'
        

    # Validation

    # # field level validation
    # # name should be greater than 2
    # def validate_title(self, value):
    #     if len(value) < 3:
    #         raise serializers.ValidationError("Name is to short")
    #     return value
        
    # # Object level Validation
    # # name and description can't be same        
    # def validate(self, data):
    #     if data['title'].lower() == data['storyline'].lower():
    #         raise serializers.ValidationError(" name and description can't be same ")
    #     return data






# # Without model serializers

# class MovieSerializer(serializers.Serializer):

#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField()
#     active = serializers.BooleanField()


#     # Creating new data
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         '''
#         instance -> contain old value
#         validated_data -> contain new value
#         '''

#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

    

#     # Validation

#     # field level validation
#     # name should be greater than 2
#     def validate_name(self, value):
#         if len(value) < 3:
#             raise serializers.ValidationError("Name is to short")
#         return value
        
#     # Object level Validation
#     # name and description can't be same        
#     def validate(self, data):
#         if data['name'].lower() == data['description'].lower():
#             raise serializers.ValidationError(" name and description can't be same ")
#         return data