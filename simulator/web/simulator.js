const size = 16;
const stepMs = 180;
const directions = ["up", "right", "down", "left"];
const deltas = {
  up: { x: 0, y: -1 }, right: { x: 1, y: 0 },
  down: { x: 0, y: 1 }, left: { x: -1, y: 0 },
};
const opposites = { up: "down", down: "up", left: "right", right: "left" };
const moveNames = { up: "hoch", right: "rechts", down: "runter", left: "links" };
const levelTasks = {
  1: {
    demo: ["Level 1 beobachten", "Verfolge, wie einfache Prioritätsregeln das Futter ansteuern.", "Der Regelbot kennt noch keine vollständige Sicherheitsanalyse."],
    assignment: ["Eigene Regeln bauen", "Ordne Bedingungen und Aktionen. Die erste passende Regel bestimmt den nächsten Zug.", "Deine Regelblöcke steuern die Snake direkt im Browser."],
    challenge: ["Drei Futterstücke erreichen", "Deine selbst gebauten Regeln müssen auf einer unbekannten Karte drei Futterstücke erreichen.", "Nur deine Blockregeln werden ausgeführt."],
  },
  2: {
    demo: ["Level 2 beobachten", "Vergleiche direkte und sichere Züge auf einem Feld mit Hindernissen.", "Der sichere Bot prüft Wand, Körper und Hindernisse."],
    assignment: ["Sichere Züge in Python", "Implementiere die vorbereiteten Funktionen in learning/level2/student_bot.py.", "Die Ausführung erfolgt durch pytest; der Browser zeigt das Szenario."],
    challenge: ["50 Schritte sicher überleben", "Dein Python-Bot muss unbekannte Hindernisse berücksichtigen.", "Die Challenge wird mit den Level-2-Tests bewertet."],
  },
  3: {
    demo: ["Level 3 beobachten", "Beobachte Pfadsuche, Fallback und Hindernisse unter einem Zeitlimit.", "Der Referenzbot dient nur als Benchmark."],
    assignment: ["Embedded Bot entwickeln", "Implementiere chooseStudentMove in learning/level3/student_bot.h.", "Build, Telemetrie und Hardwaremessung bewerten deine Lösung."],
    challenge: ["Robust unter 3 ms", "Der C++-Bot soll Futter erreichen, Fallen vermeiden und das Zeitbudget einhalten.", "Die Challenge läuft über PlatformIO und die Uno-Telemetrie."],
  },
};

const grid = document.querySelector("#grid");
const currentLevelEl = document.querySelector("#current-level");
const scoreEl = document.querySelector("#score");
const lengthEl = document.querySelector("#length");
const stepsEl = document.querySelector("#steps");
const statusEl = document.querySelector("#status");
const lastMoveEl = document.querySelector("#last-move");
const resetBtn = document.querySelector("#reset");
const toggleBtn = document.querySelector("#toggle");
const stepBtn = document.querySelector("#step");
const levelSelect = document.querySelector("#level");
const levelField = document.querySelector("#level-field");
const lockedLevelTitle = document.querySelector("#locked-level-title");
const botSelect = document.querySelector("#bot");
const demoBotField = document.querySelector("#demo-bot-field");
const taskTitle = document.querySelector("#task-title");
const taskText = document.querySelector("#task-text");
const botText = document.querySelector("#bot-text");
const modeLabel = document.querySelector("#mode-label");
const modeTabs = [...document.querySelectorAll(".mode-tab")];
const modePanels = {
  demo: document.querySelector("#demo-panel"),
  assignment: document.querySelector("#assignment-panel"),
  challenge: document.querySelector("#challenge-panel"),
};
const learningPanels = {
  1: document.querySelector("#level-1-builder"),
  2: document.querySelector("#level-2-work"),
  3: document.querySelector("#level-3-work"),
};
const challengeTitle = document.querySelector("#challenge-title");
const challengeText = document.querySelector("#challenge-text");
const challengeResult = document.querySelector("#challenge-result");

const blockEditor = new AutoSnakeBlockEditor({
  listElement: document.querySelector("#rule-list"),
  codeElement: document.querySelector("#generated-code"),
  feedbackElement: document.querySelector("#rule-feedback"),
});

let state;
let timerId;
let running = true;
let mode = "demo";
let customRulesApplied = false;
let lockedLevel = null;
let lockedMode = null;

function reset({ challenge = mode === "challenge" } = {}) {
  const level = Number(levelSelect.value);
  state = {
    level,
    snake: [{ x: 8, y: 8 }, { x: 7, y: 8 }, { x: 6, y: 8 }],
    food: challenge ? challengeFood(level) : { x: 12, y: 8 },
    obstacles: challenge ? challengeObstacles(level) : buildObstacles(level),
    direction: "right",
    score: 0,
    steps: 0,
    over: false,
    status: mode !== "demo"
      ? level > 1
        ? "Szenarioansicht"
        : customRulesApplied
          ? "Läuft"
          : "Regeln bauen"
      : "Läuft",
    lastMove: "right",
  };
  if (isBlocked(state.food)) placeFood();
  challengeResult.classList.remove("success");
  challengeResult.textContent = mode === "challenge" ? "Noch nicht abgeschlossen." : "";
  updateTask();
  render();
}

function buildObstacles(level) {
  if (level < 2) return [];
  const base = [{ x: 5, y: 4 }, { x: 5, y: 5 }, { x: 5, y: 6 }, { x: 10, y: 9 }, { x: 11, y: 9 }, { x: 12, y: 9 }];
  return level === 2 ? base : [...base, { x: 3, y: 11 }, { x: 4, y: 11 }, { x: 5, y: 11 }, { x: 9, y: 3 }, { x: 9, y: 4 }];
}

function challengeObstacles(level) {
  if (level === 1) return [];
  if (level === 2) return [{ x: 4, y: 5 }, { x: 5, y: 5 }, { x: 6, y: 5 }, { x: 10, y: 8 }, { x: 10, y: 9 }, { x: 10, y: 10 }];
  return [{ x: 4, y: 4 }, { x: 5, y: 4 }, { x: 6, y: 4 }, { x: 6, y: 5 }, { x: 6, y: 6 }, { x: 9, y: 9 }, { x: 10, y: 9 }, { x: 11, y: 9 }];
}

function challengeFood(level) {
  return level === 1 ? { x: 14, y: 8 } : level === 2 ? { x: 12, y: 6 } : { x: 13, y: 10 };
}

function basicBot() {
  const head = state.snake[0];
  const preferred = [];
  if (state.food.x > head.x) preferred.push("right");
  if (state.food.x < head.x) preferred.push("left");
  if (state.food.y > head.y) preferred.push("down");
  if (state.food.y < head.y) preferred.push("up");
  preferred.push(state.direction);
  return preferred.find((move) => move !== opposites[state.direction]) || state.direction;
}

function safeBot() {
  return foodFirstMoves().find((move) => isSafeMove(move)) || state.direction;
}

function bfsBot() {
  const start = state.snake[0];
  const blocked = new Set([...state.snake.slice(0, -1), ...state.obstacles].map(keyOf));
  const queue = [{ point: start, path: [] }];
  const seen = new Set([keyOf(start)]);
  const startedAt = performance.now();
  while (queue.length > 0 && performance.now() - startedAt < 3) {
    const current = queue.shift();
    if (samePoint(current.point, state.food) && current.path.length > 0) return current.path[0];
    for (const move of directions) {
      if (current.path.length === 0 && move === opposites[state.direction]) continue;
      const next = movePoint(current.point, move);
      const key = keyOf(next);
      if (inside(next) && !blocked.has(key) && !seen.has(key)) {
        seen.add(key);
        queue.push({ point: next, path: [...current.path, move] });
      }
    }
  }
  return safeBot();
}

function customBlockBot() {
  return blockEditor.chooseMove({
    head: state.snake[0], food: state.food, direction: state.direction,
    blocked: (point) => !inside(point) || isBlocked(point),
    next: movePoint,
  });
}

function chooseMove() {
  if (mode === "assignment" || mode === "challenge") {
    if (state.level === 1 && customRulesApplied) return customBlockBot();
    if (state.level === 1) return state.direction;
    if (state.level > 1) return state.direction;
  }
  if (botSelect.value === "safe") return safeBot();
  if (botSelect.value === "bfs") return bfsBot();
  return basicBot();
}

function step() {
  if (state.over || (mode !== "demo" && state.level > 1)) return;
  const move = chooseMove();
  if (move !== opposites[state.direction]) state.direction = move;
  state.lastMove = state.direction;
  state.steps += 1;
  const head = movePoint(state.snake[0], state.direction);
  if (!inside(head)) return finish("Wandkollision");
  if (containsObstacle(head)) return finish("Hinderniskollision");
  const willGrow = samePoint(head, state.food);
  const body = willGrow ? state.snake : state.snake.slice(0, -1);
  if (body.some((part) => samePoint(part, head))) return finish("Selbstkollision");
  state.snake.unshift(head);
  if (willGrow) {
    state.score += 1;
    state.status = "Futter gegessen";
    placeFood();
  } else {
    state.snake.pop();
    state.status = "Läuft";
  }
  evaluateChallenge();
  render();
}

function finish(message) {
  state.over = true;
  state.status = message;
  running = false;
  syncTimer();
  if (mode === "challenge") challengeResult.textContent = `Nicht geschafft: ${message} nach ${state.steps} Schritten.`;
  render();
}

function evaluateChallenge() {
  if (mode !== "challenge") return;
  const success = state.level === 1 ? state.score >= 3 : state.level === 2 ? state.steps >= 50 : state.score >= 3;
  if (success) {
    running = false;
    syncTimer();
    challengeResult.textContent = `Geschafft: ${state.score} Futterstücke in ${state.steps} Schritten.`;
    challengeResult.classList.add("success");
  }
}

function foodFirstMoves() {
  const head = state.snake[0];
  const moves = [];
  if (state.food.x > head.x) moves.push("right");
  if (state.food.x < head.x) moves.push("left");
  if (state.food.y > head.y) moves.push("down");
  if (state.food.y < head.y) moves.push("up");
  return [...new Set([...moves, ...directions])];
}

function isSafeMove(move) {
  if (move === opposites[state.direction]) return false;
  const next = movePoint(state.snake[0], move);
  return inside(next) && !containsObstacle(next) && !state.snake.slice(0, -1).some((part) => samePoint(part, next));
}

function movePoint(point, direction) {
  const delta = deltas[direction];
  return { x: point.x + delta.x, y: point.y + delta.y };
}

function inside(point) { return point.x >= 0 && point.y >= 0 && point.x < size && point.y < size; }
function containsObstacle(point) { return state.obstacles.some((obstacle) => samePoint(obstacle, point)); }
function isBlocked(point) { return state.snake.some((part) => samePoint(part, point)) || containsObstacle(point); }
function samePoint(a, b) { return a.x === b.x && a.y === b.y; }
function keyOf(point) { return `${point.x},${point.y}`; }

function placeFood() {
  for (let y = 0; y < size; y += 1) {
    for (let x = 0; x < size; x += 1) {
      const candidate = { x, y };
      if (!isBlocked(candidate)) { state.food = candidate; return; }
    }
  }
}

function render() {
  grid.innerHTML = "";
  for (let y = 0; y < size; y += 1) {
    for (let x = 0; x < size; x += 1) {
      const point = { x, y };
      const cell = document.createElement("div");
      cell.className = "cell";
      const index = state.snake.findIndex((part) => samePoint(part, point));
      if (containsObstacle(point)) cell.classList.add("obstacle");
      if (samePoint(state.food, point)) cell.classList.add("food");
      if (index > 0) cell.classList.add("snake");
      if (index === 0) cell.classList.add("head");
      grid.appendChild(cell);
    }
  }
  currentLevelEl.textContent = String(state.level);
  scoreEl.textContent = String(state.score);
  lengthEl.textContent = String(state.snake.length);
  stepsEl.textContent = String(state.steps);
  statusEl.textContent = state.status;
  lastMoveEl.textContent = moveNames[state.lastMove];
  toggleBtn.textContent = running ? "Pause" : "Start";
  const learnerExecutionUnavailable = mode !== "demo" && (state.level > 1 || !customRulesApplied);
  toggleBtn.disabled = learnerExecutionUnavailable;
  stepBtn.disabled = learnerExecutionUnavailable;
}

function updateTask() {
  const [title, text, bot] = levelTasks[state.level][mode];
  modeLabel.textContent = mode === "demo" ? "Demo" : mode === "assignment" ? "Aufgabe" : "Challenge";
  taskTitle.textContent = title;
  taskText.textContent = text;
  botText.textContent = bot;
  challengeTitle.textContent = levelTasks[state.level].challenge[0];
  challengeText.textContent = levelTasks[state.level].challenge[1];
}

function setMode(nextMode) {
  mode = lockedMode || nextMode;
  modeTabs.forEach((tab) => tab.classList.toggle("active", tab.dataset.mode === mode));
  Object.entries(modePanels).forEach(([name, panel]) => panel.classList.toggle("hidden", name !== mode));
  demoBotField.classList.toggle("hidden", mode !== "demo");
  updateLearningPanel();
  running = mode === "demo" || (state?.level === 1 && customRulesApplied);
  reset();
  syncTimer();
}

function updateLearningPanel() {
  const level = Number(levelSelect.value);
  Object.entries(learningPanels).forEach(([number, panel]) => panel.classList.toggle("hidden", Number(number) !== level));
}

function syncTimer() {
  if (timerId) clearInterval(timerId);
  timerId = running ? setInterval(step, stepMs) : undefined;
}

toggleBtn.addEventListener("click", () => { running = !running; syncTimer(); render(); });
stepBtn.addEventListener("click", () => { running = false; syncTimer(); step(); });
resetBtn.addEventListener("click", () => { running = mode === "demo" || (state.level === 1 && customRulesApplied); reset(); syncTimer(); });
levelSelect.addEventListener("change", () => {
  if (lockedLevel !== null) {
    levelSelect.value = String(lockedLevel);
    return;
  }
  botSelect.value = Number(levelSelect.value) === 1 ? "basic" : Number(levelSelect.value) === 2 ? "safe" : "bfs";
  updateLearningPanel();
  setMode(mode);
});
botSelect.addEventListener("change", () => { reset(); });
modeTabs.forEach((tab) => tab.addEventListener("click", () => setMode(tab.dataset.mode)));
document.querySelector("#add-rule").addEventListener("click", () => blockEditor.addRule());
document.querySelector("#restore-rules").addEventListener("click", () => { blockEditor.restore(); customRulesApplied = false; running = false; reset(); syncTimer(); });
document.querySelector("#apply-rules").addEventListener("click", () => {
  customRulesApplied = true;
  running = true;
  reset();
  syncTimer();
});
document.querySelector("#load-challenge").addEventListener("click", () => {
  running = state.level === 1 && customRulesApplied;
  reset({ challenge: true });
  if (state.level === 1 && !customRulesApplied) challengeResult.textContent = "Aktiviere zuerst deine eigenen Regeln im Aufgabenmodus.";
  syncTimer();
});

const startup = new URLSearchParams(window.location.search);
const startupLevel = Number(startup.get("level"));
const requestedLockedLevel = Number(startup.get("lockLevel"));
const startupMode = startup.get("mode");
const requestedLockedMode = startup.get("lockMode");
if ([1, 2, 3].includes(requestedLockedLevel)) lockedLevel = requestedLockedLevel;
if (lockedLevel !== null) {
  levelSelect.value = String(lockedLevel);
  levelField.classList.add("hidden");
  lockedLevelTitle.textContent = `Level ${lockedLevel}`;
  lockedLevelTitle.classList.remove("hidden");
}
if (["demo", "assignment", "challenge"].includes(requestedLockedMode)) lockedMode = requestedLockedMode;
if (lockedMode !== null) document.querySelector(".mode-tabs").classList.add("hidden");
if ([1, 2, 3].includes(startupLevel)) levelSelect.value = String(startupLevel);
if (lockedLevel !== null) levelSelect.value = String(lockedLevel);
if (["demo", "assignment", "challenge"].includes(startupMode)) mode = startupMode;
if (lockedMode !== null) mode = lockedMode;
updateLearningPanel();
setMode(mode);
