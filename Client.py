import socket

# Create a socket object for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the client socket to the server at localhost:5555
client_socket.connect(('localhost', 5555))

# Get the player's name from user input and send it to the server
name = input("Enter your name: ")
client_socket.send(name.encode())

# Main loop for interacting with the server
while True:
    # Receive responses from the server
    response = client_socket.recv(1024).decode()
    if not response:  # If the response is empty, break the loop
        break

    print(response)  # Print the server's response to the console

    if "Guess the number" in response:  # If the server asks for a guess
        guess = input("Enter your guess: ")  # Get the user's guess
        client_socket.send(guess.encode())  # Send the guess to the server
    elif "Select difficulty" in response:  # If the server asks for leaderboard difficulty
        user_input = input("Enter difficulty to view leaderboard (easy/medium/hard): ")
        client_socket.send(user_input.encode())  # Send the difficulty choice to the server
        leaderboard_data = client_socket.recv(1024).decode()  # Receive leaderboard data from the server
        print("\nLeaderboard:")
        print(leaderboard_data)  # Print the leaderboard data to the console
    else:  # For other server messages, just send user input back to the server
        user_input = input()
        client_socket.send(user_input.encode())

# Close the client socket when the loop ends
client_socket.close()
