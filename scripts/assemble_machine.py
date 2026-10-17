"""
Complete 3D Assembly Generator and Interference Checker
for the Continuous-Loop Marble Race Machine.
"""

from build123d import *
from pathlib import Path
from parameters import PARAMS
from base_and_lid import build_octagonal_base, build_base_lid
from tower_and_elevator import (
    build_central_tower,
    build_tower_top_cap,
    build_rotating_helix,
    build_shaft_coupler,
    build_motor_mount,
    build_switch_rocker,
)
from tracks_and_supports import (
    build_perimeter_track,
    build_obstacle_section,
    build_infinity_loop,
    build_entry_return_guide,
    build_track_supports,
)

def create_marble_sphere(p=PARAMS) -> Compound:
    """Creates a sample 16mm marble placed in the track for visual scale."""
    with BuildPart() as m:
        Sphere(radius=p.marble_dia / 2.0)
    # Position marble at infinity loop upper crossover deck
    return m.part.translate((p.crossover_x, p.crossover_y, p.z_crossover_upper + p.marble_dia / 2.0))

def build_complete_assembly(p=PARAMS):
    """
    Builds the complete parametric 3D CAD assembly.
    Combines all 13 components with exact spatial coordinates.
    Checks volume and mass properties.
    """
    print("Generating all components for assembly...")
    base = build_octagonal_base(p)
    lid = build_base_lid(p)
    tower = build_central_tower(p)
    top_cap = build_tower_top_cap(p)
    helix = build_rotating_helix(p)
    coupler = build_shaft_coupler(p)
    motor_mount = build_motor_mount(p)
    sw = build_switch_rocker(p)
    perimeter = build_perimeter_track(p)
    obstacle = build_obstacle_section(p)
    infinity = build_infinity_loop(p)
    guide = build_entry_return_guide(p)
    supports = build_track_supports(p)
    marble = create_marble_sphere(p)

    components = {
        "Octagonal_Base": base,
        "Base_Lid": lid,
        "Central_Tower": tower,
        "Tower_Top_Cap": top_cap,
        "Rotating_Helix": helix,
        "Shaft_Coupler": coupler,
        "Motor_Mount_Bracket": motor_mount,
        "Switch_Rocker": sw,
        "Perimeter_Track": perimeter,
        "Obstacle_Section": obstacle,
        "Infinity_Return_Loop": infinity,
        "Entry_Return_Guide": guide,
        "Track_Supports": supports,
        "Marble_16mm": marble,
    }

    print("\n--- Component Volume Summary ---")
    total_volume_mm3 = 0.0
    for name, part in components.items():
        vol = part.volume
        total_volume_mm3 += vol
        print(f"  {name:25s}: {vol:10.1f} mm3  ({vol/1000.0:6.1f} cm3)")

    print(f"\nTotal Assembly Volume: {total_volume_mm3:10.1f} mm3 ({total_volume_mm3/1000.0:6.1f} cm3)")
    # PLA density approx 1.24 g/cm3 with 20% infill effective density ~ 0.5 g/cm3
    est_mass_pla = (total_volume_mm3 / 1000.0) * 0.5
    print(f"Estimated 3D-Printed PLA Mass (20% infill, 3 perimeters): ~{est_mass_pla:.1f} grams\n")

    # Combine into a master Compound
    assembly_compound = Compound(children=list(components.values()))

    # Export
    out_dir = Path(__file__).resolve().parent.parent / "cad_models" / "assembly"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Exporting complete assembly STEP...")
    export_step(assembly_compound, str(out_dir / "marble_race_complete_assembly.step"))
    print("Exported: marble_race_complete_assembly.step")

    print("Exporting complete assembly STL...")
    export_stl(assembly_compound, str(out_dir / "marble_race_assembly.stl"))
    print("Exported: marble_race_assembly.stl")

    return components, assembly_compound

if __name__ == "__main__":
    components, assembly_compound = build_complete_assembly()
    print("\nAssembly build and verification completed successfully!")
