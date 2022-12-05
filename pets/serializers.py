from rest_framework import serializers
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer
from django.forms.models import model_to_dict

from .models import Pet, SexOptions
from groups.models import Group
from traits.models import Trait


class PetSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=SexOptions.choices,
        default=SexOptions.NOTINFORMED
    )
    traits_count = serializers.SerializerMethodField()
    group = GroupSerializer()
    traits = TraitSerializer(many=True)
    
    def get_traits_count(self, validated_data: Pet):
         traits = Trait.objects.all()
         
         contagem = 0
         
         for trait in traits:
             pets = trait.pets.all()
             for pet in pets:
                 if pet.name == validated_data.name:
                     contagem += 1
                     
         return contagem
        
    
        
        
    
    def create(self, validated_data:dict):
        
        
        
        group = validated_data['group']
        traits = validated_data['traits']
        
        validated_data.pop('group')
        validated_data.pop('traits')
        
        try:
            pet_group = Group.objects.get(scientific_name=group['scientific_name'])
        except:
            pet_group = Group.objects.create(**group)
            
        pet = Pet.objects.create(**validated_data, group=pet_group)
        
        for trait in traits:
            try:
                pet_trait = Trait.objects.get(name=trait['name'])
            except:
                pet_trait = Trait.objects.create(**trait)
        
            pet.traits.add(pet_trait)
        
        return pet
    
    def update(self, instance: Pet, validated_data: dict):
        
        if 'group' in validated_data:
            group = validated_data.pop('group')
            
            try:
                pet_group = Group.objects.get(scientific_name=group['scientific_name'])
            except:
                pet_group = Group.objects.create(**group)
                
            instance.group = pet_group
            
        
        
        
            
        instance.name = validated_data.get("name", instance.name)
        instance.age = validated_data.get("age", instance.age)
        instance.weight = validated_data.get("weight", instance.weight)
        instance.sex = validated_data.get("sex", instance.sex)
        
        
        if 'traits' in validated_data:
            traits = validated_data.pop('traits')

            new_traits = list()
        
            for trait in traits:
                try:
                    pet_trait = Trait.objects.get(name=trait['name'])
                except:
                    pet_trait = Trait.objects.create(**trait)
        
            new_traits.append(pet_trait)
        
            instance.traits.set(new_traits)
        
        instance.save()
        
        return instance
        
        
        
              
        
        
            
            
        
            