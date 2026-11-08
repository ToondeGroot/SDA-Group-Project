import math

#extra math functions for the system and math module /\

#extra math for rotating the lil guy
def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

def distance(v1, v2):
    return math.sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)