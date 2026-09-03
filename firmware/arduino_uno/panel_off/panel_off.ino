// Sends black/off data to all 256 LEDs and keeps Arduino Uno D9 low.
// Target: 16x16 WS2812/NeoPixel-compatible panel on digital pin 9.

#include <Arduino.h>
#include <avr/interrupt.h>

const uint8_t LED_PIN = 9;          // Arduino Uno D9 = PORTB bit 1
const uint16_t LED_COUNT = 16 * 16;

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

void sendBlackPixel() {
  sendByte(0); // green
  sendByte(0); // red
  sendByte(0); // blue
}

void clearPanel() {
  noInterrupts();
  for (uint16_t index = 0; index < LED_COUNT; ++index) {
    sendBlackPixel();
  }
  interrupts();
  delayMicroseconds(80);
  dataLow();
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  dataLow();
  clearPanel();
}

void loop() {
  clearPanel();
  delay(1000);
}
