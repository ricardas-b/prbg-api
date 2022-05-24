from django.urls import path

from . import views



urlpatterns = [
    path('show-quote/<int:pk>/', views.show_quote_with_tags, name='show-quote-with-tags'),
    path('update-quote/<int:pk>/', views.update_quote, name='update-quote'),
    path('update-tags/<int:pk>/', views.update_tags, name='update-tags'),   # <pk> is that of the Quote, for which Tags are being updated

]