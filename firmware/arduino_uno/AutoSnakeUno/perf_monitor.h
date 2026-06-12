#ifndef AUTOSNAKE_PERF_MONITOR_H
#define AUTOSNAKE_PERF_MONITOR_H

#include "game_engine.h"

class PerfMonitor {
public:
  PerfMonitor();
  void begin();
  void resetCounters();
  void recordStep(uint32_t botUs, uint32_t engineUs, uint32_t renderUs, StepResult result);
  bool due(unsigned long now) const;
  void markPrinted(unsigned long now);
  void toggleCsv(Stream& out);
  void print(Stream& out, const GameEngine& engine, StepResult lastResult);

private:
  uint32_t stepCount;
  uint32_t foodCount;
  uint32_t collisionCount;
  uint32_t totalWorkUs;
  uint32_t lastBotUs;
  uint32_t lastEngineUs;
  uint32_t lastRenderUs;
  uint32_t maxBotUs;
  uint32_t maxEngineUs;
  uint32_t maxRenderUs;
  int minFreeRam;
  unsigned long lastPrintMs;
  bool csvMode;

  int freeRam() const;
  uint32_t averageWorkUs() const;
  uint32_t loadMilliPercent() const;
  void printHuman(Stream& out, const GameEngine& engine, StepResult lastResult, int currentRam) const;
  void printCsv(Stream& out, const GameEngine& engine, StepResult lastResult, int currentRam) const;
  const __FlashStringHelper* resultName(StepResult result) const;
};

#endif
