import yaml
import ply


class customset(set):
  def __init__(self):
    set.__init__(self)
  

a = customset()
a.add((1,2,3))
a.add((3,2,3))
print(a)
if(3,2,3) in a:
  print("hello")
