from django.urls import path
from . import views


urlpatterns = [
    path("send-email/", views.send_email, name="send-email"),
    path("track/click/<unique_id>", views.track_click, name="track-click"),
    path("track/open/<unique_id>", views.track_open, name="track-open"),
    path("track/dashboard/", views.track_dashboard, name="track-dashboard"),
    path("track/stats/<str:id>", views.track_stats, name="track-stats"),
]
