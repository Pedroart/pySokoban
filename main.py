import os
import copy
import multiprocessing
import threading
import pygame
from fastapi import FastAPI
#from Environment import Environment
from Level import Level
#from sokaband import movePlayer, initLevel, drawLevel
import sys
import uvicorn
from Environment import Environment
from flask import Flask, jsonify, request


theme = "default"
level_set = "original"
current_level = 1
myLevel = Level(level_set, current_level)
target_found = False
screen = None  

import pygame

# Definir valores que antes se obtenían de myEnvironment
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
THEME_PATH = "themes/default/images"  # Ajusta la ruta de los recursos según sea necesario

def drawLevel(matrix_to_draw, screen):
    # Cargar imágenes
    wall = pygame.image.load(f"{THEME_PATH}/wall.png").convert()
    box = pygame.image.load(f"{THEME_PATH}/box.png").convert()
    box_on_target = pygame.image.load(f"{THEME_PATH}/box_on_target.png").convert()
    space = pygame.image.load(f"{THEME_PATH}/space.png").convert()
    target = pygame.image.load(f"{THEME_PATH}/target.png").convert()
    player = pygame.image.load(f"{THEME_PATH}/player.png").convert()

    # Obtener tamaño del nivel
    level_width = len(matrix_to_draw[0])  # Número de columnas
    level_height = len(matrix_to_draw)    # Número de filas

    # Determinar si es necesario redimensionar las imágenes
    if level_width > SCREEN_WIDTH / 36 or level_height > SCREEN_HEIGHT / 36:
        if level_width / level_height >= 1:
            new_image_size = SCREEN_WIDTH / level_width
        else:
            new_image_size = SCREEN_HEIGHT / level_height

        # Redimensionar imágenes
        wall = pygame.transform.scale(wall, (int(new_image_size), int(new_image_size)))
        box = pygame.transform.scale(box, (int(new_image_size), int(new_image_size)))
        box_on_target = pygame.transform.scale(box_on_target, (int(new_image_size), int(new_image_size)))
        space = pygame.transform.scale(space, (int(new_image_size), int(new_image_size)))
        target = pygame.transform.scale(target, (int(new_image_size), int(new_image_size)))
        player = pygame.transform.scale(player, (int(new_image_size), int(new_image_size)))

    # Diccionario de imágenes
    images = {'#': wall, ' ': space, '$': box, '.': target, '@': player, '*': box_on_target}

    # Obtener el tamaño de una celda
    box_size = wall.get_width()

    # Dibujar el nivel
    for i in range(len(matrix_to_draw)):
        for c in range(len(matrix_to_draw[i])):
            screen.blit(images[matrix_to_draw[i][c]], (c * box_size, i * box_size))

    pygame.display.update()


def initLevel(level_set,level):
	# Create an instance of this Level
	global myLevel
	myLevel = Level(level_set,level)

	# Draw this level
	#drawLevel(myLevel.getMatrix())
	
	global target_found
	target_found = False

def movePlayer(direction,myLevel,screen):
	
	matrix = myLevel.getMatrix()
	
	myLevel.addToHistory(matrix)
	
	x = myLevel.getPlayerPosition()[0]
	y = myLevel.getPlayerPosition()[1]
	
	global target_found
	
	#print boxes
	print(myLevel.getBoxes())
	
	if direction == "L":
		print("######### Moving Left #########")
		
		# if is_space
		if matrix[y][x-1] == " ":
			print("OK Space Found")
			matrix[y][x-1] = "@"
			if target_found == True:
				matrix[y][x] = "."
				target_found = False
			else:
				matrix[y][x] = " "
		
		# if is_box
		elif matrix[y][x-1] == "$":
			print("Box Found")
			if matrix[y][x-2] == " ":
				matrix[y][x-2] = "$"
				matrix[y][x-1] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "
			elif matrix[y][x-2] == ".":
				matrix[y][x-2] = "*"
				matrix[y][x-1] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "
				
				
		# if is_box_on_target
		elif matrix[y][x-1] == "*":
			print("Box on target Found")
			if matrix[y][x-2] == " ":
				matrix[y][x-2] = "$"
				matrix[y][x-1] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
				
			elif matrix[y][x-2] == ".":
				matrix[y][x-2] = "*"
				matrix[y][x-1] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
				
		# if is_target
		elif matrix[y][x-1] == ".":
			print("Target Found")
			matrix[y][x-1] = "@"
			if target_found == True:
				matrix[y][x] = "."
			else:
				matrix[y][x] = " "
			target_found = True
		
		# else
		else:
			print("There is a wall here")
	
	elif direction == "R":
		print("######### Moving Right #########")

		# if is_space
		if matrix[y][x+1] == " ":
			print("OK Space Found")
			matrix[y][x+1] = "@"
			if target_found == True:
				matrix[y][x] = "."
				target_found = False
			else:
				matrix[y][x] = " "
		
		# if is_box
		elif matrix[y][x+1] == "$":
			print("Box Found")
			if matrix[y][x+2] == " ":
				matrix[y][x+2] = "$"
				matrix[y][x+1] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "
			
			elif matrix[y][x+2] == ".":
				matrix[y][x+2] = "*"
				matrix[y][x+1] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "				
		
		# if is_box_on_target
		elif matrix[y][x+1] == "*":
			print("Box on target Found")
			if matrix[y][x+2] == " ":
				matrix[y][x+2] = "$"
				matrix[y][x+1] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
				
			elif matrix[y][x+2] == ".":
				matrix[y][x+2] = "*"
				matrix[y][x+1] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
			
		# if is_target
		elif matrix[y][x+1] == ".":
			print("Target Found")
			matrix[y][x+1] = "@"
			if target_found == True:
				matrix[y][x] = "."
			else:
				matrix[y][x] = " "
			target_found = True
			
		# else
		else:
			print("There is a wall here")		

	elif direction == "D":
		print("######### Moving Down #########")

		# if is_space
		if matrix[y+1][x] == " ":
			print ("OK Space Found")
			matrix[y+1][x] = "@"
			if target_found == True:
				matrix[y][x] = "."
				target_found = False
			else:
				matrix[y][x] = " "
		
		# if is_box
		elif matrix[y+1][x] == "$":
			print("Box Found")
			if matrix[y+2][x] == " ":
				matrix[y+2][x] = "$"
				matrix[y+1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "
			
			elif matrix[y+2][x] == ".":
				matrix[y+2][x] = "*"
				matrix[y+1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "
		
		# if is_box_on_target
		elif matrix[y+1][x] == "*":
			print("Box on target Found")
			if matrix[y+2][x] == " ":
				matrix[y+2][x] = "$"
				matrix[y+1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
				
			elif matrix[y+2][x] == ".":
				matrix[y+2][x] = "*"
				matrix[y+1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
		
		# if is_target
		elif matrix[y+1][x] == ".":
			print("Target Found")
			matrix[y+1][x] = "@"
			if target_found == True:
				matrix[y][x] = "."
			else:
				matrix[y][x] = " "
			target_found = True
			
		# else
		else:
			print("There is a wall here")

	elif direction == "U":
		print("######### Moving Up #########")

		# if is_space
		if matrix[y-1][x] == " ":
			print ("OK Space Found")
			matrix[y-1][x] = "@"
			if target_found == True:
				matrix[y][x] = "."
				target_found = False
			else:
				matrix[y][x] = " "
		
		# if is_box
		elif matrix[y-1][x] == "$":
			print ("Box Found")
			if matrix[y-2][x] == " ":
				matrix[y-2][x] = "$"
				matrix[y-1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "

			elif matrix[y-2][x] == ".":
				matrix[y-2][x] = "*"
				matrix[y-1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
					target_found = False
				else:
					matrix[y][x] = " "					
					
		# if is_box_on_target
		elif matrix[y-1][x] == "*":
			print ("Box on target Found")
			if matrix[y-2][x] == " ":
				matrix[y-2][x] = "$"
				matrix[y-1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
				
			elif matrix[y-2][x] == ".":
				matrix[y-2][x] = "*"
				matrix[y-1][x] = "@"
				if target_found == True:
					matrix[y][x] = "."
				else:
					matrix[y][x] = " "
				target_found = True
					
		# if is_target
		elif matrix[y-1][x] == ".":
			print ("Target Found")
			matrix[y-1][x] = "@"
			if target_found == True:
				matrix[y][x] = "."
			else:
				matrix[y][x] = " "
			target_found = True
			
		# else
		else:
			print ("There is a wall here")
	
	drawLevel(matrix,pygame.display.get_surface())
	
	print ("Boxes remaining: " + str(len(myLevel.getBoxes())))
	
	if len(myLevel.getBoxes()) == 0:
		#myEnvironment.screen.fill((0, 0, 0))
		print ("Level Completed")
		global current_level
		current_level += 1
		initLevel(level_set,current_level)	


app = Flask(__name__)

def format_matrix(matrix):
    """Converts the matrix into a properly formatted string block."""
    return f"""\n{chr(10).join("".join(row) for row in matrix)}\n"""

def update_game_state():
    """Updates and returns the current game state."""
    return {
        "level": current_level,
        "player_position": myLevel.getPlayerPosition(),
        "boxes": myLevel.getBoxes(),
        "matrix": format_matrix(myLevel.getMatrix()),
    }

@app.route("/state", methods=["GET"])
def get_state():
    """Obtener el estado actual del juego"""
    return jsonify(update_game_state())

@app.route("/move", methods=["POST"])
def move_player():
    """Mover al jugador en una dirección dada"""
    data = request.json
    direction = data.get("direction")

    """Move the player in the given direction (L, R, U, D)."""
    if direction.upper() in ["L", "R", "U", "D"]:
        movePlayer(direction.upper(), myLevel,screen)
        return jsonify({"message": f"Moved {direction}", "state": update_game_state()})
    
    return jsonify({"error": "Invalid direction. Use L, R, U, or D."}), 400

@app.route("/reset", methods=["POST"])
def reset_game():
    """Reiniciar el estado del juego"""
    global myLevel
    myLevel = Level(level_set, current_level)
    return jsonify({"message": "Game reset", "state": update_game_state()})

def run_pygame():
    

    running = True
    pygame.quit()  # Asegura que no haya una instancia anterior
    pygame.init()
    
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Sokoban Game")
    clock = pygame.time.Clock()

    while running:
        #screen.fill((0, 0, 0))  # Clear screen
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    movePlayer("L",myLevel,screen)
                elif event.key == pygame.K_RIGHT:
                    movePlayer("R",myLevel,screen)
                elif event.key == pygame.K_DOWN:
                    movePlayer("D",myLevel,screen)
                elif event.key == pygame.K_UP:
                    movePlayer("U",myLevel,screen)
                elif event.key == pygame.K_u:
                    drawLevel(myLevel.getLastMatrix(),screen)
                    pass
                elif event.key == pygame.K_r:
                    initLevel(level_set,current_level)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        clock.tick(30)  # Limit FPS to 30
    pygame.quit()

if __name__ == "__main__":
	
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    
	    # Run Pygame in a separate thread
        pygame_thread = threading.Thread(target=run_pygame, daemon=True)
        pygame_thread.start()
    
    
    app.run(host="0.0.0.0", port=5000, debug=True)
