#include "DHT.h"

#define DHTPIN1 2     // Pin digital donde conectamos el sensor
#define DHTPIN2 3     // Pin digital donde conectamos el sensor
#define DHTTYPE DHT22   // Define si usas el DHT22 o DHT11

DHT dht1(DHTPIN1, DHTTYPE);
DHT dht2(DHTPIN2, DHTTYPE);

void setup() {
  Serial.begin(9600);
  //Serial.println("--- Iniciando Monitoreo de Monotub ---");
  dht1.begin();
  dht2.begin();
}

void loop() {
  // Esperamos 4 segundos entre mediciones (el DHT22 es lento pero preciso)
  delay(4000);

  // Leemos la humedad y temperatura del exterior
  float humInterior = dht1.readHumidity();
  float tempInterior = dht1.readTemperature(); // Temperatura en Celsius

  // Leemos la humedad y temperatura del interior
  float humExterior = dht2.readHumidity();
  float tempExterior = dht2.readTemperature(); // Temperatura en Celsius

  bool error = false;

  // Validamos que el sensor esté respondiendo correctamente
  if (isnan(humInterior) || isnan(tempInterior)) {
    Serial.println("Error: No se puede leer el sensor DHT1 (exterior). Revisa las conexiones.");
    error = true;
  }

  if (isnan(humExterior) || isnan(tempExterior)) {
    Serial.println("Error: No se puede leer el sensor DHT2 (interior). Revisa las conexiones.");
    error = true;
  }

  if (error)
    return;


  Serial.print(millis());
  Serial.print(",");

  Serial.print(humInterior);
  Serial.print(",");
  Serial.print(tempInterior);
  Serial.print(",");

  Serial.print(humExterior);
  Serial.print(",");
  Serial.println(tempExterior);
}