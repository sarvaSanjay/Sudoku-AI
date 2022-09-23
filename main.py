import pygame
from copy import deepcopy
import time
import random
# Initialising pygame
pygame.init()

#Fonts
Font = pygame.font.Font("OpenSans-Regular.ttf", 20)
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 30)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

# setting window size
screen = pygame.display.set_mode((400, 800))

# setting caption
pygame.display.set_caption('Sudoku')

# DEFINES INITIAL BOARD
def init_state():
  state = [[9,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0]]
  state = generate_state(state)[1]
  for x in range(9):
    lis = list(range(9))
    while len(lis) != 3:
      y = random.choice(lis)
      state[x][y] = 0
      lis.remove(y)
  return state

def generate_state(state):
    actions = moves()
    for x in range(9):
      for y in range(9):
        if state[x][y] != 0:
          continue
        while len(actions[x][y]) != 0:
          action = random.choice(actions[x][y])
          state[x][y] = action
          if not constraints(state, [x,y]):
            state[x][y] = 0
            actions[x][y].remove(action)
            continue
          results = generate_state(state)
        
          if not results[0]:
            state[x][y] = 0
            actions[x][y].remove(action)
            continue
          return [True, results[1]]
        return [False, None]
    return [True, state]
  
  # RETURNS POSSIBLE MOVES
def moves():
  actions = []
  for x in range(9):
    row = []
    for y in range(9):
      row.append([x for x in range(1,10)])
    actions.append(row)
  return actions


  
# CHECKS WHETHER VALID MOVE
def constraints(board, key):
  xcoord = key[0]
  ycoord = key[1]
  if xcoord < 0 or ycoord < 0 or board[xcoord][ycoord] == 0:
    return True
  success = True
  for k in range(9):
    if board[k][ycoord] == board[xcoord][ycoord] and xcoord != k:
      success = False
      break
    if board[xcoord][k] == board[xcoord][ycoord] and ycoord != k:
      success = False
      break
  low_x = (xcoord // 3) * 3
  low_y = (ycoord // 3) * 3
  for x in range(low_x, low_x + 3):
    for y in range(low_y, low_y + 3):
      if board[x][y] == board[xcoord][ycoord] and (x != xcoord and y != ycoord):
        success = False
        break
  return success

  
# CHECKS WHETHER GAME IS OVER
def game_over(board):
  for row in board:
    if 0 in row:
      return False
  for x in range(9):
    for y in range(9):
      if not constraints(board, [x,y]):
        return False
  return True



hover = [-1, -1]
started = False
compsolve = False

def backtrack(state, init_board):
  actions = list(range(1, 10))
  for x in range(9):
    for y in range(9):
      if state[x][y] != 0:
        continue
      while len(actions) != 0:
        action = actions[0]
        state[x][y] = action
        time.sleep(0.01)
        screen.fill((255, 255, 255))
        
        # Title
        title = moveFont.render('Sudoku', True, (0,0,0))
        title_rect = title.get_rect()
        title_rect.center = (200, 50)
        screen.blit(title, title_rect)
        
        # Board border
        big_rect = pygame.Rect(13, 198, 374, 374)
        pygame.draw.rect(screen, (0,0,0), big_rect)

        # drawing board
        board = deepcopy(state)
        hover = [x,y]
        for x1 in range(9):
          for y1 in range(9):
            x_ex = x1 // 3
            y_ex = y1 // 3
            rect = pygame.Rect(15 + y1*41 + y_ex, 200 + x1*41 + x_ex, 40, 40)
            if hover[0] == x1 and hover[1] == y1:
              pygame.draw.rect(screen, (150, 150, 255), rect)
            elif not (constraints(board, [x1,y1]) or board[x1][y1] == 0):
              pygame.draw.rect(screen, (255, 150, 150), rect)
            else:
              pygame.draw.rect(screen, (255, 255, 255), rect)
            if board[x1][y1] != 0:
              if init_board[x1][y1] != 0:
                text = largeFont.render(str(board[x1][y1]), True, (0,0,0))
              else:
                text = largeFont.render(str(board[x1][y1]), True, (0,0,255))
              text_rect = text.get_rect()
              text_rect.center = rect.center
              screen.blit(text, text_rect)
              #screen.fill((255,0,0))'''
        pygame.display.update()
        if not constraints(state, [x,y]):
          state[x][y] = 0
          actions.remove(action)
          continue
        results = backtrack(state, init_board)
        
        if not results[0]:
          state[x][y] = 0
          actions.remove(action)
          continue
        return [True, results[1]]
      return [False, None]
  return [True, state]

while True:
  screen.fill((255, 255, 255))
  # Title
  title = moveFont.render('Sudoku', True, (0,0,0))
  title_rect = title.get_rect()
  title_rect.center = (200, 50)
  screen.blit(title, title_rect)
  
  # Board border
  big_rect = pygame.Rect(13, 198, 374, 374)
  pygame.draw.rect(screen, (0,0,0), big_rect)
  
  # starting board
  if not started:
    started = True
    init_board = init_state()
    board = deepcopy(init_board)

  # drawing board
  for x in range(9):
    for y in range(9):
      x_ex = x // 3
      y_ex = y // 3
      rect = pygame.Rect(15 + y*41 + y_ex, 200 + x*41 + x_ex, 40, 40)
      if hover[0] == x and hover[1] == y:
         pygame.draw.rect(screen, (150, 150, 255), rect)
      elif not (constraints(board, [x,y]) or board[x][y] == 0):
        pygame.draw.rect(screen, (255, 150, 150), rect)
      else:
        pygame.draw.rect(screen, (255, 255, 255), rect)
      if board[x][y] != 0:
        if init_board[x][y] != 0:
          text = largeFont.render(str(board[x][y]), True, (0,0,0))
        else:
          text = largeFont.render(str(board[x][y]), True, (0,0,255))
        text_rect = text.get_rect()
        text_rect.center = rect.center
        screen.blit(text, text_rect)

  # checking if game is over
  if game_over(board):
    game_over_text = Font.render("You won!", True, (0,0,0))
    game_over_rect = game_over_text.get_rect()
    game_over_rect.center = (200, 120)
    screen.blit(game_over_text, game_over_rect)
    restart_rect = pygame.Rect(150, 140, 100, 30)
    pygame.draw.rect(screen, (150, 150, 150), restart_rect)
    restart = Font.render("Restart", True, (0,0,0))
    restart_text_rect = restart.get_rect()
    restart_text_rect.center = restart_rect.center
    screen.blit(restart, restart_text_rect)

  else:
    comp_rect = pygame.Rect(125, 600, 150, 30)
    pygame.draw.rect(screen, (150, 150, 150), comp_rect)
    comp = Font.render("Computer Solve", True, (0,0,0))
    comp_text_rect = comp.get_rect()
    comp_text_rect.center = comp_rect.center
    screen.blit(comp, comp_text_rect)
  if compsolve:
    for x in range(9):
      for y in range(9):
        board[x][y] = init_board[x][y]
    board = backtrack(board, init_board)[1]
    compsolve = False
    
  # Listening for events
  for event in pygame.event.get():
    key_no = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse = event.pos
      if mouse[0] <=250 and mouse[0] >= 150 and mouse[1] >= 140 and mouse[1] <= 170:
        started = False
        compsolve = False
      if mouse[0] >= 125 and mouse[0] <= 275 and mouse[1] >= 600 and mouse[1] <= 630:
        print('Boom')
        compsolve = True
      x = (mouse[1] - 200) // 41
      y = (mouse[0] - 15) // 41
      print(x, y)      
      if x in range(9) and y in range(9) and init_board[x][y] == 0 and not compsolve:
        print('Hi')
        hover = [x, y]
    if event.type == pygame.KEYDOWN:
      if event.key in key_no and hover[0] + hover[1] >=0:
        board[hover[0]][hover[1]] = key_no.index(event.key) + 1
  
  pygame.display.update()

