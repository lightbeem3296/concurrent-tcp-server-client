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

1. **Environment**: `Linux` or `WSL`
2. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

3. **Install Dependencies**:
   No external dependencies are needed beyond Python 3.x.

4. **Download Text Files**:
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

```bash
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

### Client Usage

The `client.py` file provides a simple way to connect to the server and send text data. You can run the client using the following command:

```bash
python3 client.py -i <server_address> -p <port> -f <file>
```

- Replace `<server_address>` with the address of the server (e.g., `localhost`).
- Replace `<port>` with the port number the server is listening on (e.g., `8080`).
- Replace `<file>` with the path to the text file you want to send.

**Example**: Send the file `book.txt` to the server on `localhost` and port `8080`.

```bash
python3 client.py localhost 8080 book.txt
```

#### Client Output Example

When the client sends data, you should see output similar to:

```bash
[INFO] Connecting to server at localhost:8080
[INFO] Sent 1024 bytes from book.txt
[INFO] File sent successfully.
```

### Performing Pattern Analysis

If a search pattern is provided when starting the server, the server will periodically check for occurrences of the pattern in the received data and log the results.

### Stopping the Server

To stop the server, you can use `CTRL + C` in the terminal where it is running. This will trigger a graceful shutdown.

#### Example Output on Server Shutdown

```bash
[INFO] Server shutting down...
[INFO] Server socket closed.
```

## Testing

This project includes tests to ensure thread safety, scalability, and correct file creation. The tests are located in the `test_server.py` file and can be run using the following command:

```bash
python3 -m unittest test_server.py
```

### Test Cases

- **Concurrent Connections**: The server is tested with 10 simultaneous client connections to ensure it handles multiple connections efficiently.
- **No Data Connection**: Tests verify that connections without sent data do not result in file creation.
- **Logging Behavior**: Tests check that appropriate logging occurs for various connection scenarios.

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
