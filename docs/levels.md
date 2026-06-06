# Difficulty Levels

AutoSnake Remote Lab uses exactly three levels. Each level builds on the same game and bot interface but expects more structure, safety, and validation.

## 1. Schüler

### Learning Goals

- Understand the Snake grid, direction, food, and collisions.
- Write simple rule-based control logic.
- Avoid immediate wall collisions.
- Move roughly toward food.

### Requirements

- Bot returns only valid directions.
- Bot does not intentionally reverse into itself.
- Bot uses simple comparisons between snake head and food position.
- Bot includes a fallback move if the preferred direction is unsafe.

### Assessment Ideas

- Run the bot for a fixed number of steps on simple maps.
- Check that it avoids walls in basic situations.
- Check that it can move closer to food when no obstacle blocks the path.

## 2. Student Anfang Studium

### Learning Goals

- Build a structured algorithm with clear helper functions.
- Maintain or inspect a field model.
- Distinguish safe and unsafe moves.
- Optionally use simple BFS to find food.

### Requirements

- Bot evaluates all legal moves before choosing.
- Bot avoids walls and its own body when possible.
- Bot separates analysis, decision, and fallback logic.
- Optional: bot finds a shortest path to food with BFS on small boards.

### Assessment Ideas

- Test move validity across several game states.
- Verify that the bot prefers safe moves over direct but unsafe moves.
- Compare optional BFS output with known shortest paths.

## 3. Fortgeschrittener Student

### Learning Goals

- Implement robust pathfinding and safety validation.
- Reason about dead ends and future reachable space.
- Respect limited runtime on embedded hardware.
- Use tests to validate behavior under edge cases.

### Requirements

- Bot uses pathfinding or an equivalent systematic strategy.
- Bot checks whether a chosen path leaves enough safe space.
- Bot has a bounded compute budget.
- Bot includes tests for collision-heavy and near-dead-end scenarios.

### Assessment Ideas

- Run deterministic challenge maps.
- Measure that decision time stays within a configured limit.
- Test that the bot avoids obvious traps even when food is nearby.
- Require learner-authored tests for advanced scenarios.
