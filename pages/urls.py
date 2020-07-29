from django.urls import path
from . import views
# app_name='pages'
urlpatterns = [
    # path('<int:page_id>/<slug:page_slug>/', views.page, name="page"),
    path('page/', views.page, name="page")
]
