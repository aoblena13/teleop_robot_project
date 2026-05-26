import serial
import time

PORT = "/dev/ttyACM0"
BAUD = 9600

def send_command(ser, left, right):
    command = f"L{left} R{right}\n"
    ser.write(command.encode())
    print("Sent:", command.strip())

    time.sleep(0.1)

    while ser.in_waiting:
        print("Arduino:", ser.readline().decode(errors="ignore").strip())

def main():
    print("Opening serial port...")
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)

    send_command(ser, 120, 120)
    time.sleep(2)

    send_command(ser, 0, 0)
    time.sleep(1)

    send_command(ser, -120, -120)
    time.sleep(2)

    send_command(ser, 0, 0)

    ser.close()
    print("Done")

if __name__ == "__main__":
    main()
