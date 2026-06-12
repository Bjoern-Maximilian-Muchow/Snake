const assert = require("node:assert");
const AutoSnakeBlockEditor = require("./block_editor.js");

function editorWith(rules) {
  const editor = Object.create(AutoSnakeBlockEditor.prototype);
  editor.rules = rules;
  return editor;
}

const context = {
  head: { x: 4, y: 4 },
  food: { x: 8, y: 4 },
  direction: "right",
  blocked: (point) => point.x === 5 && point.y === 4,
  next: (point, direction) => {
    const delta = { up: [0, -1], right: [1, 0], down: [0, 1], left: [-1, 0] }[direction];
    return { x: point.x + delta[0], y: point.y + delta[1] };
  },
};

assert.equal(
  editorWith([
    { condition: "front_blocked", action: "turn_left" },
    { condition: "always", action: "forward" },
  ]).chooseMove(context),
  "up",
);

assert.equal(
  editorWith([
    { condition: "food_right", action: "right" },
    { condition: "always", action: "forward" },
  ]).chooseMove({ ...context, blocked: () => false }),
  "right",
);

console.log("Blockeditor-Logik OK");
