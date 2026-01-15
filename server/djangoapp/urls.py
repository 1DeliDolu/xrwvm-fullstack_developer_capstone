from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from . import views


app_name = "djangoapp"
urlpatterns = [
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.registration, name="register"),
    path("get_cars", views.get_cars, name="getcars"),
    path("get_dealers", views.get_dealerships, name="get_dealers"),
    path(
        "get_dealers/<str:state>",
        views.get_dealerships,
        name="get_dealers_by_state",
    ),
    path(
        "dealer/<int:dealer_id>",
        views.get_dealer_details,
        name="dealer_details",
    ),
    path(
        "dealer/<int:dealer_id>/reviews",
        views.get_dealer_reviews,
        name="dealer_reviews",
    ),
    path("dealers/", TemplateView.as_view(template_name="index.html")),
    path("add_review", views.add_review, name="add_review"),
    path(
        "postreview/<int:dealer_id>",
        TemplateView.as_view(template_name="index.html"),
    ),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
