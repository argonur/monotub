#pragma once

#include <DHT.h>

class DHT22Sensor
{
public:
    DHT22Sensor(uint8_t pin, uint32_t updateInterval = 2000);

    void begin();
    void update();
    bool isValid() const;
    float getTemperature() const;
    float getHumidity() const;

private:
    DHT m_dht;
    bool m_valid;
    float m_temperature;
    float m_humidity;
    uint32_t m_updateInterval;
    unsigned long m_lastUpdate;
};