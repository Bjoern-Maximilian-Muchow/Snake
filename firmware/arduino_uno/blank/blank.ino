// Minimal blank Arduino Uno sketch.
// Does not drive the LED panel data line.

#include <Arduino.h>

const uint8_t LED_PIN = 9;

void setup() {
  pinMode(LED_PIN, INPUT);
}

void loop() {
}
