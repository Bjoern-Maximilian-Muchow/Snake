class AutoSnakeBlockEditor {
  constructor({ listElement, codeElement, feedbackElement }) {
    this.listElement = listElement;
    this.codeElement = codeElement;
    this.feedbackElement = feedbackElement;
    this.conditions = {
      food_right: "Futter liegt rechts",
      food_left: "Futter liegt links",
      food_down: "Futter liegt unten",
      food_up: "Futter liegt oben",
      front_blocked: "Feld vorne ist blockiert",
      left_free: "Feld links ist frei",
      right_free: "Feld rechts ist frei",
      always: "Sonst",
    };
    this.actions = {
      right: "gehe rechts",
      left: "gehe links",
      down: "gehe runter",
      up: "gehe hoch",
      forward: "gehe vorwärts",
      turn_left: "biege links ab",
      turn_right: "biege rechts ab",
    };
    this.restore();
  }

  restore() {
    this.rules = [
      { condition: "front_blocked", action: "turn_left" },
      { condition: "food_right", action: "right" },
      { condition: "food_left", action: "left" },
      { condition: "food_down", action: "down" },
      { condition: "food_up", action: "up" },
      { condition: "always", action: "forward" },
    ];
    this.render();
  }

  addRule() {
    if (this.rules.length >= 8) return;
    this.rules.push({ condition: "always", action: "forward" });
    this.render();
  }

  moveRule(index, offset) {
    const target = index + offset;
    if (target < 0 || target >= this.rules.length) return;
    [this.rules[index], this.rules[target]] = [this.rules[target], this.rules[index]];
    this.render();
  }

  removeRule(index) {
    if (this.rules.length <= 1) return;
    this.rules.splice(index, 1);
    this.render();
  }

  render() {
    this.listElement.innerHTML = "";
    this.rules.forEach((rule, index) => {
      const block = document.createElement("div");
      block.className = "rule-block";
      block.innerHTML = `
        <span class="rule-index">${index + 1}</span>
        <select aria-label="Bedingung Regel ${index + 1}">${this.options(this.conditions, rule.condition)}</select>
        <span>dann</span>
        <select aria-label="Aktion Regel ${index + 1}">${this.options(this.actions, rule.action)}</select>
        <span class="rule-tools">
          <button class="icon-button" type="button" title="Regel nach oben" aria-label="Regel nach oben">↑</button>
          <button class="icon-button" type="button" title="Regel nach unten" aria-label="Regel nach unten">↓</button>
          <button class="icon-button" type="button" title="Regel entfernen" aria-label="Regel entfernen">×</button>
        </span>`;
      const selects = block.querySelectorAll("select");
      selects[0].addEventListener("change", (event) => {
        rule.condition = event.target.value;
        this.updateOutput();
      });
      selects[1].addEventListener("change", (event) => {
        rule.action = event.target.value;
        this.updateOutput();
      });
      const buttons = block.querySelectorAll("button");
      buttons[0].addEventListener("click", () => this.moveRule(index, -1));
      buttons[1].addEventListener("click", () => this.moveRule(index, 1));
      buttons[2].addEventListener("click", () => this.removeRule(index));
      this.listElement.appendChild(block);
    });
    this.updateOutput();
  }

  options(values, selected) {
    return Object.entries(values)
      .map(([value, label]) => `<option value="${value}"${value === selected ? " selected" : ""}>${label}</option>`)
      .join("");
  }

  chooseMove(context) {
    for (const rule of this.rules) {
      if (this.matches(rule.condition, context)) {
        return this.resolveAction(rule.action, context.direction);
      }
    }
    return context.direction;
  }

  matches(condition, context) {
    const head = context.head;
    if (condition === "food_right") return context.food.x > head.x;
    if (condition === "food_left") return context.food.x < head.x;
    if (condition === "food_down") return context.food.y > head.y;
    if (condition === "food_up") return context.food.y < head.y;
    if (condition === "front_blocked") return context.blocked(context.next(head, context.direction));
    if (condition === "left_free") return !context.blocked(context.next(head, this.turn(context.direction, -1)));
    if (condition === "right_free") return !context.blocked(context.next(head, this.turn(context.direction, 1)));
    return condition === "always";
  }

  resolveAction(action, direction) {
    if (action === "forward") return direction;
    if (action === "turn_left") return this.turn(direction, -1);
    if (action === "turn_right") return this.turn(direction, 1);
    return action;
  }

  turn(direction, offset) {
    const order = ["up", "right", "down", "left"];
    return order[(order.indexOf(direction) + offset + order.length) % order.length];
  }

  updateOutput() {
    this.codeElement.textContent = this.rules
      .map((rule, index) => `${index === 0 ? "WENN" : "SONST WENN"} ${this.conditions[rule.condition]}\n  ${this.actions[rule.action]}`)
      .join("\n");
    const checks = this.validate();
    this.feedbackElement.innerHTML = checks
      .map((check) => `<li class="${check.pass ? "feedback-pass" : "feedback-warn"}">${check.text}</li>`)
      .join("");
  }

  validate() {
    const conditions = this.rules.map((rule) => rule.condition);
    return [
      { pass: conditions.includes("always"), text: "Es gibt eine Sonst-Regel als Rückfall." },
      { pass: conditions.includes("front_blocked"), text: "Eine Regel reagiert auf eine blockierte Fahrtrichtung." },
      {
        pass: ["food_right", "food_left", "food_down", "food_up"].some((condition) => conditions.includes(condition)),
        text: "Mindestens eine Regel orientiert sich am Futter.",
      },
    ];
  }
}

if (typeof module !== "undefined") module.exports = AutoSnakeBlockEditor;
