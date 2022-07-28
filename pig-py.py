# Name: pig-py.py
# Author: Stephen C. Sanders <https://stephensanders.me>
# Description: This program allows the user to play Pig against the computer. The user and computer will take turns rolling a 6-sided die.
# Each turn will last until a 1 is rolled. The user can also signal after each roll if they want to continue rolling. The computer has a turn score limit
# of 20; once it reaches that limit, the computer's turn will end. Rolling a number between 2 and 6 will be added to the turn subtotal.
# The first to reach 100 wins the game. After the game, the program will display how many combined turns were taken between the user and computer.

import random        # Needed in order to determine who is Player 1 and Player 2 using choice() method
import time          # Needed to add short time delay between computer rolls using sleep() method

# Main function which introduces/ends the program, handles overall scores and the main loop to alternate scores, and announces the winner
def main():
    # Initialize variables
    die = [1, 2, 3, 4, 5, 6]      # Used to store the values of a 6-sided die
    continue_turn = 'Y'           # Used to determine if user wants to keep rolling
    score_to_reach = 100          # Used to set winning score
    tot_score_hum = 0             # Used to keep track of human's total score
    tot_score_comp = 0            # Used to keep track of computer's total score
    check_win = False             # Used to determine if the score_to_reach has been reached
    comp_lim = 20                 # Used to store the cutoff score that is used to determine when computer needs to stop turn
    turn = 0                      # Used to keep track of whose turn it is; initialized to 0 to make sure Player 1 always goes first
    turn_count = 0                # Used to keep track of how many turns were taken during the course of the game
    
    # Opening prompts
    print('Welcome to the Pig game!')
    print('You will be playing against the computer.')
    print('You and the computer will take turns rolling the die.')
    print('Rolling a number between 2 and 6 will be added to your running score.')
    print('Rolling a 1 will end your turn and 0 points will be added to your score.')
    print('You and the computer can signal when you want your turn to end.')
    print('The first to reach a score of at least 100, wins.')
    input('Click ENTER to continue.....')

    # Determine who is Player 1 and Player 2 - if the variable is equal to 0, they are Player 1; equal to 1 is Player 2
    human, computer = decide_players()

    # Display who is Player 1 and Player 2
    if human == turn:
        print('You are Player 1, and the computer is Player 2.')
    else:
        print('The computer is Player 1, and you are Player 2.')

    # Signal user to officially begin game
    input('Click ENTER to begin game...')
    
    # Keep the game going until the check_win variable is True
    while not(check_win):
        # Determine whether it's the human's turn or the computer's turn, and get relevant turn score
        if turn == human:
            turn_score_hum = user_turn_score(die, comp_lim, turn, human, computer, continue_turn, score_to_reach, tot_score_hum)
            tot_score_hum += turn_score_hum

            time.sleep(0.25)  # Stall display of round score by 0.25 seconds

            # Display turn subtotal as long as it is greater than 0
            if turn_score_hum != 0:
                print(F'This round, you had a score of {turn_score_hum}.')
        else:
            turn_score_comp = computer_turn_score(die, comp_lim, turn, human, computer, continue_turn, score_to_reach, tot_score_comp)
            tot_score_comp += turn_score_comp

        # Add the turn to the turn counter
        turn_count += 1

        # Check to see if either of the players has earned at least 100 points
        check_win = check_for_win(tot_score_hum, tot_score_comp, score_to_reach)

        # Next player's turn if there is no winner yet
        if check_win == False:
            # Display updated score totals
            print(f'Current total scores: Human = {tot_score_hum} ; Computer: {tot_score_comp}\n')
            
            # Toggle turn to next player
            turn = toggle_turn(turn)
        else:
            # Ending scores message depending on who won
            if tot_score_hum >= score_to_reach:
                print(f'Congratulations! You defeated the computer by a score of:\n{tot_score_hum} to {tot_score_comp}.')
            else:
                print(f'Unfortunately, you were defeated by the computer by a score of:\n{tot_score_hum} to {tot_score_comp}')
        
    # Display number of turns taken and closing salutations
    time.sleep(0.5)  # Stall for half a second so that there are aren't multiple outputs all at once
    print(f'Between you and the computer, there were {turn_count} turns taken over the course of the game.')
    print('Thank you for playing the Pig game. I hope to see you again soon!')

# Decide which player will go first;  0 is Player 1, and 1 is Player 2
def decide_players():
    # Initialize list used to decide which player is which
    players = [0, 1]

    # Randomly assign human and computer variables to either of the two numbers in players list
    hum = random.choice(players)
    comp = random.choice(players)

    # Make sure human and computer don't have the same value
    while hum == comp:
        comp = random.choice(players)

    return hum, comp

# Human takes their turn and their score for the turn is returned to main
def user_turn_score(d, com_lim, t, hum, comp, c_t, cutoff, tot_sc_hum):
    # Initialize total score variable
    score = 0
    
    # Keep asking 
    while c_t == 'Y' or c_t == 'y':
        # Roll die
        roll = die_roll(d)

        # Display roll value
        print(f'You rolled: {roll}.')

        # If user rolls a 1, turn ends with no score for that round
        if roll == 1:
            time.sleep(0.5)  # Stall for half a second to make game seem more fluid
            score = 0
            print('Since you rolled a 1, your turn ends with a score of 0 for this round.')
            
            return score

        # Add to total score for turn
        score += roll
        
        # Get continue turn status from user
        c_t = roll_or_end(score, com_lim, t, hum, comp, cutoff, tot_sc_hum)

    return score

# Computer takes its turn and its score for the turn is returned to main
def computer_turn_score(d, com_lim, t, hum, comp, c_t, cutoff, tot_sc_comp):
    # Initialize total score variable
    score = 0

    # Computer keeps rolling die until cutoff is reached, computer rolls a 1, or computer's total score passes 100
    while c_t == 'Y':
        # Add 0.25 second time delay between each of computer's rolls
        time.sleep(0.25)
        
        # Roll die
        roll = die_roll(d)

        # Display roll value
        print(f'The computer rolled: {roll}')

        # If computer rolls a 1, its turn ends with no points for that round
        if roll == 1:
            time.sleep(0.5)  # Stall for half a second to make game easier to follow
            score = 0
            print('Since the computer rolled a 1, its turn ends with a score of 0 for this round.')
            
            return score

        # Add value of roll to running subtotal
        score += roll
        
        # Determine if turn should continue
        c_t = roll_or_end(score, com_lim, t, hum, comp, cutoff, tot_sc_comp)
    
    # Display when the computer reaches its turn score limit, but only on non-game-winning rounds
    if score >= com_lim and (score + tot_sc_comp) < cutoff:
        print(f'The computer reached its limit, scoring {score} points that round.')
    
    return score

# Roll the die, and return number
def die_roll(die):
    # Pick random number between 1 and 6 in die list and return to main
    return random.choice(die)

# Determine whether to keep rolling depending on whether it's the turn of the human or computer
def roll_or_end(sc, com_lim, turn, hu, com, cutoff, tot_sc):
    # Don't roll again if the current turn's score plus the total player score (not including current round) is at least past the cutoff point (i.e. >= 100)
    if (tot_sc + sc) >= cutoff:
        return 'N'

    # Determine whether to roll or end turn based on whether player is human or computer
    if turn == hu:
        # Get user's answer
        an = input('Would you like to continue your turn? Enter \'Y\' or \'N\': ')

        # Validate that user input is either Y, y, N, or n
        while an.upper() != 'Y' and an.upper() != 'N':
            print('ERROR: That is invalid input. Please try again.')
            an = input('Would you like to continue your turn? Enter \'Y\' or \'N\': ')

        return an
    else:
        # Determine continue status of computer by seeing if turn score is less than its 20 point turn cutoff
        if sc >= com_lim:
            return 'N'
        else:
            return 'Y'

# Determine if either of the players won from the previous turn
def check_for_win(score_hum, score_comp, lim):
    # If either player ellipses 100, end game loop; otherwise go to the next turn
    if score_hum >= lim or score_comp >= lim:
        return True
    else:
        return False

# Switch to next player for their turn
def toggle_turn(tu):
    # Toggle the turn variable between 0 and 1 to go to whoever is next
    if tu == 1:
        return tu - 1
    else:
        return tu + 1

# Execute main function
if __name__ == '__main__':
    main()
