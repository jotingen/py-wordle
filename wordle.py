import csv
import random
import tqdm
import itertools

from wakepy import keep

from lib.Wordle import Wordle


def main():
    #brute_force()
    first_guess_valid_guesses()

#Make a table of the # of valid guesses after the first guess, average out to see what gives the fewest
def first_guess_valid_guesses():
    w = Wordle(hard_mode=True)
    #w.words = random.sample(w.words, 50)
    score = {}
    for word in w.words:
        score[word] = {}
    with keep.running():

        with open('results.csv', 'w', newline='') as file:
            # Create a CSV writer object
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(['Initial Guess', 'Remaining Valid Guesses'])

            for guess in (gbar := tqdm.tqdm(w.valid_guesses)):
                gbar.set_postfix_str(guess)
                row = [guess,0]
                for word in (wbar := tqdm.tqdm(w.words, leave=False)):
                    wbar.set_postfix_str(word)
                    w.reset(hard_mode=True, word=word)
                    w.guess(guess)
                    if w.status() is True:
                        row.append(0)
                    else:
                        row.append(len(w.remaining_guesses))
                row[1] = sum(row[2:])/len(row[2:])
                writer.writerow(row[:2])
                file.flush()

#Brute force search, seems like it will take literal years
def brute_force():
    w = Wordle(hard_mode=True)
    #w.words = random.sample(w.words, 50)
    score = {}
    for word in w.words:
        score[word] = [0, 0, 0, 0, 0, 0, 0]
    with keep.running():
        for word in (wbar := tqdm.tqdm(w.words)):
            wbar.set_postfix_str(word)
            for guess1 in (g1bar := tqdm.tqdm(w.words, leave=False)):
                g1bar.set_postfix_str(guess1)
                w.reset(hard_mode=True, word=word)
                w.guess(guess1)
                if w.status() is True:
                    score[guess1][0] += 1
                    continue
                for guess2 in (
                    g2bar := tqdm.tqdm(
                        [guess for guess in w.remaining_guesses if guess not in w.guesses],
                        leave=False,
                    )
                ):
                    g2bar.set_postfix_str(guess2)
                    w.reset(hard_mode=True, word=word)
                    w.guess(guess1)
                    w.guess(guess2)
                    if w.status() is True:
                        score[guess1][1] += 1
                        continue
                    for guess3 in (
                        g3bar := tqdm.tqdm(
                            [
                                guess
                                for guess in w.remaining_guesses
                                if guess not in w.guesses
                            ],
                            leave=False,
                        )
                    ):
                        g3bar.set_postfix_str(guess3)
                        w.reset(hard_mode=True, word=word)
                        w.guess(guess1)
                        w.guess(guess2)
                        w.guess(guess3)
                        if w.status() is True:
                            score[guess1][2] += 1
                            continue
                        for guess4 in (
                            g4bar := tqdm.tqdm(
                                [
                                    guess
                                    for guess in w.remaining_guesses
                                    if guess not in w.guesses
                                ],
                                leave=False,
                            )
                        ):
                            g4bar.set_postfix_str(guess4)
                            w.reset(hard_mode=True, word=word)
                            w.guess(guess1)
                            w.guess(guess2)
                            w.guess(guess3)
                            w.guess(guess4)
                            if w.status() is True:
                                score[guess1][3] += 1
                                continue
                            for guess5 in (
                                g5bar := tqdm.tqdm(
                                    [
                                        guess
                                        for guess in w.remaining_guesses
                                        if guess not in w.guesses
                                    ],
                                    leave=False,
                                    miniters=100,
                                )
                            ):
                                g5bar.set_postfix_str(guess5)
                                w.reset(hard_mode=True, word=word)
                                w.guess(guess1)
                                w.guess(guess2)
                                w.guess(guess3)
                                w.guess(guess4)
                                w.guess(guess5)
                                if w.status() is True:
                                    score[guess1][4] += 1
                                    continue
                                # Last guess must be word to count
                                w.reset(hard_mode=True, word=word)
                                w.guess(guess1)
                                w.guess(guess2)
                                w.guess(guess3)
                                w.guess(guess4)
                                w.guess(guess5)
                                score[guess1][5] += 1
                                score[guess1][6] += len(w.remaining_guesses) - 1

        with open('results.csv', 'w', newline='') as file:
            # Create a CSV writer object
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(['Guess', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Failed'])

            # Write data rows
            for guess, results in score.items():
                print(guess, results)
                writer.writerow([guess] + results)



if __name__ == "__main__":
    main()
