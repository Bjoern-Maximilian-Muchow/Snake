const size = 16;
const grid = document.querySelector("#grid");
const scoreEl = document.querySelector("#score");
const statusEl = document.querySelector("#status");
const resetBtn = document.querySelector("#reset");

let state;

function reset() {
  state = {
    snake: [
      { x: 8, y: 8 },
      { x: 7, y: 8 },
      { x: 6, y: 8 },
    ],
    food: { x: 12, y: 8 },
    direction: "right",
    score: 0,
    over: false,
  };
  render();
}

function basicBot() {
  const head = state.snake[0];
  if (state.food.x > head.x && state.direction !== "left") return "right";
  if (state.food.x < head.x && state.direction !== "right") return "left";
  if (state.food.y > head.y && state.direction !== "up") return "down";
  if (state.food.y < head.y && state.direction !== "down") return "up";
  return state.direction;
}

function nextHead(direction) {
  const head = state.snake[0];
  const next = { ...head };
  if (direction === "up") next.y -= 1;
  if (direction === "down") next.y += 1;
  if (direction === "left") next.x -= 1;
  if (direction === "right") next.x += 1;
  return next;
}

function contains(point) {
  return state.snake.some((part) => part.x === point.x && part.y === point.y);
}

function placeFood() {
  for (let y = 0; y < size; y += 1) {
    for (let x = 0; x < size; x += 1) {
      const candidate = { x, y };
      if (!contains(candidate)) {
        state.food = candidate;
        return;
      }
    }
  }
}

function step() {
  if (state.over) return;
  const move = basicBot();
  state.direction = move;
  const head = nextHead(move);

  if (head.x < 0 || head.y < 0 || head.x >= size || head.y >= size || contains(head)) {
    state.over = true;
    render();
    return;
  }

  state.snake.unshift(head);
  if (head.x === state.food.x && head.y === state.food.y) {
    state.score += 1;
    placeFood();
  } else {
    state.snake.pop();
  }
  render();
}

function render() {
  grid.innerHTML = "";
  for (let y = 0; y < size; y += 1) {
    for (let x = 0; x < size; x += 1) {
      const cell = document.createElement("div");
      cell.className = "cell";
      const index = state.snake.findIndex((part) => part.x === x && part.y === y);
      if (index === 0) cell.classList.add("head");
      if (index > 0) cell.classList.add("snake");
      if (state.food.x === x && state.food.y === y) cell.classList.add("food");
      grid.appendChild(cell);
    }
  }
  scoreEl.textContent = String(state.score);
  statusEl.textContent = state.over ? "Game over" : "Running";
}

resetBtn.addEventListener("click", reset);
reset();
setInterval(step, 180);
