import json

from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import IssueForm, ProjectForm
from .models import Issue, Project

# Create your views here.


def kanban_view(request, project_id):
    project = Project.objects.get(id=project_id)
    issues = Issue.objects.filter(project=project)

    # Use the STATUS_CHOICES from the Issue model
    statuses = Issue.STATUS_CHOICES

    return render(
        request,
        "tickets/kanban.html",
        {"project": project, "issues": issues, "statuses": statuses},
    )


def backlog_view(request, project_id):
    project = Project.objects.get(id=project_id)
    issues = Issue.objects.filter(project=project).order_by("created_at")
    return render(
        request, "tickets/backlog.html", {"project": project, "issues": issues}
    )


def issue_detail_view(request, issue_id):
    issue = Issue.objects.get(id=issue_id)
    return render(request, "tickets/issue_detail.html", {"issue": issue})


def issue_create_view(request, project_id):
    project = get_object_or_404(
        Project, id=project_id
    )  # Retrieve the project using the project ID
    if request.method == "POST":
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(
                commit=False
            )  # Create an issue instance but don't save to the database yet
            issue.project = project  # Associate the issue with the selected project
            issue.save()  # Now save the issue to the database
            return redirect(
                "backlog_view", project_id=project.id
            )  # Redirect to the backlog view
    else:
        form = IssueForm(
            initial={"project": project}
        )  # Pre-fill the form with the project

    return render(
        request,
        "tickets/issue_create.html",
        {
            "form": form,
            "project": project,
        },
    )


def issue_update_view(request, issue_id):
    issue = Issue.objects.get(id=issue_id)
    form = IssueForm(request.POST or None, instance=issue)
    if form.is_valid():
        form.save()
        return redirect("issue_detail_view", issue_id=issue_id)
    return render(request, "tickets/issue_update.html", {"form": form})


def dashboard_view(request):
    projects = Project.objects.all()  # Get all projects
    return render(request, "tickets/dashboard.html", {"projects": projects})


def create_project_view(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard_view")
    else:
        form = ProjectForm()

    return render(request, "tickets/create_project.html", {"form": form})


@csrf_exempt
def update_issue_status(request, issue_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data
            new_status = data.get(
                "new_status_id"
            )  # Get the new status from AJAX request

            # Debug logging for incoming request
            print("Received data:", data)  # Log incoming data for debugging

            if (
                new_status in dict(Issue.STATUS_CHOICES).keys()
            ):  # Validate against valid choices
                issue = Issue.objects.get(id=issue_id)
                issue.status = new_status
                issue.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"error": "Invalid status value"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Issue.DoesNotExist:
            return JsonResponse({"error": "Issue not found"}, status=404)
