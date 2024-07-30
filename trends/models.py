from django.contrib.auth.models import User
from django.db import models

class DesignSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    design_link = models.URLField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='designs')
    top_image_url = models.URLField(null=True, blank=True)
    top_buy_url = models.URLField(null=True, blank=True)
    pants_image_url = models.URLField(null=True, blank=True)
    pants_buy_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Design Submission {self.id}: {self.name}"
    
class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.ForeignKey(DesignSubmission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'design')

class ClosetItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_designs')
    design = models.ForeignKey(DesignSubmission, on_delete=models.CASCADE, related_name='closet_items')

    class Meta:
        unique_together = ('user', 'design')
