// AutoSnake LED panel smoke test for Arduino Uno R3.
//
// Target: 16x16 addressable RGB panel on digital pin 9.
// Protocol: WS2812/NeoPixel-style one-wire data, color order GRB.
//
// Power safety: this sketch lights only one LED at low brightness.
// Keep the panel powered from the external 5 V supply and connect GND
// between the supply, panel, and Arduino.

#include <Arduino.h>
#include <avr/interrupt.h>

const uint8_t LED_PIN = 9;          // Arduino Uno D9 = PORTB bit 1
const uint16_t LED_COUNT = 16 * 16;
const uint8_t BRIGHTNESS = 12;      // Low current: one LED at ~5% duty
const uint16_t LED_ON_TIME_MS = 1000;
const uint16_t LED_OFF_TIME_MS = 80;

static inline void dataHigh() {
  PORTB |= _BV(PORTB1);
}

static inline void dataLow() {
  PORTB &= ~_BV(PORTB1);
}

static inline void waitShort() {
  asm volatile("nop\nnop\nnop\nnop\nnop\n");
}

static inline void waitLong() {
  asm volatile(
    "nop\nnop\nnop\nnop\nnop\nnop\nnop\nnop\n"
    "nop\nnop\nnop\nnop\nnop\nnop\nnop\nnop\n"
  );
}

void sendBit(bool bitValue) {
  if (bitValue) {
    dataHigh();
    waitLong();
    dataLow();
    waitShort();
  } else {
    dataHigh();
    waitShort();
    dataLow();
    waitLong();
  }
}

void sendByte(uint8_t value) {
  for (uint8_t mask = 0x80; mask != 0; mask >>= 1) {
    sendBit((value & mask) != 0);
  }
}

void sendPixel(uint8_t red, uint8_t green, uint8_t blue) {
  sendByte(green);
  sendByte(red);
  sendByte(blue);
}

void showSingleLed(uint16_t activeIndex) {
  noInterrupts();
  for (uint16_t index = 0; index < LED_COUNT; ++index) {
    if (index == activeIndex) {
      sendPixel(BRIGHTNESS, BRIGHTNESS, BRIGHTNESS);
    } else {
      sendPixel(0, 0, 0);
    }
  }
  interrupts();
  delayMicroseconds(80);
}

void clearPanel() {
  noInterrupts();
  for (uint16_t index = 0; index < LED_COUNT; ++index) {
    sendPixel(0, 0, 0);
  }
  interrupts();
  delayMicroseconds(80);
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  dataLow();
  clearPanel();
}

void loop() {
  for (uint16_t index = 0; index < LED_COUNT; ++index) {
    showSingleLed(index);
    delay(LED_ON_TIME_MS);
    clearPanel();
    delay(LED_OFF_TIME_MS);
  }
}
