from rest_framework import generics, viewsets
from rest_framework.response import Response
from . import models, serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer


class StepViewSet(viewsets.ModelViewSet):
    queryset = models.Step.objects.all()
    serializer_class = serializers.StepSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeListView(generics.ListAPIView):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer


class RecipeCreateView(generics.CreateAPIView):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer


class RecipeDetailView(generics.RetrieveAPIView):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    lookup_field = 'pk'


class RecipeUpdateView(generics.UpdateAPIView):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    lookup_field = 'pk'


class RecipeDeleteView(generics.DestroyAPIView):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    lookup_field = 'pk'


class RecipeByUserPKView(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        recipes = models.Recipe.objects.all().filter(user=self.get_object())
        serializer = serializers.RecipeSerializer(recipes, many=True)
        return Response(serializer.data)


class RecipeByUserUsernameView(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'

    def retrieve(self, request, *args, **kwargs):
        recipes = models.Recipe.objects.all().filter(user=self.get_object())
        serializer = serializers.RecipeSerializer(recipes, many=True)
        return Response(serializer.data)
