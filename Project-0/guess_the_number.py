import os

import numpy as np


def binary_predict(number: int=1) -> int:
    """Guess the number game.
    
    The computer guesses the number that was made up to him.
    The binary search algorithm is used.

    Args:
        number (int, optional): The number was made up. Defaults to 1.

    Returns:
        int: Number of attempts
    """
    count = 0   # Number of attempts
    left_end = 1    # Setting the boundaries of the possible values of the number
    right_end = 100

    while True:
        count += 1
        # Assume the number as midle of the segment
        predict_number = (left_end+right_end) // 2  
        if number == predict_number:
            break   # Exit when the number is found
        #  else change the boundaries of the possible values
        elif number > predict_number:
            left_end = predict_number + 1
        else:
            right_end = predict_number - 1
            
    return (count)


def score_game(guessing_function) -> int:
    """For how many attempts, on average, out of 1000
    approaches, a given algorithm guesses a hidden number.

    Args:
        binary_predict (function): Guessing function

    Returns:
        int: Average number of attempts
    """
    
    os.system('CLS') # Clear terminal
    
    count_ls = []  # List to save the number of attempts
    np.random.seed(1)  # Fix the seed for reproducibility
    random_array = np.random.randint(
        1, 101, size=(1000))  # Making a list of numbers to guess
    
    for number in random_array:
        count_ls.append(guessing_function(number))
    
    score = int(np.mean(count_ls))  # Find the average number of attempts

    print(f'Ваш алгоритм угадывает число в среднем за: {score} попыток')
    return (score)


# RUN
if __name__ == "__main__":
    score_game(binary_predict)
    
