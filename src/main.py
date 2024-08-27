from typing import Union

from fastapi import FastAPI
from db import DB

app = FastAPI()
db_client = DB()

""" Rooms """

@app.get("/rooms")
def rooms():
  """
  Gets all rooms.
  """
  rooms = db_client.all_rooms()
  return {
    "success" : True,
    "rooms" : [{"room_id" : x["room_id"]}  for x in rooms]
  }

@app.get("/rooms/{room_id}")
def room(room_id: str):
  """
  Gets a single room.
  """
  room = db_client.single_room(room_id)
  if room:
    return {"success" : True, "room_id" : room["room_id"]}  
  else:
    return {"success" : False, "info" : "room not found"}

@app.post("/rooms")
def create_room():
  """
  Creates a room.
  """
  result = db_client.create_room()
  return {"success" : result["success"], "room_id": str(result["room_id"])}

""" Movies """
@app.get("/search")
def search(term: str):
  """
  Returns a list of movies that contain the search term.
  """
  movies = db_client.search_movies(term)
  return {"success" : True, "movies" : movies}

@app.post("/add_movie_to_room")
def add_movie_to_room(room_id: str, movie_id: str, user_id: str):
  """
  Adds a movie-user combination to a specified room. If the movie_id and user_id combination exists,
  this does nothing.
  """
  db_client.add_movie_to_room(room_id, movie_id, user_id)
  return {"success" : True}

@app.delete("/remove_movie_from_room")
def add_movie_to_room(room_id: str, movie_id: str, user_id: str):
  """
  Removes a movie-user from a room. If the movie_id and user_id combination doesn't exist, 
  this does nothing.
  """
  db_client.remove_movie_from_room(room_id, movie_id, user_id)
  return {"success" : True}