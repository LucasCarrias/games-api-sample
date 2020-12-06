from datetime import datetime, timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Game
from .serializers import GameSerializer


class GameTests(APITestCase):
    def set_up(self):
        gamedatetime = timezone.make_aware(
                    datetime.now() + timedelta(hours=1),
                    timezone.get_current_timezone()
                )
        print(gamedatetime)
        data = {
            'name': 'TestGame',
            'release_date': gamedatetime,
            'game_category': 'Test Category',
            'played':False
        }
        game_test = Game(**data)
        game_test.save()

    def test_create_game(self):
        url = reverse('games-list')
        gamedatetime = timezone.make_aware(
                    datetime.now(),
                    timezone.get_current_timezone()
                )
        data = {
            'name': 'TestGame',
            'release_date': gamedatetime,
            'game_category': 'Test Category',
            'played':False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Game.objects.get().name, 'TestGame')
    
    def test_list_game(self):
        self.set_up()
        url = reverse('games-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Game.objects.get().name, 'TestGame')

    def test_get_detail_game(self):
        self.set_up()
        url = reverse('games-detail', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Game.objects.get().name, 'TestGame')
    
    def test_get_detail_game_not_found(self):
        url = reverse('games-detail', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_detail_game(self):
        self.set_up()
        game = Game.objects.get(pk=1)
        game.name = "UpdatedTestGame"
        game_serializer = GameSerializer(game)

        url = reverse('games-detail', kwargs={'pk':1})
        response = self.client.put(url, game_serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Game.objects.get().name, 'UpdatedTestGame')

    def test_delete_detail_game(self):
        self.set_up()
        url = reverse('games-detail', kwargs={'pk':1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Game.objects.count(), 0)

    def test_should_not_post_with_duplicated_name(self):
        self.set_up()
        url = reverse('games-list')
        gamedatetime = timezone.make_aware(
                    datetime.now(),
                    timezone.get_current_timezone()
                )
        data = {
            'name': 'TestGame',
            'release_date': gamedatetime,
            'game_category': 'Test Category',
            'played':False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_not_update_with_duplicated_name(self):
        self.set_up()
        url = reverse('games-detail', kwargs={'pk':2})
        gamedatetime = timezone.make_aware(
                    datetime.now(),
                    timezone.get_current_timezone()
                )
        data = {
            'name': 'TestGame2',
            'release_date': gamedatetime,
            'game_category': 'Test Category',
            'played':False
        }
        game_test = Game(**data)
        game_test.save()
        game_test.name = 'TestGame'
        game_serializer = GameSerializer(game_test)

        response = self.client.put(url, game_serializer.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_not_delete_released_games(self):
        gamedatetime = timezone.make_aware(
                    datetime.now() - timedelta(hours=1),
                    timezone.get_current_timezone()
                )
        data = {
            'name': 'TestGame',
            'release_date': gamedatetime,
            'game_category': 'Test Category',
            'played':False
        }
        game_test = Game(**data)
        game_test.save()
        game_serializer = GameSerializer(game_test)

        url = reverse('games-detail', kwargs={'pk':1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Game.objects.count(), 1)