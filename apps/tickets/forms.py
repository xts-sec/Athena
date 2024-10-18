from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Issue, Project


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            "title",
            "short_description",
            "long_description",
            "priority",
            "status",
        ]  # Exclude 'project'
        widgets = {
            "long_description": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }

    def __init__(self, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        # Include the project as a hidden field:
        if "project" in kwargs:
            self.fields["project"] = forms.ModelChoiceField(
                queryset=Project.objects.all(),
                widget=forms.HiddenInput(),
                initial=kwargs["project"],
            )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]
