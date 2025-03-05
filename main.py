import os
import copy
import multiprocessing
#import pygame
from fastapi import FastAPI
#from Environment import Environment
from Level import Level
#from sokaband import movePlayer, initLevel, drawLevel
import sys
import uvicorn
from flask import Flask, jsonify, request

theme = "default"
level_set = "original"
current_level = 1
myLevel = Level(level_set, current_level)
target_found = False

def initLevel(level_set,level):
	# Create an instance of this Level
	global myLevel
	myLevel = Level(level_set,level)

	# Draw this level
	#drawLevel(myLevel.getMatrix())
	
	global target_found
	target_found = False

def movePlayer(direction,myLevel):
	
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
	
	#drawLevel(matrix)
	
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
        movePlayer(direction.upper(), myLevel)
        return jsonify({"message": f"Moved {direction}", "state": update_game_state()})
    
    return jsonify({"error": "Invalid direction. Use L, R, U, or D."}), 400

@app.route("/reset", methods=["POST"])
def reset_game():
    """Reiniciar el estado del juego"""
    global myLevel
    myLevel = Level(level_set, current_level)
    return jsonify({"message": "Game reset", "state": update_game_state()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
