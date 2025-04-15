from controller import Supervisor, Keyboard

# Create a Supervisor instance
supervisor = Supervisor()

# Get the simulation timestep
timestep = int(supervisor.getBasicTimeStep())

# Enable the keyboard to capture user input
keyboard = Keyboard()
keyboard.enable(timestep)

# Access the node by its DEF name
material_node = supervisor.getFromDef("f1")  # Replace "f" with the actual DEF name
if material_node is None:
    print("Error: Node with DEF name 'f1' not found! Please check the DEF name in your Webots scene tree.")
    exit()

print("Node successfully retrieved: 'f1'")

# Access the 'diffuseColor' field
diffuse_color_field = material_node.getField("diffuseColor")
if diffuse_color_field is None:
    print("Error: 'diffuseColor' field not found! Ensure the node has a material with a 'diffuseColor' property.")
    exit()

# Function to set a new color
def set_color(color, color_name):
    diffuse_color_field.setSFVec3f(color)
    print(f"Material color updated to {color_name} ({color})")

# Run the simulation loop
print("Press 'r' for red, 'y' for yellow, 'b' for blue, or 'g' for green.")
while supervisor.step(timestep) != -1:
    key = keyboard.getKey()  # Get the pressed key
    if key == ord('R') or key == ord('r'):  # Press 'R' or 'r' for red
        set_color([1.0, 0.0, 0.0], "red")
    elif key == ord('Y') or key == ord('y'):  # Press 'Y' or 'y' for yellow
        set_color([1.0, 1.0, 0.0], "yellow")
    elif key == ord('B') or key == ord('b'):  # Press 'B' or 'b' for blue
        set_color([0.0, 0.0, 1.0], "blue")
    elif key == ord('G') or key == ord('g'):  # Press 'G' or 'g' for green
        set_color([0.0, 1.0, 0.0], "green")