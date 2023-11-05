from rest_framework import serializers
from watchlist.models import Movie

def equality_check(value):
    if len(value) < 5:
        raise serializers.ValidationError("Description should be atleast 5 characters long")
    return data
class MovieSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField()
    description=serializers.CharField(validators=[equality_check])
    active=serializers.BooleanField()
    
    def validate_name(self,value):
        if len(value) < 3:
            raise serializers.ValidationError("name should be greater than 3 letters")
        return value
    
    # def validate(self,data):
    #     if data['name']==data['description']:
    #         raise serializers.ValidationError("name and description should be different")
    #     return value
        
        
        
    def create(self,validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(self,instance,validated_data):
        instance.name=validated_data.get('name',instance.name)
        instance.description=validated_data.get('description',instance.description)
        instance.active=validated_data.get('active',instance.active)
        instance.save()
        return instance