from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# creating table
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))
    
# how it is going to be shown
    def __repr__(self):
        return f"{self.name} - {self.description}"
       
# from now on, routes creations (first one is a test)
@app.route('/')
def index():
    return 'Hello!'

# show all
@app.route('/games')
def get_games():
    games = Game.query.all()
    
    output = []
    for game in games:
        game_data = {'name': game.name, 'description': game.description}
        output.append(game_data)
    return {'Games' : output}

# get
@app.route('/games/<id>')
def get_game(id):
    game = Game.query.get_or_404(id)
    return {"name": game.name, "description": game.description}

# add/post
@app.route('/games', methods=['POST'])
def add_game():
    game = Game(name=request.json['name'], description=request.json['description'])
    db.session.add(game)
    db.session.commit()
    return {'id': game.id}

# delete
@app.route('/games/<id>', methods=['DELETE'])
def delete_game(id):
    game = Game.query.get(id)
    if game is None:
        return {"error": "not found"}
    db.session.delete(game)
    db.session.commit()
    return {"message": "lesgo"}

# update
@app.route('/games/<id>', methods=['PUT'])
def update_game(id):
    game = Game.query.get_or_404(id)
    game_add = Game(name=request.json['name'], description=request.json['description'])
    if game is None:
        return {"error": "not found"}
    else:
        db.session.delete(game)
        db.session.add(game_add)
        db.session.commit()
        return {"message": "success"}

# export FLASK_APP=application.py
# export FLASK_ENV=development
# these are needed