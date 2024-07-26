from django.contrib.auth.models import User
from django.db import models

class DesignSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    design_link = models.URLField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='designs')

    def __str__(self):
        return f"Design Submission {self.id}: {self.name}"

class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.ForeignKey(DesignSubmission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'design')

class ClosetItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_designs')
    design = models.ForeignKey(DesignSubmission, on_delete=models.CASCADE)

    def __str__(self):
        return f"Closet Item {self.id} for User {self.user.username}"
