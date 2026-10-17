# MECHANICAL ENGINEERING REPORT (REVISION 2 - BLUEPRINT COMPLIANT)
## Continuous-Loop Motor-Driven Marble Race Machine
**Document Reference:** MR-ENG-002  
**Author:** Mechanical CAD & 3D-Printing Design Specialist  
**Design Reference:** User Concept Blueprint (Pages 1, 2, 3)  
**Target Marble:** Ø16.0 mm Spherical Marble (Chrome Steel or Soda-Lime Glass)  
**Parametric CAD Engine:** OpenCASCADE / `build123d` (Python BREP / CSG Architecture)  

---

### 1. Executive Summary & Design Revision Overview
In response to the user's concept blueprint, the 3D CAD model has been overhauled to ensure that all trajectories are **organically curved, mathematically smooth ($C^\infty$), and directly grounded in the blueprint specifications**:

1. **Multi-Turn Concentric Spiral Track (Page 1):** Instead of faceted polygonal segments, the marble exit transitions into smooth concentric circular loops that spiral outward around the central cylinder and octagonal base.
2. **Semicircular Round-Bottom U-Channel (Page 2):** The track cross section has been updated to feature a curved semicircular bottom groove ($R_{inner} = 9.0\text{ mm}$) with tangent vertical side walls ($H = 6.0\text{ mm}$). This nests the 16 mm marble in a low-friction channel while providing lateral guidance.
3. **Curved Rectangular Hurdle Section (Pages 1 & 3):** Located along the front quadrant of the base, featuring a wide rectangular channel ($22\text{ mm}$ width) with raised $9\text{ mm}$ safety side walls and 7 staggered cylindrical collision posts ($\varnothing 4.5\text{ mm} \times 3.5\text{ mm}$ height) that decelerate the marble via controlled glancing impacts.
4. **Infinity (Figure-Eight) Return Loop & Entry Channel (Page 1):** Positioned on the left side of the machine, the track loops through a smooth figure-eight with a $28\text{ mm}$ vertical crossover bridge and exits directly into the Entry channel, feeding back into the cylinder inlet.

---

### 2. Archimedes Screw Elevator Mechanics & Anti-Rotation Constraint

#### 2.1 Physics of the Vertical Lift
As identified on Page 1 ("Cylinder inside helix with slots so marble can climb up"):
- When a spherical marble rests on a rotating helical flight, normal forces tend to spin the ball azimuthally rather than translating it vertically.
- To produce positive vertical climbing, an azimuthal anti-rotation constraint is mandatory.

#### 2.2 Implemented Engineering Solution
- **Central Hollow Cylinder:** Outer Diameter $\varnothing 60.0\text{ mm}$, Inner Diameter $\varnothing 54.0\text{ mm}$.
- **Rotating Helix:** Flight Outer Diameter $\varnothing 50.0\text{ mm}$, Central Core Shaft $\varnothing 14.0\text{ mm}$, Pitch $P = 26.0\text{ mm/rev}$.
- **Radial Clearance:** $2.0\text{ mm}$ dynamic radial clearance between helix flight and cylinder bore prevents binding.
- **Vertical Reaction Guide & Viewing Window:** A $12.0\text{ mm}$ wide vertical slot along the front of the cylinder from $Z = 22\text{ mm}$ to $Z = 125\text{ mm}$.
  - The clockwise helical flight pushes the marble against the vertical stationary edge of the window slot.
  - The stationary wall supplies a normal reaction force $F_{rxn} = N \sin(\alpha)$, canceling azimuthal rotation.
  - The advancing helical incline $N \cos(\alpha)$ drives the ball vertically upward along the slot line.
  - Because the marble is **$16.0\text{ mm}$** and the window is **$12.0\text{ mm}$**, the marble physically cannot escape the tower.

---

### 3. Track Cross-Section Kinematics (Page 2 Blueprint)

#### 3.1 Semicircular Round-Bottom U-Profile
Page 2 shows the cross-section of the path in which the marble fits:
- **Inner Profile:** Semicircular bottom arc of radius $R_{in} = 9.0\text{ mm}$ (inner diameter $18.0\text{ mm}$ for $16.0\text{ mm}$ ball $\to 1.0\text{ mm}$ lateral clearance per side).
- **Vertical Walls:** Extend upward by $H_{wall} = 6.0\text{ mm}$ from the center of the arc, with $2.5\text{ mm}$ wall thickness.
- **Total Depth:** $9.0\text{ mm} + 6.0\text{ mm} = 15.0\text{ mm}$, keeping the marble contained through high-speed turns.
- **Contact Line Physics:** Because the bottom is circular with $R_{in} = 9.0\text{ mm}$ and the ball has $R_b = 8.0\text{ mm}$, the marble establishes a single-point bottom rolling contact line, minimizing lateral scrubbing friction.

---

### 4. Continuous Gravity Route Kinematics & Slopes

#### 4.1 Kinematic Elevation Budget

| Track Segment | Start Elevation ($Z_1$) | End Elevation ($Z_2$) | Drop ($\Delta Z$) | Developed Length ($L$) | Mean Slope Angle | Feature / Blueprint Reference |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **1. Concentric Spiral Track** | 138.0 mm | 95.0 mm | 43.0 mm | ~720 mm | ~3.4° – 5.5° | Multi-turn concentric loops around tower & base (Page 1) |
| **2. Curved Hurdle Section** | 95.0 mm | 70.0 mm | 25.0 mm | ~175 mm | ~8.1° | 22mm channel, 9mm walls, 7 staggered posts (Page 3) |
| **3. Infinity Loop (Upper Bridge)**| 70.0 mm | 56.0 mm | 14.0 mm | ~110 mm | ~7.2° | Figure-eight left loop, crossing over at Z=56mm (Page 1) |
| **4. Infinity Loop (Lower Underpass)**| 56.0 mm | 28.0 mm | 28.0 mm | ~210 mm | ~7.6° | Descending loop passing under bridge at Z=28mm (Page 1) |
| **5. Infinity Exit to Return Ramp** | 28.0 mm | 18.0 mm | 10.0 mm | ~75 mm | ~7.6° | Leads directly toward Entry channel |
| **6. Entry Path Channel** | 18.0 mm | 6.0 mm | 12.0 mm | ~60 mm | ~11.3° | Tangential lead-in into cylinder bottom inlet port |
| **TOTAL GRAVITY COURSE** | **138.0 mm** | **6.0 mm** | **132.0 mm** | **~1350 mm (1.35 m)** | **~5.6° Average** | **Continuous Autonomous Cycle** |

#### 4.2 Infinity Crossover Headroom Validation
At the 3D crossover point $(X = -70.0, Y = -15.0)$:
- **Upper Bridge Floor:** $Z_{upper} = 56.0\text{ mm}$ (underside at $Z = 53.0\text{ mm}$).
- **Lower Underpass Floor:** $Z_{lower} = 28.0\text{ mm}$.
- **Vertical Floor Separation:** $\Delta Z = 56.0 - 28.0 = \mathbf{28.0\text{ mm}}$.
- **Marble Top Apex on Lower Track:** $28.0 + 16.0 = 44.0\text{ mm}$.
- **Net Headroom Clearance:** $53.0 - 44.0 = \mathbf{9.0\text{ mm}}$ of free air clearance above the marble.

---

### 5. Motor Sizing & Drive Calculations

- **Load Mass:** $m = 0.0168\text{ kg}$ (16.8 g for steel marble).
- **Lift Height:** $\Delta Z = 132.0\text{ mm}$, pitch $P = 26.0\text{ mm/rev}$.
- **Speed:** At $N = 45\text{ RPM}$, lift speed $v = 19.5\text{ mm/s}$ (climb time $\approx 6.8\text{ s}$).
- **Torque Requirement:**
  $$T_{load} \approx F_g \cdot \left[ \frac{\sin(\alpha) + \mu \cos(\alpha)}{\cos(\alpha) - \mu \sin(\alpha)} \right] \cdot R_{mean} \approx 0.0137\text{ kg}\cdot\text{cm}$$
  With 3 marbles queued in the helix and bearing friction, maximum torque demand is $T_{demand} \approx 0.091\text{ kg}\cdot\text{cm}$.
- **Selected Motor:** Standard GA25-370 or Yellow TT DC Geared Motor ($6\text{V}–12\text{V}$, $45\text{ RPM}$, Rated Torque $1.20\text{ kg}\cdot\text{cm}$).
- **Safety Factor:** $\text{SF} = \frac{1.20}{0.091} \approx \mathbf{13.2\times}$ (and $> 80\times$ against a single marble).

---

### 6. Summary of Manufacturing Specifications

1. **3D Printing Material:** PLA or PETG (0.20 mm layer height, 0.4 mm nozzle).
2. **Total Printed Mass:** ~512.9 grams (at 20% infill, 4 perimeters) — comfortably under a single 1 kg filament spool.
3. **Hardware Requirements:** 1× DC Gear Motor, 1× KCD1 Rocker Switch, 1× DC 5.5×2.1 mm Jack, 12× M3 Brass Inserts, 8× M3×12 mm Screws, 4× M3×10 mm Screws, 2× M3×5 mm Grub Screws, 3–5× Ø16 mm Marbles.
