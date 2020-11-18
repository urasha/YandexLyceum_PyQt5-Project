def create_random_list():
    from random import choice

    NUMBER_OF_LETTERS = 25

    fridge_random = list()
    letters = 'abcdefghijklmnopqrstuvwxyz'

    for letter in range(NUMBER_OF_LETTERS):
        fridge_random.append(choice(letters).upper())

    return fridge_random
