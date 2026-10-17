"""
High-Resolution 3D CAD Renderer for the Marble Race Machine.
Updated to reflect the User Blueprint layout (Pages 1, 2, 3):
- Multi-turn smooth concentric spiral loops around cylinder and base.
- Semicircular round-bottom U-channel cross-section.
- Curved rectangular hurdle section with raised walls.
- Infinity (figure-eight) loop on the left side with 28mm crossover.
Renders 6 professional views:
1. assembly_isometric.png
2. assembly_top_view.png
3. assembly_side_view.png
4. tower_cutaway.png
5. helix_detail.png
6. infinity_crossover.png
"""

import os
from pathlib import Path
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import to_rgb

PARTS_DIR = Path(__file__).resolve().parent.parent / "cad_models" / "parts"
RENDERS_DIR = Path(__file__).resolve().parent.parent / "renders"
RENDERS_DIR.mkdir(parents=True, exist_ok=True)

PART_COLORS = {
    "octagonal_base.stl": ("#334155", 1.0),      # Charcoal Slate
    "base_lid.stl": ("#94A3B8", 0.9),            # Technical Silver
    "central_tower.stl": ("#0284C7", 0.45),      # Translucent Cyan Blue
    "tower_top_cap.stl": ("#0369A1", 0.9),       # Ocean Blue
    "rotating_helix.stl": ("#EA580C", 1.0),      # Safety Orange
    "helix_shaft_coupler.stl": ("#CBD5E1", 1.0), # Machined Aluminum
    "motor_mount_bracket.stl": ("#1E293B", 1.0), # Powder-coated Black
    "switch_rocker.stl": ("#DC2626", 1.0),       # Power Red
    "perimeter_track.stl": ("#EAB308", 0.95),    # Vibrant Yellow (Multi-turn Spiral)
    "obstacle_section.stl": ("#7C3AED", 0.95),   # Royal Violet (Curved Hurdles)
    "infinity_loop.stl": ("#059669", 0.95),      # Emerald Green (Figure-8)
    "entry_return_guide.stl": ("#0D9488", 0.95), # Deep Teal (Entry Channel)
    "track_supports.stl": ("#64748B", 0.95),     # Sturdy Structural Gray
}

LIGHT_DIR = np.array([0.5, 0.4, 0.8])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

def render_mesh_to_ax(ax, mesh, base_color_hex, alpha=1.0, light_dir=LIGHT_DIR):
    """Renders a trimesh mesh onto a 3D matplotlib axis with Lambertian shading."""
    v = mesh.vertices
    f = mesh.faces
    if len(f) > 14000:
        f = f[::2]
        
    triangles = v[f]
    
    normals = mesh.face_normals
    if len(normals) != len(f):
        v0 = triangles[:, 0]
        v1 = triangles[:, 1]
        v2 = triangles[:, 2]
        cross = np.cross(v1 - v0, v2 - v0)
        norm = np.linalg.norm(cross, axis=1, keepdims=True)
        norm[norm == 0] = 1.0
        normals = cross / norm
    
    dots = np.dot(normals, light_dir)
    intensity = 0.45 + 0.55 * np.clip(dots, 0.0, 1.0)
    
    base_rgb = np.array(to_rgb(base_color_hex))
    face_colors = np.zeros((len(f), 4))
    face_colors[:, :3] = intensity[:, None] * base_rgb[None, :]
    face_colors[:, 3] = alpha
    
    poly = Poly3DCollection(triangles, facecolors=face_colors, edgecolors='none', linewidths=0)
    ax.add_collection3d(poly)

def setup_ax_style(ax, title=""):
    ax.set_facecolor("#F8FAFC")
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('#E2E8F0')
    ax.yaxis.pane.set_edgecolor('#E2E8F0')
    ax.zaxis.pane.set_edgecolor('#E2E8F0')
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=12, color='#0F172A')

def create_marble_mesh(center=(-70.0, -15.0, 56.0 + 8.0), radius=8.0):
    """Creates a 16mm sphere mesh."""
    return trimesh.creation.icosphere(subdivisions=2, radius=radius).apply_translation(center)

def render_isometric_view():
    print("Rendering: assembly_isometric.png...")
    fig = plt.figure(figsize=(12, 10), dpi=150)
    ax = fig.add_subplot(111, projection='3d')
    setup_ax_style(ax, "Continuous-Loop Marble Race Machine - Isometric View (Blueprint Architecture)")

    for fname, (color, alpha) in PART_COLORS.items():
        fpath = PARTS_DIR / fname
        if fpath.exists():
            mesh = trimesh.load(str(fpath))
            render_mesh_to_ax(ax, mesh, color, alpha=alpha)

    # Add marble on track
    marble_mesh = create_marble_mesh()
    render_mesh_to_ax(ax, marble_mesh, "#F1F5F9", alpha=1.0)

    ax.set_xlim(-160, 160)
    ax.set_ylim(-160, 160)
    ax.set_zlim(-55, 160)
    ax.view_init(elev=32, azim=-55)
    plt.tight_layout()
    out_file = RENDERS_DIR / "assembly_isometric.png"
    plt.savefig(out_file, bbox_inches='tight', facecolor='#F8FAFC')
    plt.close()
    print("Saved:", out_file)

def render_top_view():
    print("Rendering: assembly_top_view.png...")
    fig = plt.figure(figsize=(10, 10), dpi=150)
    ax = fig.add_subplot(111, projection='3d')
    setup_ax_style(ax, "Top Plan View - Concentric Spiral & Blueprint Layout")

    for fname, (color, alpha) in PART_COLORS.items():
        fpath = PARTS_DIR / fname
        if fpath.exists():
            mesh = trimesh.load(str(fpath))
            render_mesh_to_ax(ax, mesh, color, alpha=alpha, light_dir=np.array([0.2, 0.2, 0.95]))

    marble_mesh = create_marble_mesh()
    render_mesh_to_ax(ax, marble_mesh, "#F1F5F9", alpha=1.0)

    ax.set_xlim(-165, 165)
    ax.set_ylim(-165, 165)
    ax.set_zlim(-55, 160)
    ax.view_init(elev=90, azim=-90)
    plt.tight_layout()
    out_file = RENDERS_DIR / "assembly_top_view.png"
    plt.savefig(out_file, bbox_inches='tight', facecolor='#F8FAFC')
    plt.close()
    print("Saved:", out_file)

def render_side_view():
    print("Rendering: assembly_side_view.png...")
    fig = plt.figure(figsize=(12, 7), dpi=150)
    ax = fig.add_subplot(111, projection='3d')
    setup_ax_style(ax, "Front Elevation View - Gravity Drop Profile")

    for fname, (color, alpha) in PART_COLORS.items():
        fpath = PARTS_DIR / fname
        if fpath.exists():
            mesh = trimesh.load(str(fpath))
            render_mesh_to_ax(ax, mesh, color, alpha=alpha, light_dir=np.array([0.1, -0.8, 0.5]))

    marble_mesh = create_marble_mesh()
    render_mesh_to_ax(ax, marble_mesh, "#F1F5F9", alpha=1.0)

    ax.set_xlim(-165, 165)
    ax.set_ylim(-165, 165)
    ax.set_zlim(-55, 160)
    ax.view_init(elev=8, azim=-90)
    plt.tight_layout()
    out_file = RENDERS_DIR / "assembly_side_view.png"
    plt.savefig(out_file, bbox_inches='tight', facecolor='#F8FAFC')
    plt.close()
    print("Saved:", out_file)

def render_tower_cutaway():
    print("Rendering: tower_cutaway.png...")
    fig = plt.figure(figsize=(9, 10), dpi=150)
    ax = fig.add_subplot(111, projection='3d')
    setup_ax_style(ax, "Central Tower Cutaway - Rotating Archimedes Screw")

    tower_mesh = trimesh.load(str(PARTS_DIR / "central_tower.stl"))
    # Cut half for viewing internal screw
    mask = tower_mesh.triangles[:, :, 0].mean(axis=1) > -10
    cut_tower = tower_mesh.submesh([mask], append=True)
    render_mesh_to_ax(ax, cut_tower, "#0284C7", alpha=0.85)

    helix_mesh = trimesh.load(str(PARTS_DIR / "rotating_helix.stl"))
    render_mesh_to_ax(ax, helix_mesh, "#EA580C", alpha=1.0)

    cap_mesh = trimesh.load(str(PARTS_DIR / "tower_top_cap.stl"))
    render_mesh_to_ax(ax, cap_mesh, "#0369A1", alpha=0.9)
    coupler_mesh = trimesh.load(str(PARTS_DIR / "helix_shaft_coupler.stl"))
    render_mesh_to_ax(ax, coupler_mesh, "#CBD5E1", alpha=1.0)

    # 16mm marble in flight
    m_climb = create_marble_mesh(center=(18.0, 0.0, 50.0), radius=8.0)
    render_mesh_to_ax(ax, m_climb, "#F1F5F9", alpha=1.0)

    ax.set_xlim(-45, 45)
    ax.set_ylim(-45, 45)
    ax.set_zlim(-20, 160)
    ax.view_init(elev=20, azim=-30)
    plt.tight_layout()
    out_file = RENDERS_DIR / "tower_cutaway.png"
    plt.savefig(out_file, bbox_inches='tight', facecolor='#F8FAFC')
    plt.close()
    print("Saved:", out_file)

def render_helix_detail():
    print("Rendering: helix_detail.png...")
    fig = plt.figure(figsize=(8, 10), dpi=150)
    ax = fig.add_subplot(111, projection='3d')
    setup_ax_style(ax, "Rotating Helix Elevator - Detail Geometry (26 mm Pitch)")

    helix_mesh = trimesh.load(str(PARTS_DIR / "rotating_helix.stl"))
    render_mesh_to_ax(ax, helix_mesh, "#EA580C", alpha=1.0)

    m_detail = create_marble_mesh(center=(18.0, 0.0, 45.0), radius=8.0)
    render_mesh_to_ax(ax, m_detail, "#38BDF8", alpha=1.0)

    ax.set_xlim(-35, 35)
    ax.set_ylim(-35, 35)
    ax.set_zlim(-10, 160)
    ax.view_init(elev=25, azim=-45)
    plt.tight_layout()
    out_file = RENDERS_DIR / "helix_detail.png"
    plt.savefig(out_file, bbox_inches='tight', facecolor='#F8FAFC')
    plt.close()
    print("Saved:", out_file)

def render_infinity_crossover():
    print("Rendering: infinity_crossover.png...")
    fig = plt.figure(figsize=(10, 8), dpi=150)
    ax = fig.add_subplot(111, projection='3d')
    setup_ax_style(ax, "Infinity Loop Crossover (Left Side) - 28 mm Headroom Clearance")

    loop_mesh = trimesh.load(str(PARTS_DIR / "infinity_loop.stl"))
    render_mesh_to_ax(ax, loop_mesh, "#059669", alpha=0.95)

    # Marble on lower track (underpass Z=28)
    m_lower = create_marble_mesh(center=(-70.0, -15.0, 28.0 + 8.0), radius=8.0)
    render_mesh_to_ax(ax, m_lower, "#F1F5F9", alpha=1.0)

    # Marble on upper track (crossover bridge Z=56)
    m_upper = create_marble_mesh(center=(-70.0, -15.0, 56.0 + 8.0), radius=8.0)
    render_mesh_to_ax(ax, m_upper, "#38BDF8", alpha=1.0)

    ax.set_xlim(-125, -20)
    ax.set_ylim(-65, 45)
    ax.set_zlim(15, 80)
    ax.view_init(elev=28, azim=-60)
    plt.tight_layout()
    out_file = RENDERS_DIR / "infinity_crossover.png"
    plt.savefig(out_file, bbox_inches='tight', facecolor='#F8FAFC')
    plt.close()
    print("Saved:", out_file)

if __name__ == "__main__":
    render_isometric_view()
    render_top_view()
    render_side_view()
    render_tower_cutaway()
    render_helix_detail()
    render_infinity_crossover()
    print("All 6 blueprint-matched views rendered successfully!")
