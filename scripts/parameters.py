"""
Master Parameters for the Motor-Driven Continuous-Loop Marble Race Machine.
All dimensions are in millimeters (mm) unless otherwise noted.
Updated according to User Concept Blueprint (Pages 1, 2, 3):
- Multi-turn smooth concentric spiral loops around cylinder and base.
- Semicircular round-bottom U-channel cross-section (Page 2).
- Curved rectangular obstacle path with staggered collision hurdles (Page 3).
- Figure-eight infinity return loop on the left ending at entry channel (Page 1).
"""

from dataclasses import dataclass
import math

@dataclass
class MachineParameters:
    # -------------------------------------------------------------
    # Marble Specifications
    # -------------------------------------------------------------
    marble_dia: float = 16.0          # Standard spherical marble diameter
    marble_mass_steel: float = 0.0165 # kg (~16.5 g for 16mm steel ball)
    marble_mass_glass: float = 0.0055 # kg (~5.5 g for 16mm glass marble)

    # -------------------------------------------------------------
    # 3D Printing Tolerances & Clearances
    # -------------------------------------------------------------
    clearance_slip: float = 0.4       # General mating slip fit clearance
    clearance_press: float = 0.15     # Snug / light press fit
    clearance_moving: float = 1.5     # Dynamic / moving clearance (helix to tube)

    # -------------------------------------------------------------
    # Octagonal Base Enclosure & Lid
    # -------------------------------------------------------------
    base_flat_to_flat: float = 300.0  # Width across opposite flat sides
    base_depth: float = 50.8          # External depth / height of base box (2 inches)
    base_wall_thick: float = 3.0      # Enclosure side-wall thickness
    base_floor_thick: float = 3.0     # Base floor plate thickness
    lid_thick: float = 3.0            # Removable top lid thickness
    
    # Fastener / Boss Details (M3 hardware)
    boss_outer_dia: float = 10.0      # Mounting boss diameter
    boss_hole_dia: float = 2.8        # Pilot hole for M3 heat-set insert or self-tapping
    lid_screw_hole_dia: float = 3.4   # Clearance hole for M3 screws
    lid_counterbore_dia: float = 6.2  # M3 socket cap counterbore
    lid_counterbore_depth: float = 1.8
    
    # Power Switch & DC Jack Cutouts (on side face)
    switch_cutout_w: float = 19.5     # Standard KCD1 rocker switch cutout width
    switch_cutout_h: float = 13.0     # Rocker switch cutout height
    dc_jack_dia: float = 8.2          # 5.5x2.1mm DC barrel jack cutout diameter

    # -------------------------------------------------------------
    # Central Tower (Stationary Cylinder)
    # -------------------------------------------------------------
    tower_od: float = 60.0            # Outer diameter of tower
    tower_id: float = 54.0            # Inner diameter of tower (bore)
    tower_height: float = 140.0       # Tower height above base lid
    tower_flange_dia: float = 82.0    # Bottom mounting flange diameter
    tower_flange_thick: float = 4.0   # Flange thickness
    tower_view_slot_w: float = 12.0   # Front viewing slot / reaction guide width
    tower_inlet_w: float = 22.0       # Bottom marble inlet width
    tower_inlet_h: float = 24.0       # Bottom marble inlet height
    tower_exit_w: float = 22.0        # Top marble outlet width
    tower_exit_h: float = 24.0        # Top marble outlet height

    # -------------------------------------------------------------
    # Rotating Helix Elevator (Archimedes Screw)
    # -------------------------------------------------------------
    helix_od: float = 50.0            # Outer diameter of helical flight (2mm radial clearance to 54mm ID)
    helix_core_dia: float = 14.0      # Central shaft diameter
    helix_pitch: float = 26.0         # Vertical pitch per revolution
    helix_height: float = 138.0       # Active helix height (~5.3 turns)
    helix_flight_thick: float = 3.0   # Flight blade thickness
    helix_shaft_lower_dia: float = 8.0 # Bottom drive shaft stub diameter
    helix_shaft_lower_len: float = 20.0 # Length extending into base
    helix_shaft_upper_dia: float = 6.0 # Top pivot pin diameter
    helix_shaft_upper_len: float = 10.0 # Length engaging top cap bushing

    # -------------------------------------------------------------
    # Motor & Coupling
    # -------------------------------------------------------------
    motor_type: str = "Standard 37D/TT DC Geared Motor"
    motor_shaft_dia: float = 6.0      # Motor shaft diameter (supports 6mm D-shaft or 5.4mm TT)
    coupler_od: float = 18.0          # Coupler outer diameter
    coupler_len: float = 24.0         # Coupler overall length
    coupler_set_screw_dia: float = 3.0 # M3 set screw threads

    # -------------------------------------------------------------
    # Semicircular U-Channel Track Geometry (Page 2 Blueprint)
    # -------------------------------------------------------------
    track_radius_inner: float = 9.0   # Semicircular floor radius (fits 16mm marble with 1mm clearance)
    track_wall_h: float = 6.0         # Vertical tangent side-wall height above center
    track_wall_thick: float = 2.5     # Track shell wall thickness (outer radius = 11.5mm)
    track_floor_thick: float = 3.0    # Floor thickness for rectangular obstacle channel

    # -------------------------------------------------------------
    # Curved Rectangular Hurdle Section (Page 3 Blueprint)
    # -------------------------------------------------------------
    hurdle_channel_w: float = 22.0    # Internal rectangular channel width
    hurdle_wall_h: float = 9.0        # Raised side walls to retain marble during collisions
    hurdle_pin_dia: float = 4.5       # Cylindrical hurdle post diameter
    hurdle_pin_h: float = 3.5         # Hurdle post height above track floor
    hurdle_pin_count: int = 7         # 7 staggered collision posts

    # -------------------------------------------------------------
    # Infinity-Shaped Return Loop (Page 1 Blueprint)
    # -------------------------------------------------------------
    crossover_x: float = -70.0        # X coordinate of crossover junction
    crossover_y: float = -15.0        # Y coordinate of crossover junction
    z_crossover_upper: float = 56.0   # Upper bridge deck height
    z_crossover_lower: float = 28.0   # Lower underpass deck height
    crossover_clearance_z: float = 28.0 # Floor separation: 28 - 3 floor = 25mm > 16mm ball (9mm headroom)

    # -------------------------------------------------------------
    # Continuous Kinematic Drop & Slopes
    # -------------------------------------------------------------
    z_tower_exit: float = 138.0       # Track start height above lid at top of cylinder
    z_obstacle_start: float = 95.0    # Obstacle section entry height
    z_infinity_start: float = 70.0    # Infinity loop entry height
    z_return_ramp_start: float = 18.0 # Return entry ramp start height
    z_tower_inlet: float = 6.0        # Cylinder inlet floor height

    @property
    def base_inradius(self) -> float:
        """Inradius (center to flat side) = half of flat-to-flat width."""
        return self.base_flat_to_flat / 2.0  # 150.0 mm

    @property
    def base_circumradius(self) -> float:
        """Circumradius (center to corner vertex) of regular octagon."""
        return self.base_inradius / math.cos(math.radians(22.5))  # ~162.36 mm

    @property
    def base_side_length(self) -> float:
        """Side length of regular octagon."""
        return 2.0 * self.base_inradius * math.tan(math.radians(22.5))  # ~124.26 mm

PARAMS = MachineParameters()
