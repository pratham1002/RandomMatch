from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class SiteUser(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    bits_id = models.CharField(max_length=50)
    year=models.CharField(max_length=5)
    gender=models.CharField(max_length=2, default='M')
    verification_code=models.CharField(max_length=10, default='0')
    participate_request=models.BooleanField(default=False)
    participate_request_change_pr=models.BooleanField(default=True)
    participate_request_granted=models.BooleanField(default=False)
    priority_number=models.IntegerField(default=0)
    assigned_place=models.CharField(max_length=100, default='')
    matched_with=models.CharField(max_length=50)
    match_number=models.CharField(max_length=50)

    def __str__(self):
        return self.bits_id

class Places(models.Model):
    place_name=models.CharField(max_length=100)

    def __str__(self):
        return self.place_name

def validate_only_one_instance(obj):
    model=obj.__class__
    if (model.objects.count()>0 and obj.id != model.objects.get().id):
        raise ValidationError("Can create only one instance of Preferences")

class Sitesettings(models.Model):
    obj_number=models.IntegerField(default=0)
    allow_change_participation=models.BooleanField(default=True)
    allow_user_match=models.BooleanField(default=False)
    pr_no=models.IntegerField(default=0)
    data_populated=models.BooleanField(default=False)

    
    def clean(self):
        validate_only_one_instance(self)

