# Amoeba Shape Geometry Explanation

## Overview
The 3-lobed amoeba consists of a circular center with three symmetrical lobes extending outward at 120° intervals.

## Key Components

```
                    Lobe 0 (Top)
                       ╱───╲
                      ╱     ╲
                     ╱       ╲
            tip_edge_ccw   tip_edge_cw
                    │         │
                    │  ●tip_x │
                    │         │
                    │         │
         center_ccw ●         ● center_cw
                     ╲       ╱
                      ╲  ●  ╱ ← Center (cx, cy)
                       ╲   ╱    with center_radius
                        ╲ ╱
                     
        Lobe 2              Lobe 1
      (Bottom Left)     (Bottom Right)
```

## Node Creation Logic (For Each Lobe)

### 1. **Lobe Angle** (Line 25)
```
angle = (i * 2π / 3) - π/2
```
- Lobe 0: -90° (points up)
- Lobe 1: 30° (bottom right)
- Lobe 2: 150° (bottom left)

### 2. **Direction Vectors** (Lines 28-29)
```
cos_a = cos(angle)  → X component of lobe direction
sin_a = sin(angle)  → Y component of lobe direction
```

### 3. **Angular Offset for Branch Width** (Lines 32-34)
```
angle_offset = atan2(center_radius, center_radius * 2)
angle_cw = angle - angle_offset    (clockwise edge)
angle_ccw = angle + angle_offset   (counter-clockwise edge)
```
This creates a narrow "wedge" at the base of each lobe.

### 4. **Center Circle Points** (Lines 37-40)
```
center_cw_x = cx + center_radius * cos(angle_cw)
center_cw_y = cy + center_radius * sin(angle_cw)
center_ccw_x = cx + center_radius * cos(angle_ccw)
center_ccw_y = cy + center_radius * sin(angle_ccw)
```
**Purpose**: Where the lobe connects to the central circle
- `center_cw`: Clockwise edge at base
- `center_ccw`: Counter-clockwise edge at base

### 5. **Perpendicular Direction** (Lines 44-45)
```
perp_cos = -sin_a
perp_sin = cos_a
```
Rotates direction 90° counter-clockwise for width calculations.

### 6. **Tip Center Point** (Lines 48-50)
```
tip_center_dist = lobe_radius - lobe_tip_radius
tip_x = cx + tip_center_dist * cos_a
tip_y = cy + tip_center_dist * sin_a
```
**Purpose**: Center of the circular tip (offset inward by tip radius).

### 7. **Tip Edge Points** (Lines 54-57)
```
tip_edge_cw_x = tip_x - lobe_tip_radius * perp_cos
tip_edge_cw_y = tip_y - lobe_tip_radius * perp_sin
tip_edge_ccw_x = tip_x + lobe_tip_radius * perp_cos
tip_edge_ccw_y = tip_y + lobe_tip_radius * perp_sin
```
**Purpose**: Where the branch edges meet the circular tip.
- Uses perpendicular direction to place points on either side of tip center
- Distance = `lobe_tip_radius` (creates the taper)

### 8. **Bézier Control Points** (Lines 60-68)
```
# Clockwise edge (going out)
ctrl1_cw = center_cw + curve_radius * [cos_a, sin_a]
ctrl2_cw = tip_edge_cw - curve_radius * [cos_a, sin_a]

# Counter-clockwise edge (coming back)
ctrl1_ccw = tip_edge_ccw - curve_radius * [cos_a, sin_a]
ctrl2_ccw = center_ccw + curve_radius * [cos_a, sin_a]
```
**Purpose**: Control handles for smooth cubic Bézier curves
- `ctrl1`: Pulled toward the tip from base point
- `ctrl2`: Pulled toward base from tip point
- Distance = `curve_radius` (determined by `curve_pct`)

## Path Construction Order

For **each lobe** (i = 0, 1, 2):

```
1. Start at center_cw (or arc from previous lobe)
   ↓
2. Cubic Bézier curve to tip_edge_cw
   Using ctrl1_cw and ctrl2_cw
   ↓
3. Circular arc to tip_edge_ccw
   Arc radius = lobe_tip_radius
   ↓
4. Cubic Bézier curve back to center_ccw
   Using ctrl1_ccw and ctrl2_ccw
   ↓
5. Circular arc to next lobe's center_cw
   Arc radius = center_radius (follows center circle)
```

## Detailed Point Relationships

```
       tip_edge_ccw ●━━━━━━━━━● tip_edge_cw
                    ╲         ╱
                     ╲       ╱  
         ctrl1_ccw ●  ╲  ●  ╱  ● ctrl2_cw
                       ╲   ╱ tip_x
                        ╲ ╱
                         ●
                         │
         ctrl2_ccw ●     │     ● ctrl1_cw
                    ╲    │    ╱
                     ╲   │   ╱
      center_ccw ●━━━╲━━●━━╱━━━● center_cw
                      ╲ cx ╱
                       ╲ cy╱
                        ╲ ╱
                         ●
```

## Key Parameters Effect

| Parameter | Controls |
|-----------|----------|
| `lobe_radius` | Distance from center to tip (overall lobe length) |
| `lobe_tip_radius` | Size of circular tip; also determines taper width at tip |
| `branch_thickness` | Width at center (tapers down to `lobe_tip_radius`) |
| `curve_pct` | Smoothness of curves (0=sharp, 100=very smooth) |
| `center_radius` | Radius of central circle = `branch_thickness / 2` |

## Mathematical Transformations

**From center to any point on lobe axis:**
```
point = (cx, cy) + distance * (cos_a, sin_a)
```

**From point on axis to side edges:**
```
left_edge = point + offset * (perp_cos, perp_sin)
right_edge = point - offset * (perp_cos, perp_sin)
```

**Bézier curve control point:**
```
control = endpoint + influence_distance * direction_vector
```

Where `direction_vector` points toward/away from the other endpoint.
