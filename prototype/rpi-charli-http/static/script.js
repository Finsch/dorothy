// for Charli

let ledState = false; // État initial : éteint

// Fonction pour mettre à jour les valeurs du capteur
async function updateSensorValue() {
    try {
        const response = await fetch("/get_sensor_value");
        const data = await response.json();
        
        // Affiche la valeur avec le symbole %
        const value = data.sensor_value || 0;
        document.getElementById("sensor-value").textContent = `${value}%`;
        
        // Met à jour la barre de progression
        const progressBar = document.getElementById("progress-bar");
        progressBar.style.width = `${value}%`;
        
        // Change la couleur en fonction de l'intensité
        if (value > 70) {
            progressBar.style.backgroundColor = "#e74c3c"; // Rouge
        } else if (value < 30) {
            progressBar.style.backgroundColor = "#3498db"; // Bleu
        } else {
            progressBar.style.backgroundColor = "#2ecc71"; // Vert
        }
        
        // Animation de feedback
        const sensorValue = document.getElementById("sensor-value");
        sensorValue.style.transform = "scale(1.1)";
        setTimeout(() => {
            sensorValue.style.transform = "scale(1)";
        }, 300);
        
        // Met à jour le timestamp
        if (data.timestamp) {
            document.getElementById("sensor-timestamp").textContent = 
                `Dernière mise à jour: ${data.timestamp}`;
        }
        
        // Met à jour l'historique
        updateHistory();
    } catch (error) {
        console.error("Erreur :", error);
    }
}

// Fonction pour contrôler la LED
async function toggleLed() {
    ledState = !ledState;
    const command = ledState ? 'ON' : 'OFF';
    const toggle = document.getElementById('ledToggle');
    const label = document.getElementById('ledLabel');
    
    // Animation du toggle
    toggle.classList.toggle('active', ledState);
    label.textContent = ledState ? 'LED ALLUMÉE' : 'LED ÉTEINTE';

    // Envoi de la commande
    fetch("/command", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `command=${command}`
    })
    .catch(error => console.error("Erreur :", error));
}

// Fonction pour mettre à jour l'historique
async function updateHistory() {
    try {
        const response = await fetch("/get_history");
        const history = await response.json();
        
        const historyList = document.getElementById("history-list");
        historyList.innerHTML = history.map(item => 
            `<div class="history-item">${item.timestamp} - ${item.value}%</div>`
        ).join("");
    } catch (error) {
        console.error("Erreur :", error);
    }
}

// Actualisation automatique toutes les 10 secondes
setInterval(updateSensorValue, 10000);

// Initialisation au chargement
document.addEventListener('DOMContentLoaded', () => {
    updateSensorValue();
});