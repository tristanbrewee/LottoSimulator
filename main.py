# Global functions used in classes
import random
import threading


def generate_random_number_single():
    """
    Generates a random int between 1 and 45.
    """
    import random
    return random.randint(1, 46)


def generate_numbers_set():
    """
    Generates a set of 6 random ints between 1 and 45.
    """
    return set(random.sample(range(1, 46), 6))


# National Lottery Class
class NationalLottery:
    """
    Represents the National Lottery.
    Has earnings, expenses, set of winning numbers, dictionary of score/price-pairs, and a big price.
    Has getBalance, increaseBigPrice, resetBigPrice, checkNumbers, changeNumbers, and printSummary.
    """

    def __init__(self):
        """
        Sets all attributes at it's default value.
        """
        self.earnings = 0.0
        self.expenses = 0.0
        self.winning_numbers = None
        self.prices = {1.5: 1.25,
                       2.5: 3.75,
                       3.0: 6.25,
                       3.5: 7.8,
                       4.0: 19.0,
                       4.5: 250.0,
                       5.0: 1000.0,
                       5.5: 35000.0}
        self.big_price = 1000000.0

    def get_balance(self):
        """
        Returns earnings - expenses, thus reflecting the profit or balance.
        """
        return self.earnings - self.expenses

    def increase_big_price(self):
        """
        Increases the bigPrice with 750000, as is custom when the price isn't won.
        """
        self.big_price += 750000.0

    def reset_big_price(self):
        """
        Resets the bigPrice to 1000000, as is custom when the prices is won.
        """
        self.big_price = 1000000.0

    def check_numbers(self, player_numbers, extra_number):
        """
        Checks if a given set (from player) matches the winningNumbers.
        Checks if the extraNumber is in the winningNumbers.
        A score is returned based on matches (1 for number in set, 0.5 for extraNumber).
        """
        score = len(list(player_numbers & self.winning_numbers))
        if extra_number in self.winning_numbers:
            score += 0.5
        return score

    def change_numbers(self):
        """
        Changes the winningNumbers, as is custom with every new round.
        """
        self.winning_numbers.clear()
        self.winning_numbers.update(generate_numbers_set())

    def print_summary(self):
        """
        Prints the earnings, expenses, and balance of the National Lottery.
        """
        print("----- National Lottery -----")
        print(f"Earnings: €{self.earnings}")
        print(f"Expenses: €{self.expenses}")
        print("Balance: €" + str(self.get_balance()))


# Functions used in Player Class
def generate_new_numbers_for_player(all_numbers):
    """
    Updates all_numbers.
    Generates a set of size 6 for each element in the tuple, with its between 1 and 45.
    """
    for number_set in all_numbers:
        number_set.clear()
    for number_set in all_numbers:
        number_set.update(generate_numbers_set())
        while all_numbers.count(number_set) > 1:
            number_set.clear()
            number_set.update(generate_numbers_set())


# Player Class
class Player:
    """
    Represents a player.
    Has earnings, expenses, isFixedPlayer, allNumbers, allExtras, and wonBig.
    Has generateNewNumbers, generateExtras, wonBigAdd, getBalance, play, and printSummary.
    """

    def __init__(self, is_fixed_player):
        """
        Sets all attributes at it's default or given value.
        """
        self.earnings = 0.0
        self.expenses = 0.0
        self.is_fixed_player = is_fixed_player
        self.all_numbers = tuple(set() for _ in range(8))
        self.all_extras = [None for _ in range(8)]
        self.won_big = 0

    def generate_extras(self):
        """
        Updates all_extras
        Generates a int between 1 and 45 that is not in all_numbers with the same index.
        """
        for i in range(len(self.all_extras)):
            self.all_extras[i] = generate_random_number_single()
            while self.all_extras[i] in self.all_numbers[i]:
                self.all_extras[i] = generate_random_number_single()

    def won_big_add(self):
        """
        Increments wonBig with 1.
        """
        self.won_big += 1

    def get_balance(self):
        """
        Returns earnings - expenses, thus reflecting the profit or balance.
        """
        return self.earnings - self.expenses

    def play(self, national_lottery):
        """
        Simulates a player playing a round in the Lottery.
        If the player isn't a fixed player, new numbers are generated.
        €10 are added to the players expenses.
        The players numbers are checked with the Lottery's winningNumbers.
        Potential winnings are added to the players earnings.
        An exception is when the player won the bigPrice.
        In this case true is returned, else false.
        The bigPrice is split evenly among all winners.
        Returns a list of lotto_earning, lotto_expanses, _is_big_winner
        """
        if not self.is_fixed_player or not len(self.all_numbers[0]):
            generate_new_numbers_for_player(self.all_numbers)
            self.generate_extras()
        lottery_earnings_expenses_big_winner = [10, 0, False]
        self.expenses += 10
        prices = national_lottery.prices
        for i in range(len(self.all_numbers)):
            score = national_lottery.check_numbers(self.all_numbers[i], self.all_extras[i])
            if score == 6:
                lottery_earnings_expenses_big_winner[2] = True
            elif score not in (0, 0.5, 1, 2):
                winnings = prices.get(score)
                self.earnings += winnings
                lottery_earnings_expenses_big_winner[1] = winnings
        return lottery_earnings_expenses_big_winner

    def print_summary(self):
        """
        Prints the players balance, if he is a fixed player, and if he won big.
        """
        print("Balance: €" + str(self.get_balance()) + "; plays with " + (lambda x: "SAME" if x else "DIFFERENT")(
            self.is_fixed_player) + f" numbers; won big {self.won_big} times")


# Thread Create Players Class
class ThreadCreatePlayersClass(threading.Thread):
    """
    A custom thread to create players.
    """

    def __init__(self, amount, name, player_lis, lock):
        """
        Sets all attributes to their default value based on the given parameters.
        """
        super().__init__()
        self.player_tuple_from_thread = ()
        self.amount = amount
        self.name = name
        self.player_list = player_lis
        self.lock = lock

    def run(self):
        """
        Generates players and adds them to the players_list with a lock.
        """
        print(str(self.name) + " started")
        if not self.amount % 2 == 0:
            players_true = tuple(Player(True) for _ in range(self.amount // 2 + 1))
        else:
            players_true = tuple(Player(True) for _ in range(self.amount // 2))
        players_false = tuple(Player(False) for _ in range(self.amount // 2))
        self.player_tuple_from_thread += players_true + players_false
        with self.lock:
            self.player_list += self.player_tuple_from_thread
        print(str(self.name) + " done")


# Thread Play Round Class
class ThreadPlayRoundClass(threading.Thread):
    """
    A custom thread to play a single round.
    """

    def __init__(self, begin_index, end_index, name, player_list, national_lottery, big_winners, lock):
        """
        Sets all attributes to their default value based on the given parameters.
        """
        super().__init__()
        self.begin_index = begin_index
        self.end_index = end_index
        self.name = name
        self.player_list = player_list
        self.national_lottery = national_lottery
        self.big_winners = big_winners
        self.lock = lock

    def run(self):
        """
        Plays a round for a given subset of the player_list.
        """
        print(str(self.name) + " at 0%")
        flag_25 = False
        flag_50 = False
        flag_75 = False
        point_25 = (self.end_index - self.begin_index) / 100 * 25 + self.begin_index
        point_50 = (self.end_index - self.begin_index) / 100 * 50 + self.begin_index
        point_75 = (self.end_index - self.begin_index) / 100 * 75 + self.begin_index
        lottery_earnings = 0
        lottery_expenses = 0
        if self.end_index == -1:
            self.end_index = len(self.player_list)
        for i in range(self.begin_index, self.end_index):
            lottery_earnings_expenses_big_winner = self.player_list[i].play(self.national_lottery)
            if lottery_earnings_expenses_big_winner[2]:
                with self.lock:
                    self.big_winners.append(self.player_list[i])
            lottery_earnings += lottery_earnings_expenses_big_winner[0]
            lottery_expenses += lottery_earnings_expenses_big_winner[1]
            if not flag_25 and i > point_25:
                print(str(self.name) + " at 25%")
                flag_25 = True
            elif not flag_50 and i > point_50:
                print(str(self.name) + " at 50%")
                flag_50 = True
            elif not flag_75 and i > point_75:
                print(str(self.name) + " at 75%")
                flag_75 = True
        with self.lock:
            self.national_lottery.earnings += lottery_earnings
            self.national_lottery.expenses += lottery_expenses
        print(str(self.name) + " done")


# Global functions used in actual program
def get_cpu_count():
    """
    Returns the amount of available cpus
    """
    import multiprocessing
    return multiprocessing.cpu_count()


def generate_players_multi_threaded(amount):
    """
    Generates an amount of players and returns them as a list.
    This function uses multithreading based on the available cpus
    """
    cpus = get_cpu_count()
    players_list = []
    lock = threading.Lock()
    if not amount % cpus == 0:
        amount_per_thread = amount // (cpus - 1)
        rest_amount = amount - amount_per_thread * (cpus - 1)
        thread_tuple = tuple(ThreadCreatePlayersClass(amount_per_thread, str("playerCreate" + str(i + 1)),
                                                         players_list, lock) for i in range(cpus - 1))
        thread_tuple += (ThreadCreatePlayersClass(rest_amount, str("playerCreate" + str(cpus)), players_list, lock), )
    else:
        amount_per_thread = amount // cpus
        thread_tuple = tuple(ThreadCreatePlayersClass(amount_per_thread, str("playerCreate" + str(i + 1)),
                                                         players_list, lock) for i in range(cpus))
    for thread in thread_tuple:
        thread.start()
    for thread in thread_tuple:
        thread.join()
    return players_list


def play_rounds_multi_threaded(players_list, national_lottery, amount):
    """
    Simulates a given amount of rounds played.
    This function uses multithreading.
    """
    cpus = get_cpu_count()
    lock = threading.Lock()
    total_players = len(players_list)
    for round_number in range(amount):
        national_lottery.change_numbers()
        big_winners = []
        if not total_players % cpus == 0:
            amount_players_per_thread = total_players // (cpus - 1)
            rest_amount = total_players - amount_players_per_thread * (cpus - 1)
            thread_tuple = tuple(ThreadPlayRoundClass((amount_players_per_thread * i),
                                                     (amount_players_per_thread * i + amount_players_per_thread),
                                                     str("PlayRound" + str(i + 1)), players_list, national_lottery,
                                                     big_winners, lock) for i in range(cpus - 1))
            thread_tuple += (ThreadPlayRoundClass((total_players - rest_amount), -1, str("PlayRound" + str(cpus)),
                                                     players_list, national_lottery, big_winners, lock), )
        else:
            amount_players_per_thread = total_players // cpus
            thread_tuple = tuple(ThreadPlayRoundClass((amount_players_per_thread * i),
                                                         (amount_players_per_thread * i + amount_players_per_thread),
                                                         str("PlayRound" + str(i + 1)), players_list, national_lottery,
                                                         big_winners, lock) for i in range(cpus))
        for thread in thread_tuple:
            thread.start()
        for thread in thread_tuple:
            thread.join()
        if len(big_winners) > 0:
            price = national_lottery.big_price / len(big_winners)
            for winner in big_winners:
                winner.earnings += price
                winner.won_big_add()
            national_lottery.expenses += national_lottery.big_price
            national_lottery.reset_big_price()
        else:
            national_lottery.increase_big_price()
        print("----- Round " + str(round_number + 1) + " played! -----")


def print_statistics(players_tuple, national_lottery):
    """
    Prints the 10 biggest winners, the 10 biggest losers, the Summary of the National Lottery, the number of players
    with profit, how much percentage that is, the number of players with loses, how much percentage that it,
    the number of players with a big win, and how much percentage that is..
    """
    players_list = list(players_tuple)
    this_is_str = "This is "
    percent_of_all_players_str = "% of all players"
    print("----- Biggest Winners -----")
    players_list.sort(key=lambda x: x.get_balance(), reverse=True)
    [i.print_summary() for i in players_list[0:10]]
    print("----- Biggest Losers -----")
    [i.print_summary() for i in players_list[-1:-10:-1]]
    national_lottery.print_summary()
    print("----- Other statistics -----")
    profit_count = 0
    loss_count = 0
    jackpot_count = 0
    for player in players_list:
        if player.get_balance() > 0.0:
            profit_count += 1
        elif player.get_balance() < 0.0:
            loss_count += 1
        if player.won_big > 0:
            jackpot_count += 1
    print("Number of players with profit: " + str(profit_count))
    print(this_is_str + str(profit_count / len(players_list) * 100) + percent_of_all_players_str)
    print("Number of players with losses: " + str(loss_count))
    print(this_is_str + str(loss_count / len(players_list) * 100) + percent_of_all_players_str)
    print("Number of players who hit the jackpot: " + str(jackpot_count))
    print(this_is_str + str(jackpot_count / len(players_list) * 100) + percent_of_all_players_str)


def get_user_input(message):
    """
    Message is the prompt shown to the user.
    Returns user input as int.
    """
    error_message = "Input must be an Integer bigger then 0"
    while True:
        try:
            number = int(input(message))
            if number < 1:
                raise ValueError
            return number
        except ValueError:
            print(error_message)


if __name__ == '__main__':
    number_of_players = get_user_input("How many people should play?\n1000000 is a realistic number, but the bigger "
                                       "the number, the longer it takes.\n")
    number_of_rounds = get_user_input("How many rounds should be played?\n112 is the amount for 1 year, but the "
                                      "bigger the number, the longer it takes.\n")
    nl = NationalLottery()
    players = tuple(generate_players_multi_threaded(number_of_players))
    play_rounds_multi_threaded(players, nl, number_of_rounds)
    print_statistics(players, nl)
