from django.conf.urls import include, url
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, 'users')
router.register(r'recipes', views.RecipeViewSet, 'recipes')
router.register(r'steps', views.StepViewSet, 'steps')
router.register(r'ingredients', views.IngredientViewSet, 'ingredients')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(regex=r'^recipe/$', view=views.RecipeList.as_view(), name='recipe'),
    url(regex=r'^recipe/add/$', view=views.RecipeCreate.as_view(), name='recipe-add'),
    url(regex=r'^recipe/(?P<pk>\d+)/detail/$', view=views.RecipeDetail.as_view(), name='recipe-detail'),
    url(regex=r'^recipe/(?P<pk>\d+)/change/$', view=views.RecipeChange.as_view(), name='recipe-change'),
    url(regex=r'^recipe/(?P<pk>\d+)/delete/$', view=views.RecipeDelete.as_view(), name='recipe-delete'),
    url(regex=r'^recipe-by-user/(?P<pk>\d+)/$', view=views.recipe_by_user, name='recipe-by-user'),
]
