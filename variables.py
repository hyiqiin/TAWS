from dataclasses import dataclass

url = 'https://ch.tetr.io/api/'

# TETR.IO Game Ranks (High to Low)
ranks = ['x', 'u', 'ss',
         's+', 's', 's-',
         'a+', 'a', 'a-',
         'b+', 'b', 'b-',
         'c+', 'c', 'c-',
         'd+', 'd', 'z']

# Central tournaments list
tournaments = []

# Registration Status
open_reg = True

# League stats
@dataclass
class League():
  rank:str          # rank
  bestrank:str      # best rank
  apm:float         # Attack Per Minute
  pps:float         # Pieces Per Second
  vs:float          # Versus Stat
  tr:float          # TR

# Player information
@dataclass
class Info():
  _id:str           # ID
  username:str      # Username
  country:str       # Country
  rd:str            # Rating Deviation
  decaying:bool  # Has not played in the last week

@dataclass
class TourInfo():
  name:str
  channel:str
  role:str
  rank_cap:str
  rank_floor:str
  usernames:dict