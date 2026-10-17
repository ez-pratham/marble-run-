"""
Geometry generator for Octagonal Base Enclosure and Removable Lid.
Updated to support blueprint layout with entry port on the left
and 6 dedicated pillar support sockets on the lid deck.
"""

from build123d import *
import math
from pathlib import Path
from parameters import PARAMS

def build_octagonal_base(p=PARAMS) -> Compound:
    """
    Builds the octagonal base enclosure.
    Distance across opposite flat sides: 300 mm.
    External depth: 50.8 mm.
    Base floor thickness: 3 mm.
    Side-wall thickness: 3 mm.
    Includes corner mounting bosses with M3 pilot holes,
    central motor mounting pad with slotted holes,
    and side cutouts for rocker switch and DC jack.
    """
    in_r = p.base_inradius      # 150 mm
    r_vertex_outer = in_r / math.cos(math.pi / 8) # ~162.36 mm
    r_vertex_inner = (in_r - p.base_wall_thick) / math.cos(math.pi / 8) # ~159.11 mm
    h = p.base_depth            # 50.8 mm
    t_wall = p.base_wall_thick  # 3 mm
    t_floor = p.base_floor_thick # 3 mm
    cavity_h = h - t_floor

    with BuildPart() as base:
        # 1. Outer Octagonal Solid Prism
        with BuildSketch(Plane.XY):
            RegularPolygon(radius=r_vertex_outer, side_count=8)
        extrude(amount=h)
        
        # 2. Hollow out cavity from top (Z = t_floor to h)
        with BuildSketch(Plane.XY.offset(t_floor)):
            RegularPolygon(radius=r_vertex_inner, side_count=8)
        extrude(amount=cavity_h + 1.0, mode=Mode.SUBTRACT)

        # 3. Add 8 Corner Mounting Bosses for M3 Lid Screws
        r_boss = (in_r - t_wall - 4.0) / math.cos(math.pi / 8)
        boss_pts = [
            (
                r_boss * math.cos(2 * math.pi * i / 8 + math.pi / 8),
                r_boss * math.sin(2 * math.pi * i / 8 + math.pi / 8),
            )
            for i in range(8)
        ]
        with BuildSketch(Plane.XY.offset(t_floor)):
            with Locations(boss_pts):
                Circle(radius=p.boss_outer_dia / 2.0)
        extrude(amount=cavity_h, mode=Mode.ADD)

        # Drill M3 pilot holes in bosses (depth 14mm from top)
        with BuildSketch(Plane.XY.offset(h - 14.0)):
            with Locations(boss_pts):
                Circle(radius=p.boss_hole_dia / 2.0)
        extrude(amount=15.0, mode=Mode.SUBTRACT)

        # 4. Central Motor Mounting Platform on the floor
        with BuildSketch(Plane.XY.offset(t_floor)):
            with Locations([(0, 0)]):
                Rectangle(70, 70)
        extrude(amount=6.0, mode=Mode.ADD)

        # Motor mounting screw holes (4x M3 on 50mm square pattern)
        motor_mount_pts = [
            (-25, -25), (25, -25), (25, 25), (-25, 25)
        ]
        with BuildSketch(Plane.XY.offset(t_floor)):
            with Locations(motor_mount_pts):
                Circle(radius=p.boss_hole_dia / 2.0)
        extrude(amount=7.0, mode=Mode.SUBTRACT)

        # Center motor shaft / wiring pass-through pocket
        with BuildSketch(Plane.XY.offset(t_floor)):
            with Locations([(0, 0)]):
                Circle(radius=12.0)
        extrude(amount=7.0, mode=Mode.SUBTRACT)

        # 5. Switch & DC Jack Cutout on one flat side face (at y = -in_r)
        with BuildSketch(Plane.XZ.offset(-in_r)):
            with Locations([(-25, h / 2.0)]):
                Rectangle(p.switch_cutout_w, p.switch_cutout_h)
            with Locations([(25, h / 2.0)]):
                Circle(radius=p.dc_jack_dia / 2.0)
        extrude(amount=t_wall + 4.0, mode=Mode.SUBTRACT)

    return base.part.translate((0, 0, -h))


def build_base_lid(p=PARAMS) -> Compound:
    """
    Builds the removable top lid.
    Thickness: 3 mm.
    Includes 8 counterbored M3 screw holes matching base bosses,
    central aperture for drive shaft / coupler,
    4 tower flange bolt holes, marble inlet slot on the left,
    and 6 locating sockets for track support pillars.
    """
    in_r = p.base_inradius
    t_lid = p.lid_thick

    with BuildPart() as lid:
        # 1. Octagonal Plate
        with BuildSketch(Plane.XY):
            RegularPolygon(radius=in_r / math.cos(math.pi / 8), side_count=8)
        extrude(amount=t_lid)

        # 2. 8 Counterbored Holes for M3 Screws
        r_boss = (in_r - p.base_wall_thick - 4.0) / math.cos(math.pi / 8)
        boss_pts = [
            (
                r_boss * math.cos(2 * math.pi * i / 8 + math.pi / 8),
                r_boss * math.sin(2 * math.pi * i / 8 + math.pi / 8),
            )
            for i in range(8)
        ]
        with BuildSketch(Plane.XY):
            with Locations(boss_pts):
                Circle(radius=p.lid_screw_hole_dia / 2.0)
        extrude(amount=t_lid + 1.0, mode=Mode.SUBTRACT)

        with BuildSketch(Plane.XY.offset(t_lid - p.lid_counterbore_depth)):
            with Locations(boss_pts):
                Circle(radius=p.lid_counterbore_dia / 2.0)
        extrude(amount=p.lid_counterbore_depth + 1.0, mode=Mode.SUBTRACT)

        # 3. Central Drive Shaft Aperture
        with BuildSketch(Plane.XY):
            with Locations([(0, 0)]):
                Circle(radius=10.0)  # 20mm dia clearance for shaft/coupler
        extrude(amount=t_lid + 1.0, mode=Mode.SUBTRACT)

        # 4. Tower Mounting Holes (4x M3 on 70mm bolt circle, r=35mm)
        tower_bolt_pts = [
            (35 * math.cos(math.pi * i / 2 + math.pi / 4), 35 * math.sin(math.pi * i / 2 + math.pi / 4))
            for i in range(4)
        ]
        with BuildSketch(Plane.XY):
            with Locations(tower_bolt_pts):
                Circle(radius=p.lid_screw_hole_dia / 2.0)
        extrude(amount=t_lid + 1.0, mode=Mode.SUBTRACT)

        # 5. Marble Inlet Sump (at 9 o'clock: x = -27mm, y = 0)
        with BuildSketch(Plane.XY):
            with Locations([(-27.0, 0.0)]):
                Circle(radius=11.0)
        extrude(amount=t_lid + 1.0, mode=Mode.SUBTRACT)

        # 6. Sockets for Track Support Pillars (6 locating sockets matching the blueprint layout)
        support_locs = [
            (60.0, 0.0),    # Pillar 1 (High spiral)
            (-85.0, 0.0),   # Pillar 2 (Mid spiral)
            (0.0, 115.0),   # Pillar 3 (Outer perimeter)
            (0.0, -105.0),  # Pillar 4 (Hurdle center)
            (-70.0, -15.0), # Pillar 5 (Infinity crossover)
            (-45.0, 0.0),   # Pillar 6 (Entry ramp)
        ]
        with BuildSketch(Plane.XY.offset(t_lid - 1.5)):
            with Locations(support_locs):
                Circle(radius=4.5)  # 9mm dia socket, 1.5mm deep
        extrude(amount=2.0, mode=Mode.SUBTRACT)

    return lid.part

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "cad_models" / "parts"
    out_dir.mkdir(parents=True, exist_ok=True)
    print("Generating updated Base and Lid...")
    base = build_octagonal_base()
    lid = build_base_lid()
    export_step(base, str(out_dir / "octagonal_base.step"))
    export_stl(base, str(out_dir / "octagonal_base.stl"))
    export_step(lid, str(out_dir / "base_lid.step"))
    export_stl(lid, str(out_dir / "base_lid.stl"))
    print("Updated Base & Lid exported successfully!")
