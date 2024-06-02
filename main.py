import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import methods as m

normalDiceList = []
hungerDiceList = []


# def new_roll():  # roll a fresh set of dice
#     global normalDiceList, hungerDiceList
#     m.clear_results(normalDiceList, hungerDiceList)
#
#     normalDice = int(m.get_dice(True))
#     hungerDice = int(m.get_dice(False))
#
#     normalDiceList = m.roll_dice(normalDice)
#     hungerDiceList = m.roll_dice(hungerDice)
#
#     results = m.evaluate_dice(normalDiceList, hungerDiceList)
#
#     m.print_results(results, normalDiceList, hungerDiceList)
#
#     return results
#
#
# def roll_again_input():
#
#     while True:
#         answer = input("Roll again? (Or \"re-roll\"). ").lower().strip()
#         acceptableTerms = ["re-roll", "reroll", "redo", "re-do", "willpower"]
#         for word in answer.split():
#             if word in acceptableTerms:
#                 return 0
#         if "n" in [*answer]:
#             return 2
#         elif "y" in [*answer]:
#             return 1
#         else:
#             print("Please type \"Y\", \"N\", or \"re-roll\"\n")
#             continue
#
#
# def re_roll(results):  # spend willpower to re-roll 3 existing normal dice
#     global normalDiceList
#
#     # show existing normal rolls, receive values to re-roll
#     values = m.get_reroll_values(normalDiceList, results)
#     diceToReroll = sum(values)
#
#     # remove the dice we're going to re-roll from the list, return the amended list
#     normalDiceList = m.pop_rerolls(normalDiceList, values)
#
#     # roll all popped values
#     newRolls = m.roll_dice(diceToReroll)
#
#     # evaluate & print new rolls
#     m.print_rerolls(newRolls, normalDiceList)
#
#     # append all rolls to normal dice list
#     normalDiceList += newRolls
#
#     # evaluate entire set again, print again
#     newResults = m.evaluate_dice(normalDiceList, hungerDiceList)
#     m.print_results(newResults, normalDiceList, hungerDiceList)
#
#
# def main():
#
#     results = new_roll()
#     while True:
#         rollAgain = roll_again_input()
#         if rollAgain == 0:
#             re_roll(results)
#         elif rollAgain == 1:
#             results = new_roll()
#         else:
#             break


# main()

# set up main application window & title it
root = Tk()
root.title("Vampire: The Masquerade | Dice Roller")

normalDice = StringVar(value="0")
hungerDice = StringVar(value="0")
results = StringVar()


def instant_validation(attemptedInput, action):  # validation that happens while the user inserts characters
    if action == "1":  # only validate on inserting characters -- overwriting, deleting, etc. is always allowed
        if not attemptedInput.isdigit():  # only allow numbers
            return False
        if len([*attemptedInput]) > 2:  # character limit of 2
            return False
        else:
            return True
    else:
        return True


def submit_validation():  # validation that happens only once the user has submitted their entry
    if not normalDice.get(): normalDice.set("0")
    if not hungerDice.get(): hungerDice.set("0")

    try:
        (int(normalDice.get()) + int(hungerDice.get())) / (int(normalDice.get()) + int(hungerDice.get()))
        results.set(f"{normalDice.get()}, {hungerDice.get()}")
    except ZeroDivisionError:
        tkinter.messagebox.showerror("Invalid Input", "Please enter at least one number.")


def rolling(*args):
    submit_validation()
    # roll the dice
    # evaluate the dice
    # generate list of buttons for normal dice, list of labels for hunger dice
    # generate label with evaluations


def normal_dice_input(event):  # auto highlight existing text inside the entry field for easy overwriting
    normalEntry.selection_range(0, END)


def hunger_dice_input(event):  # auto highlight existing text inside the entry field for easy overwriting
    hungerEntry.selection_range(0, END)


# frame widget that will hold everything else
mainFrame = ttk.Frame(root, padding=25, relief="groove")
# "grid" places the created widget in the window
mainFrame.grid()
# these 2 tell the widget to fill the window if it's resized
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
normalLabel = ttk.Label(mainFrame, text="NORMAL:")
hungerLabel = ttk.Label(mainFrame, text="HUNGER:")
normalLabel.grid(column=0, row=0)
hungerLabel.grid(column=0, row=1)

normalEntry = ttk.Entry(mainFrame, textvariable=normalDice, validate="key")
normalEntry["validatecommand"] = normalEntry.register(instant_validation), "%P", "%d"
normalEntry.grid(column=1, row=0)
hungerEntry = ttk.Entry(mainFrame, textvariable=hungerDice, validate="key")
hungerEntry["validatecommand"] = hungerEntry.register(instant_validation), "%P", "%d"
hungerEntry.grid(column=1, row=1)


normalEntry.bind("<FocusIn>", normal_dice_input)
hungerEntry.bind("<FocusIn>", hunger_dice_input)

rollButton = ttk.Button(mainFrame, text="Roll", command=rolling)
rollButton.grid(column=1, row=2)
root.bind("<Return>", rolling)  # also bind return (no matter what is selected) to the roll method

resultsLabel = ttk.Label(mainFrame, textvariable=results)
resultsLabel.grid(column=1, row=3)

root.mainloop()
