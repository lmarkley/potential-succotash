import requests
import json

BASE_URL='http://GamesAPI:5000/api/v1/resources/games'

def get_all_games():
	response = requests.get(BASE_URL + '/all')
	return response.json()

def get_game_by_id(game_id):
	ID_URL = BASE_URL + '?id=' + str(game_id)
	response = requests.get(ID_URL)
	return response.json()[0]

def count_games(games):
	return len(games)


def add_game():
	ADD_URL = BASE_URL + '/add'
	data = '{ \
				"title":"Halo Infinite", \
				"publisher": "Microsoft", \
				"year_published": "2021" \
			}'
	headers = {"Content-Type": "application/json"}

	response = requests.post(ADD_URL, headers=headers, data=data)

def remove_game(game_id):
	REM_URL = BASE_URL + '/remove?id=' + str(game_id)
	response = requests.get(REM_URL)
