import flask
from flask import request, jsonify, abort
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# games = [
# 	{
# 		'id':0,
# 		'title': 'The Witcher 3',
# 		'publisher': 'CD Project Red',
# 		'year_published': '2015'
# 	},
# 	{
# 		'id':1,
# 		'title': 'The Elder Scrolls V: Skyrim',
# 		'publisher': 'Bethesda Softworks',
# 		'year_published': '2011'
# 	}
# ]

'''
Helper functions
'''

def check_for_duplicates(cursor, param):
	if not cursor.execute("SELECT * FROM games WHERE title='" + param + "';").fetchall():
		return False
	else:
		return True

def get_next_id(cursor):
	last_index = cursor.execute("SELECT id FROM games ORDER BY id DESC LIMIT 1;").fetchall()[0]['id']
	next_index = int(last_index) + 1
	return next_index

def populate_dicts(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

'''
Error handling
'''

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.errorhandler(500)
def invalid_input(e):
	return "<h1>500</h1><p>The input provided is invalid.</p>", 500

'''
Pages
'''

@app.route('/', methods=['GET'])
def home():
	return "<h1> Silly-Ass Game Archive</h1><p>This site is a prototype API for keeping track of your silly-ass games.</p>"


'''
Endpoints
'''

@app.route('/api/v1/resources/games/all', methods=['GET'])
def api_all():

	conn = sqlite3.connect('games.db')
	conn.row_factory = populate_dicts
	cur = conn.cursor()
	all_games = cur.execute('SELECT * FROM games;').fetchall()

	return jsonify(all_games) 


@app.route('/api/v1/resources/games', methods=['GET'])
def api_id():

	# if 'id' in request.args:
	# 	id = int(request.args['id'])
	# else:
	# 	return "Error: Please specify a valid integer ID"

	# results = []

	# for game in games:
	# 	if game['id'] == id:
	# 		results.append(game)
	
	# return jsonify(results)

	query_parameters = request.args
	game_id = query_parameters.get('id')
	year_published = query_parameters.get('year_published')
	publisher = query_parameters.get('publisher')

	db_query = "SELECT * FROM games WHERE"
	to_filter = []

	if game_id:
		db_query += ' id=? AND'
		to_filter.append(game_id)
	if year_published:
		db_query += ' year_published=? AND'
		to_filter.append(year_published)
	if publisher:
		db_query += ' publisher=? AND'
		to_filter.append(publisher)
	if not (game_id or publisher or year_published):
		return page_not_found(404)

	db_query = db_query[:-4]+';'

	conn = sqlite3.connect('games.db')
	conn.row_factory = populate_dicts
	cur = conn.cursor()

	results = cur.execute(db_query, to_filter).fetchall()
	return jsonify(results)


@app.route('/api/v1/resources/games/add', methods=['POST'])
def api_add():

	query_parameters = request.get_json()

	db_query = "INSERT INTO games VALUES("

	conn = sqlite3.connect('games.db')
	conn.row_factory = populate_dicts
	cur = conn.cursor()

	game_id = get_next_id(cur)
	title = query_parameters['title']
	publisher = query_parameters['publisher']
	year_published = query_parameters['year_published']

	if check_for_duplicates(cur, title):
		abort(500, "Invalid input")

	if game_id:
		db_query += "'" + str(game_id) + "', "
	if title:
		db_query += "'" + str(title) + "', "
	if publisher:
		db_query += "'" + publisher + "', "
	if year_published:
		db_query += "'" + str(year_published) + "');"

	results = cur.execute(db_query).fetchall()
	results = cur.execute('commit;')

	return jsonify(success=True)

# 	results = []
# 	last_index = 0

# 	for game in games:
# 		last_index += 1

# 	if request.json:

# 	for game in games:
# 		if game['id'] == id:
# 			results.append(game)

# 	return jsonify(results) 

@app.route('/api/v1/resources/games/remove', methods=['GET'])
def api_remove():
	query_parameters = request.args

	game_id = query_parameters.get('id')

	db_query = "DELETE FROM games WHERE id = " + str(game_id) + ";"

	conn = sqlite3.connect('games.db')
	conn.row_factory = populate_dicts
	cur = conn.cursor()

	results = cur.execute(db_query).fetchall()
	cur.execute('commit;')

	return jsonify(success=True)

if __name__ == '__main__':
	app.run()