import pyvista as pv
import numpy as np

def load_febio_vtk(filepath: str, field_name: str) -> pv.DataSet:
    """
    Loads a VTK file and ensures the specified field data is available as Point Data.
    If the data is found in Cell Data, it is converted to Point Data.

    Args:
        filepath (str): Path to the .vtk file.
        field_name (str): The name of the scalar field to check (e.g., 'stress', 'displacement').

    Returns:
        pv.DataSet: The loaded PyVista mesh with the field available as Point Data.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the field_name is missing from both Cell and Point data.
    """
    try:
        mesh = pv.read(filepath)
    except Exception as e:
        raise FileNotFoundError(f"Could not read file at {filepath}. Error: {e}")

    # Check if field exists in Point Data
    if field_name in mesh.point_data:
        print(f"Field '{field_name}' found in Point Data.")
        return mesh

    # Check if field exists in Cell Data
    if field_name in mesh.cell_data:
        print(f"Field '{field_name}' found in Cell Data. Converting to Point Data...")
        mesh = mesh.cell_data_to_point_data()
        
        # Verify conversion
        if field_name not in mesh.point_data:
             raise RuntimeError(f"Failed to convert '{field_name}' from Cell Data to Point Data.")
             
        return mesh

    available_arrays = list(mesh.point_data.keys()) + list(mesh.cell_data.keys())
    raise ValueError(f"Field '{field_name}' not found in mesh data. Available arrays: {available_arrays}")