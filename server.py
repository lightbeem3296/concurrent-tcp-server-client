import socket
import threading
import argparse
import time
from collections import defaultdict
from queue import Queue

# Global data structures to store received data and pattern counts
received_data = defaultdict(str)
lock = threading.Lock()
pattern_queue = Queue()

# Function to handle each client connection
def handle_client(conn, addr, client_id, search_pattern=None):
    print(f"[INFO] Client {client_id} connected from {addr}")
    
    file_name = f"book_{client_id}.txt"
    file_written = False
    
    try:
        with conn:
            while True:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break

                with lock:
                    received_data[client_id] += data
                file_written = True
                
                # Logging received data
                print(f"[LOG] Received {len(data)} bytes from client {client_id}")

            # Write received data to file
            if file_written:
                try:
                    with open(file_name, 'w') as f:
                        f.write(received_data[client_id])
                    print(f"[INFO] Data from client {client_id} written to {file_name}")
                except IOError as e:
                    print(f"[ERROR] Failed to write data to {file_name}: {e}")
            else:
                print(f"[INFO] No data received from client {client_id}")
                
            if search_pattern:
                pattern_queue.put((client_id, search_pattern))
    
    except Exception as e:
        print(f"[ERROR] Error handling client {client_id}: {e}")
    finally:
        print(f"[INFO] Client {client_id} disconnected.")

# Function to analyze patterns in data
def pattern_analysis(search_pattern):
    while True:
        if not pattern_queue.empty():
            client_id, pattern = pattern_queue.get()
            data = received_data.get(client_id, "")
            occurrences = data.lower().count(pattern.lower())
            
            if occurrences > 0:
                print(f"[ANALYSIS] Pattern '{pattern}' found {occurrences} times in book_{client_id}.txt")
        time.sleep(3)  # Adjust the interval for pattern checking

# Main server function
def start_server(port, search_pattern=None):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))
    server.listen(10)  # Listening to 10 connections
    print(f"[INFO] Server listening on port {port}")

    client_count = 0
    threads = []

    try:
        while True:
            conn, addr = server.accept()
            client_count += 1
            client_id = client_count
            thread = threading.Thread(target=handle_client, args=(conn, addr, client_id, search_pattern))
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
    parser.add_argument("-l", "--listen", type=int, required=True, help="Port to listen on")
    parser.add_argument("-p", "--pattern", type=str, help="Pattern to search in text")

    args = parser.parse_args()
    
    # Start pattern analysis in a separate thread if the pattern is provided
    if args.pattern:
        pattern_thread = threading.Thread(target=pattern_analysis, args=(args.pattern,))
        pattern_thread.daemon = True
        pattern_thread.start()

    # Start the server
    start_server(args.listen, args.pattern)
