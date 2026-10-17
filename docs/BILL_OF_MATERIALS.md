# BILL OF MATERIALS (BOM) - REVISION 2 (BLUEPRINT COMPLIANT)
## Continuous-Loop Motor-Driven Marble Race Machine
**Document Reference:** MR-BOM-002  
**Target Marble Diameter:** 16.0 mm (Standard Glass or Steel Ball)  
**Overall Footprint:** 300 mm (Octagonal Flat-to-Flat) × 201.8 mm (Total Height)  

---

### 1. Custom 3D Printed Components (FDM)

| Item # | Part Name | File Name (STEP / STL) | Qty | Material | Recommended Infill / Walls | Est. Mass (g) | Key Function / Features |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---|
| **1** | Octagonal Base Enclosure | `octagonal_base` | 1 | PLA / PETG | 20% Infill, 4 Perimeters | ~210.0 | Houses motor, wiring, switch, power jack. 50.8 mm depth, 3 mm walls. |
| **2** | Removable Top Lid | `base_lid` | 1 | PLA / PETG | 25% Infill, 4 Perimeters | ~110.5 | 3 mm deck with counterbored M3 screw holes, drive shaft port, 6 pillar sockets. |
| **3** | Central Hollow Tower | `central_tower` | 1 | PLA / PETG | 30% Infill, 4 Perimeters | ~38.3 | Ø60mm OD / Ø54mm ID, 140mm H. Front 12mm viewing slot, 9 o'clock inlet, 12 o'clock exit. |
| **4** | Tower Top Cap / Bushing | `tower_top_cap` | 1 | PETG / Nylon | 40% Infill, 4 Perimeters | ~16.8 | Upper stabilizing bushing for Ø6mm helix pivot pin. Slip-fits into tower rebate. |
| **5** | Rotating Helix Elevator | `rotating_helix` | 1 | PLA / PETG | 30% Infill, 4 Perimeters | ~27.5 | Archimedes lifting screw, Ø50mm flight, Ø14mm shaft, 26mm pitch, 3mm flight blade. |
| **6** | Helix Shaft Coupler | `helix_shaft_coupler` | 1 | PETG / Tough | 60% Infill, 5 Perimeters | ~3.0 | Adapts Ø8mm helix lower D-shaft to Ø6mm motor shaft with dual M3 set-screws. |
| **7** | Motor Mount Bracket | `motor_mount_bracket` | 1 | PETG / PLA | 40% Infill, 4 Perimeters | ~8.3 | Slotted L-bracket supporting GA25-370 / TT DC gear motors with height adjustment. |
| **8** | Power Rocker Switch Bezel| `switch_rocker` | 1 | PLA | 20% Infill, 3 Perimeters | ~2.9 | Physical mock-up bezel for standard KCD1 rocker switch (19.5 × 13 mm). |
| **9** | Concentric Spiral Track | `perimeter_track` | 1 | PLA | 25% Infill, 4 Perimeters | ~34.0 | Multi-turn concentric spiral U-channel (R_in=9mm round bottom, Z=138mm to Z=95mm). |
| **10** | Curved Hurdle Section | `obstacle_section` | 1 | PLA | 30% Infill, 4 Perimeters | ~11.0 | 22mm channel, 9mm walls, 7 staggered Ø4.5mm collision posts (Z=95mm to Z=70mm). |
| **11** | Infinity (Figure-8) Loop| `infinity_loop` | 1 | PLA | 25% Infill, 4 Perimeters | ~13.0 | Lemniscate crossover track on left. Upper bridge Z=56mm, lower bridge Z=28mm (28mm gap). |
| **12** | Entry Path Channel | `entry_return_guide` | 1 | PLA | 30% Infill, 4 Perimeters | ~2.0 | Smooth descending chute from Z=18mm to Z=6mm feeding into tower inlet port. |
| **13** | Modular Track Supports | `track_supports` | 1 set (6 pillars) | PLA / PETG | 35% Infill, 4 Perimeters | ~35.0 | Set of 6 calibrated pillars with 9mm base spigots and top cradle alignment pins. |
| **—** | **Subtotal Printed Parts** | — | **18 pcs** | — | — | **~512.9 g** | **< 0.55 kg (Single spool of filament)** |

---

### 2. Commercial Off-The-Shelf (COTS) Hardware & Fasteners

| Item # | Component Description | Specification / Standard | Qty | Purpose / Placement |
|:---:|:---|:---|:---:|:---|
| **C-1** | DC Geared Motor | 6V–12V DC, 30–60 RPM, Torque ≥ 1.0 kg·cm (e.g. GA25-370 or Yellow TT Dual Shaft) | 1 | Primary elevator drive motor housed inside the base cavity. |
| **C-2** | Power Rocker Switch | KCD1 Miniature SPST Snap-in Rocker (Panel cutout 19.5 × 13.0 mm) | 1 | Main ON/OFF power control on octagonal side face. |
| **C-3** | DC Power Jack (or Battery Holder) | 5.5 × 2.1 mm Barrel Socket (Ø8.0 mm hole) OR 4×AA Battery Box (6V) | 1 | Power input to motor and switch circuit. |
| **C-4** | Steel or Glass Marbles | Ø16.0 mm (±0.2 mm tolerance), Mass: 5.5 g (Glass) or 16.5 g (Chrome Steel) | 3–5 | Racing marbles for continuous operation. |
| **C-5** | Lid Fastener Screws | M3 × 12 mm Socket Head Cap Screws (DIN 912, Stainless Steel) | 8 | Secure removable top lid into base corner mounting bosses. |
| **C-6** | Tower Mounting Screws | M3 × 10 mm Socket Head Cap Screws (DIN 912) | 4 | Fasten central tower flange onto base lid threaded inserts. |
| **C-7** | Motor Mount Screws | M3 × 8 mm Button Head Screws + M3 Washers | 4 | Secure motor bracket to base floor and motor face to bracket. |
| **C-8** | Threaded Heat-Set Inserts | M3 × 4.0 mm OD × 4.5 mm Length (Brass, knurled) | 12 | Embedded in 8 base corner bosses and 4 tower lid mounting bosses. |
| **C-9** | Coupler Set-Screws | M3 × 5 mm Cone-Point Grub Screws (DIN 914) | 2 | Secure coupler onto motor shaft and helix D-shaft stub. |
| **C-10** | Lubricant (Optional) | Silicone Oil or Dry PTFE Powder Lubricant | 1 tube | Applied to tower inner bore, helix flight, and top bushing pin. |
