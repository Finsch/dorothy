import paho.mqtt.client as mqtt

# Configuration du broker MQTT
broker = "localhost"  # Adresse du broker
port = 1883           # Port par défaut de MQTT
topic = "actuator/led"  # Topic sur lequel s'abonner

# Fonction pour se connecter au broker
def on_connect(client, userdata, flags, rc):
    print("Connecté au broker MQTT")
    if rc == 0:
        print("Connexion réussie")
    else:
        print(f"Échec de la connexion, code retourné {rc}")

# Fonction pour traiter les messages reçus
def on_message(client, userdata, msg):
    command = msg.payload.decode()
    print(f"Commande reçue : {command}")
    if command == "ON":
        print("LED allumée")
    elif command == "OFF":
        print("LED éteinte")

# Créer un client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Se connecter au broker et s'abonner au topic
client.connect(broker, port, 60)
client.subscribe(topic)

# Boucle pour maintenir la connexion et traiter les messages
client.loop_forever()