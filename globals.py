# globals.py

# Global counter to track the number of moves made by the snake
COUNTER = 0

# Global variable to determine the tick interval for closed eyes
close_eyes_ticks = 21

def get_tick_counter(counts):
    """
    Check if the global COUNTER is a multiple of the given `counts`.

    Args:
        counts (int): The number to check divisibility against.

    Returns:
        bool: True if COUNTER is a multiple of `counts`, False otherwise.

    Example:
        get_tick_counter(5) will return True if COUNTER is 5, 10, 15, etc.,
        and False for other values like 2, 3, 4, 6, 7, etc.
    """
    return COUNTER % counts == 0

def IncreaseCounter():
    global COUNTER
    # Log the counter value in the terminal
    print(f"COUNTER: {COUNTER}")
    if COUNTER >= 100:
        COUNTER = 1
    else:
        COUNTER += 1