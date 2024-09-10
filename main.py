from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Board():
  
  def __init__(self, inputString):
    self.directionMapping = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1,0)}
    self.board = []
    for i in range(0, int(len(inputString) / 4)):
      self.board.append(list(inputString[i*4:i*4+4]))

  def display(self):
    for row in self.board:
      print(row)
    print("")

  def moveBlock(self, move):
    ignore = set()
    noOverwrite = set()
    letter, direction = move[0], move[1]
    for i in range(len(self.board)):
      for j in range(0, 4):
        if (i,j) not in ignore and self.board[i][j] == letter:
          x,y = self.directionMapping[direction]
          if self.board[i+y][j+x] != letter:
            ignore.add((i+y, j+x))
          else:
            noOverwrite.add((i+y, j+x))
          self.board[i+y][j+x] = letter
          if (i,j) not in noOverwrite:
            self.board[i][j] = '@'
          
    self.display()

  def moves(self, movesString):
    for i in range(0, int(len(movesString) / 2)):
      self.moveBlock(movesString[i*2:i*2+2])
  
  def getString(self):
    return ''.join([item for row in self.board for item in row])


@app.get("/")
async def root():
    return {"message": "Hello World, should be working fine."}

class KlotskyInput(BaseModel):
    board: str
    moves: str

@app.post("/klotski")
def klotsky(testCases: list[KlotskyInput]):
    response = []
    for board, moves in testCases:
        board2D = Board(board)
        board2D.moves(moves)
        response.append(board2D.getString())
    return response
        

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}