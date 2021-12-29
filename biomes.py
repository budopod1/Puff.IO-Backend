from random import random
from math import sin
from tiles import Grass


class Wave:
  def __init__(self):
    self.size = 100
    self.wave_streches = [random() for i in range(self.size)]
    self.wave_offsets = [random() * self.size for i in range(self.size)]
    self.scale = 1
    self.hill = 20
  
  def generate(self, x):
    total = 0
    for wave in zip(self.wave_streches, self.wave_offsets):
      total += sin((x / self.scale - wave[1]) * wave[0]) * self.hill
    return total / self.size * self.scale


class Biome:
  def __init__(self):
    self.wave = Wave()
  
  def generate(self, x, y):
    if self.wave.generate(x) >= y:
      return Grass()
    return None
