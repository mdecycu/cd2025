from controller import Supervisor

def run_supervisor():
    # Create the Supervisor instance
    supervisor = Supervisor()

    # Get simulation time step
    timestep = int(supervisor.getBasicTimeStep())

    # Get the emitter for sending commands
    emitter = supervisor.getDevice("emitter")  # Ensure the emitter is defined in your world file
    if emitter is None:
        print("Error: Could not find emitter device")
        return

    # Get the ball node to calculate distance
    ball_node = supervisor.getFromDef("ball")  # Replace "ball" with the ball's DEF name
    if ball_node is None:
        print("Error: Could not find ball with DEF name 'ball'")
        return

    # Get the sensor node (to calculate distance from the sensor to the ball)
    sensor_node = supervisor.getFromDef("MySensor")  # Replace "MySensor" with the sensor's DEF name
    if sensor_node is None:
        print("Error: Could not find sensor with DEF name 'MySensor'")
        return

    # Initialize scoring logic
    score = 0
    last_score_time = 0
    cooldown = 1.0  # Cooldown time in seconds

    # Main control loop
    while supervisor.step(timestep) != -1:
        # Get the positions of the sensor and the ball
        sensor_position = sensor_node.getPosition()  # Get the sensor's global position
        ball_position = ball_node.getPosition()  # Get the ball's global position

        # Calculate the distance between the sensor and the ball
        distance = ((sensor_position[0] - ball_position[0]) ** 2 +
                    (sensor_position[1] - ball_position[1]) ** 2 +
                    (sensor_position[2] - ball_position[2]) ** 2) ** 0.5

        # Simulate a sensor value based on distance
        sensor_value = 1000 - (distance * 1000)  # Example: Convert distance to an approximate sensor value
        sensor_value = max(sensor_value, 0)  # Ensure sensor value is not negative

        # Scoring logic
        current_time = supervisor.getTime()
        if sensor_value > 200 and (current_time - last_score_time) > cooldown:
            score += 2
            last_score_time = current_time
            print(f"得分! Score: {score}")

        # Send motor position command to the robot
        motor_position = 38 * 3.14159 / 180  # Motor position in radians
        message = f"SET_POSITION:{motor_position}"  # Construct the command message
        emitter.send(message.encode("utf-8"))  # Send the message via the emitter

if __name__ == "__main__":
    run_supervisor()