from random import randint


class string_gen:
    
    def __init__(self) -> None:
        pass

    def random_string(size, alpha_numeric):

        if alpha_numeric:
            # return a string containing alphabets and numbers
            characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz1234567890'
            _random_string = ''

            for i in range(size):
                _random_string += characters[randint(0, len(characters) - 1)]

        return _random_string
    
