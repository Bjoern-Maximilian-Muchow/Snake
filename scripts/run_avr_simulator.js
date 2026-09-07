const fs = require("fs");
const {
  CPU,
  avrInstruction,
  AVRIOPort,
  portBConfig,
  portCConfig,
  portDConfig,
  AVRUSART,
  usart0Config,
  AVRTimer,
  timer0Config,
  timer1Config,
  timer2Config,
} = require("avr8js");

function parseHex(text) {
  const bytes = new Uint8Array(0x8000);
  let upperAddress = 0;
  for (const line of text.split(/\r?\n/)) {
    if (!line.startsWith(":")) continue;
    const length = parseInt(line.slice(1, 3), 16);
    const address = parseInt(line.slice(3, 7), 16);
    const type = parseInt(line.slice(7, 9), 16);
    const data = line.slice(9, 9 + length * 2);
    if (type === 0) {
      for (let index = 0; index < length; index += 1) {
        const absolute = upperAddress + address + index;
        if (absolute < bytes.length) bytes[absolute] = parseInt(data.slice(index * 2, index * 2 + 2), 16);
      }
    } else if (type === 4) {
      upperAddress = parseInt(data, 16) << 16;
    }
  }
  const program = new Uint16Array(bytes.length / 2);
  for (let index = 0; index < program.length; index += 1) {
    program[index] = bytes[index * 2] | (bytes[index * 2 + 1] << 8);
  }
  return program;
}

const hexPath = process.argv[2];
const maxCycles = Number(process.argv[3] || 16_000_000);
if (!hexPath) throw new Error("Aufruf: node scripts/run_avr_simulator.js <firmware.hex> [maxCycles]");

const cpu = new CPU(parseHex(fs.readFileSync(hexPath, "utf8")), 2048);
new AVRIOPort(cpu, portBConfig);
new AVRIOPort(cpu, portCConfig);
new AVRIOPort(cpu, portDConfig);
const usart = new AVRUSART(cpu, usart0Config, 16_000_000);
usart.onByteTransmit = (value) => process.stdout.write(String.fromCharCode(value));
new AVRTimer(cpu, timer0Config);
new AVRTimer(cpu, timer1Config);
new AVRTimer(cpu, timer2Config);

let cycles = 0;
while (cycles < maxCycles) {
  avrInstruction(cpu);
  cycles += 1;
}
process.stderr.write(`AVR_SIM cycles=${cycles} sram=2048\n`);
