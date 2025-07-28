let ledState = false; // État initial : éteint

function updateSensorValue() {
    fetch("/get_sensor_value")
        .then(response => response.json())
        .then(data => {
            document.querySelector(".sensor-value").textContent = data.sensor_value;
            
            // Animation de feedback
            const sensorValue = document.querySelector(".sensor-value");
            sensorValue.style.transform = "scale(1.1)";
            setTimeout(() => {
                sensorValue.style.transform = "scale(1)";
            }, 300);
        })
        .catch(error => console.error("Erreur :", error));
}

function toggleLed() {
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

// Actualisation automatique toutes les 10 secondes (optionnel)
setInterval(updateSensorValue, 10000);