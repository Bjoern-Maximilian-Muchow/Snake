#include "perf_monitor.h"

#if defined(__AVR__)
extern unsigned int __heap_start;
extern void* __brkval;
#endif

PerfMonitor::PerfMonitor()
  : stepCount(0),
    totalStepUs(0),
    lastStepUs(0),
    maxStepUs(0),
    minFreeRam(32767),
    lastPrintMs(0) {
}

void PerfMonitor::begin() {
  minFreeRam = freeRam();
  lastPrintMs = millis();
}

void PerfMonitor::recordStep(uint32_t stepDurationUs) {
  stepCount++;
  lastStepUs = stepDurationUs;
  totalStepUs += stepDurationUs;
  if (stepDurationUs > maxStepUs) {
    maxStepUs = stepDurationUs;
  }

  int ram = freeRam();
  if (ram < minFreeRam) {
    minFreeRam = ram;
  }
}

bool PerfMonitor::due(unsigned long now) const {
  return now - lastPrintMs >= STATS_INTERVAL_MS;
}

void PerfMonitor::markPrinted(unsigned long now) {
  lastPrintMs = now;
}

void PerfMonitor::print(Stream& out, const GameEngine& engine, StepResult lastResult) const {
  uint32_t avgStepUs = stepCount == 0 ? 0 : totalStepUs / stepCount;

  out.print(F("steps="));
  out.print(stepCount);
  out.print(F(" score="));
  out.print(engine.score());
  out.print(F(" len="));
  out.print(engine.length());
  out.print(F(" state="));
  out.print(resultName(lastResult));
  out.print(F(" step_us="));
  out.print(lastStepUs);
  out.print(F(" avg_us="));
  out.print(avgStepUs);
  out.print(F(" max_us="));
  out.print(maxStepUs);
  out.print(F(" free_ram="));
  out.print(freeRam());
  out.print(F(" min_free_ram="));
  out.println(minFreeRam);
}

int PerfMonitor::freeRam() const {
#if defined(__AVR__)
  int stackVariable = 0;
  if (__brkval == 0) {
    return (int)&stackVariable - (int)&__heap_start;
  }
  return (int)&stackVariable - (int)__brkval;
#else
  return -1;
#endif
}

const __FlashStringHelper* PerfMonitor::resultName(StepResult result) const {
  switch (result) {
    case STEP_OK:
      return F("ok");
    case STEP_ATE_FOOD:
      return F("food");
    case STEP_WALL_COLLISION:
      return F("wall");
    case STEP_SELF_COLLISION:
      return F("self");
    default:
      return F("unknown");
  }
}
