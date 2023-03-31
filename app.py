from flask import Flask, jsonify, request
from sqlalchemy import Column, String, Integer, create_engine, select
from sqlalchemy.orm import declarative_base, Session
from populate_data import populate_data

app = Flask(__name__)
engine = create_engine("sqlite+pysqlite:///database.db", echo=True, future=True)
Base = declarative_base()
session = Session(engine)

class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    platform = Column(String(30))
    price = Column(Integer)
    quantity = Column(Integer)
   
    def to_dict(self):
       return {
           'id': self.id,
           'name': self.name,
           'platform': self.platform,
           'price': 'R$' + str(self.price) + ',00',
           'quantity': self.quantity
       } 
    
Base.metadata.create_all(engine)

@app.route('/games', methods=['GET'])
def get_games():
    games = session.scalars(select(Game)).all()
    games_json = []
    for game in games:
        games_json.append(game.to_dict())
    return games_json

@app.route('/games', methods=['POST'])
def create_game():
    data = request.get_json()
    game = Game(name=data['name'], platform=data['platform'], price=data['price'], quantity=data['quantity'])
    session.add(game)
    session.commit()
    return jsonify({'message': 'Game created successfully!'})

@app.route('/populate', methods=['GET'])
def populate_games():
    for game in populate_data:
        game_instance = Game(name=game['name'], platform=game['platform'], price=game['price'], quantity=game['quantity'])
        session.add(game_instance)
    session.commit()
   
    return jsonify({'message': 'Database populated successfully!'})

if __name__ == '__main__':
    app.run(port=3000, debug=True)