#include "logger.h"
#include "globals.h"

namespace Logger
{
    static uint32_t m_logInterval;

    void init(uint32_t logInterval) {
        m_logInterval = logInterval;
        Serial.begin(9600);
    }

    void log() {

        static unsigned long m_lastLog;

        if(millis() - m_lastLog < m_logInterval)
        {
            return;
        }
        m_lastLog = millis();

        // Validamos que el sensor esté respondiendo correctamente
        bool error = false;

        if (g_dhtExterior.isValid() == false) {
            Serial.println("Error: No se puede leer el sensor DHT exterior. Revisa las conexiones.");
            error = true;
        }

        if (g_dhtInterior.isValid() == false) {
            Serial.println("Error: No se puede leer el sensor DHT interior. Revisa las conexiones.");
            error = true;
        }

        /*if (g_sht41.isValid() == false) {
            Serial.println("Error: No se puede leer el sensor SHT41. Revisa las conexiones.");
            error = true;
        }*/

        if (g_scd41.isValid() == false) {
            Serial.println("Error: No se puede leer el sensor SCD41. Revisa las conexiones.");
            error = true;
        }

        if (error)
            return;

        // Leemos la humedad y temperatura del exterior
        float humExterior = g_dhtExterior.getHumidity();
        float tempExterior = g_dhtExterior.getTemperature(); // Temperatura en Celsius

        // Leemos la humedad y temperatura del interior
        float humInterior = g_dhtInterior.getHumidity();
        float tempInterior = g_dhtInterior.getTemperature(); // Temperatura en Celsius
        
        /*
        // Leemos la humedad y temperatura del SHT41
        float humSHT41 = g_sht41.getHumidity();
        float tempSHT41 = g_sht41.getTemperature(); // Temperatura en Celsius
        */
        
        // Leemos la humedad y temperatura del SCD41
        float humSCD41 = g_scd41.getHumidity();
        float tempSCD41 = g_scd41.getTemperature(); // Temperatura en Celsius
        float co2SCD41 = g_scd41.getCO2(); // Concentración de CO2 en ppm

        //manda los datos al serial en formato CSV: millis(), humInterior, tempInterior, humExterior, tempExterior
        Serial.print(millis());
        Serial.print(",");

        Serial.print(humInterior);
        Serial.print(",");
        Serial.print(tempInterior);
        Serial.print(",");

        /*
        Serial.print(humSHT41);
        Serial.print(",");
        Serial.print(tempSHT41);
        Serial.print(",");
        */
        
        Serial.print(humSCD41);
        Serial.print(",");
        Serial.print(tempSCD41);
        Serial.print(",");
        Serial.print(co2SCD41);
        Serial.print(",");

        Serial.print(humExterior);
        Serial.print(",");
        Serial.println(tempExterior);
    }
}

