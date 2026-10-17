# 📋 Bill of Materials (BOM) – Marble Run Mini Hack

**Project:** Marble Run Mini Hack (Hack Club Highway to Half-Life – Week 2)  
**Author:** Pratham Prajapati ([@ez-pratham](https://github.com/ez-pratham))  
**Target Ball / Marble:** Ø14.0 mm – Ø16.0 mm (Standard Glass or Steel Bearing Ball)  
**Printing Process:** Fused Deposition Modeling (FDM / 3D Printing)  
**Print Material:** PLA or PETG (~350 g total filament)  

---

## 1. 🖨️ 3D Printed Components (Custom CAD Models)

All 3D models are located in the [`stl/`](stl/) and [`CAD/`](CAD/) directories.

| Item # | Part Name | File Name (STL) | Source CAD | Qty | Recommended Material | Infill / Perimeters | Est. Print Time | Function & Placement |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|:---|
| **1** | Hexagonal Foundation Base | [`base1.stl`](stl/base1.stl) | `CAD/` | 1 | PLA / PETG | 15–20% Infill, 3 Walls | ~3.5 hrs | Rigid interlocking ground base; catches marbles and anchors upright pillars. |
| **2** | Conical Vortex Funnel | [`funnel.stl`](stl/funnel.stl) | [`funnel.FCStd`](CAD/funnel.FCStd) | 1 | PLA | 20% Infill, 3 Walls (0.16mm layer) | ~2.5 hrs | Upper infeed funnel; marbles swirl with increasing angular speed into central throat. |
| **3** | Funnel Cylindrical Support | [`fsupport.stl`](stl/fsupport.stl) | `CAD/` | 1 | PLA / PETG | 25% Infill, 4 Walls | ~3.0 hrs | Main vertical elevation tower supporting the vortex funnel. |
| **4** | Helical Spiral Track | [`track1.stl`](stl/track1.stl) | [`track.FCStd`](CAD/track.FCStd) | 1 | PLA | 20% Infill, 3 Walls | ~4.0 hrs | Banked U-channel descending spiral; preserves marble momentum without jumping off. |
| **5** | Spiral Transition Track | [`trackf.stl`](stl/trackf.stl) | [`track.FCStd`](CAD/track.FCStd) | 1 | PLA | 20% Infill, 3 Walls | ~3.5 hrs | Secondary spiral transition feed into downstream obstacles. |
| **6** | Straight Track Guide | [`straight1.stl`](stl/straight1.stl) | [`straight.FCStd`](CAD/straight.FCStd) | 1 | PLA | 20% Infill, 3 Walls | ~1.0 hr | Linear connecting track bridging vertical tower to the spiral descent. |
| **7** | Single-Entrance Maze | [`maze1.stl`](stl/maze1.stl) | `CAD/` | 1 | PLA | 20% Infill, 3 Walls | ~2.0 hrs | Kinetic obstacle course; single inlet challenge routing marble through labyrinth. |
| **8** | Standard Support Column | [`support.stl`](stl/support.stl) | `CAD/` | 1–2 | PLA / PETG | 25% Infill, 4 Walls | ~1.5 hrs | Mid-height structural riser supporting track incline. |
| **9** | Short Support Riser | [`supportshort.stl`](stl/supportshort.stl) | `CAD/` | 1–2 | PLA / PETG | 25% Infill, 4 Walls | ~1.0 hr | Lower riser maintaining slope before entering maze. |
| **10** | 50mm Riser Spacer | [`s50.stl`](stl/s50.stl) | `CAD/` | 1 | PLA / PETG | 25% Infill, 4 Walls | ~45 mins | Fine-tuning spacer column for height calibration. |
| **11** | Cura Build Plate Project | [`trackm.3mf`](stl/trackm.3mf) | Cura 3MF | 1 | — | Pre-sliced plate | — | Complete pre-oriented multi-part build plate. |

---

## 2. 🔩 Commercial Off-The-Shelf (COTS) Hardware & Consumables

| Item # | Component Name | Specification | Qty | Purpose / Notes |
|:---:|:---|:---|:---:|:---|
| **C-1** | Marbles | Ø14 mm – Ø16 mm Glass or Steel Bearing Balls | 3–5 pcs | Rolling projectiles tested for track clearance and weight. |
| **C-2** | 3D Printing Filament | 1.75 mm PLA or PETG (Any color) | ~350 g | Total filament required for all structural and track parts. |
| **C-3** | Adhesive / Bonding (Optional) | Cyanoacrylate (Super Glue) or 3D Gloop | 1 bottle | For permanent joint bonding between pillars and base if desired. |
| **C-4** | Non-slip Rubber Feet (Optional) | Self-adhesive silicone/rubber pads (Ø8–10 mm) | 4–6 pcs | Applied under hexagonal base to prevent table slippage during high-speed runs. |

---

## 3. ⚖️ Total Project Cost & Material Summary

- **Total 3D Printing Filament:** ~350 grams (~$7.00 USD equivalent)
- **COTS Hardware (Marbles, pads):** ~$2.00 – $4.00 USD
- **Total Estimated Build Cost:** **< $12.00 USD**
- **Filament Spools Needed:** 1 Standard 1 kg Spool (plenty of extra for testing and spares)
