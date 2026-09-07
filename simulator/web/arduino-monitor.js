const gridElement = document.querySelector("#led-grid");
const connectionStatus = document.querySelector("#connection-status");
const frameLabel = document.querySelector("#frame-label");
const stopButton = document.querySelector("#stop-button");

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

function renderMonitor(data) {
  renderGrid(data.grid);
  setText("#frame-label", `Frame ${data.frame}`);

  const cpuPercent = data.cpu_percent;
  const ramPercent = data.ram_total_bytes > 0 ? (data.ram_bytes / data.ram_total_bytes) * 100 : 0;
  setText("#cpu-value", `${cpuPercent.toFixed(2)} % Laptop-Prozess`);
  setText("#ram-value", `${(data.ram_bytes / 1024 / 1024).toFixed(1)} MB / ${(data.ram_total_bytes / 1024 / 1024 / 1024).toFixed(1)} GB (${ramPercent.toFixed(2)} %)`);
  document.querySelector("#cpu-meter").style.width = `${Math.min(cpuPercent, 100)}%`;
  document.querySelector("#ram-meter").style.width = `${Math.min(ramPercent, 100)}%`;
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
