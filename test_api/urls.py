from django.urls import path
from .views import LatencyView, LogoutView, SigninView, SignupView, UserInfoView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("signin/", SigninView.as_view(), name="signin"),
    path("info/", UserInfoView.as_view(), name="user-info"),
    path("latency/", LatencyView.as_view(), name="latency"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
