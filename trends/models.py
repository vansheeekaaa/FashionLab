from django.db import models

class DesignSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    design_link = models.URLField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Design Submission {self.id}: {self.name}"

