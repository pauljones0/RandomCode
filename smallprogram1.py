from random import randint 

num=0
cnum=0

print("The computer is going to choose a random number between one and ten.\nEach time you guess, the computer will choose a new number. \nIf you can guess the same number as the computer, you win!\n")

def guess():
  human_guess = int(input("Pick a number between one and ten!\n"))
  computer_guess = randint(1, 10)
  return human_guess, computer_guess


num, cnum = guess()
while num != cnum:
  print("Whoopsie! You guessed the wrong number. Try again!\n")
  num, cnum = guess()
print("Congrats you won!")
