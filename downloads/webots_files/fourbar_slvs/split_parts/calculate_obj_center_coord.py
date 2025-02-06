def read_obj(filename):
    """Read OBJ file and return vertices."""
    vertices = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('v '):  # vertex
                coords = line.split()[1:]
                vertices.append([float(x) for x in coords])
            
    return vertices

def find_center(vertices):
    """Calculate and display the center point of all vertices."""
    if not vertices:
        return [0, 0, 0]
        
    # Calculate min and max for each coordinate
    x_coords = [v[0] for v in vertices]
    y_coords = [v[1] for v in vertices]
    z_coords = [v[2] for v in vertices]
    
    center_x = (max(x_coords) + min(x_coords)) / 2
    center_y = (max(y_coords) + min(y_coords)) / 2
    center_z = (max(z_coords) + min(z_coords)) / 2
    
    print("\nShaft2.obj Analysis Report:")
    print("-" * 50)
    print(f"X range: {min(x_coords):.6f} to {max(x_coords):.6f}")
    print(f"Y range: {min(y_coords):.6f} to {max(y_coords):.6f}")
    print(f"Z range: {min(z_coords):.6f} to {max(z_coords):.6f}")
    print("-" * 50)
    print(f"Center coordinates:")
    print(f"X center: {center_x:.6f}")
    print(f"Y center: {center_y:.6f}")
    print(f"Z center: {center_z:.6f}")
    print("-" * 50)
    print(f"Dimensions:")
    print(f"Width (X): {max(x_coords) - min(x_coords):.6f}")
    print(f"Height (Y): {max(y_coords) - min(y_coords):.6f}")
    print(f"Depth (Z): {max(z_coords) - min(z_coords):.6f}")
    
    return [center_x, center_y, center_z]

def main():
    input_file = "shaft4.obj"
    
    try:
        print(f"Analyzing {input_file}...")
        vertices = read_obj(input_file)
        center = find_center(vertices)
        
        # Save the center coordinates to a text file
        with open("shaft2_center.txt", "w") as f:
            f.write(f"Shaft2.obj Center Coordinates:\n")
            f.write(f"X: {center[0]:.6f}\n")
            f.write(f"Y: {center[1]:.6f}\n")
            f.write(f"Z: {center[2]:.6f}\n")
            
        print(f"\nCenter coordinates have been saved to shaft2_center.txt")
        
    except FileNotFoundError:
        print(f"Error: File {input_file} not found")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    main()