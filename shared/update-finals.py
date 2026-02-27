import json
import os

modules = [
    {
        "path": "../training/caet/mod1-maintenance-regs/data/jeopardy.json",
        "finals": [
            {
                "category": "Final Challenge: Regulatory Authority",
                "clue": "Under 14 CFR Part 43, this specific document must be completed and submitted to the FAA within 48 hours after a major repair or major alteration.",
                "choices": ["Form 337", "Form 8130-3", "Form 8110-3", "Logbook Entry"],
                "correctIndex": 0,
                "explanation": "FAA Form 337 (Major Repair and Alteration) is required to document major repairs/alterations and must be forwarded to the FAA within 48 hours of returning the aircraft to service.",
                "difficulty": 500
            },
            {
                "category": "Final Challenge: Part 145",
                "clue": "A Part 145 Repair Station cannot perform alterations on an aircraft without approved data. Which of the following is NOT considered 'approved data' by the FAA?",
                "choices": ["Type Certificate Data Sheet (TCDS)", "Airworthiness Directives (ADs)", "Advisory Circular 43.13-1B", "Supplemental Type Certificate (STC)"],
                "correctIndex": 2,
                "explanation": "AC 43.13-1B is 'acceptable data', not 'approved data' unless specifically approved by an FAA inspector for a major alteration. TCDS, ADs, and STCs are approved data.",
                "difficulty": 500
            },
            {
                "category": "Final Challenge: Return to Service",
                "clue": "When approving an aircraft for return to service after a 100-hour inspection, the maintenance record entry must include this specific statement.",
                "choices": ["Certified airworthy for immediate flight", "I certify that this aircraft has been inspected in accordance with a 100-hour inspection and was determined to be in airworthy condition", "Inspected and cleared per 14 CFR Part 91", "Operations check satisfactory"],
                "correctIndex": 1,
                "explanation": "14 CFR 43.11 dictates the exact wording required for an inspection return to service: 'I certify that this aircraft has been inspected in accordance with... and was determined to be in airworthy condition.'",
                "difficulty": 500
            }
        ]
    },
    {
        "path": "../training/caet/mod2-basic-electrical/data/jeopardy.json",
        "finals": [
            {
                "category": "Final Challenge: Advanced Circuit Analysis",
                "clue": "In a parallel circuit with three resistors (100Ω, 200Ω, and 400Ω), what is the total equivalent resistance (Rt)?",
                "choices": ["700Ω", "57.1Ω", "114.2Ω", "14.2Ω"],
                "correctIndex": 1,
                "explanation": "Using the reciprocal formula: 1/Rt = 1/100 + 1/200 + 1/400. 1/Rt = 4/400 + 2/400 + 1/400 = 7/400. Rt = 400/7 ≈ 57.14 ohms.",
                "difficulty": 500
            },
            {
                "category": "Final Challenge: AC Reactance",
                "clue": "As the frequency of an AC circuit increases, what happens to inductive reactance (X_L) and capacitive reactance (X_C)?",
                "choices": ["X_L increases, X_C decreases", "X_L decreases, X_C increases", "Both increase", "Both decrease"],
                "correctIndex": 0,
                "explanation": "Inductive reactance (X_L = 2πfL) is directly proportional to frequency, so it increases. Capacitive reactance (X_C = 1 / 2πfC) is inversely proportional, so it decreases.",
                "difficulty": 500
            },
            {
                "category": "Final Challenge: Power Systems",
                "clue": "In an aircraft AC power system, a Transformer Rectifier Unit (TRU) performs this primary function.",
                "choices": ["Converts 28V DC to 115V AC", "Converts 115V AC to 28V DC", "Steps up 115V AC to 230V AC", "Synchronizes multiple AC generators"],
                "correctIndex": 1,
                "explanation": "A TRU contains a transformer to step down the voltage (e.g., 115V to 28V) and a rectifier to convert the AC into stable DC power for the aircraft's DC buses.",
                "difficulty": 500
            }
        ]
    },
    {
        "path": "../training/caet/mod3-cns-systems/data/jeopardy.json",
        "finals": [
            {
                "category": "Final Challenge: Surveillance & Transponders",
                "clue": "A Mode S transponder differs from Mode A/C by featuring unique selective addressing. How many bits are in a discrete Mode S ICAO aircraft address?",
                "choices": ["12-Bit", "24-Bit", "32-Bit", "64-Bit"],
                "correctIndex": 1,
                "explanation": "Every Mode S equipped aircraft is assigned a unique 24-bit ICAO address, hardcoded or strapped into the transponder, allowing over 16 million distinct addresses.",
                "difficulty": 500
            },
            {
                "category": "Final Challenge: Navigation Arrays",
                "clue": "A VOR receiver determines bearing to a station by measuring the phase difference between a reference phase signal and this type of signal.",
                "choices": ["A variable directional phase signal", "A paired DME pulse pair", "A 1090 MHz reply", "An ILS localizer tone"],
                "correctIndex": 0,
                "explanation": "VORs transmit a 30Hz reference signal (omnidirectional) and a 30Hz variable signal (sweeping directional). The receiver compares their phase difference to determine the specific radial.",
                "difficulty": 500
            },
            {
                "category": "Final Challenge: WAAS Precision",
                "clue": "The Wide Area Augmentation System (WAAS) provides GPS corrections to the aircraft via this specific method.",
                "choices": ["VHF datalink from ground stations", "Geostationary satellites transmitting on the L1 frequency", "Cellular LTE networks", "Mode S Extended Squitter"],
                "correctIndex": 1,
                "explanation": "WAAS ground stations calculate GPS error corrections, uplink them to geostationary (GEO) satellites, which broadcast the corrections back to aircraft using the standard GPS L1 frequency.",
                "difficulty": 500
            }
        ]
    },
    {
        "path": "../training/caet/mod4-flight-instruments/data/jeopardy.json",
        "finals": [
            {
                "category": "Final Challenge: Glass Cockpit Systems",
                "clue": "In an EFIS architecture, a failure of the Air Data Computer (ADC) will result in red 'X's over which combination of primary flight instruments?",
                "choices": ["Attitude and Heading", "Airspeed, Altimeter, and VSI", "Navigation Maps and Weather Radar", "Engine Instruments"],
                "correctIndex": 1,
                "explanation": "The ADC processes pitot-static information. A failure blanks out the Airspeed Indicator, Altimeter, and Vertical Speed Indicator. Attitude and Heading are handled by the AHRS.",
                "difficulty": 500
            },
            {
                "category": "Final Challenge: AHRS Alignment",
                "clue": "A modern AHRS unit uses this specific sensor combination to align to magnetic north without requiring a physical spinning flux valve.",
                "choices": ["A 3-axis solid-state magnetometer", "A ring laser gyro", "Dual GPS receivers", "A tuned resonant cavity"],
                "correctIndex": 0,
                "explanation": "Modern AHRS uses a 3-axis solid-state magnetometer (usually mounted in the wing to avoid interference) to electronically sense the Earth's magnetic field and derive magnetic heading.",
                "difficulty": 500
            },
            {
                "category": "Final Challenge: Pitot-Static Faults",
                "clue": "If an aircraft takes off with the static port taped over, how will the airspeed indicator react during the climb?",
                "choices": ["It will read zero", "It will lock at the takeoff speed", "It will read falsely low", "It will read falsely high"],
                "correctIndex": 2,
                "explanation": "With a trapped static pressure from takeoff altitude (which is higher pressure than at altitude), the pitot-static differential is smaller than it should be. The ASI will read falsely low in a climb.",
                "difficulty": 500
            }
        ]
    },
    {
        "path": "../training/caet/mod5-digital-databus/data/jeopardy.json",
        "finals": [
            {
                "category": "Final Challenge: ARINC 429",
                "clue": "An ARINC 429 data word is exactly 32 bits long. Which bit acts as the parity bit for error checking?",
                "choices": ["Bit 1", "Bit 8", "Bit 32", "There is no parity bit"],
                "correctIndex": 2,
                "explanation": "ARINC 429 words are 32 bits long. Bit 32 is exclusively used as an Odd Parity bit—set to 1 or 0 to ensure the total number of 1s in the word is an odd number, allowing basic error detection.",
                "difficulty": 500
            },
            {
                "category": "Final Challenge: Military Databuses",
                "clue": "MIL-STD-1553 uses a bi-directional, half-duplex architecture controlled by a Bus Controller. The devices responding to the controller are known as what?",
                "choices": ["Slaves", "Remote Terminals (RT)", "Transceivers", "Sub-systems"],
                "correctIndex": 1,
                "explanation": "In a 1553 bus, the central controller is the Bus Controller (BC), and it commands up to 31 Remote Terminals (RTs) that act upon those commands.",
                "difficulty": 500
            },
            {
                "category": "Final Challenge: Ethernet in Aviation",
                "clue": "The AFDX (Avionics Full-Duplex Switched Ethernet) standard, used extensively on modern aircraft like the A380 and 787, is defined by which ARINC specification?",
                "choices": ["ARINC 429", "ARINC 717", "ARINC 664", "ARINC 818"],
                "correctIndex": 2,
                "explanation": "ARINC 664 (specifically Part 7) defines AFDX, which brings deterministic Ethernet networking to avionics, vastly reducing wiring weight compared to point-to-point ARINC 429.",
                "difficulty": 500
            }
        ]
    },
    {
        "path": "../training/caet/mod6-aircraft-wiring/data/jeopardy.json",
        "finals": [
            {
                "category": "Final Challenge: Wiring Separation",
                "clue": "To prevent electromagnetic interference (EMI), AC power lines and sensitive sensor wiring (like ARINC databuses) must be separated by what absolute minimum clearance if they must run parallel without physical barriers?",
                "choices": ["0.5 inches", "2.0 inches", "6.0 inches", "They cannot run parallel under any circumstances"],
                "correctIndex": 1,
                "explanation": "Standard wiring practices (MIL-W-5088L and AC 43.13-1B) dictate a minimum 2-inch clearance between power/control cables and sensitive signal/radio wiring where possible, though 6 inches is preferred.",
                "difficulty": 500
            },
            {
                "category": "Final Challenge: Crimping Tool Logic",
                "clue": "When using a mil-spec Daniels indent crimper with a positioner, what prevents the tool from being opened mid-crimp, guaranteeing a full compression cycle?",
                "choices": ["The ratcheting pawl mechanism", "The turret lock", "The go/no-go gauge", "The safety wire seal"],
                "correctIndex": 0,
                "explanation": "A precision ratcheting mechanism ensures the tool handles must be fully compressed before they can be released, preventing under-crimped pins.",
                "difficulty": 500
            },
            {
                "category": "Final Challenge: Shield Termination",
                "clue": "When terminating a shielded wire via a shield drain loop or solder sleeve, the unshielded portion of the inner conductor should generally not exceed what length to maintain EMI protection?",
                "choices": ["0.5 to 1.0 inch", "2.0 to 3.0 inches", "There is no limit", "Quarter wavelength of the signal"],
                "correctIndex": 0,
                "explanation": "To maintain shielding effectiveness and prevent the exposed wire from acting like an antenna, the 'window' of unshielded wire at a termination should be kept as short as possible, typically under 1 inch.",
                "difficulty": 500
            }
        ]
    },
    {
        "path": "../training/caet/mod7-tools-test-equipment/data/jeopardy.json",
        "finals": [
            {
                "category": "Final Challenge: TDR Diagnostics",
                "clue": "When using a Time Domain Reflectometer (TDR) to shoot a coaxial cable fault, an upward (positive) reflection spike on the trace indicates what type of cable fault?",
                "choices": ["A direct short to ground", "An open circuit or break", "Water intrusion", "Normal impedance matching"],
                "correctIndex": 1,
                "explanation": "A TDR trace reflects upward for a high-impedance fault (an open/break) and downward for a low-impedance fault (a short).",
                "difficulty": 500
            },
            {
                "category": "Final Challenge: Oscilloscopes",
                "clue": "On an oscilloscope capturing an ARINC 429 signal, you observe a square wave that fails to cross the 0V baseline, instead fluctuating between +10V and +5V. What does this indicate?",
                "choices": ["Normal bipolar return-to-zero operation", "A loss of the HI or LO wire, preventing differential measurement", "The baud rate is too fast", "The termination resistor is missing"],
                "correctIndex": 1,
                "explanation": "ARINC 429 uses a differential bipolar signal (+10V, 0V, -10V). If the scope sees it entirely floating positive, it means one of the legs (A or B) is broken or improperly referenced to ground.",
                "difficulty": 500
            },
            {
                "category": "Final Challenge: Insulation Testing",
                "clue": "When testing a high-voltage generator feeder cable with a Megohmmeter (Megger), why must you discharge the cable immediately after the test?",
                "choices": ["To reset the meter", "To clear the error code", "To dissipate the high voltage capacitance stored in the cable", "To prevent a false short reading on the next test"],
                "correctIndex": 2,
                "explanation": "A Megger injects high voltage (e.g., 500V or 1000V). A long run of insulated wire acts as a capacitor and can store a dangerous charge that will shock the technician if not discharged to ground.",
                "difficulty": 500
            }
        ]
    },
    {
        "path": "../training/caet/mod8-shop-safety/data/jeopardy.json",
        "finals": [
            {
                "category": "Final Challenge: Hazardous Materials",
                "clue": "Skydrol (phosphate ester hydraulic fluid), often encountered in large aircraft bays, requires immediate cleaning with soap and water upon skin contact because it is highly corrosive and causes what primary physical symptom?",
                "choices": ["Instant freezing of tissue", "Intense burning sensation similar to chemical burns", "Painless numbness", "Immediate blistering"],
                "correctIndex": 1,
                "explanation": "Skydrol is notorious for causing intense, painful burning sensations upon contact with skin and, particularly, the eyes. Immediate flushing with water is the required first aid.",
                "difficulty": 500
            },
            {
                "category": "Final Challenge: Radome Safety",
                "clue": "Before approaching the radome of a powered-up transport category aircraft on the ramp, you must verify what system is pinned or disabled to prevent potentially lethal RF exposure?",
                "choices": ["The Weather Radar", "The TCAS transmitters", "The VHF Comm antennas", "The GPS receiver"],
                "correctIndex": 0,
                "explanation": "Weather radar systems emit high-power non-ionizing radiation that can cause severe internal burns. They must be off or disabled via pin before personnel work near the nose of the aircraft.",
                "difficulty": 500
            },
            {
                "category": "Final Challenge: ESD Protocols",
                "clue": "When working on highly sensitive avionics LRUs, an ESD wrist strap must be worn. What internal component is built into the wrist strap wire to protect the technician from electrocution if they touch a live power source?",
                "choices": ["A 1 Amp fuse", "A 1 Megohm resistor", "A grounding busbar", "A diode"],
                "correctIndex": 1,
                "explanation": "A 1MΩ resistor is built into the strap. It allows static electricity to safely bleed to ground, but limits the current to a harmless level (milliamps) if the technician touches 115V AC.",
                "difficulty": 500
            }
        ]
    }
]

for mod in modules:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.normpath(os.path.join(base_dir, mod["path"]))
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}, does not exist")
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Modifying {file_path}")
    data["final"] = mod["finals"]
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

print("Finals updated successfully.")
