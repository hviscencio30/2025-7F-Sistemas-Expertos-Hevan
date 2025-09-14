import json

# Cargar base de datos de conocimiento
try:
    with open("knowledge_base.json", "r") as file:
        knowledge_base = json.load(file)
except FileNotFoundError:
    knowledge_base = {}

def guardar_conocimiento():
    with open("knowledge_base.json", "w") as file:
        json.dump(knowledge_base, file, indent=4)

def obtener_respuesta(pregunta):
    # Buscar coincidencia exacta
    if pregunta in knowledge_base:
        return knowledge_base[pregunta]
    else:
        # Preguntar por nuevo conocimiento
        print("No conozco la respuesta. ¿Qué debería responder?")
        respuesta_nueva = input("Tu respuesta: ")
        knowledge_base[pregunta] = respuesta_nueva
        guardar_conocimiento()
        return "Gracias! He aprendido algo nuevo."

def chat():
    print("Chat iniciado. Escribe 'salir' para terminar.")
    while True:
        pregunta = input("Tú: ")
        if pregunta.lower() == "salir":
            print("Chat terminado.")
            break
        respuesta = obtener_respuesta(pregunta)
        print("Bot:", respuesta)

if __name__ == "__main__":
    chat()