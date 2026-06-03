#include "DHT.h"

#define DHTPIN1 2     // Pin digital donde conectamos el sensor
#define DHTPIN2 3     // Pin digital donde conectamos el sensor
#define DHTTYPE DHT22   // Define si usas el DHT22 o DHT11

DHT dht1(DHTPIN1, DHTTYPE);
DHT dht2(DHTPIN2, DHTTYPE);

void setup() {
  Serial.begin(9600);
  Serial.println("--- Iniciando Monitoreo de Monotub ---");
  dht1.begin();
  dht2.begin();
}

void loop() {
  // Esperamos 2 segundos entre mediciones (el DHT22 es lento pero preciso)
  delay(2000);

  float humedad1 = dht1.readHumidity();
  float temperatura1 = dht1.readTemperature(); // Temperatura en Celsius

  float humedad2 = dht2.readHumidity();
  float temperatura2 = dht2.readTemperature(); // Temperatura en Celsius

  bool error = false;

  // Validamos que el sensor esté respondiendo correctamente
  if (isnan(humedad1) || isnan(temperatura1)) {
    Serial.println("Error: No se puede leer el sensor DHT1. Revisa las conexiones.");
    error = true;
  }

  if (isnan(humedad2) || isnan(temperatura2)) {
    Serial.println("Error: No se puede leer el sensor DHT2. Revisa las conexiones.");
    error = true;
  }

  if (error)
    return;

  // Desplegamos los datos en el Monitor Serie
  Serial.print("Humedad ambiente: ");
  Serial.print(humedad1);
  Serial.print("%\t");
  Serial.print("Temperatura ambiente: ");
  Serial.print(temperatura1);
  Serial.print(" *C");
  
  Serial.print("\t\t");

  Serial.print("Humedad interior: ");
  Serial.print(humedad2);
  Serial.print("%\t");
  Serial.print("Temperatura interior: ");
  Serial.print(temperatura2);
  Serial.println(" *C");
}