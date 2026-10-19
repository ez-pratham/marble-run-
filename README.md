# Merbl

![Merbl - 3D Printable Marble Run](image/final_assembly.jpeg)

Merbl is a 3d printable marble run made in freecad.

## What is it?

Merbl is a marble run designed in CAD software it is basically divided into three parts:

- **Funnel:** It is the starting parts marble is thrown into it.
  
  ![Funnel](image/funnel_design.jpeg)

- **Round Track:** It is the second parts which is in two parts straight and a round track with this marble rolls down.
  
  ![Round Track](image/spiral_track_1.jpeg)

- **Maze:** This is the last part here marble passes through a small maze and reaches the end.
  
  ![Maze](image/maze_design.jpeg)

## Why?

It is my hack club's week 2 project.

## Project Status

It's stl, cad files everthing is included. It full usable 3d printable marble run.

## Printing

As merbl uses a round track it need some tree support print that parts. Other parts can be printed normally only funnel support is suggested to printed upside down.

## Repository content

- **`CAD/`**: Editable FreeCAD source files (`.FCStd`) and neutral STEP files (`.step`)
  - `straight.FCStd` – Straight track section
  - `track.FCStd` – Round track section
  - `funnel.FCStd` – Vortex funnel model
  - `marble_run_assembly.step` – Complete assembly in STEP format
  - `ee.skp`, `Untitled.skp`, `xyz.skp` – SketchUp CAD models
- **`stl/`**: 3D printable models (`.stl`, `.3mf`)
  - `funnel.stl` – Funnel
  - `fsupport.stl` – Funnel support (print upside down)
  - `track1.stl` & `trackf.stl` – Round track segments
  - `straight1.stl` – Straight track section
  - `maze1.stl` – Maze
  - `base1.stl` – Hexagonal base
  - `support.stl` & `supportshort.stl` – Track support pillars
  - `s50.stl` – 50mm riser column
  - `trackm.3mf` – 3MF build plate project file
- **`image/`**: Photos, screenshots, and CAD renders of the project
- **`BOM.csv`**: Bill of Materials with pricing and supplier details
- **`JOURNAL.md`**: Complete day-by-day design and development journal
