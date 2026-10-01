#include "SCD41Sensor.h"
#include <Wire.h>

SCD41Sensor::SCD41Sensor(uint32_t updateInterval)
    : m_valid(false),
      m_temperature(NAN),
      m_humidity(NAN),
      m_co2(0),
      m_updateInterval(updateInterval),
      m_lastUpdate(0)
{
}

void SCD41Sensor::begin()
{
    Wire.begin();
    
    // Se usa SCD41_I2C_ADDR_62 (0x62)
    m_scd.begin(Wire, SCD41_I2C_ADDR_62);

    // Detiene cualquier medición previa en segundo plano
    m_scd.stopPeriodicMeasurement();

    // Inicia la medición periódica continua
    uint16_t error = m_scd.startPeriodicMeasurement();
    if (error != 0)
    {
        m_valid = false;
    }
}

void SCD41Sensor::update()
{
    if (millis() - m_lastUpdate < m_updateInterval)
    {
        return;
    }

    m_lastUpdate = millis();

    bool dataReady = false;
    // Pasa la variable bool por referencia
    uint16_t error = m_scd.getDataReadyStatus(dataReady);

    if (error == 0 && dataReady)
    {
        uint16_t co2 = 0;
        float temp = 0.0f;
        float hum = 0.0f;

        error = m_scd.readMeasurement(co2, temp, hum);
        if (error == 0)
        {
            m_co2 = co2;
            m_temperature = temp;
            m_humidity = hum;
            m_valid = true;
            return;
        }
    }

    m_valid = false;
}

bool SCD41Sensor::isValid() const
{
    return m_valid;
}

float SCD41Sensor::getTemperature() const
{
    return m_temperature;
}

float SCD41Sensor::getHumidity() const
{
    return m_humidity;
}

uint16_t SCD41Sensor::getCO2() const
{
    return m_co2;
}