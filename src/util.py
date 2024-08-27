import random
import string

from models import Movie

def generate_room_id():
  return ''.join([random.choice(string.ascii_uppercase) for x in range(5)])

def convert_movie(movie):
  """
  Converts a mongo movie result to a Movie object
  """
  return Movie(id=movie["id"], title=movie["title"])