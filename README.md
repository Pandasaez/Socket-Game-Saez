# Socket-Game-Saez
 > Here is a simple Socket Guessing Game using Python

> The Giving instruction to make this Number Guessing Game program
1. user/client can repeat the game without disconnecting
1. user can choose difficulty based on the generated random number to guess
   
  * easy (1-50)
* medium (1-100)
* hard (1-500)
3. the game implements a scoring mechanism based on the number of tries the user guesses the number to guess (less tries the better), and provide a leaderboard containing the name of the user and her/his score which is displayed after the user/client disconnects from the server.
4. persistence - the server should save the user's name, his/her score, and the last chosen difficulty (should default to easy) into a file and this file will be loaded/updated during leaderboard display and when the user set's the difficulty.
