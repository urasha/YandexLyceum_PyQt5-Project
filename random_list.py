def create_random_list(language):
    from random import choice

    fridge_random = list()
    letters = ''
    NUMBER_OF_LETTERS = 50

    if language == 'ru':
        letters = 'йцукенгшщзхъфывапролджэячсмитьбю'
    elif language == 'en':
        letters = 'abcdefghijklmnopqrstuvwxyz'

    for letter in range(NUMBER_OF_LETTERS):
        fridge_random.append(choice(letters).upper())

    return fridge_random