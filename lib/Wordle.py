import random


class Wordle:
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
        with open(word_list_file) as f:
            self.words = f.read().splitlines()

        self.valid_guesses = self.words.copy()
        with open(guess_list_file) as f:
            self.valid_guesses += f.read().splitlines()
        self.valid_guesses = sorted(set(self.valid_guesses))

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
        word_char_used = [False, False, False, False, False]

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
                    if guess[n] == self.word[w] and not word_char_used[w]:
                        guess_state[n]["contains"] = guess[n]
                        guess_char_used[n] = True
                        word_char_used[w] = True
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

    def status(self) -> bool | None:
        if len(self.guesses) == 0:
            return None
        elif self.guesses[-1] == self.word:
            return True
        elif len(self.guesses) >= 6:
            return False
        else:
            return None
