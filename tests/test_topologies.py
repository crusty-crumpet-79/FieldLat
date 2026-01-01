import sys
import os
import numpy as np
import pyvista as pv
import pytest

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from fieldlat import generate_adaptive_lattice

def test_all_topologies():
    # 1. Create a simple dummy mesh
    mesh = pv.Cube(center=(0, 0, 0), x_length=1.0, y_length=1.0, z_length=1.0)
    mesh = mesh.triangulate().subdivide(1)
    
    # 2. Add a scalar field
    field_name = 'stress'
    mesh.point_data[field_name] = np.linspace(0, 1, mesh.n_points)
    
    lattice_types = ['gyroid', 'diamond', 'primitive', 'lidinoid']
    
    for lat_type in lattice_types:
        print(f"Testing lattice type: {lat_type}")
        try:
            lattice = generate_adaptive_lattice(
                mesh,
                field_name=field_name,
                lattice_type=lat_type,
                resolution=20, # Low resolution for speed
                base_scale=5.0,
                dense_scale=10.0,
                threshold=0.3,
                pad_width=1
            )
            
            assert lattice.n_points > 0, f"Lattice {lat_type} is empty!"
            assert lattice.n_cells > 0, f"Lattice {lat_type} has no cells!"
            
            # Check for watertightness as well to be safe
            lattice = lattice.clean()
            assert lattice.n_open_edges == 0, f"Lattice {lat_type} is not watertight!"
            
            print(f"  -> {lat_type} passed.")
            
        except Exception as e:
            pytest.fail(f"Lattice generation failed for type '{lat_type}': {e}")

if __name__ == "__main__":
    test_all_topologies()
