import math

def create_3_point_star(cx, cy, outer_radius, inner_radius_percentage):
    """
    Create a 3-point star path.
    
    Args:
        cx, cy: Center coordinates (in inches)
        outer_radius: Distance from center to outer points (in inches)
        inner_radius_percentage: Inner radius as percentage of outer radius (0-100)
    """
    points = []
    num_points = 3
    inner_radius = outer_radius * (inner_radius_percentage / 100)
    
    # Generate alternating outer and inner points
    for i in range(num_points * 2):
        angle = (i * math.pi / num_points) - (math.pi / 2)  # Start from top
        radius = outer_radius if i % 2 == 0 else inner_radius
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append(f"{x},{y}")
    
    return "M " + " L ".join(points) + " Z"

def get_star_tips(cx, cy, outer_radius):
    """
    Get the coordinates of the star's outer tips.
    
    Returns list of (x, y, angle) tuples for each tip.
    """
    tips = []
    num_points = 3
    
    for i in range(num_points):
        angle = (i * 2 * math.pi / num_points) - (math.pi / 2)  # Start from top
        x = cx + outer_radius * math.cos(angle)
        y = cy + outer_radius * math.sin(angle)
        tips.append((x, y, angle))
    
    return tips

def generate_svg(width=60, height=60, inner_radius_pct=20, circle_radius=7, outer_radius=25, stroke_width=0.001):
    """
    Generate SVG with a 3-point star and circles at each tip.
    All measurements in inches.
    
    Args:
        width, height: Canvas dimensions (inches)
        inner_radius_pct: Inner radius as percentage of outer radius (0-100)
        circle_radius: Radius of circles at the tips (inches)
        outer_radius: Outer radius of star (inches)
        stroke_width: Width of strokes (inches)
    """
    
    # Star parameters (center of canvas)
    cx, cy = width / 2, height / 2
    
    star_path = create_3_point_star(cx, cy, outer_radius, inner_radius_pct)
    tips = get_star_tips(cx, cy, outer_radius)
    
    # Build SVG with inches
    svg_parts = [f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}in" height="{height}in" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="#f0f0f0"/>
    <path d="{star_path}" fill="none" stroke="#000000" stroke-width="{stroke_width}"/>''']
    
    # Add circles at each tip (positioned inward so they stay within star bounds)
    for tip_x, tip_y, angle in tips:
        # Position circle inward from the tip (subtract radius to move toward center)
        circle_cx = tip_x - circle_radius * math.cos(angle)
        circle_cy = tip_y - circle_radius * math.sin(angle)
        svg_parts.append(f'    <circle cx="{circle_cx}" cy="{circle_cy}" r="{circle_radius}" fill="none" stroke="#000000" stroke-width="{stroke_width}"/>')
    
    svg_parts.append('</svg>')
    
    return '\n'.join(svg_parts)

if __name__ == "__main__":
    inner_radius_pct = 20
    circle_radius = 7
    outer_radius = 28
    stroke_width = 0.05
    
    svg_content = generate_svg(
        width=60,
        height=60,
        inner_radius_pct=inner_radius_pct, 
        circle_radius=circle_radius,
        outer_radius=outer_radius,
        stroke_width=stroke_width
    )
    
    with open("star.svg", "w") as f:
        f.write(svg_content)
    
    print(f"✨ 3-point star SVG generated (all measurements in inches): star.svg")