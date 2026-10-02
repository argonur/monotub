#include "logger.h"
#include "globals.h"

unsigned long last_control = 0;
unsigned long last_report = 0;

constexpr unsigned long UPDATE_INTERVAL = 5000; // Intervalo de actualización de los sensores en milisegundos

DHT22Sensor g_dhtExterior(PIN_DHT_EXTERIOR, UPDATE_INTERVAL);
DHT22Sensor g_dhtInterior(PIN_DHT_INTERIOR, UPDATE_INTERVAL);
//SHT41Sensor g_sht41(UPDATE_INTERVAL);
SCD41Sensor g_scd41(UPDATE_INTERVAL);

void setup() {
  Logger::init(UPDATE_INTERVAL); // Inicializamos el logger con un intervalo de x milisegundos
  g_dhtExterior.begin();
  g_dhtInterior.begin();
  //g_sht41.begin();
  g_scd41.begin();
}

void updateSensors() {
  g_dhtExterior.update();
  g_dhtInterior.update();
  //g_sht41.update();
  g_scd41.update();
}

void loop() {

  updateSensors();

  Logger::log();

}