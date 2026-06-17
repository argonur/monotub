#include "DHT22Sensor.h"

DHT22Sensor::DHT22Sensor(uint8_t pin, uint32_t updateInterval)
    : m_dht(pin, DHT22),
      m_valid(false),
      m_temperature(NAN),
      m_humidity(NAN),
      m_updateInterval(updateInterval),
      m_lastUpdate(0)
{
}

void DHT22Sensor::begin()
{
    m_dht.begin();
}

void DHT22Sensor::update()
{
    if(millis() - m_lastUpdate < m_updateInterval)
    {
        return;
    }
    m_lastUpdate = millis();

    float humidity = m_dht.readHumidity();
    float temperature = m_dht.readTemperature();

    if (!isnan(humidity) && !isnan(temperature))
    {
        m_humidity = humidity;
        m_temperature = temperature;
        m_valid = true;
    }
    else
    {
        m_valid = false;
    }
}

bool DHT22Sensor::isValid() const
{
    return m_valid;
}

float DHT22Sensor::getTemperature() const
{
    return m_temperature;
}

float DHT22Sensor::getHumidity() const
{
    return m_humidity;
}