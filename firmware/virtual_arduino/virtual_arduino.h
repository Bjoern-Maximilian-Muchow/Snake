#ifndef AUTOSNAKE_VIRTUAL_ARDUINO_H
#define AUTOSNAKE_VIRTUAL_ARDUINO_H

#include <chrono>
#include <cstring>
#include <ctime>
#include <cstdint>
#include <iostream>
#include <thread>
#ifdef _WIN32
#include <windows.h>
#include <psapi.h>
#else
#include <fstream>
#endif

using std::uint8_t;
using std::uint16_t;
using std::uint32_t;

struct __FlashStringHelper {
};

#define F(text) (reinterpret_cast<const __FlashStringHelper*>(text))

constexpr uint8_t HIGH = 1;
constexpr uint8_t LOW = 0;
constexpr uint8_t OUTPUT = 1;
constexpr uint8_t LED_BUILTIN = 13;
#define _BV(bit) (static_cast<unsigned int>(1U) << (bit))
constexpr uint16_t VIRTUAL_RAM_BASE_USED = 770;
constexpr uint16_t VIRTUAL_RAM_TOTAL = 2048;
constexpr uint32_t VIRTUAL_BOT_TIME_LIMIT_US = 3000;

template <typename T, typename Lower, typename Upper>
T constrain(T value, Lower lower, Upper upper) {
  return value < lower ? static_cast<T>(lower) : value > upper ? static_cast<T>(upper) : value;
}

class Stream {
public:
  void begin(uint32_t) {}

  int available() {
    return std::cin.rdbuf()->in_avail();
  }

  char read() {
    char value = 0;
    std::cin.get(value);
    return value;
  }

  void print(const __FlashStringHelper* value) {
    std::cout << reinterpret_cast<const char*>(value);
  }
  void print(const char* value) { std::cout << value; }
  void print(char value) { std::cout << value; }
  void print(int value) { std::cout << value; }
  void print(unsigned int value) { std::cout << value; }
  void print(unsigned long value) { std::cout << value; }

  void println() { std::cout << '\n'; }
  void println(const __FlashStringHelper* value) { print(value); println(); }
  void println(const char* value) { print(value); println(); }
  void println(int value) { print(value); println(); }
  void println(unsigned int value) { print(value); println(); }
  void println(unsigned long value) { print(value); println(); }
};

using HardwareSerial = Stream;
inline HardwareSerial Serial;

inline uint8_t (&virtualPins())[20] {
  static uint8_t pins[20] = {};
  return pins;
}

inline uint32_t& virtualClockMs() {
  static uint32_t value = 0;
  return value;
}

inline unsigned long millis() {
  return virtualClockMs();
}

inline std::chrono::steady_clock::time_point& virtualStartTime() {
  static const auto value = std::chrono::steady_clock::now();
  static auto start = value;
  return start;
}

inline uint32_t micros() {
  const auto elapsed = std::chrono::steady_clock::now() - virtualStartTime();
  return static_cast<uint32_t>(std::chrono::duration_cast<std::chrono::microseconds>(elapsed).count());
}

inline void delay(unsigned long milliseconds) {
  virtualClockMs() += static_cast<uint32_t>(milliseconds);
  std::this_thread::sleep_for(std::chrono::milliseconds(milliseconds));
}

inline void pinMode(uint8_t, uint8_t) {}
inline void digitalWrite(uint8_t pin, uint8_t value) {
  if (pin < 20) virtualPins()[pin] = value;
}

struct VirtualPixel {
  uint8_t r;
  uint8_t g;
  uint8_t b;
};

inline VirtualPixel (&virtualFrame())[16][16] {
  static VirtualPixel frame[16][16] = {};
  return frame;
}

inline void virtualLedGridClear();

inline void virtualLedGridBegin() {
  virtualLedGridClear();
}

inline void virtualLedGridClear() {
  for (auto& row : virtualFrame()) {
    for (auto& pixel : row) pixel = {0, 0, 0};
  }
}

inline void virtualLedGridSetPixel(uint8_t x, uint8_t y, uint8_t r, uint8_t g, uint8_t b) {
  if (x < 16 && y < 16) virtualFrame()[y][x] = {r, g, b};
}

inline uint32_t& virtualFrameNumber() {
  static uint32_t value = 0;
  return value;
}

inline bool& virtualBudgetFailed() {
  static bool failed = false;
  return failed;
}

inline uint64_t virtualHostRamBytes() {
#ifdef _WIN32
  PROCESS_MEMORY_COUNTERS counters = {};
  GetProcessMemoryInfo(GetCurrentProcess(), &counters, sizeof(counters));
  return static_cast<uint64_t>(counters.WorkingSetSize);
#else
  std::ifstream statm("/proc/self/statm");
  uint64_t pages = 0;
  statm >> pages >> pages;
  return pages * 4096ULL;
#endif
}

inline uint64_t virtualHostRamTotalBytes() {
#ifdef _WIN32
  MEMORYSTATUSEX status = {};
  status.dwLength = sizeof(status);
  GlobalMemoryStatusEx(&status);
  return static_cast<uint64_t>(status.ullTotalPhys);
#else
  return 0;
#endif
}

inline uint64_t virtualHostCpuTicks() {
#ifdef _WIN32
  FILETIME creation = {}, exit = {}, kernel = {}, user = {};
  GetProcessTimes(GetCurrentProcess(), &creation, &exit, &kernel, &user);
  ULARGE_INTEGER kernelTicks = {}, userTicks = {};
  kernelTicks.LowPart = kernel.dwLowDateTime;
  kernelTicks.HighPart = kernel.dwHighDateTime;
  userTicks.LowPart = user.dwLowDateTime;
  userTicks.HighPart = user.dwHighDateTime;
  return kernelTicks.QuadPart + userTicks.QuadPart;
#else
  return static_cast<uint64_t>(std::clock());
#endif
}

inline double virtualCpuSeconds(uint64_t ticks) {
#ifdef _WIN32
  return static_cast<double>(ticks) / 10000000.0;
#else
  return static_cast<double>(ticks) / CLOCKS_PER_SEC;
#endif
}

inline void virtualLedGridPresent() {
  std::cerr << "FRAME " << ++virtualFrameNumber() << '\n';
  for (const auto& row : virtualFrame()) {
    for (const auto& pixel : row) {
      std::cerr << (pixel.r > 200 ? 'F' : pixel.g > 200 ? 'H' : pixel.g > 0 ? 'S' : '.');
    }
    std::cerr << '\n';
  }
}

inline void virtualMonitorEmit(uint8_t level, uint16_t score, uint16_t length,
                               uint32_t botUs, uint32_t engineUs, uint32_t renderUs,
                               int state) {
  static uint16_t steps = 0;
  static uint64_t lastCpu = virtualHostCpuTicks();
  static const auto monitorStart = std::chrono::steady_clock::now();
  static auto lastWall = monitorStart;
  const auto now = std::chrono::steady_clock::now();
  const auto wallUs = std::chrono::duration_cast<std::chrono::microseconds>(now - lastWall).count();
  const uint64_t cpuTicks = virtualHostCpuTicks();
  const double cpuPercent = wallUs > 0
    ? virtualCpuSeconds(cpuTicks - lastCpu) / (wallUs / 1000000.0) * 100.0
    : 0.0;
  lastCpu = cpuTicks;
  lastWall = now;
  const uint64_t hostRamBytes = virtualHostRamBytes();
  const uint64_t hostRamTotalBytes = virtualHostRamTotalBytes();
  const bool botWithinBudget = botUs <= VIRTUAL_BOT_TIME_LIMIT_US;
  if (!botWithinBudget) virtualBudgetFailed() = true;
  std::cout << "AUTOSNAKE_MONITOR {\"frame\":" << virtualFrameNumber()
            << ",\"level\":" << static_cast<unsigned int>(level)
            << ",\"score\":" << score
            << ",\"length\":" << length
            << ",\"steps\":" << ++steps
            << ",\"state\":" << state
            << ",\"cpu_percent\":" << cpuPercent
            << ",\"bot_us\":" << botUs
            << ",\"bot_budget_us\":" << VIRTUAL_BOT_TIME_LIMIT_US
            << ",\"budget_ok\":" << (botWithinBudget ? "true" : "false")
            << ",\"ram_bytes\":" << hostRamBytes
            << ",\"ram_total_bytes\":" << hostRamTotalBytes
            << ",\"arduino_ram_used\":" << (VIRTUAL_RAM_BASE_USED + length * 4 + level * 8)
            << ",\"arduino_ram_total\":" << VIRTUAL_RAM_TOTAL
            << ",\"pins\":{\"D9\":0,\"D13\":" << static_cast<unsigned int>(virtualPins()[LED_BUILTIN])
            << "},\"grid\":[";
  for (uint8_t y = 0; y < 16; ++y) {
    if (y > 0) std::cout << ',';
    std::cout << '"';
    for (uint8_t x = 0; x < 16; ++x) {
      const VirtualPixel& pixel = virtualFrame()[y][x];
      std::cout << (pixel.r > 200 ? 'F' : pixel.g > 200 ? 'H' : pixel.g > 0 ? 'S' : '.');
    }
    std::cout << '"';
  }
  std::cout << "]}\n" << std::flush;
}

#endif