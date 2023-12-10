"""
URL configuration for recipeApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from mainapp.views import recipe_list, new_recipe, recipe_detail, signup, signin, my_recipes, delete_recipe, edit_recipe

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='login/', permanent=False), name='index'),
    path('recipes/', recipe_list, name='recipe_list'),
    path('recipes/new/', new_recipe, name='new_recipe'),
    path('recipes/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
    path('recipes/<int:pk>/delete/', delete_recipe, name='recipe_delete'),
    path('recipes/<int:pk>/edit/', edit_recipe, name='recipe_edit'),
    path('my_recipes/', my_recipes, name='my_recipes'),
    path('signup/', signup, name='signup'),
    path('login/', signin, name='login'),
    path('logout/', LogoutView.as_view(),   name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

