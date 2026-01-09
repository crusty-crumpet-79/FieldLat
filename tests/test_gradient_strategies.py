import sys
import os
import numpy as np
import pyvista as pv
import pytest

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from fieldlat import generate_adaptive_lattice

def test_gradient_strategies():
    # 1. Create a simple dummy mesh
    mesh = pv.Cube(center=(0, 0, 0), x_length=1.0, y_length=1.0, z_length=1.0)
    mesh = mesh.triangulate().subdivide(1)
    
    # 2. Add a scalar field
    field_name = 'stress'
    mesh.point_data[field_name] = np.linspace(0, 1, mesh.n_points)
    
    strategies = ['blend', 'warp']
    
    for strategy in strategies:
        print(f"Testing gradient strategy: {strategy}")
        try:
            lattice = generate_adaptive_lattice(
                mesh,
                field_name=field_name,
                lattice_type='gyroid',
                resolution=20,
                base_scale=5.0,
                dense_scale=10.0,
                threshold=0.3,
                pad_width=1,
                gradient_strategy=strategy
            )
            
            assert lattice.n_points > 0, f"Lattice with strategy {strategy} is empty!"
            assert lattice.n_cells > 0, f"Lattice with strategy {strategy} has no cells!"
            
            # Check for watertightness
            lattice = lattice.clean()
            assert lattice.n_open_edges == 0, f"Lattice with strategy {strategy} is not watertight!"
            
            print(f"  -> Strategy {strategy} passed.")
            
        except Exception as e:
            pytest.fail(f"Lattice generation failed for strategy '{strategy}': {e}")

def test_invalid_strategy():
    mesh = pv.Cube()
    mesh.point_data['val'] = np.zeros(mesh.n_points)
    
    with pytest.raises(ValueError, match="Unknown gradient_strategy"):
        generate_adaptive_lattice(
            mesh,
            field_name='val',
            gradient_strategy='invalid_strategy'
        )

if __name__ == "__main__":
    test_gradient_strategies()
    test_invalid_strategy()
