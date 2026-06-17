#include "logger.h"
#include "globals.h"

unsigned long last_control = 0;
unsigned long last_report = 0;

constexpr unsigned long UPDATE_INTERVAL = 4000; // Intervalo de actualización de los sensores en milisegundos

DHT22Sensor g_dhtExterior(PIN_DHT_EXTERIOR, UPDATE_INTERVAL);
DHT22Sensor g_dhtInterior(PIN_DHT_INTERIOR, UPDATE_INTERVAL);

void setup() {
  Logger::init(60000); // Inicializamos el logger con un intervalo de 60 segundos
  g_dhtExterior.begin();
  g_dhtInterior.begin();
}

void updateSensors() {
  g_dhtExterior.update();
  g_dhtInterior.update();
}

void loop() {

  updateSensors();

  Logger::log();

}