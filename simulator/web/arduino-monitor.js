const gridElement = document.querySelector("#led-grid");
const connectionStatus = document.querySelector("#connection-status");
const runState = document.querySelector("#run-state");
const frameLabel = document.querySelector("#frame-label");
const stopButton = document.querySelector("#stop-button");
const pinList = document.querySelector("#pin-list");
const pinNames = ["D9", "D13"];

function setText(selector, value) {
  document.querySelector(selector).textContent = String(value);
}

function renderGrid(rows) {
  gridElement.innerHTML = "";
  rows.forEach((row) => {
    [...row].forEach((cellValue) => {
      const cell = document.createElement("span");
      cell.className = `led-cell led-${cellValue}`;
      gridElement.appendChild(cell);
    });
  });
}

function renderPins(pins) {
  pinList.innerHTML = "";
  pinNames.forEach((pinName) => {
    const active = Boolean(pins[pinName]);
    const row = document.createElement("div");
    row.className = "pin-row";
    row.innerHTML = `<span class="pin-name">${pinName}</span><span class="pin-state ${active ? "active" : "low"}">${active ? "HIGH" : "LOW"}</span>`;
    pinList.appendChild(row);
  });
}

function renderMonitor(data) {
  renderGrid(data.grid);
  renderPins(data.pins);
  setText("#level", data.level);
  setText("#steps", data.steps);
  setText("#score", data.score);
  setText("#length", data.length);
  setText("#step-state", data.state);
  setText("#frame-label", `Frame ${data.frame}`);

  const cpuPercent = data.cpu_milli_percent / 1000;
  const ramPercent = (data.ram_used / data.ram_total) * 100;
  const flashPercent = (data.flash_used / data.flash_total) * 100;
  setText("#cpu-value", `${cpuPercent.toFixed(3)} %`);
  setText("#ram-value", `${data.ram_used} / ${data.ram_total} Byte (${ramPercent.toFixed(1)} %)`);
  setText("#flash-value", `${data.flash_used} / ${data.flash_total} Byte (${flashPercent.toFixed(1)} %)`);
  document.querySelector("#cpu-meter").style.width = `${Math.min(cpuPercent, 100)}%`;
  document.querySelector("#ram-meter").style.width = `${Math.min(ramPercent, 100)}%`;
  document.querySelector("#flash-meter").style.width = `${Math.min(flashPercent, 100)}%`;
  runState.textContent = "Läuft";
  runState.className = "state-badge running";
}

function handleLine(line) {
  if (line.startsWith("AUTOSNAKE_MONITOR ")) {
    try {
      renderMonitor(JSON.parse(line.slice("AUTOSNAKE_MONITOR ".length)));
    } catch (_error) {
      connectionStatus.textContent = "Ungültige Monitor-Nachricht erhalten";
    }
    return;
  }
  if (line.startsWith("AUTOSNAKE_STATUS beendet")) {
    runState.textContent = "Beendet";
    runState.className = "state-badge stopped";
  }
  if (line.startsWith("AUTOSNAKE_STATUS gestoppt")) {
    runState.textContent = "Gestoppt";
    runState.className = "state-badge stopped";
  }
}

const socket = io("/monitor");
socket.on("connect", () => {
  connectionStatus.textContent = "Mit der Station verbunden";
  runState.textContent = "Bereit";
});
socket.on("disconnect", () => {
  connectionStatus.textContent = "Verbindung zur Station verloren";
  runState.textContent = "Offline";
  runState.className = "state-badge stopped";
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
    runState.textContent = "Gestoppt";
    runState.className = "state-badge stopped";
    stopButton.textContent = "Simulation beendet";
  }
});

renderPins({ D9: 0, D13: 0 });
