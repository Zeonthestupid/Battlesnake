# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# ________  ________  ________  ________  ________  ______________
#   /    /  |   |     |      |  /      \    |  |    |  |   | |
#  /    /   |   ----  |      | /   /\\   \  |  |    | | | |  |
# /    /    |   |     |      ||   |  |   |  |  |   | |   |  | |
# ------    |-------  |      ||---|  |---|  |  |  | |        | |

import math
import typing
moves = []
snakename = "Zeothesnek"
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Zeonim",  # TODO: Your Battlesnake Username
        "color": "#FFAAFF",  # TODO: Choose color
        "head": "replit-mark",  # TODO: Choose head
        "tail": "replit-notmark",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")
    print(game_state)
    


def checkboundries(x, y, matrix):
  if x >= 0 and x <= 10 and y >= 0 and y <= 10:
    return True
  else:
    return False

def decaytiles(coord_x, coord_y, start_value, matrix, game_state):
  size_x = game_state["board"]["height"]
  size_y = game_state["board"]["width"]
  print(coord_y)
  print(coord_x)
  for x in range(size_x):
    for y in range(size_y):
      distance = abs(x - coord_x) + abs(y - coord_y)
      value = math.floor(start_value / ((distance * distance) + 1))

      matrix[x][y] += value

  return matrix


def printmatrix(matrix):
  size_x = len(matrix)
  print (size_x)
  print("---------------------")
  for rows in reversed(range(len(matrix))):
    currentrow = []
    for columns in range(len(matrix[0])):
      currentrow.append(matrix[columns][rows])
      if len(currentrow) >= size_x:
        print(currentrow)
        currentrow = []
  print("---------------------")
def end(game_state: typing.Dict):
    print("GAME OVER\n")
    print(moves)
    for names in game_state['board']['snakes']:
      print (names['name'])
def snakematrix(matrix, game_state, snake_weight):
  snake_weight = snake_weight * 3
  for snake in game_state["board"]["snakes"]:
    if snake['name'] == snakename:
      snakelength = len(snake['body'])
      for body in snake['body']:
        decaytiles(body["x"], body['y'], 500, matrix, game_state)
  for snake in game_state["board"]["snakes"]:
    if snake['name'] != snakename:
      body = snake["body"][0]
      if len(snake["body"]) < snakelength: # if their snake is smaller than my snake
        matrix[body["x"]][body["y"]] += -5000 
        decaytiles(body["x"], body["y"], -1000, matrix, game_state)
      elif len(snake["body"]) == snakelength:
        matrix[body["x"]][body["y"]] += 10000
        decaytiles(body["x"], body["y"], 5000, matrix, game_state)
      else:
        matrix[body["x"]][body["y"]] += 10000 # When their snake is >= mine
        decaytiles(body["x"], body["y"], 5000, matrix, game_state)
    else: # Head of snakes
      body = snake["body"][0]
      matrix[body["x"]][body["y"]] += 500
    for body in snake['body']: # Body of every snake
      matrix[body["x"]][body["y"]] += 50000
      # decaytiles(body["x"], body["y"], 50, matrix, game_state)


def foodmatrix(matrix, game_state, snake_weight):
  snake_weight = snake_weight * 10
  for food in game_state["board"]["food"]:
    decaytiles(food["x"], food["y"], snake_weight, matrix, game_state)


def centermatrix (matrix, game_state, snake_weight):
    decaytiles(0, 0, 1000, matrix, game_state)
    decaytiles(10, 0, 1000, matrix, game_state)
    decaytiles(0, 10, 1000, matrix, game_state)
    decaytiles(10, 10, 1000, matrix, game_state)



def move(game_state: typing.Dict) -> typing.Dict:
    snakeweight = 0
    opplength = 0
    sizeY = game_state["board"]["height"]
    sizeX = game_state["board"]["width"]
    matrix = [[0 for _ in range(sizeY)] for _ in range(sizeX)]
    for snake in game_state["board"]["snakes"]:
      if snake["name"] == snakename:
        head = snake["head"]
        length = len(snake["body"])
      

    for snake in game_state["board"]["snakes"]:
      if snake["name"] != snakename:
        opplength = length
    
    for snake in game_state["board"]["snakes"]:
      if snake["name"] == snakename:
        health = snake["health"]
        if health < 50:
          snakeweight = -100 * (1/health)
        else: 
          snakeweight = -3
    if opplength > 10:
      snakeweight = snakeweight * 2
    
    snakematrix(matrix, game_state, snakeweight)
    for snakes in game_state["board"]["snakes"]:
      if snakes["name"] == snakename:
        snakelength = len(snakes["body"])
    for snakes in game_state["board"]["snakes"]:
      if snakes["name"] != snakename:
        if len(snakes["body"]) > snakelength:
          snakeweight = snakeweight * 20
        elif len(snakes["body"]) == snakelength:
          snakeweight = snakeweight * 80
        
    foodmatrix(matrix, game_state, snakeweight)
    centermatrix(matrix, game_state, snakeweight)
  
  # for some odd reason its called snake weight
    printmatrix(matrix)
    minimumval = 100000

    if checkboundries(head["x"] + 1, head["y"], matrix) == True:
      if (matrix[head["x"] + 1][head["y"]]) < minimumval:
        best_move = "right"
        minimumval = matrix[head["x"] + 1][head["y"]]
    if checkboundries(head["x"] - 1, head["y"], matrix) == True:
      if (matrix[head["x"] - 1][head["y"]]) < minimumval:
        best_move = "left"
        minimumval = matrix[head["x"] - 1][head["y"]]
    if checkboundries(head["x"], head["y"] + 1, matrix) == True:
      if (matrix[head["x"]][head["y"] + 1]) < minimumval:
        best_move = "up"
        minimumval = matrix[head["x"]][head["y"] + 1]
    if checkboundries(head["x"], head["y"] - 1, matrix) == True:
      if (matrix[head["x"]][head["y"] - 1]) < minimumval:
        best_move = "down"
        minimumval = matrix[head["x"]][head["y"] - 1]

    print(best_move)
    return {"move": best_move}



# Start server when `python main.py` is run
if __name__ == "__main__":
  from server import run_server

  run_server({
      "info": info, 
      "start": start, 
       "move": move, 
      "end": end
  })
