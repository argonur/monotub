#pragma once

#include <SensirionI2cScd4x.h>
#include "humiditySensor.h"

class SCD41Sensor : public HumiditySensor
{
public:
    explicit SCD41Sensor(uint32_t updateInterval = 5000);

    void begin() override;
    void update() override;

    bool isValid() const override;
    float getTemperature() const override;
    float getHumidity() const override;
    uint16_t getCO2() const;

private:
    SensirionI2cScd4x m_scd;

    bool m_valid;
    float m_temperature;
    float m_humidity;
    uint16_t m_co2;

    uint32_t m_updateInterval;
    uint32_t m_lastUpdate;
};