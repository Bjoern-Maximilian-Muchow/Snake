#include "perf_monitor.h"

#if defined(__AVR__)
extern unsigned int __heap_start;
extern void* __brkval;
#endif

PerfMonitor::PerfMonitor()
  : csvMode(false) {
  resetCounters();
}

void PerfMonitor::begin() {
  resetCounters();
  lastPrintMs = millis();
}

void PerfMonitor::resetCounters() {
  stepCount = 0;
  foodCount = 0;
  collisionCount = 0;
  totalWorkUs = 0;
  lastBotUs = 0;
  lastEngineUs = 0;
  lastRenderUs = 0;
  maxBotUs = 0;
  maxEngineUs = 0;
  maxRenderUs = 0;
  minFreeRam = freeRam();
  lastPrintMs = millis();
}

void PerfMonitor::recordStep(uint32_t botUs, uint32_t engineUs, uint32_t renderUs, StepResult result) {
  stepCount++;
  lastBotUs = botUs;
  lastEngineUs = engineUs;
  lastRenderUs = renderUs;
  totalWorkUs += botUs + engineUs + renderUs;

  if (botUs > maxBotUs) maxBotUs = botUs;
  if (engineUs > maxEngineUs) maxEngineUs = engineUs;
  if (renderUs > maxRenderUs) maxRenderUs = renderUs;
  if (result == STEP_ATE_FOOD) foodCount++;
  if (result >= STEP_WALL_COLLISION) collisionCount++;

  int ram = freeRam();
  if (ram < minFreeRam) minFreeRam = ram;
}

bool PerfMonitor::due(unsigned long now) const {
  return now - lastPrintMs >= STATS_INTERVAL_MS;
}

void PerfMonitor::markPrinted(unsigned long now) {
  lastPrintMs = now;
}

void PerfMonitor::toggleCsv(Stream& out) {
  csvMode = !csvMode;
  if (csvMode) {
    out.println(F("level,steps,score,length,state,food,collisions,bot_us,engine_us,render_us,avg_work_us,load_milli_pct,free_ram,min_free_ram"));
  } else {
    out.println(F("Textmodus aktiv"));
  }
}

void PerfMonitor::print(Stream& out, const GameEngine& engine, StepResult lastResult) {
  int currentRam = freeRam();
  if (currentRam < minFreeRam) minFreeRam = currentRam;
  if (csvMode) {
    printCsv(out, engine, lastResult, currentRam);
  } else {
    printHuman(out, engine, lastResult, currentRam);
  }
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

uint32_t PerfMonitor::averageWorkUs() const {
  return stepCount == 0 ? 0 : totalWorkUs / stepCount;
}

uint32_t PerfMonitor::loadMilliPercent() const {
  uint32_t workUs = lastBotUs + lastEngineUs + lastRenderUs;
  return (workUs * 100000UL) / (STEP_DELAY_MS * 1000UL);
}

void PerfMonitor::printHuman(Stream& out, const GameEngine& engine, StepResult lastResult, int currentRam) const {
  uint32_t load = loadMilliPercent();
  out.print(F("level=")); out.print(engine.level());
  out.print(F(" steps=")); out.print(stepCount);
  out.print(F(" score=")); out.print(engine.score());
  out.print(F(" len=")); out.print(engine.length());
  out.print(F(" state=")); out.print(resultName(lastResult));
  out.print(F(" food=")); out.print(foodCount);
  out.print(F(" collisions=")); out.print(collisionCount);
  out.print(F(" bot_us=")); out.print(lastBotUs);
  out.print(F(" engine_us=")); out.print(lastEngineUs);
  out.print(F(" render_us=")); out.print(lastRenderUs);
  out.print(F(" max_bot_us=")); out.print(maxBotUs);
  out.print(F(" max_engine_us=")); out.print(maxEngineUs);
  out.print(F(" max_render_us=")); out.print(maxRenderUs);
  out.print(F(" avg_work_us=")); out.print(averageWorkUs());
  out.print(F(" load_pct=")); out.print(load / 1000); out.print('.');
  uint16_t fraction = load % 1000;
  if (fraction < 100) out.print('0');
  if (fraction < 10) out.print('0');
  out.print(fraction);
  out.print(F(" free_ram=")); out.print(currentRam);
  out.print(F(" min_free_ram=")); out.println(minFreeRam);
}

void PerfMonitor::printCsv(Stream& out, const GameEngine& engine, StepResult lastResult, int currentRam) const {
  out.print(engine.level()); out.print(',');
  out.print(stepCount); out.print(',');
  out.print(engine.score()); out.print(',');
  out.print(engine.length()); out.print(',');
  out.print(resultName(lastResult)); out.print(',');
  out.print(foodCount); out.print(',');
  out.print(collisionCount); out.print(',');
  out.print(lastBotUs); out.print(',');
  out.print(lastEngineUs); out.print(',');
  out.print(lastRenderUs); out.print(',');
  out.print(averageWorkUs()); out.print(',');
  out.print(loadMilliPercent()); out.print(',');
  out.print(currentRam); out.print(',');
  out.println(minFreeRam);
}

const __FlashStringHelper* PerfMonitor::resultName(StepResult result) const {
  switch (result) {
    case STEP_OK: return F("ok");
    case STEP_ATE_FOOD: return F("food");
    case STEP_WALL_COLLISION: return F("wall");
    case STEP_SELF_COLLISION: return F("self");
    case STEP_OBSTACLE_COLLISION: return F("obstacle");
    default: return F("unknown");
  }
}
