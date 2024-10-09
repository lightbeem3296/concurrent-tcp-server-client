import argparse
import os
import socket
import threading
import time
from pathlib import Path

# Global data structures to store received data and pattern counts
CUR_DIR = Path(__file__).parent
UPLOADS_DIR = CUR_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


# Function to handle each client connection
def handle_client(conn, addr, client_id):
    print(f"[INFO] Client {client_id} connected from {addr}")

    file_name = f"book_{client_id}.txt"
    file_path = UPLOADS_DIR / file_name
    no_data = True

    try:
        with conn:
            recv_data = ""
            while True:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    break

                no_data = False
                recv_data += data

                # Logging received data
                print(f"[LOG] Received {len(data)} bytes from client {client_id}")

            # Write received data to file
            if not no_data:
                try:
                    with file_path.open("w") as f:
                        f.write(recv_data)
                    print(f"[INFO] Data from client {client_id} written to {file_name}")
                except IOError as e:
                    print(f"[ERROR] Failed to write data to {file_name}: {e}")
            else:
                print(f"[INFO] No data received from client {client_id}")

    except Exception as e:
        print(f"[ERROR] Error handling client {client_id}: {e}")
    finally:
        print(f"[INFO] Client {client_id} disconnected.")


# Function to analyze patterns in data
def pattern_analysis(search_pattern):
    while True:
        print("[ANALYSIS] Begin")
        occurrences: dict[str, int] = {}

        fnames = os.listdir(UPLOADS_DIR)
        for fname in fnames:
            found = 0
            fpath = UPLOADS_DIR / fname
            with fpath.open("r") as file:
                for line in file:
                    if search_pattern in line:
                        found += 1
            occurrences[fname] = found

        sorted_occurrences = dict(
            sorted(
                occurrences.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        )
        for fname, value in sorted_occurrences.items():
            if value > 0:
                fpath = UPLOADS_DIR / fname
                with fpath.open("r") as file:
                    title = file.readline().strip()
                print(
                    f"[ANALYSIS] Pattern '{search_pattern}' found {value} times in `{title}`({fname})"
                )
            else:
                break
        print("[ANALYSIS] End")

        time.sleep(3)  # Adjust the interval for pattern checking


# Main server function
def start_server(port, search_pattern: None):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))
    server.listen(10)  # Listening to 10 connections
    print(f"[INFO] Server listening on port {port}")

    threads = []

    try:
        while True:
            conn, addr = server.accept()
            client_id = str(time.time())
            thread = threading.Thread(
                target=handle_client, args=(conn, addr, client_id)
            )
            thread.start()
            threads.append(thread)

    except KeyboardInterrupt:
        print("\n[INFO] Server shutting down...")
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
    finally:
        server.close()
        print("[INFO] Server socket closed.")

    for thread in threads:
        thread.join()


# Argument parsing for dynamic port and pattern input
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-threaded Network Server")
    parser.add_argument(
        "-l",
        "--listen",
        type=int,
        required=True,
        help="Port to listen on",
    )
    parser.add_argument(
        "-p",
        "--pattern",
        type=str,
        help="Pattern to search in text",
    )

    args = parser.parse_args()

    # Start pattern analysis in a separate thread if the pattern is provided
    if args.pattern:
        pattern_thread = threading.Thread(target=pattern_analysis, args=(args.pattern,))
        pattern_thread.daemon = True
        pattern_thread.start()

    # Start the server
    start_server(args.listen, args.pattern)
