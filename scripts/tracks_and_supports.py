"""
Geometry generator for Track Sections, Obstacle Section,
Infinity Return Loop, Entry Channel, and Support Pillars.
Directly implements the user concept blueprint (Pages 1, 2, 3):
- Multi-turn concentric spiral loops around cylinder and base.
- Semicircular round-bottom U-channel cross-section (Page 2).
- Curved rectangular hurdle section with raised walls and staggered pins (Page 3).
- Infinity (figure-eight) loop on left side connecting to Entry (Page 1).
"""

from build123d import *
import math
import numpy as np
from pathlib import Path
from parameters import PARAMS

def sweep_u_channel_along_points(pts, w_outer=23.0, h_outer=13.0, w_inner=18.0, h_inner=12.0) -> Compound:
    """
    Sweeps a filleted round-bottom U-channel (Page 2 Blueprint) along a 3D spline trajectory.
    Inner width = 18.0 mm (fits 16mm marble with 1mm clearance on each side).
    Wall thickness = 2.5 mm, outer width = 23.0 mm.
    Inner floor filleted with R = 6.0 mm, outer bottom filleted with R = 7.0 mm.
    """
    with BuildPart() as p:
        with BuildLine() as path:
            spl = Spline(pts)
        tang = spl % 0
        w_dir = tang.cross(Vector(0, 0, 1)).normalized()
        pln = Plane(origin=spl @ 0, x_dir=w_dir, z_dir=tang)
        
        with BuildSketch(pln) as s:
            Rectangle(w_outer, h_outer)
            bot_v = s.vertices().sort_by(Axis.Y)[:2]
            fillet(bot_v, radius=7.0)
            with BuildSketch(mode=Mode.SUBTRACT) as inner:
                with Locations([(0, 1.5)]):
                    Rectangle(w_inner, h_inner)
                    in_v = inner.vertices().sort_by(Axis.Y)[:2]
                    fillet(in_v, radius=6.0)
        sweep()
    return p.part

def sweep_rectangular_channel(pts, w_inner=22.0, h_wall=9.0, t_floor=3.0, t_wall=2.5) -> Compound:
    """
    Sweeps a rectangular open channel with raised side walls (Page 3 Blueprint)
    for the curved obstacle section.
    """
    w_outer = w_inner + 2.0 * t_wall
    h_outer = h_wall + t_floor

    with BuildPart() as p:
        with BuildLine() as path:
            spl = Spline(pts)
        tang = spl % 0
        w_dir = tang.cross(Vector(0, 0, 1)).normalized()
        pln = Plane(origin=spl @ 0, x_dir=w_dir, z_dir=tang)
        
        with BuildSketch(pln):
            with BuildSketch():
                with Locations([(0, (h_wall - t_floor) / 2.0)]):
                    Rectangle(w_outer, h_outer)
                with Locations([(0, (h_wall + 1.0) / 2.0)]):
                    Rectangle(w_inner, h_wall + 1.0, mode=Mode.SUBTRACT)
        sweep()
    return p.part


def build_perimeter_track(p=PARAMS) -> Compound:
    """
    Builds the concentric multi-turn spiral perimeter track (Page 1 Blueprint).
    Starts at cylinder top exit (0, 34, 138), spirals smoothly clockwise
    around the cylinder and the octagonal base, dropping steadily to (54.5, -106.9, 95.0).
    """
    theta = np.linspace(np.pi / 2, -2.35 * np.pi, 60)
    r = np.linspace(34.0, 120.0, 60)
    z = np.linspace(p.z_tower_exit, p.z_obstacle_start, 60)
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    pts = [(float(x[i]), float(y[i]), float(z[i])) for i in range(len(theta))]

    track_solid = sweep_u_channel_along_points(pts)

    # Underside mounting lugs for Pillar 1 (index 15), Pillar 2 (index 35), Pillar 3 (index 52)
    lug_pts = [pts[15], pts[35], pts[52]]
    with BuildPart() as assy:
        insert(track_solid)
        for pt in lug_pts:
            with BuildSketch(Plane.XY.offset(pt[2] - 6.5 - 3.0)):
                with Locations([(pt[0], pt[1])]):
                    Circle(radius=5.5)
            extrude(amount=4.0, mode=Mode.ADD)
            with BuildSketch(Plane.XY.offset(pt[2] - 6.5 - 4.0)):
                with Locations([(pt[0], pt[1])]):
                    Circle(radius=2.6)
            extrude(amount=5.0, mode=Mode.SUBTRACT)

    return assy.part


def build_obstacle_section(p=PARAMS) -> Compound:
    """
    Builds the curved rectangular hurdle section (Pages 1 & 3 Blueprint).
    Sweeps along the front arc of the octagonal base from (54.5, -106.9, 95)
    to (-84.6, -43.1, 70).
    Features raised side walls (9mm) and 7 staggered collision posts.
    """
    theta = np.linspace(-2.35 * np.pi, -2.85 * np.pi, 30)
    r = np.linspace(120.0, 95.0, 30)
    z = np.linspace(p.z_obstacle_start, p.z_infinity_start, 30)
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    pts = [(float(x[i]), float(y[i]), float(z[i])) for i in range(len(theta))]

    channel_solid = sweep_rectangular_channel(
        pts,
        w_inner=p.hurdle_channel_w,
        h_wall=p.hurdle_wall_h,
        t_floor=p.track_floor_thick,
        t_wall=p.track_wall_thick
    )

    t_vals = np.linspace(0.15, 0.85, p.hurdle_pin_count)
    lat_offsets = [4.0, -4.0, 4.0, -4.0, 4.0, -4.0, 3.5]

    with BuildPart() as obs:
        insert(channel_solid)
        with BuildLine() as path_line:
            spl = Spline(pts)
        for i, (t_val, lat_off) in enumerate(zip(t_vals, lat_offsets)):
            pos = spl @ t_val
            tang = spl % t_val
            lat_vec = tang.cross(Vector(0, 0, 1)).normalized()
            post_center = pos + lat_vec * lat_off

            with BuildSketch(Plane.XY.offset(post_center.Z)):
                with Locations([(post_center.X, post_center.Y)]):
                    Circle(radius=p.hurdle_pin_dia / 2.0)
            extrude(amount=p.hurdle_pin_h, mode=Mode.ADD)

        # Underside mounting lug for Pillar 4
        mid_pt = pts[15]
        with BuildSketch(Plane.XY.offset(mid_pt[2] - p.track_floor_thick - 3.0)):
            with Locations([(mid_pt[0], mid_pt[1])]):
                Circle(radius=5.5)
        extrude(amount=4.0, mode=Mode.ADD)
        with BuildSketch(Plane.XY.offset(mid_pt[2] - p.track_floor_thick - 4.0)):
            with Locations([(mid_pt[0], mid_pt[1])]):
                Circle(radius=2.6)
        extrude(amount=5.0, mode=Mode.SUBTRACT)

    return obs.part


def build_infinity_loop(p=PARAMS) -> Compound:
    """
    Builds the infinity-shaped (figure-eight) return loop on the left side
    (Page 1 Blueprint: 'last infinite loop ends on entry').
    Upper deck crosses over at Z = 56 mm, loops around upper lobe,
    passes under at Z = 28 mm (28mm vertical clearance), and exits toward entry.
    """
    pts = [
        (-84.6, -43.1, p.z_infinity_start), # Entry from obstacle
        (-105.0, -40.0, 65.0),
        (-115.0, -20.0, 60.0),              # Lower lobe apex
        (p.crossover_x, p.crossover_y, p.z_crossover_upper), # CROSSOVER POINT UPPER (Z=56)
        (-50.0, 10.0, 48.0),
        (-70.0, 35.0, 42.0),                # Upper lobe apex
        (-95.0, 20.0, 35.0),
        (p.crossover_x, p.crossover_y, p.z_crossover_lower), # CROSSOVER POINT LOWER (Z=28)
        (-52.0, -5.0, p.z_return_ramp_start), # Exit to entry channel
    ]

    loop_solid = sweep_u_channel_along_points(pts)

    # Underside mounting lug for dual crossover tower Pillar 5
    with BuildPart() as assy:
        insert(loop_solid)
        with BuildSketch(Plane.XY.offset(p.z_crossover_lower - 6.5 - 3.0)):
            with Locations([(p.crossover_x, p.crossover_y)]):
                Circle(radius=5.5)
        extrude(amount=4.0, mode=Mode.ADD)
        with BuildSketch(Plane.XY.offset(p.z_crossover_lower - 6.5 - 4.0)):
            with Locations([(p.crossover_x, p.crossover_y)]):
                Circle(radius=2.6)
        extrude(amount=5.0, mode=Mode.SUBTRACT)

    return assy.part


def build_entry_return_guide(p=PARAMS) -> Compound:
    """
    Builds the Entry channel (Page 1 Blueprint: 'Entry' cyan path).
    Connects from infinity loop exit (-52, -5, 18) straight into
    the central tower bottom inlet port (-27, 0, 6).
    """
    pts = [
        (-52.0, -5.0, p.z_return_ramp_start),
        (-40.0, -2.0, 12.0),
        (-27.0, 0.0, p.z_tower_inlet),
        (-18.0, 0.0, p.z_tower_inlet), # Feeds tangentially into tower inner flight
    ]

    guide_solid = sweep_u_channel_along_points(pts)

    # Add support foot resting on base lid (Z = p.lid_thick = 3.0)
    with BuildPart() as guide:
        insert(guide_solid)
        with BuildSketch(Plane.XY.offset(p.lid_thick)):
            with Locations([(-40.0, -2.0)]):
                Circle(radius=5.0)
        extrude(amount=6.5, mode=Mode.ADD)

    return guide.part


def build_track_supports(p=PARAMS) -> Compound:
    """
    Builds the set of 6 modular track support pillars matching the blueprint layout.
    Features bottom locating spigots (fit into 9mm lid sockets) and top alignment pins.
    """
    with BuildPart() as pillars:
        # Pillar 1 (High spiral support at 60, 0): Z_top approx 125 mm
        h1 = 125.0 - 6.5 - p.lid_thick
        with BuildSketch(Plane.XY.offset(p.lid_thick - 1.5)):
            with Locations([(60.0, 0.0)]):
                Circle(radius=4.3)
        extrude(amount=1.5, mode=Mode.ADD)
        with BuildSketch(Plane.XY.offset(p.lid_thick)):
            with Locations([(60.0, 0.0)]):
                Circle(radius=7.0)
        extrude(amount=h1, mode=Mode.ADD)
        with BuildSketch(Plane.XY.offset(p.lid_thick + h1)):
            with Locations([(60.0, 0.0)]):
                Circle(radius=2.4)
        extrude(amount=4.0, mode=Mode.ADD)

        # Pillar 2 (Mid spiral support at -85, 0): Z_top approx 112 mm
        h2 = 112.0 - 6.5 - p.lid_thick
        with BuildSketch(Plane.XY.offset(p.lid_thick - 1.5)):
            with Locations([(-85.0, 0.0)]):
                Circle(radius=4.3)
        extrude(amount=1.5, mode=Mode.ADD)
        with BuildSketch(Plane.XY.offset(p.lid_thick)):
            with Locations([(-85.0, 0.0)]):
                Circle(radius=7.0)
        extrude(amount=h2, mode=Mode.ADD)
        with BuildSketch(Plane.XY.offset(p.lid_thick + h2)):
            with Locations([(-85.0, 0.0)]):
                Circle(radius=2.4)
        extrude(amount=4.0, mode=Mode.ADD)

        # Pillar 3 (Outer perimeter spiral support at 0, 115): Z_top approx 102 mm
        h3 = 102.0 - 6.5 - p.lid_thick
        with BuildSketch(Plane.XY.offset(p.lid_thick - 1.5)):
            with Locations([(0.0, 115.0)]):
                Circle(radius=4.3)
        extrude(amount=1.5, mode=Mode.ADD)
        with BuildSketch(Plane.XY.offset(p.lid_thick)):
            with Locations([(0.0, 115.0)]):
                Circle(radius=7.0)
        extrude(amount=h3, mode=Mode.ADD)
        with BuildSketch(Plane.XY.offset(p.lid_thick + h3)):
            with Locations([(0.0, 115.0)]):
                Circle(radius=2.4)
        extrude(amount=4.0, mode=Mode.ADD)

        # Pillar 4 (Obstacle section support at 0, -105): Z_top approx 82 mm
        h4 = 82.0 - p.track_floor_thick - p.lid_thick
        with BuildSketch(Plane.XY.offset(p.lid_thick - 1.5)):
            with Locations([(0.0, -105.0)]):
                Circle(radius=4.3)
        extrude(amount=1.5, mode=Mode.ADD)
        with BuildSketch(Plane.XY.offset(p.lid_thick)):
            with Locations([(0.0, -105.0)]):
                Circle(radius=7.0)
        extrude(amount=h4, mode=Mode.ADD)
        with BuildSketch(Plane.XY.offset(p.lid_thick + h4)):
            with Locations([(0.0, -105.0)]):
                Circle(radius=2.4)
        extrude(amount=4.0, mode=Mode.ADD)

        # Pillar 5 (Infinity crossover dual tower at -70, -15): Z_top upper = 56 mm
        h5 = p.z_crossover_upper - 6.5 - p.lid_thick
        with BuildSketch(Plane.XY.offset(p.lid_thick - 1.5)):
            with Locations([(p.crossover_x, p.crossover_y)]):
                Circle(radius=4.3)
        extrude(amount=1.5, mode=Mode.ADD)
        with BuildSketch(Plane.XY.offset(p.lid_thick)):
            with Locations([(p.crossover_x, p.crossover_y)]):
                Circle(radius=8.0)
        extrude(amount=h5, mode=Mode.ADD)
        with BuildSketch(Plane.XY.offset(p.lid_thick + h5)):
            with Locations([(p.crossover_x, p.crossover_y)]):
                Circle(radius=2.4)
        extrude(amount=4.0, mode=Mode.ADD)

        # Pillar 6 (Entry ramp support at -45, 0): Z_top approx 14 mm
        h6 = 14.0 - 6.5 - p.lid_thick
        with BuildSketch(Plane.XY.offset(p.lid_thick - 1.5)):
            with Locations([(-45.0, 0.0)]):
                Circle(radius=4.3)
        extrude(amount=1.5, mode=Mode.ADD)
        with BuildSketch(Plane.XY.offset(p.lid_thick)):
            with Locations([(-45.0, 0.0)]):
                Circle(radius=6.0)
        extrude(amount=h6, mode=Mode.ADD)
        with BuildSketch(Plane.XY.offset(p.lid_thick + h6)):
            with Locations([(-45.0, 0.0)]):
                Circle(radius=2.4)
        extrude(amount=3.0, mode=Mode.ADD)

    return pillars.part


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "cad_models" / "parts"
    out_dir.mkdir(parents=True, exist_ok=True)
    print("Generating updated Track Sections and Supports matching Blueprint...")

    perimeter = build_perimeter_track()
    export_step(perimeter, str(out_dir / "perimeter_track.step"))
    export_stl(perimeter, str(out_dir / "perimeter_track.stl"))
    print("Exported perimeter_track")

    obstacle = build_obstacle_section()
    export_step(obstacle, str(out_dir / "obstacle_section.step"))
    export_stl(obstacle, str(out_dir / "obstacle_section.stl"))
    print("Exported obstacle_section")

    infinity = build_infinity_loop()
    export_step(infinity, str(out_dir / "infinity_loop.step"))
    export_stl(infinity, str(out_dir / "infinity_loop.stl"))
    print("Exported infinity_loop")

    guide = build_entry_return_guide()
    export_step(guide, str(out_dir / "entry_return_guide.step"))
    export_stl(guide, str(out_dir / "entry_return_guide.stl"))
    print("Exported entry_return_guide")

    supports = build_track_supports()
    export_step(supports, str(out_dir / "track_supports.step"))
    export_stl(supports, str(out_dir / "track_supports.stl"))
    print("Exported track_supports")

    print("All track and support components regenerated successfully!")
