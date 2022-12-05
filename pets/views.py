from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.request import Request
from django.forms.models import model_to_dict

from .models import Pet
from groups.models import Group
from.serializers import PetSerializer


class PetView(APIView):
    def get(self, request:Request) -> Response:
        pets = Pet.objects.all()
        
        pet_dict = []
        
        for pet in pets:
            serializer = PetSerializer(pet)
            pet_dict.append(serializer.data)
        
        return Response(pet_dict, status.HTTP_200_OK)
    
    def post(self, request:Request) -> Response:
        
        errors = {}
        
        if 'name' not in request.data:
            errors['name'] = "This field is required."
        if 'age' not in request.data:
            errors['age'] = "This field is required."
        if 'weight' not in request.data:
            errors['weight'] = "This field is required."
        if 'sex' not in request.data:
            errors['sex'] = "This field is required."
        if 'group' not in request.data:
            errors['group'] = "This field is required."
        if 'traits' not in request.data:
            errors['traits'] = "This field is required."       
                     
        if len(errors) > 0:
            return Response(errors, status.HTTP_400_BAD_REQUEST)
        
        pet_data = request.data
        
        serializer = PetSerializer(data=pet_data)
        
        serializer.is_valid()
        
        serializer.save()
        
        return Response(serializer.data, status.HTTP_201_CREATED)
    
class PetIdView(APIView):
    
    def delete(self, request: Request, pet_id):
        try:
            pet = Pet.objects.get(id=pet_id)
        except:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)
        
        pet.delete()
        
        return Response({}, status.HTTP_204_NO_CONTENT)
        
        
    
    def get(self, request: Request, pet_id):
        try:
            pet = Pet.objects.get(id=pet_id)
        except:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)
        
        serializer = PetSerializer(pet)
        
        return Response(serializer.data, status.HTTP_200_OK)
        
    
    def patch(self, request: Request, pet_id):
        try:
            pet = Pet.objects.get(id=pet_id)
        except:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)
        
        new_pet_data = request.data
        
        
        serializer = PetSerializer(pet, new_pet_data, partial=True)
        serializer.is_valid()
        
        serializer.save()
        
        return Response(serializer.data, status.HTTP_200_OK)
        
        
        
        


