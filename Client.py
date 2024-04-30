import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5555))

name = input("Enter your name: ")
client_socket.send(name.encode())

while True:
    response = client_socket.recv(1024).decode()
    if not response:
        break

    print(response)

    if "Guess the number" in response:
        guess = input("Enter your guess: ")
        client_socket.send(guess.encode())
    elif "Select difficulty" in response:
        user_input = input("Enter difficulty to view leaderboard (easy/medium/hard): ")
        client_socket.send(user_input.encode())
        leaderboard_data = client_socket.recv(1024).decode()
        print("\nLeaderboard:")
        print(leaderboard_data)
    else:
        user_input = input()
        client_socket.send(user_input.encode())

client_socket.close()
