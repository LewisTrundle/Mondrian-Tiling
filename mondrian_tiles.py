import tkinter as tk
import random as ran
import copy


class Rectangle:
  def __init__(self, coords):
    self.coords = coords
    self.width = self.coords[2] - self.coords[0]
    self.height = self.coords[3] - self.coords[1]
    self.area = self.width * self.height
  

class State:
  def __init__(self, tiles, depth=0):
    self.tiles = tiles
    self.score = float("inf")
    self.depth = depth
    self.eval = self.depth + self.score

  def add_tile(self, rectangle):
    self.tiles.append(rectangle)
    self.tiles.sort(key=lambda rect: rect.area, reverse=True)
    self.score = self.get_score()

  def get_score(self):
    if len(self.tiles) >= 2:
      self.score = self.tiles[0].area - self.tiles[-1].area
    else:
      self.score = float("inf")
    return self.score

  def get_areas(self):
    return (self.tiles[0].area, self.tiles[-1].area)

  def get_eval(self):
    self.eval = self.depth + self.score
    return self.eval

  def equal(self, state):
    tile_coords_1 = [t.coords for t in self.tiles]
    tile_coords_2 = [t.coords for t in state.tiles]
    return sorted(tile_coords_1) == sorted(tile_coords_2)

  def get_tile_no(self):
    return len(self.tiles)


class Mondrian:
  def __init__(self):
    self.queue = []
    self.explored = []

  def add_to_queue(self, state):
    self.queue.append(state)
    self.queue.sort(key=lambda state: state.get_score(), reverse=True)

  def add(self, state, maxsize):
    if len(self.queue) < maxsize:
      self.add_to_queue(state)
    else:
      worst_state = self.queue[-1]
      if state.score < worst_state.score:
        self.pop()
        self.add_to_queue(state)

  def pop(self):
    return self.queue.pop(-1)


class Coord:
  def __init__(self, x0, y0, x1, y1):
    self.x0 = x0
    self.y0 = y0
    self.x1 = x1
    self.y1 = y1


def validate(l, b, state, ignore=None):
  ignore_list = []
  if ignore:
    for r in ignore:
      ignore_list.append({r.width, r.height})

  sizes = [{rect.width, rect.height} for rect in state.tiles]
  if ({l, b} in sizes) and ({l, b} not in ignore_list): return False
  return True


def pop_tiles(state, indexes):
  # have to pop smaller tile first as index will change
  index_list = sorted([i for i in indexes], reverse=True)
  for i in index_list:
    state.tiles.pop(i)


def split_helper(state, c1, c2, indexes, ignore=None):
  new_width1 = c1.x1 - c1.x0
  new_height1 = c1.y1 - c1.y0
  new_width2 = c2.x1 - c2.x0
  new_height2 = c2.y1 - c2.y0

  if ({new_width1, new_height1} == {new_width2, new_height2}) or (not validate(new_width1, new_height1, state, ignore)) or (not validate(new_width2, new_height2, state, ignore)): 
    return False
  pop_tiles(state, indexes)
  state.add_tile(Rectangle(coords=[c1.x0, c1.y0, c1.x1, c1.y1]))
  state.add_tile(Rectangle(coords=[c2.x0, c2.y0, c2.x1, c2.y1]))
  return True


def merge_helper(state, c1, indexes):
  new_width = c1.x1 - c1.x0
  new_height = c1.y1 - c1.y0
  if not validate(new_width, new_height, state): 
    return
  pop_tiles(state, indexes)
  state.add_tile(Rectangle(coords=[c1.x0, c1.y0, c1.x1, c1.y1]))


def create_initial_state(a):
  state = State([], 0)
  state.add_tile(Rectangle(coords=[0, 0, a, a]))
  for i in range(4):
    # select a random rectangle
    r_index = int(ran.randint(0, len(state.tiles)-1))
    rect = state.tiles[r_index]
    x0, y0, x1, y1 = rect.coords[0], rect.coords[1], rect.coords[2], rect.coords[3]

    # split vertically (along x-axis)
    if ran.randint(1, 2) == 1:
      if x1 - x0 <= 2: continue
      new_x1 = ran.randint(x0+1, x1-1)
      split_helper(state, Coord(x0, y0, new_x1, y1), Coord(new_x1, y0, x1, y1), [r_index])
    # split horizontally (along y-axis)
    else:
      if y1 - y0 <= 2: continue
      new_y1 = ran.randint(y0+1, y1-1)
      split_helper(state, Coord(x0, y0, x1, new_y1), Coord(x0, new_y1, x1, y1), [r_index])

  return state


def divide_tile(state, rect, isWidth=True):
  property1 = rect.height
  property2 = rect.width
  if isWidth:
    property1 = rect.width
    property2 = rect.height

  if property1 <= 2: return float("inf"), None  # cant equally split tiles

  ratio = property1 // 2
  while ratio < property1-1:  # repeat until ratio of split is equal to original width/height
    ratio += 1
    if validate(ratio, property2, state) and validate(property1-ratio, property2, state):
      diff = (ratio * property2) - ((property1-ratio) * property2)  # get difference of area between tiles
      return diff, ratio
  return float("inf"), None
  

def split(state):
  for i in range(0, len(state.tiles)):
    rect = state.tiles[i]
    best_area_diff_width, ratio_width = divide_tile(state, rect, isWidth=True)
    best_area_diff_height, ratio_height = divide_tile(state, rect, isWidth=False)

    if best_area_diff_width==float("inf") and best_area_diff_height==float("inf"): continue # cannot be split so try next rectangle
      
    x0, y0, x1, y1 = rect.coords[0], rect.coords[1], rect.coords[2], rect.coords[3]
    state.tiles.pop(i)

    # if there is no difference between splitting by width or height, choose one randomly
    r = 0
    if best_area_diff_width == best_area_diff_height: 
      r = ran.randint(1, 2)
    if (r==1) or (best_area_diff_width < best_area_diff_height):
      state.add_tile(Rectangle(coords=[x0, y0, x0+ratio_width, y1])) # left
      state.add_tile(Rectangle(coords=[x0+ratio_width, y0, x1, y1])) # right
    elif (r==2) or (best_area_diff_width > best_area_diff_height):
      state.add_tile(Rectangle(coords=[x0, y0, x1, y0+ratio_height])) # bottom
      state.add_tile(Rectangle(coords=[x0, y0+ratio_height, x1, y1])) # top
    return


# get tiles top/bottom/left/right adjacent
def get_strict_adjacent(state, rect):
  adjacent = []
  for i, r in enumerate(state.tiles):
    if rect.coords == r.coords: continue
    elif rect.coords[0] == r.coords[0] and rect.coords[2] == r.coords[2]: 
      if rect.coords[1] == r.coords[3]: adjacent.append((i, r, "top"))  
      elif rect.coords[3] == r.coords[1]: adjacent.append((i, r, "bottom"))
    elif rect.coords[1] == r.coords[1] and rect.coords[3] == r.coords[3]:
      if rect.coords[0] == r.coords[2]: adjacent.append((i, r, "left"))  
      elif rect.coords[2] == r.coords[0]: adjacent.append((i, r, "right"))
  return adjacent


# get adjacent tiles in l-shape
def get_adjacent(state, rect):
  adjacent = []
  for i, r in enumerate(state.tiles):
    if rect.coords == r.coords: continue
    elif rect.coords[0] == r.coords[0]:
      if rect.coords[3] == r.coords[3]: adjacent.append((i, r, "left-bottom"))
      elif rect.coords[1] == r.coords[1]: adjacent.append((i, r, "left-top"))
    elif rect.coords[1] == r.coords[3]:
      if rect.coords[0] == r.coords[0]: adjacent.append((i, r, "top-left"))
      elif rect.coords[2] == r.coords[2]: adjacent.append((i, r, "top-right"))
    elif rect.coords[2] == r.coords[0]:
      if rect.coords[3] == r.coords[3]: adjacent.append((i, r, "right-bottom"))
      elif rect.coords[1] == r.coords[1]: adjacent.append((i, r, "right-top"))
    elif rect.coords[3] == r.coords[3]:
      if rect.coords[2] == r.coords[2]: adjacent.append((i, r, "bottom-right"))
      elif rect.coords[0] == r.coords[0]: adjacent.append((i, r, "bottom-left"))
  return adjacent
  

def merge(state):
  start_no_rectangles = len(state.tiles)
  if start_no_rectangles <= 2: return    # cannot go to invalid state
  # starting from the smallest rect
  for index in range(len(state.tiles)-1, -1, -1):
    rect = state.tiles[index]
    adjacent = get_strict_adjacent(state, rect)

    # if there are no tiles adjacent, return. Otherwise get adjacent tile with largest area
    if len(adjacent) == 0: continue
    adjacent.sort(key=lambda x:x[1].area, reverse=True)

    for largest in adjacent:
      x0, y0, x1, y1 = rect.coords
      merge_x0, merge_y0, merge_x1, merge_y1 = largest[1].coords
      direction = largest[2]
      indexes = [index, largest[0]]
      if direction == "top":
        merge_helper(state, Coord(x0, merge_y0, x1, y1), indexes)
      elif direction == "bottom":
        merge_helper(state, Coord(x0, y0, x1, merge_y1), indexes)
      elif direction == "left":
        merge_helper(state, Coord(merge_x0, y0, x1, y1), indexes)
      elif direction == "right":
        merge_helper(state, Coord(x0, y0, merge_x1, y1), indexes)

      if start_no_rectangles > len(state.tiles):
        return 



def merge_split(state):
  if len(state.tiles) <= 2: return    # cannot go to invalid state
  # starting from the smallest rect
  for index in range(len(state.tiles)-1, -1, -1):
    rect = state.tiles[index]
    adjacent = get_adjacent(state, rect)

    # if there are no tiles adjacent, return. Otherwise get adjacent tile with largest area
    if len(adjacent) == 0: continue
    adjacent.sort(key=lambda x:x[1].area, reverse=True)

    for largest in adjacent:
      x0, y0, x1, y1 = rect.coords
      merge_x0, merge_y0, merge_x1, merge_y1 = largest[1].coords
      i, direction = largest[0], largest[2]
      merged = False

      if direction == "top-left":
        if not (merge_x1 > x1): continue
        merged = split_helper(state, Coord(x0, merge_y0, x1, y1), Coord(x1, merge_y0, merge_x1, merge_y1), [index, i], [rect, largest[1]])

      elif direction == "top-right":
        if not (merge_x0 < x0): continue
        merged = split_helper(state, Coord(x0, merge_y0, x1, y1), Coord(merge_x0, merge_y0, x0, merge_y1), [index, i], [rect, largest[1]])

      elif direction == "right-bottom":
        if not (merge_y0 < y0): continue
        merged = split_helper(state, Coord(x0, y0, merge_x1, y1), Coord(merge_x0, merge_y0, merge_x1, y0), [index, i], [rect, largest[1]])

      elif direction == "right-top":
        if not (merge_y1 > y1): continue
        merged = split_helper(state, Coord(x0, y0, merge_x1, y1), Coord(merge_x0, y1, merge_x1, merge_y1), [index, i], [rect, largest[1]])

      elif direction == "bottom-right":
        if not (merge_x0 < x0): continue
        merged = split_helper(state, Coord(x0, y0, x1, merge_y1), Coord(merge_x0, merge_y0, x1, merge_y1), [index, i], [rect, largest[1]])
 
      elif direction == "bottom-left":
        if not (merge_x1 > x1): continue
        merged = split_helper(state, Coord(x0, y0, x1, merge_y1), Coord(x1, merge_y0, merge_x1, merge_y1), [index, i], [rect, largest[1]])

      elif direction == "left-bottom":
        if not (merge_y0 < y0): continue
        merged = split_helper(state, Coord(merge_x0, y0, x1, y1), Coord(merge_x0, merge_y0, merge_x1, y0), [index, i], [rect, largest[1]])

      elif direction == "left-top":
        if not (merge_y1 > y1): continue
        merged = split_helper(state, Coord(merge_x0, y0, x1, y1), Coord(merge_x0, y1, merge_x1, merge_y1), [index, i], [rect, largest[1]])           
      
      if merged: return

# go through each state and check it's not been explored
def check_explored(explored_states, state):
  explored = False
  for st in explored_states:
    explored = state.equal(st)
    if explored:
      return explored
  explored_states.append(state)
  return explored


def optimise(init_state, maxdepth, maxsize):
  mondrian = Mondrian()
  mondrian.add(init_state, maxsize)
  best_state = init_state
  operations = [split, merge, merge_split]
  while len(mondrian.queue):
    state = mondrian.pop()
    # check state not already been explored or reached max depth
    if check_explored(mondrian.explored, state): continue
    if state.depth >= maxdepth: continue

    for op in operations:
      new_state = copy.deepcopy(state)
      op(new_state) # perform action on state
      new_state.depth += 1
      if new_state.get_score() < best_state.get_score(): 
        best_state = new_state
      mondrian.add(new_state, maxsize)
  return best_state



def drawMondrian(state, a):
  block_size = 30
  window_size = (a*block_size) + (block_size*2)
  root = tk.Tk()
  root.title(f"Mondrian Tiling Solution for {a}x{a}")
  root.geometry(f"{window_size}x{window_size+block_size}")

  canvas = tk.Canvas(root, width=window_size, height=window_size)
  for r in state.tiles:
    x0, y0, x1, y1 = list(map(lambda c: block_size + (c * block_size), r.coords))
    canvas.create_rectangle(x0, y0, x1, y1, fill="red")
    canvas.create_text(x0+(x1-x0)/2, y0+(y1-y0)/2, text=str(r.area), fill="black", font=('Helvetica 10 bold'))

  l = tk.Label(root, text = f"Mondrian Score for a {a}x{a}:\n{state.tiles[0].area} - {state.tiles[-1].area} = {state.tiles[0].area - state.tiles[-1].area}")
  l.config(font =("Helvetica", 10, "bold"))
  l.pack()
  canvas.pack()
  root.mainloop()


def SolveMondrian(a, max_depth, max_size, ran_iterations):
  best_state = None
  explored_init_states = []

  for i in range(ran_iterations):
    init_state = create_initial_state(a)
    if check_explored(explored_init_states, init_state): continue
    new_state = optimise(init_state, max_depth, max_size) # optimise the score of the initial state
    if (best_state is None) or (new_state.get_score() < best_state.get_score()):
      best_state = new_state
    
  print("\nBest state:\tscore: ", best_state.get_score(), " depth: ", best_state.depth, " eval: ", best_state.get_eval(), " no. of tiles: ", best_state.get_tile_no())
  drawMondrian(best_state, a)

SolveMondrian(12, 10, 20, 25)