import sys
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import diceHandling as d

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
root.geometry("350x350")

normalDiceImages = {"success": PhotoImage(file="DiceImages/normalSuccess.png"),
                    "crit": PhotoImage(file="DiceImages/normalCrit.png"),
                    "fail": PhotoImage(file="DiceImages/normalFail.png")}

hungerDiceImages = {"success": PhotoImage(file="DiceImages/hungerSuccess.png"),
                    "crit": PhotoImage(file="DiceImages/hungerCrit.png"),
                    "fail": PhotoImage(file="DiceImages/hungerFail.png"),
                    "bestialFail": PhotoImage(file="DiceImages/hungerBestialFail.png")}

normalDice = StringVar(value="0")
hungerDice = StringVar(value="0")
results = StringVar()

canvases = []


class ScrollableCanvas:  # class for readability + i need 2, 1 for normal & 1 for hunger
    def __init__(self, spawnParent, spawnColumn, spawnRow, normal):
        # create & configure elements
        self.normal = normal
        self.container = Frame(spawnParent)
        # canvases can have an actual size ("scrollable region") and a screen/view size ("window")
        self.canvas = Canvas(self.container)
        self.yScroll = Scrollbar(self.container, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.yScroll.set)
        # create a frame that will contain all the buttons & therefore act as the canvas' scrollable region
        self.scrollFrame = Frame(self.canvas)
        # when <Configure>d (when the scrollable frame changes size), update the frame's parent's scrollable region
        # i will never understand why this must be bound to configure & cannot just be done once after populating frame
        self.scrollFrame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # place elements
        self.container.grid(column=spawnColumn, row=spawnRow)
        self.canvas.grid(column=0, row=0)
        self.yScroll.grid(column=1, row=0, sticky=NS)
        self.canvas.create_window((0, 0), window=self.scrollFrame, anchor=NW)

    def populate_frame(self, dice):
        global normalDiceImages, hungerDiceImages

        spawnAtColumn = -1
        spawnAtRow = -1

        for die in dice:
            spawnAtColumn = (spawnAtColumn + 1) % 3  # create a 3 by X grid to present the dice results in
            if spawnAtColumn == 0:
                spawnAtRow += 1

            if self.normal:  # normal-specific function because normal dice must spawn as buttons & with diff images
                if die == 10:  # assign images to dice depending on their values
                    spawnWithImage = normalDiceImages["crit"]
                elif die >= 6:
                    spawnWithImage = normalDiceImages["success"]
                else:
                    spawnWithImage = normalDiceImages["fail"]
                ttk.Button(self.scrollFrame, text=die, image=spawnWithImage).grid(column=spawnAtColumn, row=spawnAtRow)

            else:  # hunger dice spawn as labels bc user doesn't need to click on them for re-rolling
                if die == 10:
                    spawnWithImage = hungerDiceImages["crit"]
                elif die >= 6:
                    spawnWithImage = hungerDiceImages["success"]
                elif die > 1:
                    spawnWithImage = hungerDiceImages["fail"]
                else:
                    spawnWithImage = hungerDiceImages["bestialFail"]
                ttk.Label(self.scrollFrame, image=spawnWithImage).grid(column=spawnAtColumn, row=spawnAtRow)

        self.finalise_canvas()

    def finalise_canvas(self):  # set width & potentially disable scrollbar
        # set the width & height to show 3x3 dice (i think most people will roll 9 or fewer dice)
        dieWidth = self.scrollFrame.winfo_children()[0].winfo_reqwidth()
        self.canvas.configure(width=dieWidth*3, height=dieWidth*3)
        # don't need to scroll if there are 9 or fewer dice
        if len(self.scrollFrame.winfo_children()) <= 9:
            self.yScroll.grid_forget()

    def destroy_canvas(self):
        self.container.destroy()
        self.canvas.destroy()
        self.yScroll.destroy()
        self.scrollFrame.destroy()


def rolling(*args):  # *args here because this method can be called by both a button (no argument) and
    # a <Return> event (event argument), so it must be able to receive either 0 or 1 argument
    global normalDiceList, hungerDiceList

    # discard any previous results
    for canvas_ in canvases:
        canvas_.destroy_canvas()
    canvases.clear()

    # receive and validate input (ensure blanks = 0, ensure total > 0)
    submit_validation()

    # roll the dice
    normalDiceList = d.roll_dice(int(normalDice.get()))
    hungerDiceList = d.roll_dice(int(hungerDice.get()))

    # generate scrollable canvas of buttons for normal dice, scrollable canvas of labels for hunger dice
    if normalDiceList:
        normalScrollCanvas = ScrollableCanvas(mainFrame, 0, 4, True)
        normalScrollCanvas.populate_frame(normalDiceList)
        canvases.append(normalScrollCanvas)

    if hungerDiceList:
        hungerScrollCanvas = ScrollableCanvas(mainFrame, 1, 4, False)
        hungerScrollCanvas.populate_frame(hungerDiceList)
        canvases.append(hungerScrollCanvas)

    # evaluate the dice
    evaluatedResults = d.evaluate_dice(normalDiceList, hungerDiceList)

    # populate label with evaluations
    results.set(d.print_results(evaluatedResults))


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


def normal_dice_input(event):  # auto highlight existing text inside the entry field for easy overwriting
    normalEntry.selection_range(0, END)


def hunger_dice_input(event):  # same as above but for other entry field
    hungerEntry.selection_range(0, END)


# frame widget that will hold everything else. stored as a variable so it can be referenced as a parent
mainFrame = ttk.Frame(root, padding=130, relief="groove")
mainFrame.grid()  # "grid" places the created widget in the window

# these 2 tell the widget to re-centre in the window if it's resized
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# create additional labels and buttons
ttk.Label(mainFrame, text="NORMAL:").grid(column=0, row=0)  # input label
ttk.Label(mainFrame, text="HUNGER:").grid(column=0, row=1)  # input label
ttk.Label(mainFrame, textvariable=results).grid(column=0, columnspan=2, row=3)  # temporary output label
ttk.Button(mainFrame, text="Roll", command=rolling).grid(column=0, columnspan=2, row=2)  # submit button
root.bind("<Return>", rolling)  # also bind return (no matter what is selected) to the roll method

normalEntry = ttk.Entry(mainFrame, width=4, textvariable=normalDice, validate="key")  # validate on key press
# register essentially holds the proposed edit and puts it through validation before setting the stringvar
normalEntry["validatecommand"] = normalEntry.register(instant_validation), "%P", "%d"  # %P = key pressed, %d = action
normalEntry.grid(column=1, row=0)
normalEntry.bind("<FocusIn>", normal_dice_input)

hungerEntry = ttk.Entry(mainFrame, width=4, textvariable=hungerDice, validate="key")
hungerEntry["validatecommand"] = hungerEntry.register(instant_validation), "%P", "%d"
hungerEntry.grid(column=1, row=1)
hungerEntry.bind("<FocusIn>", hunger_dice_input)

root.mainloop()
