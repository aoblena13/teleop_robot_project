import pygame
import serial
import time
import csv
import os
from datetime import datetime

PORT = "/dev/ttyACM0"
BAUD = 9600

MAX_SPEED = 180
DEADZONE = 0.15
DATASET_DIR = "datasets"

def clamp(value, low, high):
    return max(low, min(high, value))

def apply_deadzone(value):
    if abs(value) < DEADZONE:
        return 0.0
    return value

def send_motor_command(ser, left, right):
    left = int(clamp(left, -255, 255))
    right = int(clamp(right, -255, 255))
    command = f"L{left} R{right}\n"
    ser.write(command.encode())
    return command.strip()

def main():
    os.makedirs(DATASET_DIR, exist_ok=True)

    filename = datetime.now().strftime("teleop_joystick_%Y%m%d_%H%M%S.csv")
    filepath = os.path.join(DATASET_DIR, filename)

    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No joystick detected.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("Joystick detected:", joystick.get_name())
    print("Dataset:", filepath)
    print("Left stick controls driving.")
    print("Move stick up/down = forward/backward")
    print("Move stick left/right = turning")
    print("Press Ctrl+C to stop.")

    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)

    start_time = time.time()

    try:
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "time_sec",
                "axis_x",
                "axis_y",
                "left_motor",
                "right_motor",
                "serial_command"
            ])

            while True:
                pygame.event.pump()

                axis_x = joystick.get_axis(0)
                axis_y = joystick.get_axis(1)

                axis_x = apply_deadzone(axis_x)
                axis_y = apply_deadzone(axis_y)

                forward = -axis_y
                turn = axis_x

                left_motor = (forward + turn) * MAX_SPEED
                right_motor = (forward - turn) * MAX_SPEED

                left_motor = int(clamp(left_motor, -255, 255))
                right_motor = int(clamp(right_motor, -255, 255))

                command = send_motor_command(ser, left_motor, right_motor)

                elapsed = time.time() - start_time

                writer.writerow([
                    round(elapsed, 4),
                    round(axis_x, 4),
                    round(axis_y, 4),
                    left_motor,
                    right_motor,
                    command
                ])

                print(
                    f"time={elapsed:.2f} "
                    f"x={axis_x:.2f} y={axis_y:.2f} "
                    f"L={left_motor} R={right_motor}"
                )

                time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nStopping teleop...")

    finally:
        send_motor_command(ser, 0, 0)
        ser.close()
        pygame.quit()
        print("Motors stopped.")
        print("Saved dataset:", filepath)

if __name__ == "__main__":
    main()