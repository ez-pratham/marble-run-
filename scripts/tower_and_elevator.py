"""
Geometry generator for Central Hollow Tower, Rotating Helix Elevator,
Top Cap Bushing, Shaft Coupler, and Motor Mount Bracket.
Updated port orientations matching the blueprint:
- Inlet at 9 o'clock (facing -X) connecting from Entry channel.
- Outlet at 12 o'clock (facing +Y) feeding clockwise concentric spiral.
- Viewing / reaction slot on front face (facing -Y).
"""

from build123d import *
import math
from pathlib import Path
from parameters import PARAMS

def build_central_tower(p=PARAMS) -> Compound:
    """
    Builds the central hollow cylindrical tower.
    OD: 60 mm, ID: 54 mm, Height above lid: 140 mm.
    - Bottom mounting flange (OD 82mm, 4x M3 holes).
    - Bottom marble inlet at 9 o'clock (X = -30, Y = 0) for 16mm marble.
    - Top marble outlet at 12 o'clock (X = 0, Y = 30, Z = 138) for spiral track.
    - Front vertical viewing / anti-rotation slot (12mm width) at Y = -30.
    - Top rim rebate for top stabilizer cap.
    """
    r_out = p.tower_od / 2.0  # 30 mm
    r_in = p.tower_id / 2.0    # 27 mm
    h = p.tower_height         # 140 mm
    t_flange = p.tower_flange_thick # 4 mm
    r_flange = p.tower_flange_dia / 2.0 # 41 mm

    with BuildPart() as tower:
        # 1. Main Outer Cylinder
        with BuildSketch(Plane.XY):
            Circle(radius=r_out)
        extrude(amount=h)

        # 2. Bottom Mounting Flange
        with BuildSketch(Plane.XY):
            Circle(radius=r_flange)
        extrude(amount=t_flange, mode=Mode.ADD)

        # 3. Flange M3 Screw Clearance Holes (4x at r=35mm, 45 deg)
        flange_bolt_pts = [
            (35 * math.cos(math.pi * i / 2 + math.pi / 4), 35 * math.sin(math.pi * i / 2 + math.pi / 4))
            for i in range(4)
        ]
        with BuildSketch(Plane.XY):
            with Locations(flange_bolt_pts):
                Circle(radius=p.lid_screw_hole_dia / 2.0)
        extrude(amount=t_flange + 1.0, mode=Mode.SUBTRACT)

        # 4. Hollow Central Bore (ID 54 mm)
        with BuildSketch(Plane.XY):
            Circle(radius=r_in)
        extrude(amount=h + 2.0, mode=Mode.SUBTRACT)

        # 5. Bottom Marble Inlet Port at 9 o'clock (facing -X)
        # Sized 22 mm wide x 24 mm high at Z = 3 to 27 mm
        with BuildSketch(Plane.YZ.offset(-r_out - 5.0)):
            with Locations([(0, 14)]):
                Rectangle(p.tower_inlet_w, p.tower_inlet_h)
        extrude(amount=r_out + 10.0, mode=Mode.SUBTRACT)

        # 6. Top Marble Exit Port at 12 o'clock (facing +Y)
        # Sized 22 mm wide x 24 mm high at Z = 126 to 142 mm
        with BuildSketch(Plane.XZ.offset(r_out + 5.0)):
            with Locations([(0, h - 12)]):
                Rectangle(p.tower_exit_w, p.tower_exit_h)
        extrude(amount=-(r_out + 10.0), mode=Mode.SUBTRACT)

        # 7. Front Viewing & Reaction Guide Slot at 6 o'clock (facing -Y)
        # 12 mm wide, from Z = 22 to 125 mm
        with BuildSketch(Plane.XZ.offset(-r_out - 5.0)):
            with Locations([(0, (22 + 125) / 2.0)]):
                Rectangle(p.tower_view_slot_w, 125 - 22)
        extrude(amount=r_out + 10.0, mode=Mode.SUBTRACT)

        # 8. Top Cap Rebate (ID 57mm, depth 5mm)
        with BuildSketch(Plane.XY.offset(h - 5.0)):
            Circle(radius=28.5)
        extrude(amount=6.0, mode=Mode.SUBTRACT)

    return tower.part.translate((0, 0, p.lid_thick))


def build_tower_top_cap(p=PARAMS) -> Compound:
    """
    Builds the removable top cap / bushing for the tower.
    Provides upper axial alignment and smooth bushing for helix upper pivot pin.
    """
    h_cap = 8.0
    r_cap_out = p.tower_od / 2.0 # 30 mm
    r_spigot = 28.3               # Fits into 57mm rebate with 0.4mm clearance
    h_spigot = 4.5
    r_pin_bore = 3.2              # 6.4mm bore for 6mm upper pin

    with BuildPart() as cap:
        with BuildSketch(Plane.XY):
            Circle(radius=r_cap_out)
        extrude(amount=h_cap)

        with BuildSketch(Plane.XY):
            Circle(radius=r_spigot)
        extrude(amount=-h_spigot, mode=Mode.ADD)

        with BuildSketch(Plane.XY.offset(-h_spigot - 1)):
            Circle(radius=r_pin_bore)
        extrude(amount=h_cap + h_spigot + 2.0, mode=Mode.SUBTRACT)

    return cap.part.translate((0, 0, p.lid_thick + p.tower_height))


def build_rotating_helix(p=PARAMS) -> Compound:
    """
    Builds the rotating helix elevator (Archimedes screw).
    Core shaft: 14 mm diameter.
    Flight OD: 50 mm (trough width 18 mm for 16 mm marble).
    Pitch: 26 mm per revolution.
    Height: 138 mm (~5.3 full turns).
    Flight thickness: 3 mm.
    """
    r_core = p.helix_core_dia / 2.0   # 7 mm
    r_flight = p.helix_od / 2.0        # 25 mm
    flight_w = r_flight - r_core       # 18 mm
    pitch = p.helix_pitch              # 26 mm
    h_helix = p.helix_height           # 138 mm
    t_flight = p.helix_flight_thick    # 3 mm

    with BuildPart() as helix_assy:
        # Central shaft
        with BuildSketch(Plane.XY):
            Circle(radius=r_core)
        extrude(amount=h_helix)

        # Helical flight
        with BuildLine() as helix_path:
            h_line = Helix(pitch=pitch, height=h_helix, radius=(r_core + r_flight) / 2.0)
        with BuildSketch(Plane(origin=h_line @ 0, z_dir=h_line % 0)):
            Rectangle(flight_w + 2.0, t_flight)
        sweep(mode=Mode.ADD)

        # Lower drive shaft stub (Z = -20 to 0)
        with BuildSketch(Plane.XY):
            Circle(radius=p.helix_shaft_lower_dia / 2.0)
        extrude(amount=-p.helix_shaft_lower_len, mode=Mode.ADD)

        # D-flat on lower shaft
        with BuildSketch(Plane.YZ):
            with Locations([(0, -10)]):
                Rectangle(20, 20)
        extrude(amount=p.helix_shaft_lower_dia / 2.0 - 0.8, mode=Mode.SUBTRACT)

        # Upper pivot pin
        with BuildSketch(Plane.XY.offset(h_helix)):
            Circle(radius=p.helix_shaft_upper_dia / 2.0)
        extrude(amount=p.helix_shaft_upper_len, mode=Mode.ADD)

    return helix_assy.part.translate((0, 0, p.lid_thick + 3.0))


def build_shaft_coupler(p=PARAMS) -> Compound:
    """
    Builds the rigid motor-to-helix shaft coupling.
    OD: 18 mm, Length: 24 mm.
    """
    od = p.coupler_od
    l = p.coupler_len
    r_upper = (p.helix_shaft_lower_dia + 0.2) / 2.0
    r_lower = (p.motor_shaft_dia + 0.1) / 2.0

    with BuildPart() as coupler:
        with BuildSketch(Plane.XY):
            Circle(radius=od / 2.0)
        extrude(amount=l)

        # Upper bore
        with BuildSketch(Plane.XY.offset(l / 2.0)):
            Circle(radius=r_upper)
        extrude(amount=l / 2.0 + 1.0, mode=Mode.SUBTRACT)

        # Lower bore
        with BuildSketch(Plane.XY):
            Circle(radius=r_lower)
        extrude(amount=l / 2.0 + 0.5, mode=Mode.SUBTRACT)

        # Set screw holes
        with BuildSketch(Plane.XZ.offset(-od / 2.0 - 2.0)):
            with Locations([(0, l * 0.25), (0, l * 0.75)]):
                Circle(radius=p.coupler_set_screw_dia / 2.0)
        extrude(amount=od + 4.0, mode=Mode.SUBTRACT)

    return coupler.part.translate((0, 0, -p.base_depth / 2.0 + 10.0))


def build_motor_mount(p=PARAMS) -> Compound:
    """
    Builds the adjustable motor mounting bracket.
    """
    t = 3.5
    w = 60.0
    h = 42.0
    d = 45.0

    with BuildPart() as mount:
        with BuildSketch(Plane.XY):
            Rectangle(w, d)
        extrude(amount=t)

        with BuildSketch(Plane.XZ.offset(-d / 2.0)):
            with Locations([(0, h / 2.0)]):
                Rectangle(w, h)
        extrude(amount=t, mode=Mode.ADD)

        with BuildSketch(Plane.XY):
            with Locations([(-18, 5), (18, 5)]):
                SlotCenterToCenter(8, 4.0)
        extrude(amount=t + 2.0, mode=Mode.SUBTRACT)

        with BuildSketch(Plane.XZ.offset(-d / 2.0 - 1.0)):
            with Locations([(0, h / 2.0)]):
                Circle(radius=7.0)
        extrude(amount=t + 2.0, mode=Mode.SUBTRACT)

        with BuildSketch(Plane.XZ.offset(-d / 2.0 - 1.0)):
            with Locations([(-15.5, h / 2.0), (15.5, h / 2.0)]):
                SlotCenterToCenter(5, 3.4)
        extrude(amount=t + 2.0, mode=Mode.SUBTRACT)

    return mount.part.translate((0, 0, -p.base_depth + p.base_floor_thick))


def build_switch_rocker(p=PARAMS) -> Compound:
    """
    Builds 3D placeholder for the KCD1 rocker switch.
    """
    w = p.switch_cutout_w - 0.4
    h = p.switch_cutout_h - 0.4
    body_d = 18.0
    bezel_t = 2.0

    with BuildPart() as sw:
        with BuildSketch(Plane.XY):
            Rectangle(w + 3.0, h + 3.0)
        extrude(amount=bezel_t)

        with BuildSketch(Plane.XY):
            Rectangle(w, h)
        extrude(amount=-body_d, mode=Mode.ADD)

        with BuildSketch(Plane.XY.offset(bezel_t)):
            Rectangle(w - 2.0, h - 2.0)
        extrude(amount=4.0, mode=Mode.ADD)

    in_r = p.base_inradius
    return sw.part.rotate(Axis.X, -90).translate((-25, -in_r + 2.0, -p.base_depth / 2.0))


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "cad_models" / "parts"
    out_dir.mkdir(parents=True, exist_ok=True)
    print("Generating updated Tower and Elevator components...")

    tower = build_central_tower()
    export_step(tower, str(out_dir / "central_tower.step"))
    export_stl(tower, str(out_dir / "central_tower.stl"))

    top_cap = build_tower_top_cap()
    export_step(top_cap, str(out_dir / "tower_top_cap.step"))
    export_stl(top_cap, str(out_dir / "tower_top_cap.stl"))

    helix = build_rotating_helix()
    export_step(helix, str(out_dir / "rotating_helix.step"))
    export_stl(helix, str(out_dir / "rotating_helix.stl"))

    coupler = build_shaft_coupler()
    export_step(coupler, str(out_dir / "helix_shaft_coupler.step"))
    export_stl(coupler, str(out_dir / "helix_shaft_coupler.stl"))

    motor_mount = build_motor_mount()
    export_step(motor_mount, str(out_dir / "motor_mount_bracket.step"))
    export_stl(motor_mount, str(out_dir / "motor_mount_bracket.stl"))

    switch_part = build_switch_rocker()
    export_step(switch_part, str(out_dir / "switch_rocker.step"))
    export_stl(switch_part, str(out_dir / "switch_rocker.stl"))

    print("Tower & Drive components exported successfully!")
