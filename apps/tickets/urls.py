from django.urls import path

from . import views

urlpatterns = [
    path("kanban/<int:project_id>/", views.kanban_view, name="kanban_view"),
    path("backlog/<int:project_id>/", views.backlog_view, name="backlog_view"),
    path("issue/<int:issue_id>/", views.issue_detail_view, name="issue_detail_view"),
    path(
        "issue/create/<int:project_id>/",
        views.issue_create_view,
        name="issue_create_view",
    ),
    path(
        "issue/update/<int:issue_id>/",
        views.issue_update_view,
        name="issue_update_view",
    ),
    path("", views.dashboard_view, name="dashboard_view"),
    path("project/create/", views.create_project_view, name="create_project_view"),
    path(
        "update-issue-status/<int:issue_id>/",
        views.update_issue_status,
        name="update_issue_status",
    ),
]
