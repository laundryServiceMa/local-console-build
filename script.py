import serial
import time
import argparse
import sys

def send_command(arduino, command):
    """
    Sends a command to the Arduino via the serial port.

    Args:
        arduino (serial.Serial): The serial port object.
        command (str or int): The command to send.
    """
    arduino.write(f"{command}\n".encode())
    print(f"Sent command: {command}")

def main():
    """
    Main function to parse command-line arguments, connect to the Arduino,
    send a command, and exit with an appropriate status code.

    Returns:
        int: 0 for success, 1 for error.
    """
    parser = argparse.ArgumentParser(description="Send a command to Arduino via serial port.")
    parser.add_argument("--port", required=True, help="Serial port to connect to (e.g., /dev/ttyUSB0 or COM3)")
    parser.add_argument("--baud", type=int, default=9600, help="Baud rate (default: 9600)")
    parser.add_argument("--mode", required=True, help="Mode to send ('start', 'stop', or a number 1-8)")

    args = parser.parse_args()

    try:
        print(f"Connecting to {args.port} at {args.baud} baud with mode {args.mode}")
        # Connect to Arduino
        arduino = serial.Serial(args.port, args.baud) # opens serial port
        # time.sleep(2)  # Wait for connection to establish
        # time.sleep(2)  # Wait for Arduino reset to complete

        try:
            mode = int(args.mode) # Attempts to convert the provided mode to an integer
            if 1 <= mode <= 8:
                send_command(arduino, mode) # If mode is an integer between 1 and 8, send it.
            else:
                print("Mode invalid. Must be between 1 and 8.")
                return 1  # Indicate an error
        except ValueError:
            if args.mode in ['start', 'stop']: # If mode is not an integer, check if it's 'start' or 'stop'
                send_command(arduino, args.mode) # If it is, send it.
            else:
                print("Mode invalid. Must be 'start', 'stop' or a number between 1 and 8.")
                return 1 #indicate error

        arduino.close() # Closes the serial port.
        return 0  # Indicate success

    except serial.SerialException as e:
        print(f"Error: Could not open serial port {args.port}. {e}")
        return 1 #indicate error
    except Exception as e:
        print(f"An unexpected error occured: {e}")
        return 1 # indicate error

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) # exits the program using the status code.