import numpy as np

# Get number_of_players and number_of_rounds from user
import numpy.random

error_message = "Input must be an Integer bigger then 0."
while True:
    try:
        number_of_players = int(input("How many people should play?\n1000000 is a realistic number, but the bigger "
                                      "the number, the longer it takes.\n"))
        if number_of_players < 1:
            raise ValueError
        break
    except ValueError:
        print(error_message)
while True:
    try:
        number_of_rounds = int(input("How many rounds should be played?\n112 is the amount for 1 year, but the "
                                     "bigger the number, the longer it takes.\n"))
        if number_of_rounds < 1:
            raise ValueError
        break
    except ValueError:
        print(error_message)

# The fixes prices
prices = {1.5: 1.25,
          2.5: 3.75,
          3.0: 6.25,
          3.5: 7.8,
          4.0: 19.0,
          4.5: 250.0,
          5.0: 1000.0,
          5.5: 35000.0}

# national_lottery
# [
#   [earnings, expenses, big_prize],
#   [winning_numbers]
# ]
national_lottery = np.array([
    [0.0, 0.0, 1000000.0],
    np.random.choice(range(1, 46), 6, replace=False)
], dtype=object)

# player
# [
#   [earnings, expenses, is_fixed, won_big],
#   [
#      [numbers1],
#      [numbers2],
#      ...,
#      [numbers8]
#   ],
#   [extras]
# ]

# Create the players
print("PLAYER CREATION STARTED")
all_players = np.array([[]], dtype=object)
# Check if number_of_players is even or odd and act accordingly
if number_of_players % 2 == 0:
    for _ in range(number_of_players // 2):
        # Create a player with fixed numbers
        player = np.array([
            [0.0, 0.0, 1.0, 0.0],
            [np.full(6, -1) for _ in range(8)],
            []
        ], dtype=object)
        player[2] = np.full(8, -1)
        # Extend the all_player_list
        if not all_players.size == 0:
            all_players = np.vstack((all_players, player))
        else:
            all_players = np.array([player])
else:
    for _ in range(number_of_players // 2 + 1):
        # Create a player with fixed numbers
        player = np.array([
            [0.0, 0.0, 1.0, 0.0],
            [np.full(6, -1) for _ in range(8)],
            []
        ], dtype=object)
        player[2] = np.full(8, -1)
        # Extend the all_player_list
        if not all_players.size == 0:
            all_players = np.vstack((all_players, player))
        else:
            all_players = np.array([player])
print("PLAYER CREATION AT 50%")
for _ in range(number_of_players // 2):
    # Create a player with no fixed numbers
    player = np.array([
        [0.0, 0.0, 0.0, 0.0],
        [np.full(6, -1) for _ in range(8)],
        []
    ], dtype=object)
    player[2] = np.full(8, -1)
    # Extend the all_player_list
    all_players = np.vstack((all_players, player))
print("PLAYER CREATION DONE")

# Play rounds
for current_round in range(number_of_rounds):
    print(f"ROUND {current_round+1} STARTED")
    # New numbers for national_lottery
    national_lottery[1] = numpy.random.choice(range(1, 46), 6, replace=False)
    big_winners = []
    for player_index in range(len(all_players)):
        # New numbers for player if not a fixed player or numbers aren't initialized
        if all_players[player_index][0][2] == 0.0 or all_players[player_index][1][0][0] == -1.0:
            all_players[player_index][1] = [np.random.choice(range(1, 46), 6, replace=False) for _ in range(8)]
            extras = np.random.choice(range(1, 46), 8, replace=True)
            for index in range(len(extras)):
                while np.isin(extras[index], all_players[player_index][1][index]):
                    extras[index] = np.random.randint(1, 46)
            all_players[player_index][2] = extras
        # Compare numbers and pay profits
        national_lottery[0][0] += 10
        all_players[player_index][0][1] += 10
        for entry_index in range(len(all_players[player_index][1])):
            mask = np.isin(national_lottery[1], all_players[player_index][1][entry_index])
            score = np.count_nonzero(mask)
            if all_players[player_index][2][entry_index] in national_lottery[1]:
                score += 0.5
            # Pay out smaller profits
            if score == 6:
                big_winners.append(player_index)
            elif score in (1.5, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5):
                all_players[player_index][0][0] += prices.get(score)
                national_lottery[0][1] += prices.get(score)
        # pay out big winners or increase pot
        if len(big_winners) > 0:
            pot = national_lottery[0][2] / len(big_winners)
            for winner_index in big_winners:
                all_players[winner_index][0][0] += pot
                all_players[winner_index][0][3] += 1.0
            national_lottery[0][1] += national_lottery[0][2]
            national_lottery[0][2] = 1000000.0
        else:
            national_lottery[0][2] += 750000.0

# Print statistics
players_list = list(all_players)
print("----- Biggest Winners -----")
players_list.sort(key=lambda x: (x[0][0] - x[0][1]), reverse=True)
[print(f"Balance: €{i[0][0] - i[0][1]}; plays with " + (lambda x: "SAME" if x == 1.0 else "DIFFERENT")(i[0][2]) +
       f" numbers; won big {i[0][3]} times") for i in players_list[0:10]]
print("----- Biggest Losers -----")
[print(f"Balance: €{i[0][0] - i[0][1]}; plays with " + (lambda x: "SAME" if x == 1.0 else "DIFFERENT")(i[0][2]) +
       f" numbers; won big {i[0][3]} times") for i in players_list[-1:-10:-1]]
print("----- National Lottery -----")
print(f"Earnings: €{national_lottery[0][0]}")
print(f"Expenses: €{national_lottery[0][1]}")
print(f"Balance: €{national_lottery[0][0] - national_lottery[0][1]}")
print("----- Other statistics -----")
profit_count = 0
loss_count = 0
jackpot_count = 0
for player in players_list:
    if player[0][0] - player[0][1] > 0.0:
        profit_count += 1
    elif player[0][0] - player[0][1] < 0.0:
        loss_count += 1
    if player[0][3] > 0:
        jackpot_count += 1
print(f"Number of players with profit: {profit_count}")
print(f"This is {profit_count / len(players_list) * 100} % of all players")
print(f"Number of players with losses: {loss_count}")
print(f"This is {loss_count / len(players_list) * 100} % of all players")
print(f"Number of players who hit the jackpot: {jackpot_count}")
print(f"This is {jackpot_count / len(players_list) * 100} % of all players")