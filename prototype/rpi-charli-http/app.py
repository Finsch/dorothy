from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt
from threading import Lock
import os
from datetime import datetime
import time

app = Flask(__name__, static_folder='static')

# Configuration du fichier de données
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.txt')

# Dernière valeur du capteur
latest_sensor_data = {
    'value': None,
    'timestamp': None,
    'lock': Lock()
}

# Verrou pour accès au fichier
file_lock = Lock()

def init_db():
    """Initialise le fichier de données avec l'en-tête si nécessaire"""
    if not os.path.exists(DB_FILE):
        with file_lock:
            with open(DB_FILE, 'w') as f:
                f.write("timestamp,value\n")

def save_to_db(value):
    """Enregistre une nouvelle valeur dans le fichier"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with file_lock:
        with open(DB_FILE, 'a') as f:
            f.write(f"{timestamp},{value}\n")
        
        # Maintenance : garde seulement les 1000 dernières entrées
        with open(DB_FILE, 'r') as f:
            lines = f.readlines()
        
        if len(lines) > 1001:  # 1000 entrées + en-tête
            with open(DB_FILE, 'w') as f:
                f.writelines([lines[0]] + lines[-1000:])  # Garde l'en-tête + 1000 dernières

def read_last_values(n=15):
    """Lit les n dernières valeurs du fichier"""
    try:
        with file_lock:
            with open(DB_FILE, 'r') as f:
                lines = f.readlines()[1:]  # Ignore l'en-tête
                return [{
                    "timestamp": line.split(",")[0],
                    "value": line.split(",")[1].strip()
                } for line in lines[-n:][::-1]]  # Inversion pour récent -> ancien
    except FileNotFoundError:
        return []

# Initialisation au démarrage
init_db()

# Configuration MQTT
def on_mqtt_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        save_to_db(payload)
        with latest_sensor_data['lock']:
            latest_sensor_data['value'] = payload
            latest_sensor_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Reçu: {msg.topic} {payload}")
    except Exception as e:
        print(f"Erreur MQTT: {str(e)}")

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_mqtt_message
mqtt_client.connect("localhost", 1883)
mqtt_client.subscribe("esp32/sensor")
mqtt_client.loop_start()

# Routes
@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/get_sensor_value")
def get_sensor():
    with latest_sensor_data['lock']:
        return jsonify({
            "sensor_value": latest_sensor_data['value'],
            "timestamp": latest_sensor_data['timestamp']
        })

@app.route("/command", methods=["POST"])
def control_led():
    command = request.form.get("command")
    if command in ["ON", "OFF"]:
        mqtt_client.publish("esp32/led", command)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

@app.route("/get_history")
def get_history():
    history = read_last_values(15)
    return jsonify(history)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)