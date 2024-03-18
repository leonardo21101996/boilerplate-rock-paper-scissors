import random
import RPS_game

#Notes:
# - Quincy plays RPPSR in a cycle.
# - Mrugesh starts with RR, then gives the best response to the opponent's most played move among the last 10.
#       If each move was used at most once, always guesses R.
#       In case of a tie, preference is guessing R -> P -> S.
#       History carries from previous games! We're assuming that tests will be done with a fresh history.
# - Kris starts with P, then gives the best response to the opponent's last move.
# - Abbey starts with PP, then predicts the next opponent move based on the last move and history frequency.
#       In case of a tie, preference is guessing R -> P -> S.
#       History carries from previous games! We're assuming that tests will be done with a fresh history.

best_response = {'R':'P', 'P':'S', 'S':'R'}

def get_play_order(history):
    history_copy = list(history)
    if history_copy[0] == '':
        history_copy[0] = 'R'
    play_order = play_order={
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          }
    for i in range(len(history)-1):
        last_two = history_copy[i]+history_copy[i+1]
        if len(last_two) == 2:
            play_order[last_two] += 1
    return [play_order]

def player(prev_play, opponent_history=[[]], counter=[0], state=[''], self_history=[[]]):
    # Initialize the lists in case of a new opponent.
    if prev_play == '':
        opponent_history[0] = []
        counter[0] = -1
        self_history[0] = ['']
    opponent_history[0].append(prev_play)
    counter[0] += 1
    
    # In case the oppoent is unknown, tries to deduce it.
    # The deduction is based only on the first two plays, as it assummes that it will play against one of the four predefined players.
    # If the deduction is impossible, uses '?' as a failsafe.
    match opponent_history[0][1:3]:
        case []:
            state[0] = 'start'
        case ['R']:
            state[0] = 'R'
        case ['P']:
            state[0] = 'P'
        case ['R','P']:
            state[0] = 'quincy'
        case ['R', 'R']:
            state[0] = 'mrugesh'
        case ['P', 'S']:
            state[0] = 'kris'
        case ['P', 'P']:
            state[0] = 'abbey'
        case _:
            state[0] = '?'
    # Chooses either the best move against a deduced opponent, a move for information (never a losing move), or at random if deduction failed. 
    response = 'best'
    match state[0]:
        case 'start':
            response = 'P'
        case 'R':
            response = 'P'
        case 'P':
            response = 'S'
        case 'quincy':
            guess = RPS_game.quincy(self_history[0][-1], counter = [counter[0]])
        case 'mrugesh':
            guess = RPS_game.mrugesh(self_history[0][-1], self_history[0][:-1])
        case 'kris':
            guess = RPS_game.kris(self_history[0][-1])
        case 'abbey':
            guess = RPS_game.abbey(self_history[0][-1], self_history[0][:-1], get_play_order(self_history[0][:-1]))
        case _:
            guess = random.choice(['R', 'P', 'S'])
    if response == 'best':
        response = best_response[guess]
    
    self_history[0].append(response)
    return response