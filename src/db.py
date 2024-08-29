import os
import re

from pymongo import MongoClient
from util import generate_room_id
from util import convert_movie

class DB():
  
  def __init__(self):
    uri = os.environ.get("MONGOURI", "localhost:27017")
    client = MongoClient(uri)
    self.db = client.movienight

  def create_room(self):
    collection = self.db.rooms
    room_id = generate_room_id()
    result = collection.insert_one({'room_id' : room_id})
    if result.acknowledged:
      return {"success" : True, "room_id" : room_id}
    else:
      return {"success" : False}

  def all_rooms(self):
    collection = self.db.rooms
    rooms = collection.find()
    return rooms
  
  def single_room(self, room_id):
    collection = self.db.rooms
    room = collection.find_one({"room_id": room_id})
    return room
  
  def search_movies(self, term):
    collection = self.db.movies
    # consider text index to use $text
    term = re.compile(term, re.IGNORECASE)
    movies = collection.find({"title" : {"$regex" : term}})
    movies = [convert_movie(movie) for movie in movies]
    return movies
  
  def add_movie_to_room(self, room_id, movie_id, user_id):
    rooms = self.db.rooms
    result = rooms.update_one(
      {"room_id" : room_id},
      {"$addToSet": {"movies" : {"movie_id" : movie_id, "user_id" : user_id} }})
    if result.modified_count == 1:
      return {"success" : True}
    else:
      return {"success" : False}
      
  def remove_movie_from_room(self, room_id, movie_id, user_id):
    rooms = self.db.rooms
    rooms.update_one(
      {"room_id" : room_id},
      {"$pull": {"movies" : { "movie_id" : movie_id, "user_id" : user_id}  }})
    