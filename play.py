import requests
import time
import ollama

class SokobanAPIClient:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        """Inicializa la clase con la URL base de la API y variables del estado del juego."""
        self.base_url = base_url
        self.level = None
        self.player_position = None
        self.boxes = None
        self.matrix = None
        self.update_state()

    def update_state(self):
        """Consulta y actualiza el estado del juego en las variables de la clase."""
        response = requests.get(f"{self.base_url}/state")
        if response.status_code == 200:
            data = response.json()
            self.level = data["level"]
            self.player_position = data["player_position"]
            self.boxes = data["boxes"]
            self.matrix = data["matrix"]
        else:
            print("⚠️ Error: No se pudo obtener el estado del juego.")

    def move(self, direction):
        """Envía un comando para mover al jugador en la dirección especificada (L, R, U, D)."""
        response = requests.post(f"{self.base_url}/move", json={"direction": direction.upper()})
        if response.status_code == 200:
            print(f"✅ Movido a {direction.upper()}")
        else:
            print("⚠️ Error: No se pudo mover al jugador.")

    def reset_game(self):
        """Reinicia el estado del juego llamando al endpoint /reset."""
        response = requests.post(f"{self.base_url}/reset")
        if response.status_code == 200:
            print("🔄 Juego reiniciado correctamente.")
        else:
            print("⚠️ Error: No se pudo reiniciar el juego.")

    def display_state(self):
        """Muestra el estado actual del juego en la terminal."""
        print("\n🎮 Estado del Juego:")
        print(f"🟢 Nivel: {self.level}")
        print(f"👤 Posición del jugador: {self.player_position}")
        print("📦 Cajas en el nivel:", self.boxes)
        print("\n🗺️ Mapa del juego:\n")
        for row in self.matrix:
            print("".join(row))

    def get_ai_move(self):
        """Usa Ollama para decidir el mejor movimiento."""
        prompt = f"""
        Estás jugando Sokoban. El jugador está en la posición {self.player_position}.
        Las cajas están en: {self.boxes}.
        El mapa del nivel es el siguiente (donde # son paredes, . son objetivos, @ es el jugador y $ son cajas):
        {self.matrix}

        ¿Cuál es el mejor movimiento? Responde solo con L, R, U o D.
        """
        response = ollama.chat(model="phi3:3.8b", messages=[{"role": "user", "content": prompt}])
        move = response["message"]["content"].strip().upper()

        if move not in ["L", "R", "U", "D"]:
            print("⚠️ Respuesta inválida de la IA, eligiendo un movimiento al azar.")
            return "R"  # Movimiento por defecto si la IA no responde correctamente
        return move

    def run(self):
        """Bucle principal para que la IA juegue automáticamente."""
        while True:
            self.update_state()
            self.display_state()
            
            move = self.get_ai_move()
            print(f"\n🤖 La IA eligió moverse: {move}")
            self.move(move)

            time.sleep(1)  # Esperar un segundo antes de la siguiente actualización

# Ejecutar el cliente
if __name__ == "__main__":
    client = SokobanAPIClient()
    client.run()
