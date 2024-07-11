from django.db import models
from django.contrib.auth.models import User

class DesignSubmission(models.Model):
    login_id = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    design_link = models.URLField()

    def __str__(self):
        return f"Design Submission {self.id}: {self.login_id}"
    
class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return self.url

class Design(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='design_images/')

    def __str__(self):
        return self.title

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.voter} voted for {self.design}'
