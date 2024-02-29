import random


class Wordle:
    words: list[str] = []
    word: str = ""
    guesses: list[str] = []
    state: list[list[dict[str, str]]] = []
    valid_guesses: list[str] = []

    def __init__(
        self,
        word_list_file: str = "words.times.txt",
        word: str = "",
        hard_mode: bool = False,
    ):
        with open(word_list_file) as f:
            self.words = f.read().splitlines()

        if word == "":
            self.word = random.choice(self.words)
        elif word not in self.words:
            raise Exception("Word not in word list")
        else:
            self.word = word

        self.guesses = []

        self.hard_mode = hard_mode

        self.valid_guesses = self.words.copy()

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

        self.valid_guesses = self.words.copy()

    def guess(self, guess: str):
        if guess not in self.words:
            raise Exception("Guess not in word list")
        self.guesses.append(guess)

        guess_state: list[dict[str, str]] = [{}, {}, {}, {}, {}]
        guess_char_used = [False, False, False, False, False]
        word_char_used = [False, False, False, False, False]

        # Check if is
        for n in range(5):
            if guess[n] == self.word[n]:
                guess_state[n]["is"] = guess[n]
                guess_char_used[n] = True
                if self.hard_mode:
                    self.valid_guesses = [
                        k for k in self.valid_guesses if k[n] == self.word[n]
                    ]

        # Check if contains
        for n in range(5):
            if not guess_char_used[n]:
                for w in range(5):
                    if guess[n] == self.word[w] and not word_char_used[w]:
                        guess_state[n]["contains"] = guess[n]
                        guess_char_used[n] = True
                        word_char_used[w] = True
                        if self.hard_mode:
                            self.valid_guesses = [
                                k
                                for k in self.valid_guesses
                                if guess[n] in k and k[n] != self.word[w]
                            ]

        # Else is not
        for n in range(5):
            if not guess_char_used[n]:
                guess_state[n]["not"] = guess[n]

        self.state.append(guess_state)

    def status(self) -> bool | None:
        if len(self.guesses) == 0:
            return None
        elif self.guesses[-1] == self.word:
            return True
        elif len(self.guesses) >= 6:
            return False
        else:
            return None
