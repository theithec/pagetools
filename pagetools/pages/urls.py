from django.urls import path
from pagetools.pages.views import PageView

app_name = "pages"
urlpatterns = [
        path('<slug:slug>/', PageView.as_view(), name="pageview"),
]
