from random import randint
from math import floor

successes = 0
failures = 0
hungerFailures = 0
crits = 0
messyCrits = 0
bestialFails = 0

normalDiceList = []
hungerDiceList = []


def get_dice(normal):

    while True:
        dice = input("Normal dice: ") if normal else input("Hunger dice: ")
        if not dice.isdigit():
            print("Please enter a whole number.\n")
            continue
        else:
            return dice


def roll_dice(dice, list_):

    for i in range(int(dice)):
        result = randint(1, 10)
        list_.append(result)


def evaluate_dice(normal, list_):
    global successes, crits, messyCrits, failures, hungerFailures, bestialFails

    if normal:
        for result in list_:
            if result == 10:
                crits += 1
            elif result >= 6:
                successes += 1
            else:
                failures += 1

    else:
        for result in list_:
            if result == 10:
                messyCrits += 1
            elif result >= 6:
                successes += 1
            elif result == 1:
                bestialFails += 1
            else:
                hungerFailures += 1


def print_results(normalDice_, hungerDice_):
    global successes, crits, messyCrits, failures, hungerFailures, bestialFails, normalDiceList, hungerDiceList

    print()
    if normalDiceList:
        print(f"Normal dice ({normalDice_}): {normalDiceList}")
    if hungerDiceList:
        print(f"Hunger dice ({hungerDice_}): {hungerDiceList}")
    print()

    if successes + crits + messyCrits == 0:
        print(f"Oh no! 0 successes.\n"
              f"Failures: {failures} normal, {hungerFailures} hunger, and {bestialFails} bestial")

    elif crits + messyCrits >= 2:
        if messyCrits >= 1:
            additionalSuccesses = (floor((crits + messyCrits) / 2) * 4) + ((crits + messyCrits) % 2)
            print(f"Messy crit!\n"
                  f"Successes: {successes + additionalSuccesses} ({successes} success(es) + {messyCrits} hunger and "
                  f"{crits} normal crit(s)\n"
                  f"Failures: {failures} normal, {hungerFailures} hunger, and {bestialFails} bestial")
        else:
            additionalSuccesses = (floor(crits / 2) * 4) + (crits % 2)
            print(f"Crit!\n" +
                  f"Successes: {successes + additionalSuccesses} ({successes} success(es) + {crits} normal crits)\n" +
                  f"Failures: {failures} normal, {hungerFailures} hunger, and {bestialFails} bestial")

    else:
        print(f"No crits.\n"
              f"Successes: {successes + crits + messyCrits}\n"
              f"Failures: {failures} normal, {hungerFailures} hunger, and {bestialFails} bestial")

    print()


def clear_results(normalDiceList_, hungerDiceList_):
    global successes, crits, messyCrits, failures, hungerFailures, bestialFails

    successes = 0
    crits = 0
    messyCrits = 0
    failures = 0
    hungerFailures = 0
    bestialFails = 0

    normalDiceList_.clear()
    hungerDiceList_.clear()


def roll_again():

    while True:
        answer = input("Roll again? (Or \"re-roll\"): ").lower().strip()
        acceptableTerms = ["reroll", "re-roll", "re_roll" "re-do", "redo"]
        for word in answer.split():
            if word in acceptableTerms:
                return 0

        restart = list(answer)
        if "n" in restart:
            return 2
        elif "y" in restart:
            return 1
        else:
            print("Please type Y or N (or \"re-roll\").\n")
            continue


def main():
    global normalDiceList, hungerDiceList

    clear_results(normalDiceList, hungerDiceList)

    normalDice = int(get_dice(True))
    hungerDice = int(get_dice(False))

    roll_dice(normalDice, normalDiceList)
    roll_dice(hungerDice, hungerDiceList)

    evaluate_dice(True, normalDiceList)
    evaluate_dice(False, hungerDiceList)

    print_results(normalDice, hungerDice)


while True:
    main()
    if roll_again() == 1:
        continue
    # elif roll_again() == 0:
    #     re_roll()
    else:
        break
