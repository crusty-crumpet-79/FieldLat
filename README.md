# FieldLat: Field-Driven Adaptive Lattice Generation

FieldLat is a Python library for generating functionally graded lattice structures based on scalar fields (e.g., stress, strain, or temperature data from FEA simulations).

Unlike simple thickness modulation, FieldLat implements **Variable Cell Size** via lattice blending. This allows for smooth transitions between low-density (large cell) and high-density (small cell) lattice regions while maintaining a constant wall thickness, optimizing structures for both weight and mechanical performance.

## Key Features

- **Variable Cell Size**: Dynamically adjusts pore size based on field intensity.
- **Lattice Blending**: Smoothly interpolates between different Gyroid frequencies.
- **Field Mapping**: Automatically normalizes input scalar fields (stress/displacement) to control lattice density.
- **Mesh Support**: Handles FEBio/VTK data and automatically converts Cell Data to Point Data if necessary.
- **PyVista Integration**: Built on PyVista for efficient 3D processing and visualization.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/FieldLat.git
   cd FieldLat
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

The core functionality is provided by the `generate_adaptive_lattice` function. Here is a minimal example of how to use it:

```python
import pyvista as pv
from fieldlat import generate_adaptive_lattice, load_febio_vtk

# 1. Load your mesh containing field data (e.g., 'stress')
# Ensure 'stress' is a scalar field in your VTK file.
mesh = load_febio_vtk('simulation_result.vtk', field_name='stress')

# 2. Generate the adaptive lattice
# - Low stress -> Large cells (Base Scale)
# - High stress -> Small cells (Dense Scale)
lattice = generate_adaptive_lattice(
    mesh,
    field_name='stress',
    resolution=100,      # Grid resolution (higher = finer detail)
    base_scale=10.0,     # Frequency for low-stress areas
    dense_scale=25.0,    # Frequency for high-stress areas
    threshold=0.3        # Wall thickness constant
)

# 3. Save or Visualize
lattice.save('adaptive_lattice.stl')
lattice.plot(smooth_shading=True)
```

## Running the Demo

The repository includes a demo script that generates a dummy stress field on a cube and creates an adaptive lattice.

To run the demo:

```bash
python examples/demo_script.py
```

This will:
1. Create a dummy `input.vtk` file if one doesn't exist.
2. Generate an adaptive Gyroid lattice blending between two frequencies.
3. Display the result in an interactive 3D window.
4. Save the result to `output_lattice.stl`.

## API Reference

### `generate_adaptive_lattice`

```python
def generate_adaptive_lattice(
    mesh: pv.DataSet,
    field_name: str,
    resolution: int = 50,
    base_scale: float = 10.0,
    dense_scale: float = 25.0,
    threshold: float = 0.3
) -> pv.PolyData
```

**Parameters:**
- `mesh`: A PyVista DataSet containing the source geometry and scalar field.
- `field_name`: The name of the scalar array in `mesh.point_data` to use as the control field.
- `resolution`: The resolution of the voxel grid (cubed) used for marching cubes.
- `base_scale`: The Gyroid frequency factor for regions with minimum field values (larger cells).
- `dense_scale`: The Gyroid frequency factor for regions with maximum field values (smaller cells).
- `threshold`: Controls the isosurface level, effectively setting the constant wall thickness.

**Returns:**
- `pv.PolyData`: A mesh representing the generated lattice structure.
