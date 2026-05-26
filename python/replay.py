import serial
import time
import csv
import sys
import os

PORT = "/dev/ttyACM0"
BAUD = 9600

def send_motor_command(ser, left, right):
    command = f"L{left} R{right}\n"
    ser.write(command.encode())
    print("Sent:", command.strip())

def replay_file(filepath):
    if not os.path.exists(filepath):
        print("File not found:", filepath)
        return

    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)

    print("Replaying:", filepath)

    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    previous_time = 0.0

    for row in rows:
        current_time = float(row["time_sec"])
        delay = current_time - previous_time

        if delay > 0:
            time.sleep(delay)

        left_motor = int(row["left_motor"])
        right_motor = int(row["right_motor"])

        send_motor_command(ser, left_motor, right_motor)

        previous_time = current_time

    send_motor_command(ser, 0, 0)
    ser.close()

    print("Replay finished")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("python python/replay.py datasets/YOUR_FILE.csv")
        return

    filepath = sys.argv[1]
    replay_file(filepath)

if __name__ == "__main__":
    main()
