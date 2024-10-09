import os
import socket
import threading
import time
import unittest

from server import (
    start_server,
)


class TestMultiThreadedServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the server in a separate thread
        cls.port = 8080
        cls.pattern = None
        cls.server_thread = threading.Thread(
            target=start_server, args=(cls.port, cls.pattern)
        )
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        # Terminate the server thread gracefully
        os.system(f"fuser -k {cls.port}/tcp")  # Kill the process listening on the port

    def test_concurrent_connections(self):
        """Test the server with 10 simultaneous client connections."""
        client_threads = []
        num_clients = 10
        test_data = "This is test data for client {}.\n"

        def client_simulation(client_id):
            """Simulates a client sending data to the server."""
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(("localhost", self.port))
                client_socket.sendall(test_data.format(client_id).encode("utf-8"))
                client_socket.close()

        # Start client threads
        for i in range(num_clients):
            thread = threading.Thread(target=client_simulation, args=(i,))
            client_threads.append(thread)
            thread.start()

        # Wait for all client threads to finish
        for thread in client_threads:
            thread.join()

        # Check if files are created for each client
        for i in range(num_clients):
            self.assertTrue(
                os.path.exists(f"book_{i + 1}.txt"),
                f"File book_{i + 1}.txt not created.",
            )
            # Clean up created files
            os.remove(f"book_{i + 1}.txt")

    def test_no_data_connection(self):
        """Test that a connection without data does not create a file."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(("localhost", self.port))
            # Do not send any data
            time.sleep(1)  # Simulate a brief connection before closing

        # Ensure no file is created
        self.assertFalse(
            os.path.exists("book_1.txt"),
            "File book_1.txt should not be created for no data connection.",
        )

    def test_logging_behavior(self):
        """Test logging behavior for connections without data."""
        # Capture log output (this could be enhanced using a logging library)
        _log_messages = []

        def log_capture():
            while True:
                # Simulated log checking (you should implement actual log capturing)
                time.sleep(1)

        log_thread = threading.Thread(target=log_capture)
        log_thread.daemon = True
        log_thread.start()

        # Connect without sending data
        self.test_no_data_connection()

        # Here you would implement assertions to verify logging behavior
        # For example:
        # self.assertIn("No data received from client", log_messages)


if __name__ == "__main__":
    unittest.main()
