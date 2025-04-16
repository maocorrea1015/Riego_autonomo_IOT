# Write your code here :-)
import network
import socket
from machine import Pin, ADC, reset
import time

# Configuración de WiFi
SSID = "Nombre del wifi"
PASSWORD = "Contraseña del wifi"

# Sensor de humedad y bomba
sensor_humedad = ADC(Pin(34))
sensor_humedad.atten(ADC.ATTN_11DB)  # Rango de 0 a 3.3V
rele_bomba = Pin(26, Pin.OUT)

# Umbral de humedad
UMBRAL_HUMEDAD = 50

# Función para conectar a WiFi
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    for _ in range(10):
        if wlan.isconnected():
            print("Conectado:", wlan.ifconfig())
            return True
        time.sleep(1)
    print("Error: No se pudo conectar a WiFi")
    reset()  # Reiniciar ESP32 si falla WiFi


# Función para leer humedad (invertida)
def leer_humedad():
    lectura = sensor_humedad.read()  # Valor 0 - 4095
    humedad = (1 - (lectura / 4095)) * 100
    return max(0, min(100, humedad))  # Límite 0-100%


# Página HTML
def generar_pagina(humedad, estado_bomba):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32 - Monitor de Humedad</title>
    <link rel="icon" type="image/png" href="https://raw.githubusercontent.com/ProtoDevLabs/protodevlabs.com/refs/heads/main/static/images/logo.png?token=GHSAT0AAAAAADAHGCCKRMU3PTDMKYMDKLDUZ6OGC3A">
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; text-align: center; padding: 20px; }}
        .container {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); display: inline-block; }}
        .switch-container {{ margin-top: 20px; }}
        .switch-label {{ font-size: 18px; margin-right: 10px; }}
        .switch {{ width: 60px; height: 30px; appearance: none; background: #ddd; border-radius: 15px; position: relative; cursor: pointer; }}
        .switch:checked {{ background: #4CAF50; }}
        .switch::before {{ content: ""; position: absolute; width: 26px; height: 26px; background: white; border-radius: 50%; top: 2px; left: 2px; transition: 0.3s; }}
        .switch:checked::before {{ left: 32px; }}
    </style>
    <script>
        function actualizar() {{
            fetch('/datos')
                .then(response => response.json())
                .then(data => {{
                    document.getElementById('humedad').innerText = data.humedad + "%";
                    document.getElementById('switch').checked = data.bomba;
                }});
        }}

        function cambiarBomba(estado) {{
            fetch(`/bomba?estado=${{estado ? '1' : '0'}}`);
        }}

        setInterval(actualizar, 3000); // Actualiza cada 3 segundos
    </script>
</head>
<body>
    <div class="container">
        <h2>Humedad del Suelo</h2>
        <h3 id="humedad">{humedad:.2f}%</h3>
        <h2>Control de Bomba</h2>
        <div class="switch-container">
            <span class="switch-label">Activar Bomba</span>
            <input type="checkbox" id="switch" class="switch" onchange="cambiarBomba(this.checked)" { 'checked' if estado_bomba else '' }>
        </div>
    </div>
    <footer style="background: blue; color: white; text-align: center; padding: 15px; font-size: 14px;">
        <p>Protodevlabs.com & SER Electronica y Robotica</p>
        <p>&copy; 2024 Derechos Reservados - Héctor Mauricio Forero Correa</p>
    </footer>
</body>
</html>"""


# Servidor Web
def iniciar_servidor():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", 80))
    s.listen(5)
    print("Servidor iniciado")

    while True:
        conn, addr = s.accept()
        request = conn.recv(1024).decode()

        humedad = leer_humedad()
        if humedad < UMBRAL_HUMEDAD:
            rele_bomba.value(1)  # Encender bomba
        else:
            rele_bomba.value(0)  # Apagar bomba
        estado_bomba = rele_bomba.value()

        if "/bomba?estado=1" in request:
            rele_bomba.value(1)
        elif "/bomba?estado=0" in request:
            rele_bomba.value(0)
        # Endpoint para enviar datos JSON
        if "/datos" in request:
            response = f'{{"humedad": {humedad:.2f}, "bomba": {estado_bomba} }}'
            conn.send(
                "HTTP/1.1 200 OK\nContent-Type: application/json\n\n".encode()
                + response.encode()
            )
        else:
            pagina = generar_pagina(humedad, estado_bomba)
            conn.send(
                "HTTP/1.1 200 OK\nContent-Type: text/html\n\n".encode()
                + pagina.encode()
            )
        conn.close()


# Ejecutar
conectar_wifi()
iniciar_servidor()
