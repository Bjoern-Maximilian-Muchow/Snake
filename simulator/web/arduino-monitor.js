const connectionStatus = document.querySelector("#connection-status");
const stopButton = document.querySelector("#stop-button");

function setText(selector, value) {
  document.querySelector(selector).textContent = String(value);
}

function renderMonitor(data) {
  const cpuPercent = Number(data.arduino_cpu_percent || 0);
  const arduinoRamPercent = (data.arduino_ram_used / data.arduino_ram_total) * 100;
  const flashPercent = (data.arduino_flash_used / data.arduino_flash_total) * 100;
  setText("#cpu-value", `${cpuPercent.toFixed(2)} % Intervallbudget`);
  setText("#ram-value", `${data.arduino_ram_used} / ${data.arduino_ram_total} Byte (${arduinoRamPercent.toFixed(1)} %)`);
  setText("#flash-value", `${data.arduino_flash_used} / ${data.arduino_flash_total} Byte (${flashPercent.toFixed(1)} %)`);
  document.querySelector("#cpu-meter").style.width = `${Math.min(cpuPercent, 100)}%`;
  document.querySelector("#ram-meter").style.width = `${Math.min(arduinoRamPercent, 100)}%`;
  document.querySelector("#flash-meter").style.width = `${Math.min(flashPercent, 100)}%`;
}

function handleLine(line) {
  if (line.startsWith("AUTOSNAKE_MONITOR ")) {
    try {
      renderMonitor(JSON.parse(line.slice("AUTOSNAKE_MONITOR ".length)));
    } catch (_error) {
      connectionStatus.textContent = "Ungültige Monitor-Nachricht erhalten";
    }
  }
}

const socket = io("/monitor");
socket.on("connect", () => {
  connectionStatus.textContent = "Mit der Station verbunden";
});
socket.on("disconnect", () => {
  connectionStatus.textContent = "Verbindung zur Station verloren";
});
socket.on("monitor-output", ({ output }) => {
  output.split(/\r?\n/).filter(Boolean).forEach(handleLine);
});

stopButton.addEventListener("click", async () => {
  stopButton.disabled = true;
  stopButton.textContent = "Wird beendet ...";
  try {
    await fetch("/virtual/stop", { method: "POST" });
  } finally {
    stopButton.textContent = "Simulation beendet";
  }
});
