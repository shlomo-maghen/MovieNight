from pydantic import BaseModel


class Movie:
  
  def __init__(self, title, id):
    self.id = id
    self.title = title
  
  def title(self):
    return self.title
  
  def id(self):
    return self.id
  
class RoomMovie(BaseModel):
  room_id: str
  movie_id: str
  user_id: str
  user_display_name: str | None = None
  
class SearchRequest(BaseModel):
  search_term: str