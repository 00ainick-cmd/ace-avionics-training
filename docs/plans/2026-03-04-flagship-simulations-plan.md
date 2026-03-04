# Flagship Simulation Suite Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build 6 interactive avionics training simulations, each with a unique interaction model, integrated with the ACE platform's gamification and analytics systems.

**Architecture:** Single-file HTML simulations (CSS + HTML + JS embedded) following existing patterns in `simulations/`. Each sim is self-contained, uses Canvas API for rendering, and integrates with `AceSupabase` for analytics and `awardXP()` for gamification. A shared CSS file provides design tokens. The Circuit Sandbox uses Modified Nodal Analysis for real-time DC circuit solving.

**Tech Stack:** Vanilla HTML/CSS/JS, Canvas 2D API, Web Audio API (beeps/tones), existing Supabase analytics client, existing gamification engine.

**Design Doc:** `docs/plans/2026-03-04-flagship-simulations-design.md`

---

## Existing Patterns Reference

All 5 existing sims follow this structure:
```html
<style>/* All CSS here, scoped by prefix class */</style>
<div class="sim-container"><!-- All HTML --></div>
<script>document.addEventListener('DOMContentLoaded', () => { /* All JS */ });</script>
```

**Design tokens** (from existing sims):
- Backgrounds: `#020617` (main), `#0f172a` (panel), `#1e293b` (elevated)
- Borders: `#334155` (default), `#475569` (active)
- Text: `#f8fafc` (primary), `#e2e8f0` (secondary), `#94a3b8` (muted), `#64748b` (dim)
- Accents: `#ef4444` (red/DC), `#38bdf8` (sky/nav), `#10b981` (green/success), `#f59e0b` (amber/warning)
- Fonts: `'Share Tech Mono', monospace` (readouts), `'Inter', sans-serif` (body)
- Effects: `box-shadow: inset 0 0 40px rgba(0,0,0,0.8)`, `text-shadow: 0 0 10px rgba(color, 0.4)`

**Analytics integration** (from `supabase-client.js`):
```javascript
// Track a simulation interaction event
window.AceSupabase?.trackQuestionEvent({
  lessonId: 'sim-fault-detective',
  questionId: 'fd-scenario-1-step-3',
  format: 'simulation',
  loId: 'Systematic fault isolation procedure',
  category: 'electrical-troubleshooting',
  selectedIndex: 0,    // student's choice index
  correctIndex: 1,     // correct choice index
  isCorrect: false,
  points: 0
});

// Track completion summary
window.AceSupabase?.trackSessionSummary({
  lessonId: 'sim-fault-detective',
  format: 'simulation',
  questionsSeen: 8,
  questionsCorrect: 6,
  durationSec: 180
});
```

**XP integration** (from existing fault isolation sim):
```javascript
if (typeof awardXP === 'function') {
  awardXP(points, 'Simulation Completed');
}
```

---

## Phase 1: Shared Simulation Infrastructure

### Task 1.1: Create shared simulation CSS file

**Files:**
- Create: `simulations/sim-base.css`

**Step 1: Create the shared CSS file with design tokens and reusable component styles**

```css
/* simulations/sim-base.css
 * Shared design tokens and base components for all ACE simulations.
 * Import at top of each sim: @import url('sim-base.css');
 */

@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Inter:wght@400;600;700;800&display=swap');

/* ─── Design Tokens ─── */
:root {
  --sim-bg: #020617;
  --sim-panel: #0f172a;
  --sim-elevated: #1e293b;
  --sim-border: #334155;
  --sim-border-active: #475569;

  --sim-text: #f8fafc;
  --sim-text-secondary: #e2e8f0;
  --sim-text-muted: #94a3b8;
  --sim-text-dim: #64748b;

  --sim-red: #ef4444;
  --sim-sky: #38bdf8;
  --sim-green: #10b981;
  --sim-amber: #f59e0b;
  --sim-purple: #a78bfa;
  --sim-blue: #3b82f6;
  --sim-yellow: #fde047;

  --sim-font-mono: 'Share Tech Mono', monospace;
  --sim-font-body: 'Inter', sans-serif;
}

/* ─── Container ─── */
.sim-container {
  font-family: var(--sim-font-body);
  color: var(--sim-text-secondary);
  display: flex;
  flex-direction: column;
  gap: 20px;
  background: var(--sim-bg);
  padding: 30px;
  border-radius: 12px;
  border: 2px solid var(--sim-elevated);
  box-shadow: inset 0 0 40px rgba(0,0,0,0.8), 0 10px 30px rgba(0,0,0,0.5);
}

/* ─── Header ─── */
.sim-header {
  text-align: center;
  margin-bottom: 10px;
}
.sim-header h3 {
  font-size: 1.5rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin: 0 0 5px 0;
}
.sim-header p {
  color: var(--sim-text-dim);
  font-size: 0.9rem;
  margin: 0;
}

/* ─── Panels ─── */
.sim-panel {
  background: var(--sim-panel);
  padding: 20px;
  border-radius: 8px;
  border: 1px solid var(--sim-elevated);
}

/* ─── Canvas Wrap ─── */
.sim-canvas-wrap {
  position: relative;
  width: 100%;
  background: var(--sim-panel);
  border: 2px solid var(--sim-border);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: inset 0 0 30px rgba(0,0,0,0.5);
}
.sim-canvas-wrap canvas {
  width: 100%;
  height: 100%;
  display: block;
}

/* ─── Buttons ─── */
.sim-btn {
  background: var(--sim-elevated);
  color: var(--sim-text-muted);
  border: 1px solid var(--sim-border-active);
  padding: 12px 20px;
  border-radius: 6px;
  font-family: var(--sim-font-body);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}
.sim-btn:hover {
  background: var(--sim-border);
  color: var(--sim-text);
}
.sim-btn.primary {
  border-color: var(--sim-sky);
  color: var(--sim-sky);
}
.sim-btn.primary:hover {
  background: rgba(56, 189, 248, 0.1);
  box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
}
.sim-btn.disabled, .sim-btn:disabled {
  opacity: 0.5;
  pointer-events: none;
  cursor: not-allowed;
}

/* ─── Readout Display ─── */
.sim-readout {
  font-family: var(--sim-font-mono);
  font-size: 1.4rem;
  color: var(--sim-text);
  text-shadow: 0 0 5px rgba(255,255,255,0.3);
}

/* ─── Task Bar ─── */
.sim-taskbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--sim-panel);
  padding: 12px 20px;
  border-radius: 8px;
  border: 1px solid var(--sim-elevated);
  font-size: 0.9rem;
}
.sim-taskbar .task-text {
  color: var(--sim-text-secondary);
  font-weight: 600;
}
.sim-taskbar .hint-btn {
  color: var(--sim-amber);
  background: none;
  border: 1px dashed var(--sim-amber);
  padding: 4px 12px;
  border-radius: 4px;
  font-family: var(--sim-font-mono);
  font-size: 0.8rem;
  cursor: pointer;
}

/* ─── Feedback Panel ─── */
.sim-feedback {
  padding: 15px 20px;
  border-radius: 8px;
  border-left: 4px solid var(--sim-border);
  background: var(--sim-panel);
  display: none;
}
.sim-feedback.correct {
  border-color: var(--sim-green);
  background: rgba(16, 185, 129, 0.05);
}
.sim-feedback.incorrect {
  border-color: var(--sim-red);
  background: rgba(239, 68, 68, 0.05);
}
.sim-feedback.info {
  border-color: var(--sim-sky);
}
.sim-feedback .fb-label {
  font-family: var(--sim-font-mono);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 8px;
}
.sim-feedback .fb-text {
  font-size: 1rem;
  line-height: 1.6;
  color: var(--sim-text);
}

/* ─── Score Bar ─── */
.sim-scorebar {
  display: flex;
  gap: 20px;
  justify-content: center;
  align-items: center;
  padding: 10px 20px;
  background: var(--sim-panel);
  border-radius: 8px;
  border: 1px solid var(--sim-elevated);
}
.sim-score-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--sim-font-mono);
  font-size: 0.85rem;
  color: var(--sim-text-muted);
}
.sim-score-item .value {
  color: var(--sim-text);
  font-size: 1.1rem;
}

/* ─── Scanline overlay (for instrument displays) ─── */
.sim-scanline {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(255,255,255,0) 0%,
    rgba(255,255,255,0) 50%,
    rgba(16, 185, 129, 0.08) 50%,
    rgba(16, 185, 129, 0.08) 100%
  );
  background-size: 100% 4px;
  pointer-events: none;
  opacity: 0.3;
  z-index: 10;
}

/* ─── Responsive ─── */
@media (max-width: 768px) {
  .sim-container { padding: 15px; gap: 12px; }
  .sim-header h3 { font-size: 1.2rem; }
}
```

**Step 2: Verify the file is created**

Open `simulations/sim-base.css` and confirm it contains the design tokens.

**Step 3: Commit**

```bash
git add simulations/sim-base.css
git commit -m "feat(sim): add shared simulation base CSS with design tokens"
```

---

### Task 1.2: Create shared simulation analytics helper

**Files:**
- Create: `simulations/sim-analytics.js`

**Step 1: Create the analytics helper that wraps AceSupabase for simulation use**

```javascript
/**
 * sim-analytics.js
 * Shared analytics + scoring helper for ACE simulations.
 *
 * Usage (inside a sim <script>):
 *   const tracker = new SimTracker('fault-detective', 'W4-Z3-N2');
 *   tracker.recordStep({ stepId: 'check-cb', correct: true, points: 10 });
 *   tracker.complete();  // sends summary + awards XP
 */

class SimTracker {
  constructor(simName, nodeId) {
    this.simName = simName;
    this.nodeId = nodeId;
    this.startTime = Date.now();
    this.steps = [];
    this.completed = false;
  }

  /** Record a single interaction step */
  recordStep({ stepId, correct, points = 0, loId = '', category = '' }) {
    const step = { stepId, correct, points, loId, category, timestamp: Date.now() };
    this.steps.push(step);

    // Fire analytics event if available
    if (window.AceSupabase?.trackQuestionEvent) {
      window.AceSupabase.trackQuestionEvent({
        lessonId: `sim-${this.simName}`,
        questionId: `${this.simName}-${stepId}`,
        format: 'simulation',
        loId: loId || null,
        category: category || this.simName,
        selectedIndex: correct ? 0 : 1,
        correctIndex: 0,
        isCorrect: correct,
        points: points
      });
    }
  }

  /** Get current score as percentage */
  getScore() {
    if (this.steps.length === 0) return { pct: 0, correct: 0, total: 0, points: 0 };
    const correct = this.steps.filter(s => s.correct).length;
    const total = this.steps.length;
    const points = this.steps.reduce((sum, s) => sum + s.points, 0);
    return {
      pct: Math.round((correct / total) * 100),
      correct,
      total,
      points
    };
  }

  /** Calculate XP based on score percentage */
  calculateXP() {
    const { pct } = this.getScore();
    if (pct >= 100) return 100;
    if (pct >= 90) return 90;
    if (pct >= 80) return 75;
    if (pct >= 70) return 50;
    if (pct >= 60) return 30;
    return 10; // participation XP
  }

  /** Mark simulation complete, send summary, award XP */
  complete() {
    if (this.completed) return;
    this.completed = true;

    const durationSec = Math.round((Date.now() - this.startTime) / 1000);
    const score = this.getScore();
    const xp = this.calculateXP();

    // Send session summary
    if (window.AceSupabase?.trackSessionSummary) {
      window.AceSupabase.trackSessionSummary({
        lessonId: `sim-${this.simName}`,
        format: 'simulation',
        questionsSeen: score.total,
        questionsCorrect: score.correct,
        durationSec
      });
    }

    // Award XP via parent page
    if (typeof awardXP === 'function') {
      awardXP(xp, `${this.simName} Simulation Completed`);
    }

    return { score, xp, durationSec };
  }
}

// Expose globally
window.SimTracker = SimTracker;
```

**Step 2: Commit**

```bash
git add simulations/sim-analytics.js
git commit -m "feat(sim): add shared SimTracker analytics helper for simulations"
```

---

## Phase 2: Circuit Sandbox (Falstad-inspired)

This is the most complex simulation and the foundational tool students will reference from all electrical content.

### Task 2.1: Circuit Sandbox — Core engine and component model

**Files:**
- Create: `simulations/circuit-sandbox.html`

**Step 1: Build the HTML shell with component palette and canvas**

Create the file with:
- `<style>` block: layout grid (sidebar palette + main canvas + bottom controls), using `sim-base.css` tokens
- `<div>` structure: component palette (left), circuit canvas (center), meters + controls (bottom)
- `<script>` block: empty initialization

Layout structure:
```
.sandbox-container
  .sandbox-palette        (left sidebar, 120px)
    .palette-item         (one per component type, draggable)
  .sandbox-main           (flex column)
    .sandbox-canvas-wrap  (flex: 1)
      canvas#circuit-canvas
    .sandbox-controls     (bottom bar)
      .sandbox-meters     (V, I, R, P readouts)
      .sandbox-buttons    ([RUN] [STOP] [RESET] [SANDBOX] [CHALLENGE])
```

Component palette items (aircraft-specific):
- Battery (28V / 12V)
- Circuit Breaker
- Toggle Switch
- Push Button (momentary)
- Lamp (incandescent)
- LED
- Motor
- Resistor
- Relay (SPDT)
- Bus Bar
- Ground Stud
- Wire (connector mode)
- Probe (measurement)
- Fault Injector

**Step 2: Implement the component data model**

```javascript
// Component types and their electrical properties
const COMPONENTS = {
  battery:   { type: 'source', voltage: 28, symbol: 'BAT', color: '#ef4444' },
  breaker:   { type: 'protection', resistance: 0.001, tripCurrent: 5, symbol: 'CB', color: '#f59e0b' },
  switch_t:  { type: 'switch', closed: false, resistance: { on: 0.001, off: 1e9 }, symbol: 'SW', color: '#38bdf8' },
  switch_m:  { type: 'switch', momentary: true, closed: false, resistance: { on: 0.001, off: 1e9 }, symbol: 'PB', color: '#38bdf8' },
  lamp:      { type: 'load', resistance: 6.67, ratedVoltage: 28, ratedPower: 4.2, symbol: 'LAMP', color: '#fde047' },
  led:       { type: 'load', resistance: 1400, forwardVoltage: 2.0, symbol: 'LED', color: '#10b981' },
  motor:     { type: 'load', resistance: { stall: 2.0, running: 14.0 }, symbol: 'MOT', color: '#a78bfa' },
  resistor:  { type: 'load', resistance: 100, symbol: 'RES', color: '#eab308' },
  relay:     { type: 'relay', coilResistance: 200, pullInVoltage: 18, symbol: 'RLY', color: '#f97316' },
  busbar:    { type: 'junction', resistance: 0.0001, symbol: 'BUS', color: '#94a3b8' },
  ground:    { type: 'ground', symbol: 'GND', color: '#64748b' },
  wire:      { type: 'wire', resistance: 0.0001 },
  probe:     { type: 'probe', symbol: 'PRB', color: '#10b981' },
  fault:     { type: 'fault', faultType: 'open', symbol: 'FLT', color: '#ef4444' }
};
```

**Step 3: Implement the circuit graph data structure**

```javascript
class CircuitGraph {
  constructor() {
    this.nodes = new Map();      // nodeId -> { x, y, voltage: 0 }
    this.components = new Map(); // compId -> { type, nodeA, nodeB, props, state }
    this.nextNodeId = 0;
    this.nextCompId = 0;
  }

  addNode(x, y) { /* returns nodeId */ }
  addComponent(type, nodeA, nodeB, props) { /* returns compId */ }
  removeComponent(compId) { /* removes comp and orphan nodes */ }
  getConnectedNodes(nodeId) { /* returns adjacent nodeIds */ }
  solve() { /* runs MNA solver, updates node voltages and component currents */ }
}
```

**Step 4: Implement the DC circuit solver (Modified Nodal Analysis)**

The MNA solver builds a conductance matrix and solves `[G][V] = [I]`:
- For each resistive component: add conductance `1/R` to matrix
- For each voltage source: add KVL constraint row
- Solve using Gaussian elimination
- Extract node voltages and branch currents

This is the core physics engine. Key formulas:
- `V = IR` (Ohm's Law at every component)
- `KCL: sum of currents at every node = 0`
- `KVL: sum of voltages around every loop = 0`
- Circuit breaker trips when `I > tripCurrent` for > 100ms

**Step 5: Verify core engine**

Add a test circuit in code (battery + resistor + ground), run solver, log voltages and currents to console. Verify `I = V/R` matches expected values.

**Step 6: Commit**

```bash
git add simulations/circuit-sandbox.html
git commit -m "feat(sim): circuit sandbox core engine with MNA solver"
```

---

### Task 2.2: Circuit Sandbox — Canvas rendering and interaction

**Files:**
- Modify: `simulations/circuit-sandbox.html`

**Step 1: Implement grid-based canvas rendering**

- Draw grid background (20px cells, subtle lines)
- Render components as symbols on grid intersections
- Draw wire connections between component terminals
- Color-code wires by voltage level (red = high, blue = low, black = ground)
- Animate current flow with moving dots (speed proportional to amperage)

**Step 2: Implement drag-and-drop from palette to canvas**

- Click palette item to select it
- Click canvas grid cell to place component
- Click two component terminals to connect with wire
- Right-click component to edit properties or inject fault
- Delete key to remove selected component

**Step 3: Implement component rendering functions**

Each component gets a canvas draw function:
```javascript
function drawBattery(ctx, x, y, voltage, selected) { /* battery symbol with + and voltage label */ }
function drawResistor(ctx, x, y, resistance, current, selected) { /* zigzag with heat glow based on power */ }
function drawSwitch(ctx, x, y, closed, selected) { /* toggle graphic, clickable to open/close */ }
function drawLamp(ctx, x, y, voltage, ratedVoltage, selected) { /* circle with brightness based on V/Vrated */ }
function drawBreaker(ctx, x, y, tripped, selected) { /* CB symbol, red if tripped */ }
function drawMotor(ctx, x, y, current, selected) { /* M circle with spinning indicator */ }
```

**Step 4: Implement animated current flow**

- After solver runs, calculate current magnitude on each wire
- Draw moving dots along wires, speed = `clamp(abs(current) * 3, 0.5, 15)` pixels/frame
- Dot color: `#3b82f6` (blue, matching existing Ohm's Law sim)
- Dot size: 3px with `shadowBlur: 8`

**Step 5: Implement real-time update loop**

```javascript
function gameLoop(timestamp) {
  // 1. Update component states (switch positions, relay coils)
  // 2. Run MNA solver
  // 3. Check overcurrent conditions (trip breakers)
  // 4. Update current flow animation offset
  // 5. Clear canvas and redraw everything
  // 6. Update meter readouts
  requestAnimationFrame(gameLoop);
}
```

**Step 6: Visual verification**

Open in browser. Place a battery, resistor, and lamp. Wire them in series with a ground. Click RUN. Verify:
- Current dots flow around the loop
- Lamp glows proportionally to applied voltage
- Meter readouts show correct V, I, R, P values

**Step 7: Commit**

```bash
git add simulations/circuit-sandbox.html
git commit -m "feat(sim): circuit sandbox canvas rendering and drag-drop interaction"
```

---

### Task 2.3: Circuit Sandbox — Challenge mode and pre-built circuits

**Files:**
- Modify: `simulations/circuit-sandbox.html`

**Step 1: Add pre-built example circuits**

Create JSON circuit definitions that can be loaded:
```javascript
const EXAMPLE_CIRCUITS = {
  'nav-light': {
    name: 'Navigation Light Circuit',
    description: 'Basic series circuit: Battery -> CB -> Switch -> Nav Light -> Ground',
    components: [ /* array of {type, gridX, gridY, props} */ ],
    wires: [ /* array of {fromNodeId, toNodeId} */ ]
  },
  'landing-light-relay': { /* ... */ },
  'pitot-heat': { /* ... */ },
  'dual-bus': { /* ... */ },
  'starter-motor': { /* ... */ }
};
```

**Step 2: Implement challenge mode**

Challenge types:
1. **Build It**: Show a schematic image, student must recreate it
2. **Find the Fault**: Load a broken circuit, student uses probes to diagnose
3. **Design It**: Given requirements (text), student builds from scratch
4. **What's Wrong?**: Given measurements, identify the failed component

```javascript
const CHALLENGES = [
  {
    id: 'ch-1',
    type: 'build',
    title: 'Basic Nav Light',
    description: 'Build a circuit that powers a nav light through a circuit breaker and toggle switch.',
    validation: (circuit) => {
      // Check: has battery, has CB, has switch, has lamp, has ground
      // Check: all in series
      // Check: lamp voltage within 10% of rated
      return { passed: true, feedback: 'Circuit correct! Current draw: 0.63A' };
    }
  },
  {
    id: 'ch-2',
    type: 'find-fault',
    title: 'Inop Landing Light',
    circuit: 'landing-light-relay',
    fault: { componentId: 'wire-3', faultType: 'open' },
    validation: (studentAnswer) => { /* check if they identified the correct fault */ }
  },
  // ... 8 more challenges
];
```

**Step 3: Add challenge UI**

- Mode toggle: [SANDBOX] / [CHALLENGE] buttons
- Challenge panel: shows challenge description, target, submit button
- Validation feedback: green/red result with explanation
- Progress: "Challenge 3/10" indicator
- Score integration via SimTracker

**Step 4: Add save/load functionality**

```javascript
function saveCircuit() {
  const data = JSON.stringify(circuit.serialize());
  localStorage.setItem('ace_sandbox_' + Date.now(), data);
}
function loadCircuit(key) {
  const data = JSON.parse(localStorage.getItem(key));
  circuit.deserialize(data);
}
```

**Step 5: Visual verification**

Load each example circuit, verify it simulates correctly. Complete challenge 1 (Build It), verify scoring.

**Step 6: Commit**

```bash
git add simulations/circuit-sandbox.html
git commit -m "feat(sim): circuit sandbox challenge mode with 10 challenges and example circuits"
```

---

## Phase 3: Virtual DMM (Workbench Template)

### Task 3.1: Virtual DMM — Meter face and rotary selector

**Files:**
- Create: `simulations/virtual-dmm.html`

**Step 1: Build the HTML structure using workbench template layout**

```
.dmm-container (sim-container)
  .dmm-layout (grid: 65% workspace / 35% tool panel)
    .dmm-workspace (canvas: test board with circuits + probe placement zones)
    .dmm-tool-panel
      .dmm-meter-face (canvas: realistic Fluke 87V dial + display)
      .dmm-probe-controls (Red probe / Black probe indicators)
  .dmm-taskbar (current objective + hint button)
  .dmm-feedback (result panel)
  .dmm-scorebar (steps, time, score)
```

**Step 2: Render the DMM face on canvas**

- Rotary dial with click sectors for each function:
  - OFF, V DC, V AC, mV DC, A DC, mA DC, Ohms, Continuity, Diode, Capacitance
- Digital LCD display area (4.5 digit, Share Tech Mono font)
- Red/Black probe input jacks (visual indicator of which jacks probes are in)
- MIN/MAX, HOLD, RANGE buttons
- Auto-range indicator

Click the rotary dial sector to change function. Display updates to show function symbol.

**Step 3: Implement measurement simulation**

```javascript
class VirtualDMM {
  constructor() {
    this.function = 'OFF';    // Current selected function
    this.range = 'auto';
    this.probeRed = null;     // { testPointId } or null
    this.probeBlack = null;   // { testPointId } or null
  }

  measure(circuit, testPointA, testPointB) {
    switch (this.function) {
      case 'V_DC':
        return circuit.getVoltageBetween(testPointA, testPointB);
      case 'OHMS':
        if (circuit.isPowered()) return 'OL'; // Can't measure R on live circuit
        return circuit.getResistanceBetween(testPointA, testPointB);
      case 'CONT':
        const r = circuit.getResistanceBetween(testPointA, testPointB);
        return { value: r, beep: r < 50 }; // Beep if < 50 ohms
      case 'A_DC':
        return circuit.getCurrentThrough(testPointA, testPointB);
      // ... etc
    }
  }
}
```

**Step 4: Implement test board with click-to-probe interaction**

The workspace canvas shows a circuit board/schematic with labeled test points (TP1, TP2, etc.). Student clicks a test point to place the red probe, clicks another for the black probe. The DMM display updates with the reading.

Safety checks:
- Measuring current in voltage mode: "WARNING: Connecting ammeter in parallel. This would blow the fuse."
- Measuring resistance on a live circuit: "CAUTION: Power must be off to measure resistance accurately."

**Step 5: Add Web Audio beep for continuity**

```javascript
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
function beep(frequency = 2000, duration = 0.1) {
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.frequency.value = frequency;
  gain.gain.value = 0.3;
  osc.start();
  osc.stop(audioCtx.currentTime + duration);
}
```

**Step 6: Commit**

```bash
git add simulations/virtual-dmm.html
git commit -m "feat(sim): virtual DMM with realistic meter face and probe interaction"
```

---

### Task 3.2: Virtual DMM — Progressive challenges and scoring

**Files:**
- Modify: `simulations/virtual-dmm.html`

**Step 1: Implement the 3-level challenge progression**

**Level 1 (Orientation) - 3 tasks:**
1. "Measure the voltage across the battery" -> DC V, probes on battery terminals, expect ~28V
2. "Measure the resistance of the 100 ohm resistor" -> Ohms, probes across resistor, power off, expect ~100 ohms
3. "Check continuity of this wire" -> Continuity, probes on wire ends, expect beep + low resistance

**Level 2 (Guided) - 3 tasks:**
4. "The landing light is dim. Measure voltage at the light connector." -> DC V at load, expect <28V (voltage drop)
5. "This breaker keeps tripping. Measure current draw." -> A DC in series, expect >5A (overcurrent)
6. "Verify ground resistance is below 0.05 ohms" -> Ohms, probe ground stud to structure, expect <0.05

**Level 3 (Independent) - 2 tasks:**
7. "The pitot heat isn't working. You have 3 measurements to find the fault." -> Student chooses what/where
8. "Diagnose why the right nav light is dim but left is bright." -> Student drives investigation

**Step 2: Implement scoring rubric per task**

For each task, score:
- Correct function selected: 25%
- Correct probe placement: 25%
- Correct reading interpretation: 25%
- Safety compliance: 25%

**Step 3: Wire up SimTracker for analytics**

```javascript
const tracker = new SimTracker('virtual-dmm', 'W4-Z2-N1');
// After each task
tracker.recordStep({
  stepId: `level-${level}-task-${task}`,
  correct: allCriteriamet,
  points: score,
  loId: 'Correct DMM function selection and probe placement',
  category: 'tools-test-equipment'
});
// After all tasks
tracker.complete();
```

**Step 4: Visual verification**

Complete all 8 tasks. Verify scoring displays correctly, XP is awarded, analytics events fire in console.

**Step 5: Commit**

```bash
git add simulations/virtual-dmm.html
git commit -m "feat(sim): virtual DMM progressive challenges with 3-level difficulty"
```

---

## Phase 4: Fault Detective (Scenario Mission)

### Task 4.1: Fault Detective — Scenario engine with branching logic

**Files:**
- Create: `simulations/fault-detective.html`

**Step 1: Build the scenario engine**

Unlike the existing W4-Z3-N2 sim (which is a simple linear story tree), this engine supports:
- **Random fault selection** from a pool of 6+ faults per circuit
- **Measurement simulation** (student picks test points + meter function, gets realistic readings)
- **Efficiency tracking** (count of measurements taken)
- **Safety violation detection** (measuring current across voltage, probing live high-voltage, etc.)

```javascript
class FaultScenario {
  constructor(circuitDef, faultPool) {
    this.circuit = circuitDef;          // Circuit topology with test points
    this.fault = this.selectFault(faultPool); // Random fault from pool
    this.measurements = [];              // History of student's measurements
    this.phase = 'assessment';           // assessment -> testing -> diagnosis
  }

  selectFault(pool) {
    return pool[Math.floor(Math.random() * pool.length)];
  }

  /** Simulate a measurement at the given test points with the given meter function */
  takeMeasurement(testPointA, testPointB, meterFunction) {
    // Calculate what the meter would actually show, given the injected fault
    // Returns { value, unit, safe: boolean, feedback: string }
  }

  /** Student submits their diagnosis */
  submitDiagnosis(faultType, faultLocation, correctiveAction) {
    const correct = (
      faultType === this.fault.type &&
      faultLocation === this.fault.location
    );
    return { correct, actualFault: this.fault, feedback: '...' };
  }
}
```

**Step 2: Define the nav light circuit with fault pool**

```javascript
const NAV_LIGHT_CIRCUIT = {
  name: 'Right Navigation Light Circuit',
  squawk: 'Right wing navigation light is completely INOP. Left and tail are normal. NAV LIGHTS switch is ON.',
  testPoints: {
    'bus':     { label: '28V Bus Bar', x: 0.1, y: 0.2 },
    'cb-in':   { label: 'CB Input', x: 0.2, y: 0.2 },
    'cb-out':  { label: 'CB Output', x: 0.3, y: 0.2 },
    'sw-in':   { label: 'Switch Input', x: 0.4, y: 0.2 },
    'sw-out':  { label: 'Switch Output', x: 0.5, y: 0.2 },
    'wr-in':   { label: 'Wing Root Plug (supply)', x: 0.6, y: 0.3 },
    'wr-out':  { label: 'Wing Root Plug (load side)', x: 0.7, y: 0.3 },
    'lamp-hot':{ label: 'Lamp Socket (center)', x: 0.85, y: 0.3 },
    'lamp-gnd':{ label: 'Lamp Socket (shell)', x: 0.85, y: 0.5 },
    'gnd':     { label: 'Wing Ground Stud', x: 0.85, y: 0.7 }
  },
  faultPool: [
    { id: 'f1', type: 'open', location: 'wire-sw-to-wr', description: 'Open circuit: wire chafed through between switch and wing root' },
    { id: 'f2', type: 'short', location: 'wire-wr-to-lamp', description: 'Short to ground: chafed wire at wing root contacting structure' },
    { id: 'f3', type: 'high-resistance', location: 'lamp-gnd-connection', description: 'Corroded ground terminal at lamp fixture' },
    { id: 'f4', type: 'open', location: 'cb', description: 'Circuit breaker tripped (was overcurrent, now cleared)' },
    { id: 'f5', type: 'high-resistance', location: 'wing-root-plug', description: 'Corroded pins in wing root disconnect connector' },
    { id: 'f6', type: 'multiple', location: 'wr-plug+gnd', description: 'Corroded connector AND marginal ground path' }
  ]
};
```

**Step 3: Build the UI with circuit schematic, meter panel, and decision panel**

Layout:
```
.fd-container
  .fd-header (title + squawk text)
  .fd-layout (grid: 60% schematic / 40% panels)
    .fd-schematic (canvas: circuit diagram with clickable test points)
    .fd-panels
      .fd-meter (function selector + reading display)
      .fd-decision (fault type radio buttons + location dropdown + submit)
  .fd-scorebar (steps taken, time, efficiency rating)
  .fd-feedback (diagnosis result)
```

**Step 4: Implement the 3-phase interaction flow**

Phase 1 (Assessment): Student sees squawk, chooses where to start. Feedback on approach.
Phase 2 (Testing): Student clicks test points, selects meter function, reads measurements. Each measurement costs 1 "step."
Phase 3 (Diagnosis): Student selects fault type + location + corrective action from dropdowns.

**Step 5: Implement scoring**

```javascript
// Scoring rubric
function calculateScore(scenario) {
  const accuracyScore = scenario.diagnosisCorrect ? 40 : 0;
  const efficiencyScore = Math.max(0, 30 - (scenario.measurements.length - 3) * 5); // Optimal is 3-4 measurements
  const safetyScore = scenario.safetyViolations === 0 ? 20 : Math.max(0, 20 - scenario.safetyViolations * 10);
  const methodScore = scenario.usedSystematicApproach ? 10 : 0; // Started at CB, worked outward
  return { accuracy: accuracyScore, efficiency: efficiencyScore, safety: safetyScore, method: methodScore, total: accuracyScore + efficiencyScore + safetyScore + methodScore };
}
```

**Step 6: Commit**

```bash
git add simulations/fault-detective.html
git commit -m "feat(sim): fault detective scenario engine with random fault injection and scoring"
```

---

### Task 4.2: Fault Detective — Additional circuits and replayability

**Files:**
- Modify: `simulations/fault-detective.html`

**Step 1: Add landing light and pitot heat circuits**

After mastering the nav light circuit (score >= 70%), unlock:
- Landing light circuit (relay-controlled, higher current, different fault patterns)
- Pitot heat circuit (thermostat-controlled, intermittent faults)

**Step 2: Add replay logic**

Each replay selects a new random fault from the pool. Track which faults the student has successfully diagnosed.

**Step 3: Add "unlock" progression display**

Show circuit icons with lock/unlock status: [Nav Light: UNLOCKED] [Landing Light: LOCKED (score 70%+ to unlock)] [Pitot Heat: LOCKED]

**Step 4: Commit**

```bash
git add simulations/fault-detective.html
git commit -m "feat(sim): fault detective additional circuits and unlock progression"
```

---

## Phase 5: Pressure Failure (Predict-Then-Reveal)

Can be built in parallel with Phase 4.

### Task 5.1: Pressure Failure — Instrument panel and prediction interface

**Files:**
- Create: `simulations/pressure-failure.html`

**Step 1: Build the instrument panel with 6 canvas-rendered instruments**

Each instrument is a small canvas or a section of one large canvas:
- **ASI** (Airspeed Indicator): round dial, 0-350 KIAS, white arc, green arc, yellow arc
- **Altimeter**: round dial, 3 pointers (100ft, 1000ft, 10000ft), Kollsman window
- **VSI** (Vertical Speed): round dial, -2000 to +2000 fpm, center = 0
- **Attitude Indicator**: artificial horizon, pitch lines, bank pointer
- **Heading Indicator**: compass rose, lubber line
- **Turn Coordinator**: miniature aircraft, ball tube

```javascript
function drawASI(ctx, x, y, size, kias) { /* round gauge with needle at kias position */ }
function drawAltimeter(ctx, x, y, size, altitude) { /* 3-pointer altimeter */ }
function drawVSI(ctx, x, y, size, fpm) { /* vertical speed with lag simulation */ }
function drawAttitude(ctx, x, y, size, pitch, bank) { /* horizon line rotated */ }
function drawHeading(ctx, x, y, size, heading) { /* compass rose */ }
function drawTurnCoord(ctx, x, y, size, turnRate, slip) { /* miniature wings + ball */ }
```

**Step 2: Build the prediction interface**

Below each instrument, 4 buttons: `[HIGH] [LOW] [NORMAL] [FROZEN]`
- Student clicks one prediction per instrument (6 total)
- All 6 must be locked in before reveal
- Color-coded after reveal: green = correct, red = incorrect

**Step 3: Build the pitot-static cross-section diagram**

Side panel showing:
- Pitot tube (ram air opening)
- Static ports (flush on fuselage)
- Plumbing lines to ASI, ALT, VSI
- Red X overlay on blocked source when failure is announced

**Step 4: Commit**

```bash
git add simulations/pressure-failure.html
git commit -m "feat(sim): pressure failure instrument panel with prediction interface"
```

---

### Task 5.2: Pressure Failure — Failure scenarios and reveal animations

**Files:**
- Modify: `simulations/pressure-failure.html`

**Step 1: Define failure scenario physics**

```javascript
const FAILURE_SCENARIOS = [
  {
    id: 'pitot-blocked-climb',
    title: 'Pitot Tube Blocked — Climbing',
    setup: { altitude: 5000, airspeed: 150, vsi: 500, phase: 'climbing to 10000' },
    failure: { pitotBlocked: true, staticBlocked: false },
    correctAnswers: {
      asi: 'HIGH',     // Trapped pitot pressure > decreasing static = reads high
      altimeter: 'NORMAL', // Static-only, unaffected
      vsi: 'NORMAL',   // Static-only, unaffected
      attitude: 'NORMAL', // Gyro, unaffected
      heading: 'NORMAL',  // Gyro, unaffected
      turnCoord: 'NORMAL' // Gyro, unaffected
    },
    explanation: {
      asi: 'With pitot blocked during a climb, the trapped ram air pressure stays at the 5,000 ft value. As static pressure decreases with altitude, the ASI reads (trapped Pt - decreasing Ps) = HIGHER than actual airspeed.',
      altimeter: 'The altimeter uses only static pressure and is unaffected by a pitot blockage.',
      // ... etc for each instrument
    }
  },
  // ... 6 more scenarios
];
```

**Step 2: Implement the animated reveal sequence**

After student locks in predictions:
1. Dim all instruments
2. One by one (0.5s delay between each):
   - Highlight the instrument
   - Animate the needle/reading to the failure-state value
   - Show student's prediction vs. actual (green/red badge)
   - Show explanation text in the debrief panel
3. After all 6 revealed, show summary score (X/6 correct)

**Step 3: Implement the 7 failure scenarios**

Scenarios from design doc:
1. Pitot blocked during climb (ASI reads HIGH)
2. Pitot blocked during descent (ASI reads LOW)
3. Static blocked during climb (ASI reads LOW, ALT reads FROZEN, VSI reads FROZEN at 0)
4. Static blocked during descent (ASI reads HIGH, ALT FROZEN, VSI FROZEN)
5. Both blocked level flight then climb (ASI FROZEN, ALT FROZEN, VSI FROZEN)
6. Pitot drain hole open (partial blockage - ASI reads slightly LOW)
7. Alternate static source in pressurized cabin (ALT reads slightly HIGH, ASI slightly HIGH)

**Step 4: Add mastery tracking**

Track which scenarios the student has completed with 5/6 or 6/6 correct. Show progress: "Scenarios Mastered: 3/7"

**Step 5: Commit**

```bash
git add simulations/pressure-failure.html
git commit -m "feat(sim): pressure failure with 7 failure scenarios and animated reveal"
```

---

## Phase 6: Crimp Lab (Reuses Workbench Template)

Can be built in parallel with Phase 7.

### Task 6.1: Crimp Lab — Workbench interface and crimp mechanics

**Files:**
- Create: `simulations/crimp-lab.html`

**Step 1: Build the workbench layout (reusing template pattern from DMM)**

```
.crimp-container
  .crimp-layout (grid: 65% workspace / 35% tool rack)
    .crimp-workspace (canvas: close-up view of wire + terminal)
    .crimp-tools
      .tool-rack (wire stripper, crimp tool A, crimp tool B, heat gun, inspection mirror)
      .inspection-panel (zoom view, pull test gauge, cross-section)
  .crimp-taskbar (current task + hint)
  .crimp-feedback (result)
```

**Step 2: Implement wire/terminal rendering on canvas**

Render a close-up view showing:
- Wire (colored insulation, exposed conductor strands)
- Terminal (barrel, tongue/ring/pin)
- Visual states: unstripped -> stripped -> inserted -> crimped -> inspected

**Step 3: Implement the crimp sequence interaction**

1. **Select terminal**: Click from a tray of terminals (ring, spade, pin, butt splice). Must match wire gauge.
2. **Strip wire**: Click wire stripper tool, then click the wire. Animated strip. Too much = bad, too little = bad.
3. **Insert wire**: Drag stripped wire end into terminal barrel. Visual shows wire fill.
4. **Select crimp tool**: Choose between ratcheting crimp tool (correct) and generic pliers (incorrect).
5. **Crimp**: Click the tool on the terminal. Animated squeeze. Ratchet tool = proper deformation. Pliers = inconsistent.
6. **Inspect**: Switch to inspection view. Zoom on crimp, check for defects.

**Step 4: Implement defect generation**

Based on student's choices, generate realistic defects:
- Wrong tool: under-crimped or over-crimped barrel
- Wrong terminal size: visible gap or wire strands outside
- Insufficient strip: insulation inside barrel (visible in cross-section)
- Over-stripped: exposed conductor before barrel (bird-caging risk)

**Step 5: Implement inspection station**

- Zoom view: canvas-rendered close-up of the crimped terminal
- Pull test: simulated force gauge, student clicks "test" button, gauge shows pull-out force
  - Good crimp: 15-25 lbs (PASS)
  - Under-crimp: 3-8 lbs (FAIL)
  - Over-crimp: barrel cracks during pull test (FAIL)
- Cross-section view: shows wire fill percentage inside barrel
- Student clicks [PASS] or [REJECT] and selects reason from dropdown

**Step 6: Commit**

```bash
git add simulations/crimp-lab.html
git commit -m "feat(sim): crimp lab workbench with terminal selection and crimp mechanics"
```

---

### Task 6.2: Crimp Lab — Progressive levels and connector termination

**Files:**
- Modify: `simulations/crimp-lab.html`

**Step 1: Implement 3-level progression**

- Level 1: Single ring terminal on 20AWG wire (guided, with prompts)
- Level 2: D-sub pin contact on 22AWG shielded wire (adds shield termination step)
- Level 3: 6-pin circular connector per wiring diagram (student references diagram independently)

**Step 2: Add wiring diagram reference panel for Level 3**

Show a connector pinout diagram that the student must follow. Student clicks each wire from a bundle, identifies it by color code, selects the correct pin contact size, and inserts into the correct connector position.

**Step 3: Wire up SimTracker and commit**

```bash
git add simulations/crimp-lab.html
git commit -m "feat(sim): crimp lab progressive levels with connector termination"
```

---

## Phase 7: VOR Ramp Check (Procedural Walkthrough)

Can be built in parallel with Phase 6.

### Task 7.1: VOR Ramp Check — Receiver face and procedure engine

**Files:**
- Create: `simulations/vor-ramp-check.html`

**Step 1: Build the VOR receiver face on canvas**

Render a realistic VOR/ILS receiver display:
- **CDI needle** (Course Deviation Indicator): vertical needle that deflects left/right
- **OBS ring**: 360-degree compass rose, rotatable by clicking/dragging the knob
- **TO/FROM flag**: indicates whether the selected radial is TO or FROM the station
- **Frequency display**: digital readout, editable
- **NAV flag**: displayed when no valid signal

The OBS knob is the primary interaction: student drags to rotate, CDI responds.

**Step 2: Implement VOR/VOT simulation math**

```javascript
class VORSimulator {
  constructor() {
    this.votFrequency = 108.0;  // VOT always on 108.0
    this.obsSelected = 0;       // 0-359 degrees
    this.bearingError = 0;      // Injected error for this check (+/- 0 to 6 degrees)
  }

  /** Calculate CDI deflection based on OBS setting and VOT signal */
  getCDIDeflection() {
    // VOT always broadcasts 360/0 FROM. With error, the center point shifts.
    const centerBearing = 0 + this.bearingError;
    const diff = this.normalizeAngle(this.obsSelected - centerBearing);
    // CDI: 1 dot per 2 degrees, max 5 dots (10 degrees)
    const dots = Math.max(-5, Math.min(5, diff / 2));
    return dots;
  }

  getToFromFlag() {
    // VOT: centered on 0 FROM or 180 TO
    const diff = Math.abs(this.normalizeAngle(this.obsSelected - 180));
    return diff < 90 ? 'TO' : 'FROM';
  }
}
```

**Step 3: Build the procedure checklist UI**

Right panel shows the step-by-step checklist:
1. [ ] Tune VOT frequency (108.0 MHz)
2. [ ] Center the CDI needle using OBS
3. [ ] Record the OBS bearing
4. [ ] Calculate error (deviation from 000 or 180)
5. [ ] Determine: PASS or FAIL (tolerance: +/- 4 degrees for ground check)
6. [ ] Complete maintenance log entry

Steps must be completed in order. Clicking ahead shows: "Complete step N first."

**Step 4: Implement the maintenance log form**

Fields: Date, Location, VOT Used, Bearing Reading, Error (+/- degrees), PASS/FAIL, Technician Signature

Validation:
- Error calculation must match the actual bearing error
- Tolerance must be correct (+/- 4 for ground VOT, NOT +/- 6 which is airborne)
- All fields must be filled

**Step 5: Implement error handling / wrong actions**

- Wrong frequency: "No VOT signal received. Check the published VOT frequency."
- Centering CDI with wrong OBS: Not an error, just imprecise. Score reflects accuracy.
- Wrong tolerance applied: "You used the airborne tolerance (+/- 6 degrees). Ground VOT tolerance is +/- 4 degrees."
- Incomplete log: "Log entry rejected: missing date field."

**Step 6: Commit**

```bash
git add simulations/vor-ramp-check.html
git commit -m "feat(sim): VOR ramp check with receiver face and procedural engine"
```

---

### Task 7.2: VOR Ramp Check — Randomized errors and dual-VOR check

**Files:**
- Modify: `simulations/vor-ramp-check.html`

**Step 1: Randomize the bearing error per session**

Each time the sim loads, generate a random error between -6 and +6 degrees. This means sometimes it PASSES and sometimes it FAILS, and the student must correctly determine which.

**Step 2: Add second VOR receiver check**

After completing VOR 1, prompt: "This aircraft has dual VOR receivers. Repeat the check on VOR 2." Second receiver gets a different random error.

**Step 3: Add cross-check between receivers**

After both are checked, prompt: "What is the maximum allowable difference between VOR 1 and VOR 2 readings?" (Answer: 4 degrees between receivers for dual VOR ground check)

**Step 4: Wire up SimTracker and commit**

```bash
git add simulations/vor-ramp-check.html
git commit -m "feat(sim): VOR ramp check randomized errors and dual-receiver check"
```

---

## Phase 8: Integration and Polish

### Task 8.1: Link simulations to journey nodes

**Files:**
- Modify: relevant journey node JSON files in `journey-nodes/nodes/`

**Step 1: Add simulation embed blocks to journey nodes**

For each sim, add a block to the corresponding journey node JSON:
```json
{
  "type": "interactive-simulation",
  "simFile": "../../simulations/circuit-sandbox.html",
  "title": "Circuit Sandbox",
  "description": "Build and test aircraft electrical circuits"
}
```

Node mappings:
- `circuit-sandbox.html` -> linked from W3 electrical nodes (W3-Z1-N1, W3-Z2-N1, etc.)
- `virtual-dmm.html` -> W4-Z2-N1
- `fault-detective.html` -> W4-Z3-N2 (replaces existing sim)
- `pressure-failure.html` -> W8-Z3-N1
- `crimp-lab.html` -> W5-Z2-N1
- `vor-ramp-check.html` -> W7-Z3-N1

**Step 2: Verify journey node rendering handles the new block type**

Check `journey.html` to see how it renders block types. If `interactive-simulation` isn't handled, add the iframe/embed logic.

**Step 3: Commit**

```bash
git add journey-nodes/nodes/ simulations/ journey.html
git commit -m "feat: link new simulations to journey nodes"
```

---

### Task 8.2: Final visual polish and responsive testing

**Files:**
- Modify: all 6 simulation HTML files

**Step 1: Test each sim at desktop (1280px), tablet (768px), and mobile (375px)**

Verify:
- Canvas resizes correctly on window resize
- Text remains readable at all sizes
- Controls are touchable on tablet/mobile
- No horizontal scrolling

**Step 2: Add consistent loading state**

Each sim shows a brief "Initializing..." state while canvas renders, then fades in.

**Step 3: Add keyboard navigation**

- Tab between interactive elements
- Enter to confirm selections
- Escape to cancel/back
- Arrow keys for OBS rotation (VOR sim) and slider controls

**Step 4: Final commit**

```bash
git add simulations/
git commit -m "feat(sim): responsive layout, keyboard navigation, and loading states"
```

---

## Build Order Summary

| Order | Sim | Depends On | Estimated Effort |
|-------|-----|-----------|-----------------|
| 1.1 | sim-base.css | Nothing | Small |
| 1.2 | sim-analytics.js | Nothing | Small |
| 2.1-2.3 | Circuit Sandbox | 1.1, 1.2 | Large (MNA solver + canvas rendering + challenges) |
| 3.1-3.2 | Virtual DMM | 1.1, 1.2 | Medium (workbench template + meter simulation) |
| 4.1-4.2 | Fault Detective | 1.1, 1.2 | Medium (scenario engine + multiple circuits) |
| 5.1-5.2 | Pressure Failure | 1.1, 1.2 | Medium (instrument rendering + failure physics) |
| 6.1-6.2 | Crimp Lab | 1.1, 1.2, template from 3.1 | Medium (reuses workbench template) |
| 7.1-7.2 | VOR Ramp Check | 1.1, 1.2 | Medium (VOR math + procedure engine) |
| 8.1-8.2 | Integration | All sims | Small |

**Parallelization:** After Phase 1-2, sims 3-7 can all be built independently. Recommended parallel groups:
- Group A: Circuit Sandbox (2) + Virtual DMM (3)
- Group B: Fault Detective (4) + Pressure Failure (5)
- Group C: Crimp Lab (6) + VOR Ramp Check (7)
