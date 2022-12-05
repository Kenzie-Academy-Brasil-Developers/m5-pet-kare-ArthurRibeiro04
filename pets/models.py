from django.db import models

class SexOptions(models.TextChoices):
    MALE="Male"
    FEMALE="Female"
    NOTINFORMED="Not informed"

class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20,
        choices=SexOptions.choices,
        default=SexOptions.NOTINFORMED
    )
    group = models.ForeignKey(
        "groups.Group", on_delete=models.CASCADE, related_name="pets"
    )
    
    def __repr__(self) -> str:
        return f'<Pet [{self.pk}] - {self.name} - {self.sex}>'
