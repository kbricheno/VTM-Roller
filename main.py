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
        dice = input("\nNormal dice: ") if normal else input("Hunger dice: ")
        if not dice.isdigit():
            print("Please enter a whole number.\n")
            continue
        else:
            return dice


def roll_dice(dice):

    diceList = []
    for i in range(int(dice)):
        result = randint(1, 10)
        diceList.append(result)

    return diceList


def evaluate_dice():
    global successes, crits, messyCrits, failures, hungerFailures, bestialFails, normalDiceList, hungerDiceList

    for result in normalDiceList:
        if result == 10:
            crits += 1
        elif result >= 6:
            successes += 1
        else:
            failures += 1

    for result in hungerDiceList:
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


def clear_results():
    global successes, crits, messyCrits, failures, hungerFailures, bestialFails, normalDiceList, hungerDiceList

    successes = 0
    crits = 0
    messyCrits = 0
    failures = 0
    hungerFailures = 0
    bestialFails = 0

    normalDiceList.clear()
    hungerDiceList.clear()


def roll_again():

    while True:
        answer = input("Roll again? ").lower().strip()
        if "n" in [*answer]:
            return False
        elif "y" in [*answer]:
            return True
        else:
            print("Please type Y or N\n")
            continue


def main():
    global normalDiceList, hungerDiceList

    clear_results()

    normalDice = int(get_dice(True))
    hungerDice = int(get_dice(False))

    normalDiceList = roll_dice(normalDice)
    hungerDiceList = roll_dice(hungerDice)

    evaluate_dice()

    print_results(normalDice, hungerDice)


while True:
    main()
    if roll_again():
        continue
    else:
        break
