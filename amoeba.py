import math

def create_3_lobe_amoeba(cx, cy, lobe_radius, lobe_tip_radius, branch_thickness, curve_pct):
    """
    Create a 3-lobed amoeba shape path with circular tips.
    
    Args:
        cx, cy: Center coordinates
        lobe_radius: Distance from center to tip of lobe
        lobe_tip_radius: Radius of circular tip at end of lobe
        branch_thickness: Width of branch at center (tapers to tip)
        curve_pct: Curve smoothness as percentage of lobe_radius (0-100)
    """
    num_lobes = 3
    path_parts = []
    
    # Calculate curve radius from percentage
    curve_radius = lobe_radius * (curve_pct / 100)
    
    # The center should be a circle from which the lobes branch out
    center_radius = branch_thickness / 2
    
    # Generate complete path going around the perimeter
    for i in range(num_lobes):
        angle = (i * 2 * math.pi / num_lobes) - (math.pi / 2)  # Start from top
        
        # Calculate lobe direction
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        # Angle for the edge of this lobe's branch base (clockwise side)
        angle_offset = math.atan2(center_radius, center_radius * 2)  # Small angle offset
        angle_cw = angle - angle_offset
        angle_ccw = angle + angle_offset
        
        # Points on center circle where this lobe starts
        center_cw_x = cx + center_radius * math.cos(angle_cw)
        center_cw_y = cy + center_radius * math.sin(angle_cw)
        center_ccw_x = cx + center_radius * math.cos(angle_ccw)
        center_ccw_y = cy + center_radius * math.sin(angle_ccw)
        
        # Lobe extends outward from center
        # Perpendicular for width calculations
        perp_cos = -sin_a
        perp_sin = cos_a
        
        # Distance to where circular tip starts
        tip_center_dist = lobe_radius - lobe_tip_radius
        tip_x = cx + tip_center_dist * cos_a
        tip_y = cy + tip_center_dist * sin_a
        
        # Taper: start with center_radius, end with lobe_tip_radius
        # Width at tip circle base
        tip_edge_cw_x = tip_x - lobe_tip_radius * perp_cos
        tip_edge_cw_y = tip_y - lobe_tip_radius * perp_sin
        tip_edge_ccw_x = tip_x + lobe_tip_radius * perp_cos
        tip_edge_ccw_y = tip_y + lobe_tip_radius * perp_sin
        
        # Control points for smooth curves using the curve parameter
        # Clockwise edge going out
        ctrl1_cw_x = center_cw_x + curve_radius * cos_a
        ctrl1_cw_y = center_cw_y + curve_radius * sin_a
        ctrl2_cw_x = tip_edge_cw_x - curve_radius * cos_a
        ctrl2_cw_y = tip_edge_cw_y - curve_radius * sin_a
        
        # Counter-clockwise edge coming back
        ctrl1_ccw_x = tip_edge_ccw_x - curve_radius * cos_a
        ctrl1_ccw_y = tip_edge_ccw_y - curve_radius * sin_a
        ctrl2_ccw_x = center_ccw_x + curve_radius * cos_a
        ctrl2_ccw_y = center_ccw_y + curve_radius * sin_a
        
        if i == 0:
            # Start at the clockwise edge of first lobe
            path_parts.append(f"M {center_cw_x},{center_cw_y}")
        
        # Curve out along clockwise edge
        path_parts.append(f"C {ctrl1_cw_x},{ctrl1_cw_y} {ctrl2_cw_x},{ctrl2_cw_y} {tip_edge_cw_x},{tip_edge_cw_y}")
        
        # Arc around the tip (sweep outward for convex)
        path_parts.append(f"A {lobe_tip_radius},{lobe_tip_radius} 0 0 1 {tip_edge_ccw_x},{tip_edge_ccw_y}")
        
        # Curve back along counter-clockwise edge
        path_parts.append(f"C {ctrl1_ccw_x},{ctrl1_ccw_y} {ctrl2_ccw_x},{ctrl2_ccw_y} {center_ccw_x},{center_ccw_y}")
        
        # Arc around center to next lobe
        if i < num_lobes - 1:
            next_angle = ((i + 1) * 2 * math.pi / num_lobes) - (math.pi / 2)
            next_angle_cw = next_angle - angle_offset
            next_center_cw_x = cx + center_radius * math.cos(next_angle_cw)
            next_center_cw_y = cy + center_radius * math.sin(next_angle_cw)
            
            # Arc from current ccw to next cw
            path_parts.append(f"A {center_radius},{center_radius} 0 0 0 {next_center_cw_x},{next_center_cw_y}")
        else:
            # Last lobe: arc back to the first lobe to close smoothly
            first_angle = (0 * 2 * math.pi / num_lobes) - (math.pi / 2)
            first_angle_cw = first_angle - angle_offset
            first_center_cw_x = cx + center_radius * math.cos(first_angle_cw)
            first_center_cw_y = cy + center_radius * math.sin(first_angle_cw)
            
            # Arc from last ccw to first cw
            path_parts.append(f"A {center_radius},{center_radius} 0 0 0 {first_center_cw_x},{first_center_cw_y}")
    
    # Close path with arc back to start
    path_parts.append("Z")
    
    return " ".join(path_parts)

def generate_svg(width=60, height=60, lobe_length=25, lobe_tip_radius=3, branch_thickness=4, 
                 curve_pct=30, stroke_width=0.05):
    """
    Generate SVG with a 3-lobed amoeba shape.
    All measurements in inches.
    
    Args:
        width, height: Canvas dimensions (inches)
        lobe_length: Distance from center to lobe tip (inches)
        lobe_tip_radius: Radius of circular tip (inches)
        branch_thickness: Width of branches at center (inches, tapers to tip)
        curve_pct: Curve smoothness (0-100, as % of lobe_length)
        stroke_width: Width of strokes (inches)
    """
    
    # Center of canvas
    cx, cy = width / 2, height / 2
    
    amoeba_path = create_3_lobe_amoeba(cx, cy, lobe_length, lobe_tip_radius, branch_thickness, 
                                        curve_pct)
    
    # Build SVG with inches and viewBox
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}in" height="{height}in" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="#f0f0f0"/>
    <path d="{amoeba_path}" fill="none" stroke="#000000" stroke-width="{stroke_width}"/>
</svg>'''
    
    return svg

if __name__ == "__main__":
    lobe_length = 25
    lobe_tip_radius = 7
    branch_thickness = 14
    curve_pct = 25
    stroke_width = 0.05
    
    svg_content = generate_svg(
        width=60,
        height=60,
        lobe_length=lobe_length,
        lobe_tip_radius=lobe_tip_radius,
        branch_thickness=branch_thickness,
        curve_pct=curve_pct,
        stroke_width=stroke_width
    )
    
    with open("amoeba.svg", "w") as f:
        f.write(svg_content)
    
    print(f"🦠 3-lobed amoeba SVG generated (all measurements in inches): amoeba.svg")
