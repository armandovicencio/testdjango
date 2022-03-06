from django.db import models
from acceso.models import Usuario


class Wish(models.Model):
    item = models.CharField(max_length=50)
    description = models.TextField()
    uploaded_by = models.ForeignKey(
        Usuario, related_name="items_add", on_delete=models.CASCADE)
    granted = models.IntegerField(default=1)
    users_who_like = models.ManyToManyField(
        Usuario, related_name="liked_whishes_granted")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    


     
