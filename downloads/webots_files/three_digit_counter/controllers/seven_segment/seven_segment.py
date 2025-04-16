from controller import Supervisor

class SevenSegmentController:
    def __init__(self, supervisor, color_on, color_off):
        self.supervisor = supervisor

        # Define the segments for each digit
        self.digit_segments = [
            [f"a1", f"b1", f"c1", f"d1", f"e1", f"f1", f"g1"],  # Units
            [f"a2", f"b2", f"c2", f"d2", f"e2", f"f2", f"g2"],  # Tens
            [f"a3", f"b3", f"c3", f"d3", f"e3", f"f3", f"g3"]   # Hundreds
        ]

        # Segment patterns for digits 0-9
        self.segment_patterns = {
            0: [1, 1, 1, 1, 1, 1, 0],
            1: [0, 1, 1, 0, 0, 0, 0],
            2: [1, 1, 0, 1, 1, 0, 1],
            3: [1, 1, 1, 1, 0, 0, 1],
            4: [0, 1, 1, 0, 0, 1, 1],
            5: [1, 0, 1, 1, 0, 1, 1],
            6: [1, 0, 1, 1, 1, 1, 1],
            7: [1, 1, 1, 0, 0, 0, 0],
            8: [1, 1, 1, 1, 1, 1, 1],
            9: [1, 1, 1, 1, 0, 1, 1]
        }

        # Colors for on and off states
        self.color_on = color_on  # Bright green
        self.color_off = color_off  # Black

        # Retrieve material nodes for each segment
        self.segment_nodes = []
        for digit in self.digit_segments:
            digit_nodes = []
            for segment in digit:
                node = self.supervisor.getFromDef(segment)
                if node is None:
                    print(f"Error: Node with DEF name '{segment}' not found!")
                    exit()
                digit_nodes.append(node.getField("diffuseColor"))
            self.segment_nodes.append(digit_nodes)

    def set_digit(self, digit_index, value):
        """Set the digit at the given index (0 for units, 1 for tens, 2 for hundreds) to the given value (0-9)."""
        pattern = self.segment_patterns[value]
        for i, state in enumerate(pattern):
            color = self.color_on if state else self.color_off
            self.segment_nodes[digit_index][i].setSFVec3f(color)

    def display_number(self, number):
        """Display a number (0-999) using the three 7-segment displays."""
        if not (0 <= number <= 999):
            print("Error: Number out of range (must be 0-999)")
            return

        # Break the number into hundreds, tens, and units
        hundreds = number // 100
        tens = (number % 100) // 10
        units = number % 10

        # Update the displays
        self.set_digit(2, hundreds)
        self.set_digit(1, tens)
        self.set_digit(0, units)


# Main program
if __name__ == "__main__":
    # Create a Supervisor instance
    supervisor = Supervisor()

    # Define colors
    color_on = [0.0, 1.0, 0.0]  # Bright green
    color_off = [0.0, 0.0, 0.0]  # Black

    # Create an instance of the SevenSegmentController
    controller = SevenSegmentController(supervisor, color_on, color_off)

    # Run the simulation loop
    timestep = int(supervisor.getBasicTimeStep())
    while supervisor.step(timestep) != -1:
        try:
            # Get user input for the number to display
            number = 123
            controller.display_number(number)
        except ValueError:
            print("Invalid input. Please enter an integer between 0 and 999.")