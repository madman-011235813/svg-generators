# SVG Generators

A collection of Python scripts for generating customizable SVG graphics, perfect for laser cutting, CNC routing, and other fabrication projects.

## 📁 Project Contents

### Python Scripts

- **[amoeba.py](amoeba.py)** - Generates organic 3-lobed amoeba shapes with smooth curves and circular tips
- **[star.py](star.py)** - Creates 3-point stars with customizable inner/outer radius ratios and circles at each tip
- **[utility-board.py](utility-board.py)** - Generates pegboard layouts with rectangular holes and optional dog bone fillets for CNC routing

### Documentation

- **[amoeba_geometry_explained.md](amoeba_geometry_explained.md)** - Detailed mathematical explanation of the amoeba shape geometry

### Generated SVG Files

- `amoeba.svg` - Example amoeba shape output
- `star.svg` - Example star shape output  
- `pegboard.svg` - Example utility board layout

## 🚀 Usage

Each script can be run independently to generate its corresponding SVG file:

```bash
python amoeba.py      # Generates amoeba.svg
python star.py        # Generates star.svg
python utility-board.py  # Generates pegboard.svg
```

## ⚙️ Configuration

All scripts have configurable parameters in their `if __name__ == "__main__"` sections. Simply edit the values and run the script.

### Amoeba Parameters
- Canvas dimensions (width, height)
- Lobe radius and tip radius
- Branch thickness
- Curve smoothness percentage
- Stroke width

### Star Parameters
- Canvas dimensions (width × height in inches)
- Outer radius (inches)
- Inner radius percentage (0-100)
- Circle radius at tips (inches)
- Stroke width (inches)

### Utility Board Parameters
- Board dimensions (mm or inches)
- Hole dimensions (width × height)
- Spacing between holes (X and Y)
- Optional dog bone fillet diameter for CNC compatibility
- Stroke width

## 📐 Features

- **Precise measurements** - Supports both inches and millimeters
- **CNC-ready** - Dog bone fillets prevent corner radius issues
- **Auto-centering** - Pegboard automatically centers patterns
- **Parametric design** - Easily customize all dimensions
- **Clean SVG output** - Ready for laser cutters and CNC machines

## 💡 Example Use Cases

- **Amoeba shapes**: Decorative panels, artistic designs, organic patterns
- **Star shapes**: Ornaments, badges, geometric decorations
- **Pegboards**: Tool organization, utility boards, modular storage systems

## 📄 License

Open source - feel free to use and modify for your projects.

## 🛠️ Requirements

- Python 3.x
- No external dependencies (uses only standard library)