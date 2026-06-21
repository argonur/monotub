#pragma once

class HumiditySensor
{
public:
    virtual ~HumiditySensor() = default;

    virtual void begin() = 0;
    virtual void update() = 0;

    virtual bool isValid() const = 0;
    virtual float getTemperature() const = 0;
    virtual float getHumidity() const = 0;
};