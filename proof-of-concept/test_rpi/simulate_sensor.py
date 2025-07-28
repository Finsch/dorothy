import paho.mqtt.client as mqtt
import time

# Configuration du broker MQTT
broker = "localhost"  # Adresse du broker
port = 1883           # Port par défaut de MQTT
topic = "sensor/photoresistor"  # Topic sur lequel publier les données

# Fonction pour se connecter au broker
def on_connect(client, userdata, flags, rc):
    print("Connecté au broker MQTT")
    print(f"Message reçu (ID: {msg.mid})")  # Vérifiez si l'ID est dupliqué //tobedeleted
    if rc == 0:
        print("Connexion réussie")
    else:
        print(f"Échec de la connexion, code retourné {rc}")

# Créer un client MQTT
client = mqtt.Client()
client.on_connect = on_connect

# Se connecter au broker
client.connect(broker, port, 60)

# Simuler un capteur qui publie des données
counter = 0
while True:
    # Simuler une valeur de photorésistance (par exemple, un compteur)
    value = counter
    print(f"Publication de la valeur : {value}")
    client.publish(topic, value)
    counter += 1
    time.sleep(5)  # Publier toutes les 5 secondes