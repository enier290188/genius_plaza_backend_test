from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
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


class RecipeList(APIView):
    def get(self, request):
        recipes = models.Recipe.objects.all()
        serializer = serializers.RecipeSerializer(recipes, many=True)
        return Response(serializer.data)


class RecipeCreate(APIView):
    def post(self, request):
        serializer = serializers.RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetail(APIView):
    def get_object(self, pk):
        try:
            return models.Recipe.objects.get(pk=pk)
        except models.Recipe.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        recipe = self.get_object(pk)
        serializer = serializers.RecipeSerializer(recipe)
        return Response(serializer.data)


class RecipeChange(APIView):
    def get_object(self, pk):
        try:
            return models.Recipe.objects.get(pk=pk)
        except models.Recipe.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        recipe = self.get_object(pk)
        serializer = serializers.RecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDelete(APIView):
    def get_object(self, pk):
        try:
            return models.Recipe.objects.get(pk=pk)
        except models.Recipe.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        recipe = self.get_object(pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def recipe_by_user(request, pk):
    try:
        user = models.User.objects.get(pk=pk)
    except models.User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    recipes = models.Recipe.objects.all().filter(user=user)
    serializer = serializers.RecipeSerializer(recipes, many=True)
    return Response(serializer.data)
