import argparse
import socket
import time


def send_file(filename, server_ip, port, delay):
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(10)  # Add timeout for connection attempt
            client_socket.connect((server_ip, port))
            print(f"[INFO] Connected to server {server_ip}:{port}")

            # Open the file and send its content
            try:
                with open(filename, "r", encoding="utf-8") as file:
                    for line in file:
                        client_socket.sendall(line.encode("utf-8"))
                        print(f"[LOG] Sent {len(line)} bytes")
                        time.sleep(delay)  # Simulate delay in sending data
                print(f"[INFO] File '{filename}' sent successfully.")
            except IOError as e:
                print(f"[ERROR] Failed to read or send file '{filename}': {e}")

    except FileNotFoundError:
        print(f"[ERROR] File '{filename}' not found.")
    except ConnectionRefusedError:
        print(f"[ERROR] Connection refused by the server at {server_ip}:{port}.")
    except socket.timeout:
        print(f"[ERROR] Connection to {server_ip}:{port} timed out.")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client to send a file to the server")
    parser.add_argument(
        "-f", "--file", type=str, required=True, help="Path to the file to be sent"
    )
    parser.add_argument("-i", "--ip", type=str, required=True, help="Server IP address")
    parser.add_argument(
        "-p", "--port", type=int, required=True, help="Server port number"
    )
    parser.add_argument(
        "-d",
        "--delay",
        type=float,
        default=0,
        help="Delay between sending lines (in seconds)",
    )

    args = parser.parse_args()

    # Send the file to the server
    send_file(args.file, args.ip, args.port, args.delay)
