import random
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", " "]
points = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 4, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10, 0]
letters_to_points = {key:value for key, value in zip(letters, points)}
turn_count = -1
players_to_words = {}
player_letterbag = {}
word_list = []
with open('fullwordlist.txt') as fullwordlist:
    for line in fullwordlist:
      word_list.append(line.strip().lower())

def score_word(word):
  point_total = 0
  for letter in word:
    point_total += letters_to_points.get(letter.upper(), 0)
  return point_total

def playerScore(table):
  score = 0
  for word in table:
    score += score_word(word)
  return score

def letterbag(players_to_words, player_letterbag):
  for player in players_to_words:
    letter_list = []
    for i in range(0, 6):
      number = random.randint(0, 25)
      letter_list += letters[number]
    player_letterbag[player] = letter_list

def add_letter(player):
  current_letters = player_letterbag.get(player)
  if len(current_letters) > 12:
    current_letters = []
  if len(current_letters) < 6:
    num = 6 - len(current_letters)
    new_letters = current_letters
    for i in range(num):
      number = random.randint(0, 25)
      new_letters += letters[number]
  else: 
    number = random.randint(0, 25)
    new_letters = current_letters + list(letters[number])
  player_letterbag[player] = new_letters

def allScores():
  for player in players:
    player_score = playerScore(players_to_words.get(player))
    print("{player}'s total word list is: {list}".format(player = player, list = players_to_words.get(player)))
    print("{player} has a score of {player_score}".format(player = player, player_score = player_score))
    print("\n")
  main(players, num_players)


def check_word(new_word, player):
  if new_word.lower() in word_list:
      word_upper = ""
      for l in new_word:
          word_upper += l.upper()
      current_letters = player_letterbag.get(player)
      modified_letters = current_letters
      for l in word_upper:
          if l in modified_letters:
              modified_letters.remove(l)
          else:
              print("Those letters are not part of your inventory! Your turn is invalid.")
              return False
      player_letterbag[player] = modified_letters
      return True
  else:
    print("That's not a word.")
    return False
      

def landing():
  instructions = input("""
Press 1 to go to next players turn.
Press 2 to see all player's scores. """)
  if instructions == str("1"):
    main(players, num_players)
  elif instructions == str("2"):
    allScores()
  else:
    landing()


def addWord(player):
  current_words = players_to_words.get(player)
  add_letter(player)
  current_letters = player_letterbag.get(player)
  print("Your current letters: " + str(current_letters))
  new_word = str(input("Enter your new word! "))
  while " " in new_word:
    new_word = new_word.replace(" ", "")
  if new_word == "":
    print("You have skipped your turn. Maybe you'll get a good letter next time!")
  else:
    if check_word(new_word, player) == True:
      temp = current_words + [str(new_word)]
      players_to_words[player] = temp
      print("Your word \"{word}\" is worth {num} points!".format(word = new_word, num = score_word(new_word)))
    else:
      pass
  print("Your total word list:", players_to_words[player])
  print("Your total score:", playerScore(players_to_words[player]))
  landing()

def main(players, num_players):
  global turn_count
  turn_count += 1
  turn = turn_count % num_players
  current_player = players[turn]
  print("\n" + "It is {user}'s turn! ".format(user = current_player))
  addWord(current_player)

def start():
  global num_players
  num_players = int(input("How many players? "))
  for num in range(0, num_players):
    name = input("Name of player " + str(int(num + 1)) + "? ")
    if name in players_to_words:
      print("Sorry, you can't repeat names. This player has been banished.")
      num_players -= 1
    else:
      players_to_words[name] = []
  global players 
  players = list(players_to_words)
  letterbag(players_to_words, player_letterbag)
  main(players, num_players)

start()