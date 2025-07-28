#include <WiFi.h>
#include <PubSubClient.h>

// good.

// Configuration WiFi
const char* ssid = "Nightcrawl";
const char* password = "charcoal";

// Configuration MQTT
const char* mqtt_server = "172.20.10.12"; // IP_DE_LA_RPI
const char* topic_pub = "esp32/sensor";
const char* topic_sub = "esp32/led";
const char* client_id = "ESP32Client_01"; // Identifiant unique

// Broches
const int photoPin = 36; // Photorésistance sur GPIO36

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connexion à ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connecté");
  Serial.print("IP de la carte : "); Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Tentative MQTT...");
    if (client.connect(client_id)) {
      Serial.println("Connecté");
      client.subscribe(topic_sub);// Abonnement aux commandes
      Serial.print("Abonné à : ");
      Serial.println(topic_sub);
    } else {
      Serial.print("Échec, rc="); Serial.print(client.state());
      Serial.println(" Nouvel essai dans 5s...");
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (int i = 0; i < length; i++) message += (char)payload[i];
  
  Serial.print("Message reçu ["); 
  Serial.print(topic); 
  Serial.print("] "); 
  Serial.println(message);

  // Contrôle de la LED
  if (message == "ON") {
    digitalWrite(LED_BUILTIN, HIGH); // ledPin = 2
    Serial.println("LED allumée");
  } 
  else if (message == "OFF") {
    digitalWrite(LED_BUILTIN, LOW);
    Serial.println("LED éteinte");
  }
  else {
    Serial.println("Commande non reconnue");
  }
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW); // Éteindre la LED au démarrage
  Serial.begin(9600);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) reconnect();
  client.loop();


  // Lecture de la photorésistance
  int sensorValue = analogRead(photoPin); // Photorésistance sur la broche 36
  int sensorValuePerCent = map(sensorValue, 4095, 0, 0, 100); // Conversion en pourcentage
  if (client.publish(topic_pub, String(sensorValuePerCent).c_str())) {
    Serial.print("Valeur publiée: ");
    Serial.print(sensorValuePerCent);
    Serial.println("%");
  } else {
    Serial.println("Échec de publication");
  }
  
  delay(2000); // Réduit à 2s pour plus de réactivité
}