# Makefile for Multi-threaded Network Server and Client

.PHONY: all clean run_server run_client

# Variables
SERVER = server.py
CLIENT = client.py
PORT = 8080
PATTERN = "happy"
FILE = book.txt
DELAY = 1

all: run_server run_client

# Command to run the server
run_server:
	@echo "Starting the server on port $(PORT) with pattern $(PATTERN)..."
	python3 $(SERVER) -l $(PORT) -p $(PATTERN)

# Command to run the client
run_client:
	@echo "Sending file $(FILE) to the server on port $(PORT) with a delay of $(DELAY) seconds..."
	nc localhost $(PORT) -i $(DELAY) < $(FILE)

# Clean up generated files (if any)
clean:
	@echo "Cleaning up generated files..."
	rm -f book_*.txt
