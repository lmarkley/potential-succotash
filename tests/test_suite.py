import pytest
from api_calls import *

def test_get_all():
	games = get_all_games()
	num_games = count_games(games)
	assert num_games is 4

def test_get_by_id():
	game_id = 0
	game = get_game_by_id(game_id)
	assert game['title'] == "The Witcher 3" and \
			game['id'] is 0 and \
			game['publisher'] == "CD Project Red" and \
			game['year_published'] == "2015"

def test_add_game():
	add_game()
	games = get_all_games()
	num_games = count_games(games)
	assert num_games is 5

def test_rem_game():
	remove_game(4)
	games = get_all_games()
	num_games = count_games(games)
	assert num_games is 4