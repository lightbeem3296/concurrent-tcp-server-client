# Multi-threaded Network Server and Client

This project implements a multi-threaded network server in Python that can handle multiple client connections. The server receives and stores text data uniquely for each client and can perform pattern analysis based on command-line input. It is designed for scalability and robustness.

## Features

- **Multi-threaded Server**: Efficiently handles multiple simultaneous client connections.
- **Dynamic Port Handling**: The server can listen on a port specified via command line.
- **Client-Specific Output**: Each client connection generates a unique output file.
- **Pattern Analysis**: Optionally searches for specific patterns in the received data.
- **Logging**: Detailed logs of connections, data received, and pattern analysis.

## Requirements

- Python 3.x
- `netcat` for sending files to the server (Install via package manager)

## Installation

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**:
   No external dependencies are needed beyond Python 3.x.

3. **Download Text Files**:
   Download large text files (e.g., from Project Gutenberg) in plain text (UTF-8) format. Ensure that each file starts with the book title on the first line.

## Usage

### Running the Server

To run the server, use the following command:

```bash
python3 server.py -l <port> [-p <pattern>]
```

- Replace `<port>` with the desired port number (e.g., `8080`).
- Optionally, specify a search pattern using the `-p` option.

**Example**: Run the server on port `8080` and search for the pattern `"happy"`.

```bash
python3 server.py -l 8080 -p "happy"
```

#### Server Output Example

When the server starts, you should see output similar to the following:

```sh
[INFO] Server listening on port 8080
```

### Sending Files using Netcat

Use the `netcat` tool to send the text files to the server:

```bash
nc localhost <port> -i <delay> < file.txt
```

- Replace `<port>` with the port number the server is listening on (e.g., `8080`).
- Replace `<delay>` with the delay in seconds between sending lines.
- Replace `file.txt` with the path to your text file.

**Example**: Send the file `book.txt` to the server on port `8080` with a delay of `1` second between lines.

```bash
nc localhost 8080 -i 1 < book.txt
```

#### Netcat Output Example

You might see output like this when sending data:

```sh
[INFO] Connected to server 127.0.0.1:8080
[LOG] Sent 1024 bytes
[INFO] File 'book.txt' sent successfully.
```

### Server Log Example

When the server receives data from the client, you will see logs similar to:

```sh
[INFO] Client 1 connected from ('127.0.0.1', 12345)
[LOG] Received 1024 bytes from client 1
[INFO] Data from client 1 written to book_1.txt
[ANALYSIS] Pattern 'happy' found 5 times in book_1.txt
[INFO] Client 1 disconnected.
```

### Performing Pattern Analysis

If a search pattern is provided when starting the server, the server will periodically check for occurrences of the pattern in the received data and log the results.

### Stopping the Server

To stop the server, you can use `CTRL + C` in the terminal where it is running. This will trigger a graceful shutdown.

#### Example Output on Server Shutdown

```sh
[INFO] Server shutting down...
[INFO] Server socket closed.
```

## Testing

This project has been tested with multiple simultaneous client connections to ensure scalability and robustness. The server is designed to handle over 10 connections efficiently.

## Makefile

A `Makefile` is included for convenience. You can use the following commands:

- To run the server:

  ```bash
  make run_server
  ```

- To run the client:

  ```bash
  make run_client
  ```

- To clean up generated files:

  ```bash
  make clean
  ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
