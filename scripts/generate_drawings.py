"""
Professional Engineering Technical Drawings Generator
Produces:
1. drawings/technical_drawing_dimensioned.png (Multi-view dimensioned CAD drawing: Top, Front, Side, Section A-A, and Detail B: Semicircular U-channel)
2. drawings/exploded_view_assembly.png (Exploded assembly diagram with callout balloons and alignment traces)
Updated to exactly reflect the User Concept Blueprint (Pages 1, 2, 3).
"""

from pathlib import Path
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import to_rgb

DRAWINGS_DIR = Path(__file__).resolve().parent.parent / "drawings"
DRAWINGS_DIR.mkdir(parents=True, exist_ok=True)
PARTS_DIR = Path(__file__).resolve().parent.parent / "cad_models" / "parts"

def draw_title_block(ax, x0, y0, width, height, title, dwg_no, scale="1:2", sheet="1 OF 1"):
    """Draws a standard engineering title block."""
    rect = patches.Rectangle((x0, y0), width, height, linewidth=1.5, edgecolor='#0F172A', facecolor='#F8FAFC', zorder=10)
    ax.add_patch(rect)
    
    ax.plot([x0, x0 + width], [y0 + height * 0.5, y0 + height * 0.5], color='#0F172A', lw=1.0, zorder=11)
    ax.plot([x0 + width * 0.6, x0 + width * 0.6], [y0, y0 + height], color='#0F172A', lw=1.0, zorder=11)
    ax.plot([x0 + width * 0.6, x0 + width], [y0 + height * 0.25, y0 + height * 0.25], color='#0F172A', lw=0.8, zorder=11)
    ax.plot([x0 + width * 0.6, x0 + width], [y0 + height * 0.75, y0 + height * 0.75], color='#0F172A', lw=0.8, zorder=11)

    ax.text(x0 + 10, y0 + height * 0.75, "PROJECT: CONTINUOUS-LOOP MARBLE RACE MACHINE", fontsize=9, fontweight='bold', color='#1E293B', va='center')
    ax.text(x0 + 10, y0 + height * 0.25, f"DRAWING TITLE: {title}", fontsize=11, fontweight='heavy', color='#0F172A', va='center')
    
    ax.text(x0 + width * 0.62, y0 + height * 0.87, f"DWG NO: {dwg_no}", fontsize=8, fontweight='bold', color='#334155', va='center')
    ax.text(x0 + width * 0.62, y0 + height * 0.62, f"SCALE: {scale}   UNITS: mm", fontsize=8, color='#334155', va='center')
    ax.text(x0 + width * 0.62, y0 + height * 0.37, f"MATERIAL: PLA / 3D PRINTED", fontsize=8, color='#334155', va='center')
    ax.text(x0 + width * 0.62, y0 + height * 0.12, f"TOLERANCE: +/- 0.2 mm (SLIP 0.4 mm)", fontsize=8, color='#334155', va='center')

def draw_dimension_horizontal(ax, x1, x2, y, text, offset=15):
    """Draws horizontal engineering dimension with extension lines and arrows."""
    y_dim = y + offset
    ax.plot([x1, x1], [y, y_dim + np.sign(offset)*4], color='#475569', lw=0.8, ls='-')
    ax.plot([x2, x2], [y, y_dim + np.sign(offset)*4], color='#475569', lw=0.8, ls='-')
    ax.annotate('', xy=(x1, y_dim), xytext=(x2, y_dim),
                arrowprops=dict(arrowstyle='<->', color='#0F172A', lw=1.0))
    ax.text((x1 + x2)/2.0, y_dim + np.sign(offset)*3, text, ha='center', va='bottom' if offset > 0 else 'top',
            fontsize=8, fontweight='bold', color='#0F172A', backgroundcolor='#FFFFFF',
            bbox=dict(boxstyle='square,pad=0.1', fc='#FFFFFF', ec='none'))

def draw_dimension_vertical(ax, x, y1, y2, text, offset=15):
    """Draws vertical engineering dimension with extension lines and arrows."""
    x_dim = x + offset
    ax.plot([x, x_dim + np.sign(offset)*4], [y1, y1], color='#475569', lw=0.8, ls='-')
    ax.plot([x, x_dim + np.sign(offset)*4], [y2, y2], color='#475569', lw=0.8, ls='-')
    ax.annotate('', xy=(x_dim, y1), xytext=(x_dim, y2),
                arrowprops=dict(arrowstyle='<->', color='#0F172A', lw=1.0))
    ax.text(x_dim + np.sign(offset)*3, (y1 + y2)/2.0, text, ha='left' if offset > 0 else 'right', va='center',
            fontsize=8, fontweight='bold', color='#0F172A', rotation=90, backgroundcolor='#FFFFFF',
            bbox=dict(boxstyle='square,pad=0.1', fc='#FFFFFF', ec='none'))

def generate_technical_drawing():
    print("Generating: technical_drawing_dimensioned.png...")
    fig = plt.figure(figsize=(20, 14), dpi=160, facecolor='#FFFFFF')
    
    main_ax = fig.add_axes([0, 0, 1, 1], facecolor='#FFFFFF')
    main_ax.set_xlim(0, 1000)
    main_ax.set_ylim(0, 700)
    main_ax.axis('off')
    
    main_ax.add_patch(patches.Rectangle((15, 15), 970, 670, fill=False, edgecolor='#0F172A', lw=2.0))
    main_ax.add_patch(patches.Rectangle((20, 20), 960, 660, fill=False, edgecolor='#0F172A', lw=0.8))
    
    draw_title_block(main_ax, 580, 25, 395, 80, "MECHANICAL GA & BLUEPRINT INTEGRATION", "MR-CAD-002", "1:2")

    # -------------------------------------------------------------
    # VIEW 1: TOP PLAN VIEW (Blueprint Layout Matching Page 1)
    # -------------------------------------------------------------
    ax_top = fig.add_axes([0.05, 0.48, 0.42, 0.46])
    ax_top.set_aspect('equal')
    ax_top.axis('off')
    ax_top.set_title("VIEW A: TOP PLAN VIEW (CONCENTRIC SPIRAL, HURDLES & INFINITY LOOP)", fontsize=11, fontweight='bold', loc='left', color='#0F172A')

    # Octagonal Base profile (300mm flat to flat)
    angles = np.linspace(np.pi/8, 2*np.pi + np.pi/8, 9)
    r_vertex = 150.0 / np.cos(np.pi/8)
    oct_x = r_vertex * np.cos(angles)
    oct_y = r_vertex * np.sin(angles)
    ax_top.plot(oct_x, oct_y, color='#1E293B', lw=1.8, label="Base 300mm F2F")
    
    r_inner = 147.0 / np.cos(np.pi/8)
    ax_top.plot(r_inner * np.cos(angles), r_inner * np.sin(angles), color='#64748B', lw=0.9, ls='--')

    # Central Tower & Helix
    circle_theta = np.linspace(0, 2*np.pi, 100)
    ax_top.plot(30 * np.cos(circle_theta), 30 * np.sin(circle_theta), color='#0284C7', lw=1.6, label="Cylinder Ø60 OD")
    ax_top.plot(27 * np.cos(circle_theta), 27 * np.sin(circle_theta), color='#0284C7', lw=1.0, ls=':')
    ax_top.plot(25 * np.cos(circle_theta), 25 * np.sin(circle_theta), color='#EA580C', lw=1.2, ls='--') # Helix
    ax_top.plot(7 * np.cos(circle_theta), 7 * np.sin(circle_theta), color='#EA580C', lw=1.4)

    # Centerlines
    ax_top.plot([-165, 165], [0, 0], color='#DC2626', lw=0.7, ls='-.')
    ax_top.plot([0, 0], [-165, 165], color='#DC2626', lw=0.7, ls='-.')

    # 1. Multi-turn Concentric Spiral Track (Clockwise from top)
    theta1 = np.linspace(np.pi/2, -2.35*np.pi, 100)
    r1 = np.linspace(35, 120, 100)
    x1 = r1 * np.cos(theta1)
    y1 = r1 * np.sin(theta1)
    ax_top.plot(x1, y1, color='#EAB308', lw=3.0, label="1. Concentric Spiral Loops")

    # 2. Curved Rectangular Hurdle Section across front
    theta2 = np.linspace(-2.35*np.pi, -2.85*np.pi, 50)
    r2 = np.linspace(120, 95, 50)
    x2 = r2 * np.cos(theta2)
    y2 = r2 * np.sin(theta2)
    ax_top.plot(x2, y2, color='#7C3AED', lw=4.0, label="2. Curved Hurdle Section")
    # Hurdle posts
    t_pins = np.linspace(0.15, 0.85, 7)
    offs = [4, -4, 4, -4, 4, -4, 3.5]
    for tp, off in zip(t_pins, offs):
        idx = int(tp * (len(x2)-1))
        tang = np.array([x2[idx+1]-x2[idx], y2[idx+1]-y2[idx]])
        tang /= np.linalg.norm(tang)
        normal = np.array([-tang[1], tang[0]])
        px, py = x2[idx] + normal[0]*off, y2[idx] + normal[1]*off
        ax_top.plot(px, py, 'o', color='#F59E0B', markersize=4.5)

    # 3. Infinity Loop on left
    inf_pts = [
        (x2[-1], y2[-1]),
        (-105.0, -40.0),
        (-115.0, -20.0),
        (-70.0, -15.0), # Crossover
        (-50.0, 10.0),
        (-70.0, 35.0),
        (-95.0, 20.0),
        (-70.0, -15.0),
        (-52.0, -5.0),
    ]
    ix = [p[0] for p in inf_pts]
    iy = [p[1] for p in inf_pts]
    ax_top.plot(ix, iy, color='#059669', lw=3.0, label="3. Infinity Return Loop (Left)")
    ax_top.plot([-70.0], [-15.0], 'X', color='#EF4444', markersize=8, label="Crossover (-70, -15)")

    # 4. Entry Channel on left
    entry_pts = [(-52.0, -5.0), (-40.0, -2.0), (-27.0, 0.0)]
    ex = [p[0] for p in entry_pts]
    ey = [p[1] for p in entry_pts]
    ax_top.plot(ex, ey, color='#0D9488', lw=3.2, label="4. Entry Path into Cylinder")

    # Dimensions
    draw_dimension_horizontal(ax_top, -150, 150, 150, "300.0 (FLAT-TO-FLAT)", offset=22)
    draw_dimension_horizontal(ax_top, -30, 30, 0, "Ø60.0 CYLINDER", offset=38)
    draw_dimension_vertical(ax_top, 150, -150, 150, "300.0 (FLAT-TO-FLAT)", offset=22)

    ax_top.set_xlim(-185, 185)
    ax_top.set_ylim(-185, 185)
    ax_top.legend(loc='upper right', fontsize=6.5, framealpha=0.9)

    # -------------------------------------------------------------
    # VIEW 2: FRONT ELEVATION VIEW (Upper Right)
    # -------------------------------------------------------------
    ax_front = fig.add_axes([0.53, 0.48, 0.43, 0.46])
    ax_front.axis('off')
    ax_front.set_title("VIEW B: FRONT ELEVATION & GRAVITY DROP (ΔZ = 132.0 mm)", fontsize=11, fontweight='bold', loc='left', color='#0F172A')

    # Base profile
    base_rect = patches.Rectangle((-150, -50.8), 300, 50.8, linewidth=1.5, edgecolor='#1E293B', facecolor='#F1F5F9')
    ax_front.add_patch(base_rect)
    cav_rect = patches.Rectangle((-147, -47.8), 294, 47.8, linewidth=1.0, edgecolor='#64748B', facecolor='none', ls='--')
    ax_front.add_patch(cav_rect)

    # Lid
    lid_rect = patches.Rectangle((-150, 0), 300, 3.0, linewidth=1.2, edgecolor='#334155', facecolor='#CBD5E1')
    ax_front.add_patch(lid_rect)

    # Cylinder
    tower_rect = patches.Rectangle((-30, 3.0), 60, 140.0, linewidth=1.5, edgecolor='#0284C7', facecolor='#E0F2FE')
    ax_front.add_patch(tower_rect)
    cap_rect = patches.Rectangle((-30, 143.0), 60, 8.0, linewidth=1.2, edgecolor='#0369A1', facecolor='#BAE6FD')
    ax_front.add_patch(cap_rect)

    # Viewing slot
    slot_rect = patches.Rectangle((-6, 25.0), 12, 103.0, linewidth=1.0, edgecolor='#0284C7', facecolor='#FFFFFF')
    ax_front.add_patch(slot_rect)

    # Spiral coils in cylinder
    for z_c in np.arange(10, 140, 26):
        ax_front.plot([-25, 25], [z_c, z_c + 13], color='#EA580C', lw=1.8)

    # Track elevation profile
    # Spiral: 138 -> 95
    ax_front.plot([0, 60, 115, -85, 54.5], [138, 125, 112, 104, 95], color='#EAB308', lw=2.5, marker='s', markersize=4)
    # Hurdle: 95 -> 70
    ax_front.plot([54.5, 0, -84.6], [95, 82, 70], color='#7C3AED', lw=2.5, marker='^', markersize=4)
    # Infinity Upper: 70 -> 56 -> 42
    ax_front.plot([-84.6, -70, -70], [70, 56, 42], color='#059669', lw=2.5, marker='o', markersize=4)
    # Infinity Lower: 42 -> 28 -> 18
    ax_front.plot([-70, -70, -52], [42, 28, 18], color='#059669', lw=2.5, ls='--', marker='o', markersize=4)
    # Entry: 18 -> 6
    ax_front.plot([-52, -27], [18, 6], color='#0D9488', lw=2.5, marker='d', markersize=4)

    # Crossover annotation
    ax_front.annotate('CROSSOVER ΔZ = 28.0 mm\n(Upper: 56 mm, Lower: 28 mm)\n9 mm Free Headroom > 16mm Ball',
                      xy=(-70, 42), xytext=(-20, 75),
                      arrowprops=dict(arrowstyle='->', color='#EF4444', lw=1.2),
                      fontsize=7.5, fontweight='bold', color='#B91C1C',
                      bbox=dict(boxstyle='round,pad=0.2', fc='#FEF2F2', ec='#EF4444'))

    # Dimensions
    draw_dimension_vertical(ax_front, 150, -50.8, 0, "50.8 BASE DEPTH", offset=20)
    draw_dimension_vertical(ax_front, 150, 0, 3.0, "3.0", offset=35)
    draw_dimension_vertical(ax_front, 150, 3.0, 143.0, "140.0 CYLINDER HEIGHT", offset=20)
    draw_dimension_vertical(ax_front, 150, -50.8, 151.0, "201.8 OVERALL HEIGHT", offset=50)

    draw_dimension_vertical(ax_front, -150, 6.0, 138.0, "ΔZ = 132.0 mm TOTAL GRAVITY DROP", offset=-22)

    ax_front.set_xlim(-185, 215)
    ax_front.set_ylim(-65, 175)

    # -------------------------------------------------------------
    # VIEW 3: SECTION A-A & DETAIL B (Lower Left & Center)
    # -------------------------------------------------------------
    ax_sec = fig.add_axes([0.05, 0.05, 0.28, 0.38])
    ax_sec.axis('off')
    ax_sec.set_title("VIEW C: SECTION A-A (TOWER & HELIX)", fontsize=10.5, fontweight='bold', loc='left', color='#0F172A')

    # Tower Walls Section
    ax_sec.add_patch(patches.Rectangle((-30, 3), 3, 140, facecolor='#BAE6FD', edgecolor='#0284C7', hatch='//'))
    ax_sec.add_patch(patches.Rectangle((27, 3), 3, 140, facecolor='#BAE6FD', edgecolor='#0284C7', hatch='//'))

    # Flange
    ax_sec.add_patch(patches.Rectangle((-41, 3), 11, 4, facecolor='#BAE6FD', edgecolor='#0284C7', hatch='//'))
    ax_sec.add_patch(patches.Rectangle((30, 3), 11, 4, facecolor='#BAE6FD', edgecolor='#0284C7', hatch='//'))

    # Helix Core Shaft
    ax_sec.add_patch(patches.Rectangle((-7, 6), 14, 138, facecolor='#FED7AA', edgecolor='#EA580C', lw=1.2))
    ax_sec.add_patch(patches.Rectangle((-4, -14), 8, 20, facecolor='#FED7AA', edgecolor='#EA580C', lw=1.2))
    ax_sec.add_patch(patches.Rectangle((-3, 144), 6, 10, facecolor='#FED7AA', edgecolor='#EA580C', lw=1.2))

    # Helix Flights
    for z_f in np.arange(15, 140, 26):
        ax_sec.add_patch(patches.Rectangle((-25, z_f), 18, 3, facecolor='#FB923C', edgecolor='#EA580C'))
        ax_sec.add_patch(patches.Rectangle((7, z_f + 13), 18, 3, facecolor='#FB923C', edgecolor='#EA580C'))

    # 16mm marble in flight
    m_circle = patches.Circle((16, 15 + 13 + 8), 8, facecolor='#F8FAFC', edgecolor='#0F172A', lw=1.2)
    ax_sec.add_patch(m_circle)

    draw_dimension_horizontal(ax_sec, -30, 30, 155, "Ø60 OD", offset=8)
    draw_dimension_horizontal(ax_sec, -27, 27, 145, "Ø54 ID", offset=8)
    draw_dimension_horizontal(ax_sec, -25, 25, 110, "Ø50 HELIX", offset=8)
    draw_dimension_vertical(ax_sec, -30, 15, 41, "26 PITCH", offset=-12)

    ax_sec.set_xlim(-55, 65)
    ax_sec.set_ylim(-35, 175)

    # -------------------------------------------------------------
    # VIEW 4: DETAIL B: SEMICIRCULAR U-CHANNEL CROSS SECTION (Page 2 Blueprint)
    # -------------------------------------------------------------
    ax_u = fig.add_axes([0.35, 0.05, 0.22, 0.38])
    ax_u.set_aspect('equal')
    ax_u.axis('off')
    ax_u.set_title("DETAIL B: SEMICIRCULAR U-CHANNEL\n(BLUEPRINT PAGE 2 SPECIFICATION)", fontsize=10.5, fontweight='bold', loc='left', color='#0F172A')

    # Draw outer profile
    u_out_theta = np.linspace(np.pi, 2*np.pi, 50)
    ax_u.plot(11.5 * np.cos(u_out_theta), 11.5 * np.sin(u_out_theta), color='#1E293B', lw=2.0)
    ax_u.plot([-11.5, -11.5], [0, 6], color='#1E293B', lw=2.0)
    ax_u.plot([11.5, 11.5], [0, 6], color='#1E293B', lw=2.0)
    ax_u.plot([-11.5, -9.0], [6, 6], color='#1E293B', lw=2.0)
    ax_u.plot([9.0, 11.5], [6, 6], color='#1E293B', lw=2.0)

    # Draw inner profile (R=9.0, fits 16mm marble)
    u_in_theta = np.linspace(np.pi, 2*np.pi, 50)
    ax_u.plot(9.0 * np.cos(u_in_theta), 9.0 * np.sin(u_in_theta), color='#0284C7', lw=1.8)
    ax_u.plot([-9.0, -9.0], [0, 6], color='#0284C7', lw=1.8)
    ax_u.plot([9.0, 9.0], [0, 6], color='#0284C7', lw=1.8)

    # Fill wall cross section with hatching
    wall_left = patches.Polygon([[-11.5, 6], [-9, 6], [-9, 0], [-11.5, 0]], facecolor='#E2E8F0', edgecolor='none')
    wall_right = patches.Polygon([[9, 6], [11.5, 6], [11.5, 0], [9, 0]], facecolor='#E2E8F0', edgecolor='none')
    ax_u.add_patch(wall_left)
    ax_u.add_patch(wall_right)

    # Draw 16mm Marble sitting in bottom
    marble_u = patches.Circle((0, 0), 8.0, facecolor='#FEF08A', edgecolor='#CA8A04', lw=1.5, ls='--')
    ax_u.add_patch(marble_u)
    ax_u.plot([0], [0], '+', color='#CA8A04', markersize=8)
    ax_u.text(0, 0, " Ø16.0 BALL", fontsize=8, fontweight='bold', color='#854D0E', va='center')

    # Dimensions on U-channel
    draw_dimension_horizontal(ax_u, -9.0, 9.0, 8.0, "18.0 ID", offset=4)
    draw_dimension_horizontal(ax_u, -11.5, 11.5, -15.0, "23.0 OD", offset=-4)
    draw_dimension_vertical(ax_u, 11.5, 0, 6, "6.0", offset=4)
    draw_dimension_vertical(ax_u, -11.5, -11.5, 0, "R9.0", offset=-4)

    ax_u.text(0, -22, "1.0 mm Radial Clearance\nRound Bottom Profile", fontsize=7.5, color='#475569', ha='center')
    ax_u.set_xlim(-24, 24)
    ax_u.set_ylim(-26, 18)

    # Save
    out_file = DRAWINGS_DIR / "technical_drawing_dimensioned.png"
    plt.savefig(out_file, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print("Saved:", out_file)

def generate_exploded_view():
    print("Generating: exploded_view_assembly.png...")
    fig = plt.figure(figsize=(16, 12), dpi=150, facecolor='#FFFFFF')
    ax = fig.add_subplot(111, projection='3d')
    
    ax.set_facecolor("#FFFFFF")
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.axis('off')
    ax.set_title("EXPLODED ASSEMBLY VIEW WITH ITEM BALLOONS & ALIGNMENT AXES", fontsize=14, fontweight='bold', pad=15, color='#0F172A')

    offsets = {
        "switch_rocker.stl": (0, -45, -50),
        "motor_mount_bracket.stl": (0, 0, -85),
        "helix_shaft_coupler.stl": (0, 0, -45),
        "octagonal_base.stl": (0, 0, -15),
        "base_lid.stl": (0, 0, 30),
        "track_supports.stl": (0, 0, 45),
        "central_tower.stl": (0, 0, 90),
        "rotating_helix.stl": (0, 0, 160),
        "tower_top_cap.stl": (0, 0, 220),
        "entry_return_guide.stl": (0, 0, 65),
        "infinity_loop.stl": (0, 0, 105),
        "obstacle_section.stl": (0, 0, 135),
        "perimeter_track.stl": (0, 0, 170),
    }

    part_centers = {}
    from render_machine_views import PART_COLORS, render_mesh_to_ax

    for fname, (color, alpha) in PART_COLORS.items():
        fpath = PARTS_DIR / fname
        if fpath.exists():
            mesh = trimesh.load(str(fpath))
            off = offsets.get(fname, (0, 0, 0))
            mesh_exploded = mesh.copy().apply_translation(off)
            render_mesh_to_ax(ax, mesh_exploded, color, alpha=alpha)
            part_centers[fname] = mesh_exploded.bounds.mean(axis=0)

    ax.plot([0, 0], [0, 0], [-100, 250], color='#475569', lw=1.5, ls='--')

    bom_items = [
        ("tower_top_cap.stl", "1", "TOWER TOP CAP / BUSHING"),
        ("rotating_helix.stl", "2", "ROTATING HELIX ELEVATOR"),
        ("perimeter_track.stl", "3", "CONCENTRIC SPIRAL TRACK"),
        ("obstacle_section.stl", "4", "CURVED HURDLE SECTION"),
        ("central_tower.stl", "5", "CENTRAL HOLLOW CYLINDER"),
        ("infinity_loop.stl", "6", "INFINITY (FIGURE-8) RETURN LOOP"),
        ("entry_return_guide.stl", "7", "ENTRY PATH CHANNEL"),
        ("track_supports.stl", "8", "TRACK SUPPORT PILLARS"),
        ("base_lid.stl", "9", "REMOVABLE TOP LID"),
        ("octagonal_base.stl", "10", "OCTAGONAL BASE ENCLOSURE"),
        ("helix_shaft_coupler.stl", "11", "HELIX SHAFT COUPLER"),
        ("motor_mount_bracket.stl", "12", "MOTOR MOUNT BRACKET"),
        ("switch_rocker.stl", "13", "POWER ROCKER SWITCH"),
    ]

    for fname, item_no, label in bom_items:
        if fname in part_centers:
            cx, cy, cz = part_centers[fname]
            bx = cx + (70 if cx >= 0 else -70)
            by = cy + (40 if cy >= 0 else -40)
            bz = cz + 10
            ax.plot([cx, bx], [cy, by], [cz, bz], color='#64748B', lw=0.9, ls=':')
            ax.text(bx, by, bz, f" [{item_no}] {label}", fontsize=8, fontweight='bold', color='#0F172A',
                    bbox=dict(boxstyle='round,pad=0.2', fc='#FFFFFF', ec='#94A3B8', alpha=0.9))

    ax.set_xlim(-180, 180)
    ax.set_ylim(-180, 180)
    ax.set_zlim(-110, 260)
    ax.view_init(elev=26, azim=-50)

    out_file = DRAWINGS_DIR / "exploded_view_assembly.png"
    plt.tight_layout()
    plt.savefig(out_file, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print("Saved:", out_file)

if __name__ == "__main__":
    generate_technical_drawing()
    generate_exploded_view()
    print("Blueprint-matched technical drawing and exploded view generated successfully!")
