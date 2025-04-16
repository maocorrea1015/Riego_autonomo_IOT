# Riego_autonomo_IOT
# 💧 Sistema de Riego Autónomo con ESP32 e IoT

**Autor:** Hector Mauricio Forero Correa  
**Organización:** ProtoDevLabs - Semillero de electrónica y robótica  
**Fecha:** 16 de abril de 2025

---

## 📘 Introducción

Este proyecto presenta un sistema de riego autónomo basado en ESP32 e IoT, diseñado para optimizar el consumo de agua en la agricultura. Utilizando sensores de humedad del suelo y conectividad Wi-Fi, el sistema decide automáticamente cuándo regar, mientras permite supervisión y control remoto a través de una interfaz web intuitiva.

---

## ⚙️ Desarrollo del Sistema

El sistema está compuesto por tres bloques principales:

- **Sensores:** humedad del suelo, temperatura y humedad ambiental.  
- **Actuadores:** una electroválvula controlada por un módulo relé.  
- **Comunicación:** conectividad Wi-Fi para enviar datos a la nube y permitir interacción remota.

---

## 🔩 Componentes Utilizados

| Componente                            | Función                                |
|---------------------------------------|-----------------------------------------|
| ESP32                                 | Microcontrolador con Wi-Fi/Bluetooth   |
| Sensor de humedad (YL-69 o capacitivo)| Detecta la humedad del suelo           |
| Sensor DHT11/DHT22                    | Mide temperatura y humedad ambiental   |
| Módulo relé 5V                        | Controla la válvula de riego           |
| Electroválvula                        | Abre/cierra el paso del agua           |
| Fuente de alimentación                | Energía para el sistema                |
| Protoboard / PCB                      | Ensamblaje de componentes              |

---

## 🔌 Esquema de Conexiones Eléctricas

*(Incluir diagrama si está disponible)*

---

## 🔄 Funcionamiento del Sistema

1. El ESP32 realiza lecturas periódicas de humedad.
2. Si la humedad es baja, activa el relé para abrir la válvula.
3. Cuando el nivel es adecuado, detiene el riego.
4. Los datos se envían a la nube para su visualización remota.

---

## 💻 Código Fuente

Repositorio completo en GitHub:  
🔗 [https://github.com/maocorrea1015/Riego_autonomo_IOT](https://github.com/maocorrea1015/Riego_autonomo_IOT)

Características del código:
- Lectura de sensores con promedio
- Condicionales automáticos para activar el riego
- Conexión Wi-Fi con envío de datos a la nube
- Reconexión automática ante pérdida de señal

---

## 🌐 Interfaz Web

### Funcionalidades:
- Visualización en tiempo real de:
  - Humedad del suelo
  - Temperatura y humedad ambiental
  - Estado del sistema (activo/inactivo)
- Control manual de la válvula
- Historial de registros mediante gráficas

### Diseño:
Desarrollada en **HTML**, **CSS** y **JavaScript**, con diseño responsive para dispositivos móviles.

---

## ✅ Conclusiones

- Se demostró la viabilidad de un sistema de riego automatizado, confiable y de bajo costo.
- El uso del ESP32 y plataformas IoT permite una gestión eficiente del agua.
- La interfaz web mejora la experiencia del usuario, al permitir monitoreo y control remoto.
- El sistema es escalable y puede integrarse con energía solar o predicción climática en versiones futuras.

---

