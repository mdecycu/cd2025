from controller import Robot, Receiver

def run_robot():
    # Create the Robot instance
    robot = Robot()

    # Get simulation time step
    timestep = int(robot.getBasicTimeStep())

    # Get the motor device
    motor = robot.getDevice("motor1")  # Replace "motor1" with the actual motor name
    if motor is None:
        print("Error: Could not find motor device")
        return

    # Get the receiver for receiving commands
    receiver = robot.getDevice("receiver")  # Ensure the receiver is defined in your world file
    if receiver is None:
        print("Error: Could not find receiver device")
        return
    receiver.enable(timestep)

    # Main control loop
    while robot.step(timestep) != -1:
        # Process received messages
        if receiver.getQueueLength() > 0:
            message = receiver.getString() # Receive the message
            receiver.nextPacket()  # Move to the next packet

            # Parse the command message
            if message.startswith("SET_POSITION:"):
                position = float(message.split(":")[1])  # Extract the desired position
                motor.setPosition(position)  # Set the motor position

if __name__ == "__main__":
    run_robot()