const size = 16;
const stepMs = 180;
const directions = ["up", "right", "down", "left"];
const deltas = {
  up: { x: 0, y: -1 },
  right: { x: 1, y: 0 },
  down: { x: 0, y: 1 },
  left: { x: -1, y: 0 },
};
const opposites = {
  up: "down",
  down: "up",
  left: "right",
  right: "left",
};
const moveNames = {
  up: "hoch",
  right: "rechts",
  down: "runter",
  left: "links",
};
const tasks = {
  1: {
    title: "Level 1: Schüler",
    text: "Nutze einfache Regeln, um das Futter grob anzusteuern und Wände zu vermeiden.",
  },
  2: {
    title: "Level 2: Student Anfang Studium",
    text: "Berücksichtige Hindernisse, prüfe sichere Züge und trenne Analyse von Entscheidung.",
  },
  3: {
    title: "Level 3: Fortgeschrittener Student",
    text: "Nutze Pfadsuche mit Sicherheitsprüfung und begrenzter Rechenzeit.",
  },
};

const grid = document.querySelector("#grid");
const scoreEl = document.querySelector("#score");
const lengthEl = document.querySelector("#length");
const statusEl = document.querySelector("#status");
const lastMoveEl = document.querySelector("#last-move");
const resetBtn = document.querySelector("#reset");
const toggleBtn = document.querySelector("#toggle");
const stepBtn = document.querySelector("#step");
const levelSelect = document.querySelector("#level");
const botSelect = document.querySelector("#bot");
const taskTitle = document.querySelector("#task-title");
const taskText = document.querySelector("#task-text");

let state;
let timerId;
let running = true;

function reset() {
  const level = Number(levelSelect.value);
  state = {
    level,
    snake: [
      { x: 8, y: 8 },
      { x: 7, y: 8 },
      { x: 6, y: 8 },
    ],
    food: { x: 12, y: 8 },
    obstacles: level >= 2 ? buildObstacles(level) : [],
    direction: "right",
    score: 0,
    over: false,
    status: "Läuft",
    lastMove: "right",
  };
  if (isBlocked(state.food)) {
    placeFood();
  }
  updateTask();
  render();
}

function buildObstacles(level) {
  const base = [
    { x: 5, y: 4 },
    { x: 5, y: 5 },
    { x: 5, y: 6 },
    { x: 10, y: 9 },
    { x: 11, y: 9 },
    { x: 12, y: 9 },
  ];
  if (level === 2) return base;
  return [
    ...base,
    { x: 3, y: 11 },
    { x: 4, y: 11 },
    { x: 5, y: 11 },
    { x: 9, y: 3 },
    { x: 9, y: 4 },
  ];
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
  const preferred = foodFirstMoves();
  return preferred.find((move) => isSafeMove(move)) || state.direction;
}

function bfsBot() {
  const start = state.snake[0];
  const blocked = new Set([...state.snake.slice(0, -1), ...state.obstacles].map(keyOf));
  const queue = [{ point: start, path: [] }];
  const seen = new Set([keyOf(start)]);
  const startedAt = performance.now();

  while (queue.length > 0 && performance.now() - startedAt < 5) {
    const current = queue.shift();
    if (samePoint(current.point, state.food) && current.path.length > 0) {
      return current.path[0];
    }

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

function chooseMove() {
  if (botSelect.value === "safe") return safeBot();
  if (botSelect.value === "bfs") return bfsBot();
  return basicBot();
}

function step() {
  if (state.over) return;
  const move = chooseMove();
  if (move !== opposites[state.direction]) {
    state.direction = move;
  }
  state.lastMove = state.direction;

  const head = movePoint(state.snake[0], state.direction);
  if (!inside(head)) {
    finish("Wandkollision");
    return;
  }
  if (containsObstacle(head)) {
    finish("Hinderniskollision");
    return;
  }

  const willGrow = samePoint(head, state.food);
  const body = willGrow ? state.snake : state.snake.slice(0, -1);
  if (body.some((part) => samePoint(part, head))) {
    finish("Selbstkollision");
    return;
  }

  state.snake.unshift(head);
  if (willGrow) {
    state.score += 1;
    state.status = "Futter gegessen";
    placeFood();
  } else {
    state.snake.pop();
    state.status = "Läuft";
  }
  render();
}

function finish(message) {
  state.over = true;
  state.status = message;
  running = false;
  syncTimer();
  render();
}

function foodFirstMoves() {
  const head = state.snake[0];
  const moves = [];
  if (state.food.x > head.x) moves.push("right");
  if (state.food.x < head.x) moves.push("left");
  if (state.food.y > head.y) moves.push("down");
  if (state.food.y < head.y) moves.push("up");
  return [...new Set([...moves, "up", "right", "down", "left"])];
}

function isSafeMove(move) {
  if (move === opposites[state.direction]) return false;
  const next = movePoint(state.snake[0], move);
  const bodyWithoutTail = state.snake.slice(0, -1);
  return inside(next) && !containsObstacle(next) && !bodyWithoutTail.some((part) => samePoint(part, next));
}

function movePoint(point, direction) {
  const delta = deltas[direction];
  return { x: point.x + delta.x, y: point.y + delta.y };
}

function inside(point) {
  return point.x >= 0 && point.y >= 0 && point.x < size && point.y < size;
}

function containsObstacle(point) {
  return state.obstacles.some((obstacle) => samePoint(obstacle, point));
}

function isBlocked(point) {
  return state.snake.some((part) => samePoint(part, point)) || containsObstacle(point);
}

function placeFood() {
  for (let y = 0; y < size; y += 1) {
    for (let x = 0; x < size; x += 1) {
      const candidate = { x, y };
      if (!isBlocked(candidate)) {
        state.food = candidate;
        return;
      }
    }
  }
}

function samePoint(a, b) {
  return a.x === b.x && a.y === b.y;
}

function keyOf(point) {
  return `${point.x},${point.y}`;
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
  scoreEl.textContent = String(state.score);
  lengthEl.textContent = String(state.snake.length);
  statusEl.textContent = state.status;
  lastMoveEl.textContent = moveNames[state.lastMove];
  toggleBtn.textContent = running ? "Pause" : "Start";
}

function updateTask() {
  const task = tasks[state.level];
  taskTitle.textContent = task.title;
  taskText.textContent = task.text;
}

function syncTimer() {
  if (timerId) {
    clearInterval(timerId);
    timerId = undefined;
  }
  if (running) {
    timerId = setInterval(step, stepMs);
  }
}

toggleBtn.addEventListener("click", () => {
  running = !running;
  syncTimer();
  render();
});

stepBtn.addEventListener("click", () => {
  running = false;
  syncTimer();
  step();
});

resetBtn.addEventListener("click", () => {
  running = true;
  reset();
  syncTimer();
});

levelSelect.addEventListener("change", () => {
  running = true;
  reset();
  syncTimer();
});

botSelect.addEventListener("change", render);

reset();
syncTimer();
