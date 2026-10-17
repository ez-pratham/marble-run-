# STEP-BY-STEP ASSEMBLY INSTRUCTIONS (REVISION 2 - BLUEPRINT COMPLIANT)
## Continuous-Loop Motor-Driven Marble Race Machine
**Document Reference:** MR-ASM-002  
**Skill Level:** Beginner to Intermediate Maker  
**Estimated Assembly Time:** 45 – 60 minutes  

---

### Required Tools & Materials
1. **2.5 mm & 2.0 mm Hex Keys (Allen Wrenches)** for M3 socket head screws and set-screws.
2. **Soldering Iron** (set to ~220°C) with a conical tip (for pressing M3 brass heat-set inserts).
3. **Wire Strippers & Soldering Iron / Heat-Shrink** for connecting the DC motor, switch, and power jack.
4. **Fine Sandpaper / Needle File (240–400 grit)** for smoothing 3D-printed track joints.
5. **Silicone Grease or Dry PTFE Spray** for lubricating the elevator screw.

---

### Phase 1: Base Enclosure & Drive Sub-Assembly

```
       [Base Cavity Floor]
              │
         [M3 Inserts] (×4)
              │
    [Motor Mount Bracket] ◄── [Slotted Height & Radial Adjustment]
              │
       [DC Geared Motor]
              │
    [Helix Shaft Coupler] ◄── [Lower Bore Ø6.1mm + M3 Grub Screw]
```

1. **Install Base Threaded Inserts:**
   - Take the `octagonal_base`. Heat your soldering iron to ~220°C.
   - Press 8× M3 brass heat-set inserts into the vertical holes on top of the 8 corner mounting bosses until flush.
   - Press 4× M3 inserts into the central motor mounting platform on the base floor.
2. **Mount the DC Geared Motor:**
   - Fasten your DC gear motor to the `motor_mount_bracket` using 2× M3×8 mm button head screws.
   - Attach the motor bracket to the base floor bosses using 2× M3×8 mm screws through the slotted adjustment holes.
   - Keep screws finger-tight so the motor shaft can be adjusted directly beneath the lid center aperture.
3. **Install the Shaft Coupler:**
   - Slide the lower bore (Ø6.1 mm) of the `helix_shaft_coupler` onto the motor output shaft.
   - Align the lower M3 grub screw with the flat face of the motor D-shaft and tighten firmly.
4. **Wire the Power Switch & DC Jack:**
   - Snap the KCD1 rocker switch into the rectangular side opening (`19.5 × 13.0 mm`) from the outside until the plastic retention tabs click into place.
   - Insert the 5.5×2.1 mm DC barrel jack into the adjacent round hole (`Ø8.2 mm`) and tighten its hex nut.
   - Solder the circuit in series: `DC Jack (+) ──> Rocker Switch ──> Motor (+)`; `Motor (-) ──> DC Jack (-)`. Insulate with heat-shrink tubing.

---

### Phase 2: Lid & Central Elevator Sub-Assembly

```
      [Tower Top Cap / Bushing] (Upper Ø6.0mm Pin)
                 │
      [Central Hollow Cylinder] (Ø60mm OD / Ø54mm ID, 140mm H)
                 │
       [Rotating Helix Screw]   (Archimedes Flight, 26mm Pitch)
                 │
             [Base Lid]         (3mm Deck Plate, 6 Pillar Sockets)
                 │
     [M3 Screws into Base]      (×8 Perimeter Bosses)
```

1. **Install Lid & Check Shaft Protrusion:**
   - Lower the `base_lid` onto the `octagonal_base`. Ensure the 8 counterbored holes align with the 8 corner bosses.
   - Secure the lid with 8× M3×12 mm socket head cap screws.
   - Ensure the marble inlet sump notch at 9 o'clock ($X = -27\text{ mm}, Y = 0$) is clear and accessible.
2. **Insert the Rotating Helix Elevator:**
   - Take the `rotating_helix`. Lightly sand the helical flight edges to remove any stringing.
   - Apply a light film of PTFE spray or silicone oil to the flight and lower drive stub.
   - Lower the lower Ø8.0 mm shaft stub of the helix down through the central aperture of the lid and into the upper bore of the coupler.
   - Tighten the upper M3 grub screw on the coupler against the D-flat of the helix stub.
3. **Install the Central Hollow Cylinder:**
   - Slide the `central_tower` over the helix.
   - Orient the cylinder so that:
     - **Bottom Inlet Port** points toward 9 o'clock ($X = -30\text{ mm}, Y = 0$) matching the Entry channel.
     - **Top Exit Port** points toward 12 o'clock ($X = 0, Y = 30\text{ mm}$) to feed the clockwise spiral.
     - **Front Viewing Slot** faces forward (6 o'clock: $Y = -30\text{ mm}$).
   - Fasten the cylinder flange to the lid with 4× M3×10 mm screws.
4. **Install the Top Cap Bushing:**
   - Place a drop of lubricant into the center bore of the `tower_top_cap`.
   - Slip the cap over the upper Ø6.0 mm pivot pin of the helix and press the spigot into the top rebate of the cylinder until fully seated.
   - **Spin Check:** Rotate the helix by hand. It should spin freely with zero binding.

---

### Phase 3: Track Integration & Pillar Supports

```
 [Concentric Spiral Track] ──> [Curved Hurdle Section] ──> [Infinity Crossover] ──> [Entry Path]
            │                           │                          │                     │
    [Pillars 1, 2, 3]               [Pillar 4]                 [Pillar 5]            [Pillar 6]
            └───────────────────────────┴──────────────────────────┴─────────────────────┘
                                        [Base Lid Sockets]
```

1. **Insert Support Pillars:**
   - Insert the 6 locating spigots of `track_supports` into their corresponding 9.0 mm circular sockets on the lid:
     - **Pillar 1** ($H = 115.5\text{ mm}$): High spiral socket at $(60, 0)$.
     - **Pillar 2** ($H = 102.5\text{ mm}$): Mid spiral socket at $(-85, 0)$.
     - **Pillar 3** ($H = 92.5\text{ mm}$): Outer perimeter socket at $(0, 115)$.
     - **Pillar 4** ($H = 76.0\text{ mm}$): Hurdle section socket at $(0, -105)$.
     - **Pillar 5** ($H = 46.5\text{ mm}$): Dual crossover tower at $(-70, -15)$.
     - **Pillar 6** ($H = 4.5\text{ mm}$): Entry ramp socket at $(-45, 0)$.
2. **Install Concentric Spiral Track:**
   - Seat the entrance of `perimeter_track` against the top outlet port of the cylinder at $(0, 34, 138)$.
   - Click the underside lugs onto Pillars 1, 2, and 3. The smooth spiral will sweep around the tower and base.
3. **Install Curved Hurdle Section:**
   - Connect `obstacle_section` to the end of the spiral track at $(54.5, -106.9, 95)$.
   - Seat its center lug onto Pillar 4.
   - Ensure the 7 staggered collision posts are upright and clean.
4. **Install Infinity Loop:**
   - Connect the upper deck entrance of `infinity_loop` to the hurdle exit at $(-84.6, -43.1, 70)$.
   - Seat the crossover junction onto Pillar 5.
   - Verify that the upper bridge ($Z = 56\text{ mm}$) passes squarely over the lower bridge ($Z = 28\text{ mm}$) with 9 mm of open headroom above the 16 mm marble.
5. **Install Entry Channel:**
   - Connect `entry_return_guide` from the infinity loop exit $(-52, -5, 18)$ to Pillar 6.
   - Insert the exit tongue of the guide directly into the 9 o'clock bottom inlet port of the cylinder at $Z = 6\text{ mm}$.

---

### Phase 4: Calibration & Autonomous Operation

1. **Dry-Run Gravity Roll Test:**
   - Place a 16 mm marble at the top of the spiral ($Z = 138\text{ mm}$) and release it.
   - The marble will accelerate smoothly along the concentric spiral loops.
   - Enter the curved hurdle section, bounce off the 7 collision posts to scrub excess speed, and exit smoothly.
   - Traverse the figure-eight infinity loop on the left, pass under the crossover bridge without touching the overhead track, and drop into the Entry channel.
   - Roll smoothly into the elevator inlet pocket.
2. **Motor Power-On Test:**
   - Connect DC power (6V–12V) and switch the unit ON.
   - Drop the marble into the Entry channel.
   - The rotating helix scoops the marble up. As the screw turns, the marble is guided upward along the front slot edge.
   - At the top exit, the marble transfers onto the spiral track and completes the cycle autonomously!
