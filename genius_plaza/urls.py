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
    url(regex=r'^recipe/$', view=views.RecipeListView.as_view(), name='recipe-list'),
    url(regex=r'^recipe/create/$', view=views.RecipeCreateView.as_view(), name='recipe-create'),
    url(regex=r'^recipe/(?P<pk>\d+)/$', view=views.RecipeDetailView.as_view(), name='recipe-detail'),
    url(regex=r'^recipe/(?P<pk>\d+)/update/$', view=views.RecipeUpdateView.as_view(), name='recipe-update'),
    url(regex=r'^recipe/(?P<pk>\d+)/delete/$', view=views.RecipeDeleteView.as_view(), name='recipe-delete'),
    url(regex=r'^recipe-by-user-pk/(?P<pk>\d+)/$', view=views.RecipeByUserPKView.as_view(), name='recipe-by-user-pk'),
    url(regex=r'^recipe-by-user-username/(?P<username>[a-z0-9_]+)/$', view=views.RecipeByUserUsernameView.as_view(), name='recipe-by-user-username'),
]
