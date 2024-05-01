# Jasper Saez BSIT 2_B1 PROJECT GUESSING GAME!!!
import socket
import random
import threading

# Create a socket object for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to a specific address and port
server_socket.bind(('localhost', 5555))
# Set the server to listen for incoming connections, with a backlog of 2 pending connections
server_socket.listen(2)

# Print a message indicating that the server is running
print("Server is running...")

# Initialize empty leaderboards for different difficulty levels
leaderboard_easy = []
leaderboard_medium = []
leaderboard_hard = []

# Create a lock to synchronize access to shared data (leaderboards)
lock = threading.Lock()

# Function to generate a random number based on the difficulty level
def generate_number(difficulty):
    if difficulty == 'easy':
        return random.randint(1, 50)
    elif difficulty == 'medium':
        return random.randint(1, 100)
    elif difficulty == 'hard':
        return random.randint(1, 500)
    else:
        return random.randint(1, 50)  # Default to easy range

# Function to handle the game logic for each client connection
def play_game(conn, addr):
    # Receive the player's name from the client
    name = conn.recv(1024).decode()
    print(f"Player {name} connected from {addr}")

    while True:
        # Send instructions to the client
        conn.send("Choose difficulty (easy/medium/hard), type 'quit' to exit, type 'retry' to retry game, or 'leaderboard' to view leaderboard: ".encode())
        user_input = conn.recv(1024).decode()

        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'leaderboard':
            display_leaderboard(conn)
        else:
            difficulty = user_input.lower()
            secret_number = generate_number(difficulty)
            print(f"Generated secret number: {secret_number}")

            attempts = 0
            conn.send("Game Has started! Guess the number.".encode())
            while True:
                guess = int(conn.recv(1024).decode())
                attempts += 1

                if guess == secret_number:
                    conn.send("Congratulations! You guessed it right.".encode())
                    # Update the leaderboard with the player's stats
                    leaderboard = get_leaderboard(difficulty)
                    leaderboard.append((name, attempts, secret_number))
                    break
                elif guess < secret_number:
                    conn.send("Try higher.".encode())
                else:
                    conn.send("Try lower.".encode())

    conn.close()

# Function to display the leaderboard for a specific difficulty level
def display_leaderboard(conn):
    conn.send("Select difficulty for leaderboard (easy/medium/hard): ".encode())
    difficulty_choice = conn.recv(1024).decode()
    leaderboard = get_leaderboard(difficulty_choice)
    leaderboard.sort(key=lambda x: x[1])  # Sort by attempts (lower is better)
    leaderboard_str = f"\nLeaderboard ({difficulty_choice}):\n"
    for idx, (name, attempts, secret_number) in enumerate(leaderboard, start=1):
        leaderboard_str += f"{idx}. Name: {name}, Attempts: {attempts}, Number to guess: {secret_number}\n"
    conn.send(leaderboard_str.encode())

# Function to get the appropriate leaderboard based on the difficulty level
def get_leaderboard(difficulty):
    if difficulty == 'easy':
        return leaderboard_easy
    elif difficulty == 'medium':
        return leaderboard_medium
    elif difficulty == 'hard':
        return leaderboard_hard
    else:
        return leaderboard_easy  # Default to easy leaderboard

# Function to handle each client connection in a separate thread
def handle_client(conn, addr):
    play_game(conn, addr)
    conn.close()

# Main loop to accept incoming client connections
while True:
    conn, addr = server_socket.accept()
    print(f"New connection from {addr}")
    # Start a new thread to handle the client
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
