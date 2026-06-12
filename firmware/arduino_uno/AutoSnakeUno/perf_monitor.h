#ifndef AUTOSNAKE_PERF_MONITOR_H
#define AUTOSNAKE_PERF_MONITOR_H

#include "game_engine.h"

class PerfMonitor {
public:
  PerfMonitor();
  void begin();
  void recordStep(uint32_t stepDurationUs);
  bool due(unsigned long now) const;
  void markPrinted(unsigned long now);
  void print(Stream& out, const GameEngine& engine, StepResult lastResult) const;

private:
  uint32_t stepCount;
  uint32_t totalStepUs;
  uint32_t lastStepUs;
  uint32_t maxStepUs;
  int minFreeRam;
  unsigned long lastPrintMs;

  int freeRam() const;
  const __FlashStringHelper* resultName(StepResult result) const;
};

#endif
