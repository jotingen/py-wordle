import random

class Words:
    words: list[str] = []

    def __init__(
        self,
        word_list_file: str = "words.times.txt",
    ):

        with open(word_list_file) as f:
            self.words = f.read().splitlines()


class Guesses:
    guesses: list[str] = []

    def __init__(
        self,
        guess_list_file: str = "guesses.times.txt",
    ):
        self.guesses = Words().words.copy()
        with open(guess_list_file) as f:
            self.guesses += f.read().splitlines()
        self.guesses = sorted(set(self.guesses))

class GameState:
    state: list[list[dict[str, str]]] = []

    def __init__(
        self,
        hard_mode: bool = False,
    ):
        self.hard_mode = hard_mode

    def update(self, guess: str, state: str):
        update_state: list[dict[str, str]] = []
        if len(guess) != 5:
            raise Exception("Invalid guess length")
        if len(state) != 5:
            raise Exception("Invalid state length")
        for n in range(5):
            if state[n] == 'x':
                update_state.append({'not': guess[n]})
            elif state[n] == 'y':
                update_state.append({'contains': guess[n]})
            elif state[n] == 'g':
                update_state.append({'is': guess[n]})
            else:
                raise Exception("Invalid state given")
        self.state.append(update_state)
        #print(self.state)

    def next_best_guess(self) -> str:

        #Filter out impossible guesses
        words = word_filter(self)
        #print(words)


        #Run against remaining guesses
        results = {}
        for word in words:
            next_state = GameState(hard_mode=self.hard_mode) 
            next_state.state = self.state.copy()
            game = Game(word=word,hard_mode=self.hard_mode)
            for state in self.state:
                guess = ""
                for n in range(5):
                    for key in state[n]:
                        guess += state[n][key]
                #print(guess)
                game.guess(guess)
            results[word] = len(game.remaining_words)
            
        #print(results)

        # For now pick the one with the least remaining guesses, and most unique letters
        return sorted([k for k, v in results.items() if v == min(results.values())], key=lambda x: len(set(x)), reverse=True)[0]



class Game:
    words: list[str] = []
    valid_guesses: list[str] = []
    word: str = ""
    guesses: list[str] = []
    state: list[list[dict[str, str]]] = []
    remaining_guesses: list[str] = []

    def __init__(
        self,
        word_list_file: str = "words.times.txt",
        guess_list_file: str = "guesses.times.txt",
        word: str = "",
        hard_mode: bool = False,
    ):
        self.words = Words(word_list_file=word_list_file).words

        self.valid_guesses = Guesses(guess_list_file=guess_list_file).guesses

        if word == "":
            self.word = random.choice(self.words)
        elif word not in self.words:
            raise Exception("Word not in word list")
        else:
            self.word = word

        self.guesses = []

        self.hard_mode = hard_mode

        self.remaining_guesses = self.valid_guesses.copy()

        self.remaining_words = self.words.copy()

    def reset(
        self,
        word: str = "",
        hard_mode: bool = False,
    ):
        if word == "":
            self.word = random.choice(self.words)
        elif word not in self.words:
            raise Exception("Word not in word list")
        else:
            self.word = word

        self.guesses = []

        self.hard_mode = hard_mode

        self.state = []

        self.remaining_guesses = self.valid_guesses.copy()

        self.remaining_words = self.words.copy()

    def guess(self, guess: str):
        if guess not in self.valid_guesses:
            raise Exception("Guess not in guess list")
        self.guesses.append(guess)

        guess_state: list[dict[str, str]] = [{}, {}, {}, {}, {}]
        guess_char_used = [False, False, False, False, False]

        # Check if is
        for n in range(5):
            if guess[n] == self.word[n]:
                guess_state[n]["is"] = guess[n]
                guess_char_used[n] = True
                if self.hard_mode:
                    self.remaining_guesses = [
                        k for k in self.remaining_guesses if k[n] == self.word[n]
                    ]
                    self.remaining_words = [
                        k for k in self.remaining_words if k[n] == self.word[n]
                    ]

        # Check if contains
        for n in range(5):
            if not guess_char_used[n]:
                for w in range(5):
                    if guess[n] == self.word[w] and not guess_char_used[w]:
                        guess_state[n]["contains"] = guess[n]
                        guess_char_used[n] = True
                        if self.hard_mode:
                            self.remaining_guesses = [
                                k
                                for k in self.remaining_guesses
                                if guess[n] in k and k[n] != self.word[w]
                            ]
                            self.remaining_words = [
                                k
                                for k in self.remaining_words
                                if guess[n] in k and k[n] != self.word[w]
                            ]

        # Else is not
        for n in range(5):
            if not guess_char_used[n]:
                guess_state[n]["not"] = guess[n]

        self.state.append(guess_state)

        guess_str = ""
        for c in guess_state:
            if 'not' in c.keys():
                guess_str += "x"
            elif 'contains' in c.keys():
                guess_str += "y"
            elif 'is' in c.keys():
                guess_str += "g"
            else:
                raise Exception("Issue calculating state")

        return guess_str


    def status(self) -> bool | None:
        if len(self.guesses) == 0:
            return None
        elif self.guesses[-1] == self.word:
            return True
        elif len(self.guesses) >= 6:
            return False
        else:
            return None

def word_filter(game_state: GameState):
    words = Words().words.copy()
    for guess_state in game_state.state:
        for n in range(5):
            #print(n, guess_state[n])
            if "is" in guess_state[n].keys():
                words = [k for k in words if k[n] == guess_state[n]['is']]
            elif "contains" in guess_state[n].keys():
                words = [k for k in words if guess_state[n]['contains'] in k]
                words = [k for k in words if k[n] != guess_state[n]['contains']]
            elif "not" in guess_state[n].keys():
                #Skip full word compare if letter is previously is or contained
                skip = False
                for m in range(5):
                    if "is" in guess_state[m].keys() and guess_state[m]["is"] == guess_state[n]['not']:
                        words = [k for k in words if k[n] != guess_state[n]['not']]
                        skip = True
                for m in range(n):
                    if "contains" in guess_state[m].keys() and guess_state[m]["contains"] == guess_state[n]['not']:
                        words = [k for k in words if k[n] != guess_state[n]['not']]
                        skip = True
                if not skip:    
                    words = [k for k in words if guess_state[n]['not'] not in k]
            #print(words)

    return words
