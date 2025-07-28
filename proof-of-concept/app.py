from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt
import os

app = Flask(__name__, static_folder='static')

# Configuration du broker MQTT
broker = "localhost"
port = 1883

# Dernière valeur reçue du capteur
sensor_value = None

# Fichier pour stocker les données des capteurs
DATA_FILE = "sensor_data.txt"

# Fonction pour traiter les messages MQTT
def on_message(client, userdata, msg):
    global sensor_value
    sensor_value = msg.payload.decode()
    print(f"Valeur reçue du capteur xqc : {sensor_value}")
    # Enregistrer la valeur dans le fichier
    with open(DATA_FILE, "a") as f:
        f.write(f"{sensor_value}\n")

# Créer un client MQTT pour Flask
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(broker, port, 60)
mqtt_client.subscribe("sensor/photoresistor")
mqtt_client.loop_start()

# Route pour afficher la page web
@app.route("/")
def index():
    # Lire les dernières valeurs du fichier
    with open(DATA_FILE, "r") as f:
        latest_data = f.readlines()[-10:]  # Lire les 10 dernières lignes
    return render_template("index.html", sensor_value=sensor_value, latest_data=latest_data)

# Route pour envoyer une commande à l'actionneur
@app.route("/command", methods=["POST"])
def command():
    command = request.form.get("command")
    mqtt_client.publish("actuator/led", command)
    return jsonify({"status": "success", "command": command})

# Route pour obtenir la dernière valeur du capteur
@app.route("/get_sensor_value")
def get_sensor_value():
    # Lire la dernière valeur du fichier
    with open(DATA_FILE, "r") as f:
        latest_value = f.readlines()[-1].strip() if os.path.exists(DATA_FILE) else "N/A"
    return jsonify({"sensor_value": latest_value})

if __name__ == "__main__":
    app.run(debug=True)