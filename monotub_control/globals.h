#pragma once

#include "DHT22Sensor.h"

#define PIN_DHT_EXTERIOR 2     // Pin digital donde conectamos el sensor exterior
#define PIN_DHT_INTERIOR 3     // Pin digital donde conectamos el sensor interior

extern DHT22Sensor g_dhtInterior;
extern DHT22Sensor g_dhtExterior;