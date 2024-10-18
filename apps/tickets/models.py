from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()


class Issue(models.Model):
    STATUS_CHOICES = [
        ("TODO", "To Do"),
        ("IN_PROGRESS", "In Progress"),
        ("DONE", "Done"),
    ]

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    title = models.CharField(max_length=200)
    short_description = models.TextField()
    long_description = CKEditor5Field(
        "Long Description",
        config_name="extends",
        default="Long Description of issue",
        null=False,
        blank=False,
    )  # Rich text field
    priority = models.CharField(
        max_length=12,
        choices=PRIORITY_CHOICES,
        default="Medium",
        null=False,
        blank=False,  # Ensure that blank or null values are not allowed
    )

    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default="TODO",
        null=False,
        blank=False,  # Ensure that blank or null values are not allowed
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Backlog(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
