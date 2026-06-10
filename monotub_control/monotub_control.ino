#include "DHT.h"

#define DHTPIN1 2     // Pin digital donde conectamos el sensor exterior
#define DHTPIN2 3     // Pin digital donde conectamos el sensor interior
#define DHTTYPE DHT22   // Define si usas el DHT22 o DHT11

DHT dhtExterior(DHTPIN1, DHTTYPE);
DHT dhtInterior(DHTPIN2, DHTTYPE);

void setup() {
  Serial.begin(9600);
  //Serial.println("--- Iniciando Monitoreo de Monotub ---");
  dhtExterior.begin();
  dhtInterior.begin();
}

void loop() {
  // Esperamos 2 minutos entre mediciones (el DHT22 es lento pero preciso, dos segundos entre mediociones bastan)
  delay(60000);
  
  // Leemos la humedad y temperatura del exterior
  float humExterior = dhtExterior.readHumidity();
  float tempExterior = dhtExterior.readTemperature(); // Temperatura en Celsius

  // Leemos la humedad y temperatura del interior
  float humInterior = dhtInterior.readHumidity();
  float tempInterior = dhtInterior.readTemperature(); // Temperatura en Celsius

  bool error = false;

  // Validamos que el sensor esté respondiendo correctamente

  if (isnan(humExterior) || isnan(tempExterior)) {
    Serial.println("Error: No se puede leer el sensor DHT exterior. Revisa las conexiones.");
    error = true;
  }

  if (isnan(humInterior) || isnan(tempInterior)) {
    Serial.println("Error: No se puede leer el sensor DHT interior. Revisa las conexiones.");
    error = true;
  }

  if (error)
    return;

  //manda los datos al serial en formato CSV: millis(), humInterior, tempInterior, humExterior, tempExterior
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