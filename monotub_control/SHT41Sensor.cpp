#include "SHT41Sensor.h"

SHT41Sensor::SHT41Sensor(uint32_t updateInterval)
    : m_valid(false),
      m_temperature(NAN),
      m_humidity(NAN),
      m_updateInterval(updateInterval),
      m_lastUpdate(0)
{
}

void SHT41Sensor::begin()
{
    if(!m_sht.begin())
    {
        m_valid = false;
    }
}

void SHT41Sensor::update()
{
    if(millis() - m_lastUpdate < m_updateInterval)
    {
        return;
    }

    m_lastUpdate = millis();

    sensors_event_t humidity;
    sensors_event_t temperature;

    if(m_sht.getEvent(&humidity, &temperature))
    {
        m_humidity = humidity.relative_humidity;
        m_temperature = temperature.temperature;
        m_valid = true;
    }
    else
    {
        m_valid = false;
    }
}

bool SHT41Sensor::isValid() const
{
    return m_valid;
}

float SHT41Sensor::getTemperature() const
{
    return m_temperature;
}

float SHT41Sensor::getHumidity() const
{
    return m_humidity;
}