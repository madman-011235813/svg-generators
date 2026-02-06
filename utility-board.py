#!/usr/bin/env python3

"""
Peg Board SVG Generator
- Rectangular holes
- Automatically computes rows and columns
- Centers the pattern on the board
"""

from math import floor


def generate_pegboard_svg(
    board_width_mm,
    board_height_mm,
    hole_width_mm,
    hole_height_mm,
    spacing_x_mm,
    spacing_y_mm,
    stroke_width_mm=0.5,
    dogbone_diameter_mm=0,
    output_file="pegboard.svg"
):
    # Determine number of columns and rows that fit
    max_columns = floor(
        (board_width_mm - hole_width_mm) / spacing_x_mm
    ) + 1

    max_rows = floor(
        (board_height_mm - hole_height_mm) / spacing_y_mm
    ) + 1

    # Actual used pattern dimensions
    pattern_width = (max_columns - 1) * spacing_x_mm + hole_width_mm
    pattern_height = (max_rows - 1) * spacing_y_mm + hole_height_mm

    # Offset to center the pattern
    offset_x = (board_width_mm - pattern_width) / 2
    offset_y = (board_height_mm - pattern_height) / 2

    # SVG header
    svg = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{board_width_mm}mm" '
        f'height="{board_height_mm}mm" '
        f'viewBox="0 0 {board_width_mm} {board_height_mm}">'
    )

    # Optional: board outline (comment out if not desired)
    svg.append(
        f'<rect x="0" y="0" width="{board_width_mm}" height="{board_height_mm}" '
        f'fill="none" stroke="black" stroke-width="{stroke_width_mm}"/>'
    )

    # Generate holes
    for row in range(max_rows):
        for col in range(max_columns):
            x = offset_x + col * spacing_x_mm
            y = offset_y + row * spacing_y_mm

            if dogbone_diameter_mm > 0:
                # Create single path with dog bone fillets
                radius = dogbone_diameter_mm / 2
                offset = radius / (2 ** 0.5)
                
                # Calculate circle centers (45° from each corner)
                tl_cx = x + offset  # top-left
                tl_cy = y + offset
                tr_cx = x + hole_width_mm - offset  # top-right
                tr_cy = y + offset
                bl_cx = x + offset  # bottom-left
                bl_cy = y + hole_height_mm - offset
                br_cx = x + hole_width_mm - offset  # bottom-right
                br_cy = y + hole_height_mm - offset
                
                # Build path with single arc per corner (radius R, endpoints at 2*offset from corner)
                path_d = f"M {x} {y + 2*offset} "  # Start on left edge at top-left arc start
                path_d += f"L {x} {y + hole_height_mm - 2*offset} "  # Left edge to bottom-left arc start
                path_d += f"A {radius} {radius} 0 0 0 {x + 2*offset} {y + hole_height_mm} "  # Bottom-left arc
                path_d += f"L {x + hole_width_mm - 2*offset} {y + hole_height_mm} "  # Bottom edge
                path_d += f"A {radius} {radius} 0 0 0 {x + hole_width_mm} {y + hole_height_mm - 2*offset} "  # Bottom-right arc
                path_d += f"L {x + hole_width_mm} {y + 2*offset} "  # Right edge
                path_d += f"A {radius} {radius} 0 0 0 {x + hole_width_mm - 2*offset} {y} "  # Top-right arc
                path_d += f"L {x + 2*offset} {y} "  # Top edge
                path_d += f"A {radius} {radius} 0 0 0 {x} {y + 2*offset} "  # Top-left arc
                path_d += "Z"  # Close path
                
                svg.append(
                    f'<path d="{path_d}" '
                    f'fill="none" stroke="black" stroke-width="{stroke_width_mm}"/>'
                )
            else:
                # Simple rectangle without dog bones
                svg.append(
                    f'<rect x="{x}" y="{y}" '
                    f'width="{hole_width_mm}" height="{hole_height_mm}" '
                    f'fill="none" stroke="black" stroke-width="{stroke_width_mm}"/>'
                )

    svg.append('</svg>')

    # Write file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print("Peg board SVG generated:")
    print(f"  File: {output_file}")
    print(f"  Columns: {max_columns}")
    print(f"  Rows: {max_rows}")


if __name__ == "__main__":
    # -------------------------------
    # USER CONFIGURATION
    # -------------------------------

    BOARD_WIDTH_MM = 30*25.4  # 30 inches
    BOARD_HEIGHT_MM = 60*25.4  # 60 inches

    HOLE_WIDTH_MM = 13
    HOLE_HEIGHT_MM =60

    SPACING_X_MM = 3*25.4  # 3 inches
    SPACING_Y_MM = 5*25.4  # 5 inches

    STROKE_WIDTH_MM = 0.1  # stroke width for all objects

    DOGBONE_DIAMETER_MM = 0.125 * 25.4  # 0.125 inches dog bone fillet diameter

    OUTPUT_FILE = "pegboard.svg"

    generate_pegboard_svg(
        BOARD_WIDTH_MM,
        BOARD_HEIGHT_MM,
        HOLE_WIDTH_MM,
        HOLE_HEIGHT_MM,
        SPACING_X_MM,
        SPACING_Y_MM,
        STROKE_WIDTH_MM,
        DOGBONE_DIAMETER_MM,
        OUTPUT_FILE
    )