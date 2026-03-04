# Flagship Simulation Suite Design

**Date**: 2026-03-04
**Status**: Approved
**Scope**: 6 interactive simulations for ACE Avionics Training CAET prep platform

## Context

### Problem
The ACE platform has 5 existing simulations, but 3 of 5 follow the same pattern (slider + observe), resulting in passive learning. Students struggle most with applied skills: electrical troubleshooting, flight instrument diagnosis, CNS system procedures, and wiring/connector work. The current sims demonstrate concepts but don't require students to think, decide, or perform.

### Goal
Build 6 flagship simulations, each with a fundamentally different interaction model, that make students DO real avionics work. Each sim becomes a reusable template for future content.

### Design Principles
- Every sim must require the student to THINK and DECIDE, not just observe
- No two sims should feel like the same interaction
- Immediate, technically accurate feedback tied to avionics principles
- Progressive difficulty: orientation, guided practice, independent application
- Aircraft-specific components and terminology (not generic electronics)
- Match existing design system: dark slate (#020617), Share Tech Mono readouts, glow effects

### Technical Constraints
- Single HTML files (matching existing sim pattern)
- Vanilla JS, no frameworks
- Canvas-based rendering for diagrams and animations
- Must integrate with ace-gamification.js (XP) and supabase-client.js (analytics)
- Responsive design (desktop primary, tablet secondary)

---

## Simulation 1: Fault Detective

**Type**: Scenario Mission (branching decisions with consequences)
**Node**: W4-Z3-N2 (Fault Isolation)
**Pain Point**: Electrical troubleshooting

### Learning Objectives
- Apply systematic fault isolation procedures
- Select appropriate test points in a circuit
- Interpret measurement results to narrow fault location
- Distinguish between open circuits, short circuits, and high-resistance faults

### Scenario Setup
Student is an avionics tech on the flight line. Aircraft is AOG (Aircraft on Ground) with a reported squawk: "Right navigation light inoperative." Student must diagnose the fault using a systematic approach.

### Circuit Under Test
A realistic nav light circuit:
- 28V DC bus bar -> circuit breaker -> toggle switch -> right nav light -> ground
- Hidden faults injected randomly from a pool:
  - Open circuit (broken wire between switch and light)
  - Short to ground (chafed wire near wing root)
  - High resistance connection (corroded terminal at light fixture)
  - Blown circuit breaker (overcurrent from previous short, now cleared)
  - Bad ground (corrosion at ground stud)
  - Multiple faults (e.g., corroded connector AND marginal wire)

### Interaction Flow

**Phase 1: Initial Assessment** (orientation)
- Student sees the aircraft schematic with the nav light circuit
- Prompted: "Where do you start?" with options:
  - Check the circuit breaker panel
  - Go directly to the nav light
  - Check the switch
  - Review the wiring diagram first
- Feedback explains WHY systematic troubleshooting starts at the breaker panel

**Phase 2: Testing** (guided practice)
- Student selects test points on the circuit diagram by clicking nodes
- At each test point, student must:
  1. Select meter function (DC volts, resistance, continuity)
  2. Choose where to place red and black probes
  3. Read the simulated measurement
  4. Decide: fault is upstream or downstream of this point
- Each measurement costs "time" (efficiency scoring)
- Wrong meter function selection gets feedback: "You're measuring resistance on a live circuit. What should you do first?"

**Phase 3: Diagnosis** (independent application)
- After gathering evidence, student must:
  1. Identify the fault type (open, short, high resistance)
  2. Identify the fault location
  3. Recommend the corrective action
- Branching outcomes based on accuracy:
  - Correct diagnosis: "Fault isolated. Estimated repair time: 45 min. Aircraft back in service."
  - Wrong diagnosis: "You replaced the nav light but the fault persists. The circuit breaker trips again. Back to testing."
  - Dangerous action: "You applied power without isolating the short. Circuit breaker tripped again and the chafed wire arced against the wing spar. Safety write-up required."

### Scoring
- Accuracy: Did you find the correct fault? (40%)
- Efficiency: How many measurements did you take? (30%)
- Safety: Did you follow safe practices? (20%)
- Methodology: Did you use a systematic approach? (10%)

### Replayability
- Pool of 6+ fault scenarios, randomly selected
- Each replay presents a different fault in the same circuit
- After mastering the nav light circuit, unlock additional circuits (landing light, pitot heat)

### UI Layout
```
+--------------------------------------------------+
| FAULT DETECTIVE - Nav Light Circuit        [?][X] |
+--------------------------------------------------+
|                                                    |
|          CIRCUIT SCHEMATIC (canvas)                |
|    [bus]--[CB]--[switch]--[wire]--[light]--[gnd]  |
|                                                    |
|    * Click any node to place probes               |
|    * Red/green dots show probe positions           |
|                                                    |
+------------------------+-------------------------+
|   METER PANEL          |   DECISION PANEL        |
|   +----------------+   |                         |
|   | Function: [DC V]|  |   "Based on your        |
|   | Reading: 28.1 V |  |    measurements..."     |
|   | Range: Auto     |  |                         |
|   +----------------+   |   [ ] Open circuit      |
|   Probes: BUS(+) GND(-)|  [ ] Short to ground   |
|                         |   [ ] High resistance   |
|   [Measure] [Reset]    |   [ ] Bad ground        |
|                         |   [Submit Diagnosis]    |
+------------------------+-------------------------+
| Steps: 3/10  |  Time: 2:45  |  XP: +0  |  HINTS |
+--------------------------------------------------+
```

---

## Simulation 2: Virtual DMM (Workbench Template)

**Type**: Virtual Workbench (realistic instrument operation)
**Node**: W4-Z2-N1 (DMM Basics)
**Pain Point**: Electrical troubleshooting (measurement technique)
**Template**: Reusable for oscilloscope, frequency counter, megohmmeter

### Learning Objectives
- Select the correct meter function for the measurement needed
- Set the appropriate range (or understand auto-ranging)
- Connect probes correctly (series for current, parallel for voltage)
- Read and interpret displayed values with correct units
- Recognize unsafe measurement setups (measuring current across a voltage source)

### Scenario Setup
Student has a virtual Fluke-style DMM and a test board with multiple circuits/components to measure. Tasks progress from simple to complex.

### Challenge Progression

**Level 1: Basic Measurements** (orientation)
- "Measure the voltage across the battery" (set to DC V, probe + and -)
- "Measure the resistance of this resistor" (set to ohms, power must be off)
- "Check continuity of this wire" (set to continuity, listen for beep)

**Level 2: Applied Measurements** (guided practice)
- "The landing light is dim. Measure voltage at the light connector."
- "This circuit breaker keeps tripping. Measure current draw."
- "Verify the ground path resistance is below 0.05 ohms."

**Level 3: Diagnostic Measurements** (independent application)
- "Three measurements to isolate why the pitot heat isn't working."
- Student must decide WHAT to measure, WHERE, and HOW
- No prompts - student drives the investigation

### The Virtual DMM
- Realistic Fluke 87V-style face with rotary selector
- Click the rotary dial to select function (V DC, V AC, A DC, mA, ohms, continuity, diode, capacitance)
- Display shows realistic digits with appropriate resolution
- Probe leads are drag-and-drop to test points on the circuit
- Auto-range with manual override option
- Audible continuity beep (Web Audio API)
- "OVERLOAD" display when range exceeded
- Safety warnings when measuring current in voltage mode

### Workbench Template Structure
This is the reusable template shared with Crimp Lab and future workbench sims:

```
+--------------------------------------------------+
| [SIM TITLE]                        [?][Reset][X] |
+--------------------------------------------------+
|                                                    |
|    WORKSPACE CANVAS (left 65%)                    |
|    - Circuit/component being worked on            |
|    - Drag-and-drop interaction zones              |
|    - Visual feedback (glow, highlight, animate)   |
|                                                    |
+--------------------+-----------------------------+
|                    |                              |
|   TOOL PANEL       |   READOUT / RESULT          |
|   (right 35%)      |                              |
|                    |   Digital display or          |
|   - Tool selector  |   inspection result           |
|   - Settings/knobs |                              |
|   - Probe controls |                              |
|                    |                              |
+--------------------+-----------------------------+
| TASK BAR: "Measure the voltage at TP3"    [Hint] |
+--------------------------------------------------+
| FEEDBACK: "Correct! 28.1V indicates..."   [Next] |
+--------------------------------------------------+
```

### Scoring
- Correct function selection (25%)
- Correct probe placement (25%)
- Correct reading interpretation (25%)
- Safety compliance (25%)
- Bonus: Speed and minimal errors

---

## Simulation 3: Pressure Failure

**Type**: Predict-Then-Reveal (mental model builder)
**Node**: W8-Z3-N1 (Pitot-Static System)
**Pain Point**: Flight instrument systems

### Learning Objectives
- Predict instrument behavior during pitot and/or static system failures
- Understand the relationship between pressure sources and instrument displays
- Distinguish between pitot blockage, static blockage, and combined failures
- Recognize failure symptoms at different phases of flight

### Scenario Setup
Student sees a simplified cockpit panel with the "big six" instruments, plus a cross-section diagram showing the pitot tube and static ports. A failure is introduced, and the student must predict what each instrument will display.

### The Instrument Panel
Canvas-rendered instruments:
- Airspeed Indicator (pitot + static)
- Altimeter (static only)
- Vertical Speed Indicator (static only)
- Attitude Indicator (gyro - unaffected by pitot/static)
- Heading Indicator (gyro - unaffected by pitot/static)
- Turn Coordinator (gyro - unaffected by pitot/static)

### Challenge Flow

**Setup Phase**
- Student sees: "Aircraft is climbing through 5,000 ft at 150 KIAS"
- Failure announced: "The pitot tube becomes blocked by ice"
- Aircraft continues: "The pilot continues climbing to 10,000 ft"

**Prediction Phase**
- For each of the 6 instruments, student predicts:
  - "Will this instrument read HIGH, LOW, NORMAL, or FROZEN?"
  - Student clicks their prediction for each instrument
  - No feedback yet - all 6 predictions are locked in

**Reveal Phase**
- Animated reveal: instruments update one by one showing the actual behavior
- For each instrument:
  - Student's prediction shown vs. actual behavior
  - Technical explanation: "The airspeed indicator uses ram air pressure (pitot) minus static pressure. With pitot blocked, trapped pressure stays at 5,000 ft value. As the aircraft climbs, static pressure decreases, so the ASI reads HIGHER than actual airspeed."
  - Color coded: green (correct), red (incorrect)

**Debrief**
- Summary of predictions vs. reality
- Key principle reinforced: which instruments use pitot, which use static, which use both
- Link to the pressure formula: ASI reads (Pt - Ps)

### Failure Scenarios (pool of challenges)
1. Pitot blockage during climb
2. Pitot blockage during descent
3. Static port blockage during climb
4. Static port blockage during descent
5. Both pitot and static blocked (level flight, then climb)
6. Pitot drain hole open (partial blockage)
7. Alternate static source selected in pressurized cabin

### UI Layout
```
+--------------------------------------------------+
| PRESSURE FAILURE - Pitot-Static Diagnosis  [?][X] |
+--------------------------------------------------+
|                                                    |
|    INSTRUMENT PANEL (canvas)                      |
|    +------+ +------+ +------+                     |
|    | ASI  | | ATIT | | ALT  |                     |
|    |      | |      | |      |                     |
|    +------+ +------+ +------+                     |
|    +------+ +------+ +------+                     |
|    | TC   | | HDG  | | VSI  |                     |
|    |      | |      | |      |                     |
|    +------+ +------+ +------+                     |
|                                                    |
| PREDICTION BUTTONS (per instrument):              |
|   [HIGH] [LOW] [NORMAL] [FROZEN]                  |
|                                                    |
+--------------------------------------------------+
| SCENARIO: "Climbing through FL100, pitot blocked" |
| Phase: PREDICT | Score: 4/6 correct               |
+--------------------------------------------------+
| EXPLANATION PANEL (expands after reveal)           |
| "The ASI reads high because..."                   |
+--------------------------------------------------+
```

### Scoring
- Predictions correct out of 6 instruments (per scenario)
- Running accuracy across all scenarios attempted
- Mastery badge at 90%+ across all 7 failure types

---

## Simulation 4: VOR Ramp Check

**Type**: Procedural Walkthrough (order matters, mistakes have consequences)
**Node**: W7-Z3-N1 (VOR Navigation)
**Pain Point**: CNS systems & nav aids

### Learning Objectives
- Execute a VOR receiver ramp check per FAA requirements
- Identify required equipment and documentation
- Perform the check in the correct sequence
- Recognize pass/fail criteria and document results
- Understand the difference between VOT, ground checkpoint, and airborne checks

### Scenario Setup
Student is performing a VOR operational check using a VOT (VOR Test Facility) on the ramp. They have access to the aircraft VOR receiver, the VOT frequency, and the maintenance log.

### Procedure Steps (must be performed in order)

1. **Tune the VOT frequency** (108.0 MHz on most VOTs)
   - Student must look up the correct VOT frequency
   - Wrong frequency = "No signal received. Check the frequency."

2. **Center the CDI needle**
   - Rotate the OBS (Omnibearing Selector) until the CDI centers
   - Should read 000 FROM or 180 TO with CDI centered

3. **Read and record the bearing**
   - Student notes the OBS reading
   - Must determine the error: how far off from 000/180?

4. **Check tolerance**
   - Ground VOT check: must be within +/- 4 degrees
   - Student decides: PASS or FAIL

5. **Document in maintenance log**
   - Date, location, bearing error, signature
   - Student fills in the log entry fields

6. **Repeat for second VOR receiver** (if dual installation)

### Error Handling
- Skip a step: "You haven't tuned the VOT frequency yet. The CDI won't give a meaningful reading."
- Wrong tolerance applied: "You applied the airborne tolerance (+/- 6 degrees) to a ground check. The ground tolerance is +/- 4 degrees."
- Incomplete documentation: "The log entry is missing the date. This check is not valid without complete documentation."

### UI Layout
```
+--------------------------------------------------+
| VOR RAMP CHECK                             [?][X] |
+--------------------------------------------------+
|                                                    |
|  VOR RECEIVER FACE (canvas)                       |
|  +--------------------+                           |
|  |    OBS: 358        |   PROCEDURE CHECKLIST     |
|  |                    |   [x] 1. Tune VOT freq    |
|  |     CDI  /  TO     |   [ ] 2. Center CDI       |
|  |    <--|-->         |   [ ] 3. Record bearing    |
|  |                    |   [ ] 4. Check tolerance   |
|  +--------------------+   [ ] 5. Document in log   |
|                                                    |
|  [OBS knob: drag to rotate]                       |
|  [Frequency: _108.0_ MHz]                         |
|                                                    |
+--------------------------------------------------+
| MAINTENANCE LOG                                    |
| Date: [____] VOT: [____] Error: [____] Sig: [___]|
| Result: [PASS] [FAIL]                             |
+--------------------------------------------------+
| Step 2 of 5: Center the CDI by rotating the OBS  |
+--------------------------------------------------+
```

### Scoring
- Correct sequence followed (30%)
- Accurate readings and calculations (30%)
- Proper tolerance applied (20%)
- Complete documentation (20%)

---

## Simulation 5: Crimp Lab

**Type**: Virtual Workbench (shared template with DMM sim)
**Node**: W5-Z2-N1 (Crimping Fundamentals)
**Pain Point**: Wiring & connectors

### Learning Objectives
- Select the correct terminal type for the wire gauge and application
- Choose the appropriate crimp tool and die set
- Execute a proper crimp sequence (strip, insert, crimp, inspect)
- Identify common crimp defects (under-crimp, over-crimp, bell-mouth, wrong tool)
- Apply pull-test verification criteria

### Scenario Setup
Student has a virtual crimp workbench with wire, terminals, tools, and an inspection station. Tasks progress from basic crimps to complex multi-pin connector termination.

### Challenge Progression

**Level 1: Single Terminal Crimp** (orientation)
- Given: 20 AWG wire, ring terminal, destination: ground stud
- Steps: Select terminal size, select tool, strip wire to correct length, insert wire, crimp, inspect
- Guided feedback at each step

**Level 2: Connector Pin Termination** (guided practice)
- Given: 22 AWG shielded wire, D-sub pin contact, destination: avionics connector
- Additional steps: strip shield, install shield termination, crimp pin, insert into connector body
- Must check pin retention (tug test)

**Level 3: Full Harness Termination** (independent application)
- Given: wiring diagram with 6 wires of different gauges going to a circular connector
- Student must: identify each wire, select correct pin contact, crimp each one, insert in correct pin position per diagram
- No guidance - student references the wiring diagram independently

### Defect Library (things that can go wrong)
- Wire strands outside the crimp barrel ("bird-caging")
- Insulation inside the crimp barrel
- Wrong terminal size for wire gauge
- Insufficient strip length
- Over-crimped (barrel cracked)
- Under-crimped (wire pulls out)
- Wrong tool used (generic pliers vs. ratcheting crimp tool)

### Inspection Station
After crimping, student moves to inspection:
- Visual inspection: zoom view of the crimp (canvas rendered)
- Pull test: simulated force gauge, must meet spec
- Cross-section view: shows wire fill and barrel deformation
- Student must identify: PASS or REJECT and state the reason

### UI Layout (uses Workbench Template)
```
+--------------------------------------------------+
| CRIMP LAB - Wire Termination              [?][X] |
+--------------------------------------------------+
|                                                    |
|    WORKSPACE (canvas)                             |
|    - Wire and terminal close-up view              |
|    - Animated crimp sequence                      |
|    - Drag wire into terminal barrel               |
|    - Click tool to crimp                          |
|                                                    |
+--------------------+-----------------------------+
|                    |                              |
|   TOOL RACK        |   INSPECTION PANEL          |
|   [Wire stripper]  |   Zoom: [magnified view]    |
|   [Crimp tool A]   |   Pull test: [--- N]        |
|   [Crimp tool B]   |   Cross section: [view]     |
|   [Heat gun]       |                              |
|   [Inspection      |   [PASS] [REJECT]           |
|    mirror]         |   Reason: [dropdown]         |
|                    |                              |
+--------------------+-----------------------------+
| Task: "Crimp a 20AWG ring terminal"       [Hint] |
+--------------------------------------------------+
```

### Scoring
- Correct terminal selection (20%)
- Correct tool selection (20%)
- Correct strip length (15%)
- Crimp quality (25%)
- Inspection accuracy (20%)

---

## Simulation 6: Circuit Sandbox

**Type**: Interactive Simulator (Falstad-inspired, aviation-focused)
**Node**: Standalone tool (links from W3 Electrical nodes)
**Pain Point**: Electrical troubleshooting (conceptual understanding)

### Purpose
A free-form circuit building and analysis tool where students can construct, test, and troubleshoot aircraft electrical circuits. Unlike the other 5 sims which are task-driven, this is an exploratory sandbox with optional challenges.

### Core Features

#### Component Palette (aircraft-specific)
- **Power Sources**: Battery (12V/28V), Generator/Alternator, External power
- **Protection**: Circuit breakers (push-to-reset, pull-to-disconnect), Fuses, Current limiters
- **Switching**: Toggle switch, Push button (momentary), Relay (SPST/SPDT), Solenoid
- **Loads**: Incandescent lamp, LED, Motor (variable RPM), Heater element, Avionics unit (modeled as resistive load)
- **Wiring**: Wire segments (drag to connect), Bus bars, Splice points, Ground studs
- **Test Points**: Voltage probe, Current probe (shows values when circuit is running)
- **Faults**: Open circuit injection, Short to ground injection, High resistance injection

#### Circuit Physics Engine
- DC circuit analysis (Kirchhoff's current and voltage laws)
- Real-time calculation of voltage, current, and power at every node
- Component models:
  - Resistors: V = IR with realistic tolerance
  - Lamps: non-linear resistance (cold vs. hot filament)
  - Motors: back-EMF modeling, stall current vs. running current
  - Circuit breakers: trip at rated current with time delay
  - Wires: negligible resistance unless fault injected
- Animated current flow (moving dots along wires, speed proportional to current)
- Voltage-based color coding on wires (red = high, blue = low, black = ground)
- Smoke/spark animation when component limits exceeded

#### Two Modes

**Sandbox Mode**
- Free-form building, no objectives
- Student can build any circuit and experiment
- "What happens if..." exploration
- Pre-built example circuits available:
  - Basic nav light circuit
  - Landing light with relay
  - Pitot heat circuit with thermal switch
  - Dual-bus architecture with bus tie
  - Starter motor circuit with solenoid

**Challenge Mode**
- Structured challenges with scoring:
  1. "Build It" challenges: given a schematic, build the circuit
  2. "Find the Fault" challenges: given a broken circuit, diagnose and identify the fault
  3. "Design It" challenges: given requirements ("light must be controlled from two switches"), design the circuit
  4. "What's Wrong?" challenges: given measurements, identify what component has failed

#### Challenge Examples
1. "Build a circuit that powers a landing light through a circuit breaker and toggle switch. The light should draw 4.2A at 28V." (Tests: series circuit, correct component selection)
2. "This nav light circuit has a fault. The circuit breaker is good, the switch is ON, but the light is off. Find the fault." (Tests: systematic troubleshooting)
3. "Design a circuit where the landing light can be controlled from either the pilot's or copilot's switch." (Tests: parallel switch logic)
4. "You measure 28V at the bus, 28V at the CB output, 28V at the switch output, but 0V at the light. What failed?" (Tests: voltage-drop fault isolation)

### UI Layout
```
+--------+------------------------------------------+
|        |                                          |
| PARTS  |         CIRCUIT CANVAS                   |
| PALETTE|                                          |
|        |    - Grid-based layout                   |
| [Batt] |    - Snap-to-grid component placement    |
| [CB  ] |    - Click-drag to wire between nodes    |
| [Sw  ] |    - Animated current flow               |
| [Lamp] |    - Color-coded voltage levels          |
| [Motor]|    - Click component to edit values      |
| [Relay]|    - Right-click for fault injection     |
| [Wire] |                                          |
| [Probe]|                                          |
| [Fault]|                                          |
|        |                                          |
+--------+-----------+------------------------------+
| METERS             | CONTROLS                     |
| Node V: 28.0V     | [RUN] [STOP] [RESET]         |
| Wire I: 2.1A      | [SANDBOX] [CHALLENGE]         |
| Total P: 58.8W    | Challenge: 3/10               |
| R_total: 13.3 ohm | [SAVE] [LOAD] [EXAMPLES]     |
+--------------------+------------------------------+
```

### Technical Implementation Notes
- Canvas-based rendering with requestAnimationFrame for smooth animation
- Circuit solving: Modified Nodal Analysis (MNA) for DC circuits
  - Build conductance matrix from component connections
  - Solve using Gaussian elimination (sufficient for DC circuits up to ~50 nodes)
  - Update every frame (60fps target)
- Component drag-and-drop: HTML5 drag events + canvas hit detection
- Wire routing: simple orthogonal routing with Manhattan distance
- Save/Load: serialize circuit to JSON, store in localStorage
- Challenge validation: compare student circuit against expected node voltages/currents within tolerance

### Physics Simplifications (appropriate for training level)
- DC only (no AC, no reactance, no phase)
- No thermal modeling beyond simple overcurrent
- Wire resistance only when fault is injected
- Ideal switches (no contact resistance unless fault injected)
- Motors modeled as variable resistance (stall vs. running)

---

## Shared Infrastructure

### Analytics Integration
Every simulation reports to the existing analytics system:

```javascript
// Event tracking (per interaction)
{
  session_id: "sim-session-uuid",
  lesson_id: "W4-Z3-N2",           // journey node
  format: "simulation",             // new format type
  sim_type: "scenario|workbench|predict|procedural|sandbox",
  event_type: "measurement|decision|prediction|step|build",
  is_correct: true/false,
  points: 10,
  metadata: {
    sim_name: "fault-detective",
    scenario: "nav-light-open-circuit",
    step: 3,
    total_steps: 8,
    time_elapsed_sec: 45
  }
}
```

### XP Integration
- Completing a simulation awards XP based on score
- Perfect score: 100 XP (equivalent to 20 drill questions)
- Passing score (70%+): 50-90 XP scaled
- Below passing: 10 XP (participation)
- First-time completion bonus: +25 XP

### Design System Tokens
All sims use consistent design tokens from ace-theme.css:

```css
/* Backgrounds */
--sim-bg-primary: #020617;      /* Main background */
--sim-bg-panel: #0f172a;        /* Panel background */
--sim-bg-elevated: #1e293b;     /* Elevated surface */

/* Borders */
--sim-border: #334155;          /* Default border */
--sim-border-active: #475569;   /* Active/focused */

/* Accent Colors (per sim type) */
--sim-accent-electrical: #ef4444;  /* Red for DC/electrical */
--sim-accent-nav: #38bdf8;        /* Sky blue for nav/CNS */
--sim-accent-instruments: #a78bfa; /* Purple for flight instruments */
--sim-accent-wiring: #f59e0b;     /* Amber for wiring */
--sim-accent-success: #10b981;    /* Green for correct/pass */
--sim-accent-danger: #ef4444;     /* Red for incorrect/fail */

/* Typography */
--sim-font-mono: 'Share Tech Mono', monospace;  /* Readouts */
--sim-font-body: 'Inter', sans-serif;           /* Body text */

/* Effects */
--sim-glow: 0 0 10px rgba(accent, 0.4);  /* Instrument glow */
--sim-scanline: linear-gradient(...)       /* CRT scanline overlay */
```

### Workbench Template API
Sims #2 and #5 share this reusable structure:

```javascript
class WorkbenchSim {
  constructor(config) {
    this.title = config.title;
    this.tools = config.tools;          // Array of tool definitions
    this.workspace = config.workspace;  // Canvas setup
    this.challenges = config.challenges; // Progressive challenge list
    this.scoring = config.scoring;       // Scoring rubric
  }

  // Override per sim
  renderWorkspace(ctx) {}
  renderToolPanel() {}
  handleToolInteraction(tool, target) {}
  evaluateResult(studentAction, expectedAction) {}
  provideFeedback(result) {}
}
```

---

## Build Priority

| Order | Sim | Rationale |
|-------|-----|-----------|
| 1 | Circuit Sandbox | Foundation - students reference this from all electrical sims |
| 2 | Virtual DMM | Establishes the Workbench Template reused by Crimp Lab |
| 3 | Fault Detective | Uses concepts from Circuit Sandbox + DMM |
| 4 | Pressure Failure | Independent of electrical sims, can parallel |
| 5 | Crimp Lab | Reuses Workbench Template from DMM |
| 6 | VOR Ramp Check | Independent, can parallel with #5 |

### Parallelization
- Sims 4, 5, 6 are independent and can be built concurrently
- Sim 1 (Fault Detective) depends on the circuit rendering approach from Sim 6 (Circuit Sandbox)
- Sim 5 (Crimp Lab) reuses the template from Sim 2 (Virtual DMM)

---

## Success Criteria

1. Each sim must feel fundamentally different from every other sim
2. Students must make at least 5 meaningful decisions per sim session
3. No "click to continue" moments - every interaction requires thought
4. Technically accurate to CAET exam standards
5. Feedback explains WHY, not just right/wrong
6. Each sim is replayable with different scenarios/challenges
7. Scoring integrates with existing XP/gamification system
8. Passes accessibility basics (keyboard navigation, sufficient contrast)
9. Loads and runs smoothly on modern browsers (Chrome, Firefox, Safari)
10. Single HTML file per sim, no external dependencies beyond shared CSS/JS
