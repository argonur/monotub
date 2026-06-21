#pragma once

#include <Adafruit_SHT4x.h>
#include "humiditySensor.h"

class SHT41Sensor : public HumiditySensor
{
public:
    explicit SHT41Sensor(uint32_t updateInterval);

    void begin() override;
    void update() override;

    bool isValid() const override;
    float getTemperature() const override;
    float getHumidity() const override;

private:
    Adafruit_SHT4x m_sht;

    bool m_valid;
    float m_temperature;
    float m_humidity;

    uint32_t m_updateInterval;
    uint32_t m_lastUpdate;
};