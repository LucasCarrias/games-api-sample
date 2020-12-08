from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpRequest
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import Game
from .serializers import GameSerializer


@api_view(['GET', 'POST'])
def game_list(request: HttpRequest) -> Response:
    if request.method == "POST":
        game_serializer = GameSerializer(data=request.data)
        if game_serializer.is_valid():
            try:
                game_serializer.save()
            except IntegrityError as err:
                return Response({"error": str(err)}, status=status.HTTP_409_CONFLICT)
            return Response(game_serializer.data, status=status.HTTP_201_CREATED)
        return Response(game_serializer.errors, status=status.HTTP_409_CONFLICT)
    elif request.method == "GET":
        games = Game.objects.all()
        games_serializer = GameSerializer(games, many=True)
        return Response(games_serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def game_detail(request: HttpRequest, pk: int) -> Response:
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":        
        game_serializer = GameSerializer(game)
        return Response(game_serializer.data)
    elif request.method == "PUT":
        game_serializer = GameSerializer(game, data=request.data)
        if game_serializer.is_valid():
            game_serializer.save()
            return Response(game_serializer.data)
        return Response(game_serializer.errors, status=status.HTTP_409_CONFLICT)
    elif request.method == "DELETE":
        try:
            game.delete()
        except ValidationError as err:
            return Response({"error": err.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)