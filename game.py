from termcolor import colored
from random import randint

field = [1, 2, 3, 4, 5, 6, 7, 8, 9]
player, player2, computer = '', '', ''
X = "\U0000274C"
O = "\U00002B55"
lose = "\U0001F641"
win = "\U0001F31F"
middle = 5
combination_for_win = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


def who_is_who_mes(p1, p2, comp=False):
    if not comp:
        print('First player plays for %s, second player plays for %s' % (p1, p2))
    else:
        print('Player plays for %s, computer plays for %s' % (p1, p2))

def color_fields(c):
    color_char = c
    if c == X:
        color_char = colored(c, "red")
    if c == O:
        color_char = colored(c, "green")
    return color_char

def draw_field(fields):
    print("______________________")
    for j in range(3):
        print(" | ", color_fields(fields[0 + j*3]), " | ", color_fields(fields[1 + j * 3]), " | ", color_fields(fields[2 + j * 3]), " | ")
        print("______________________")

def step_ability(brd, step):
    can = True if step in range(1, 10) and brd[step - 1] not in (X, O) else False
    return can


def make_step(fields, pl, step, fl=False):
    victory = False
    if step_ability(fields, step):
        fields[step - 1] = pl
        for combination in combination_for_win:
            victory = True
            for pos in combination:
                if fields[pos] != pl:
                    victory = False
                    break
            if victory:
                break
        if fl:
            fields[step - 1] = step
        return True, victory
    return False, False


def make_step_helper(f, fields, p, step):
    for i in f:
        if make_step(fields, p, i, True)[1]:
            step = i
            break
    return step


def computer_step(first=False):
    f = range(1, 10)
    step = -1
    if first and step_ability(field, middle):
        step = middle
    step = make_step_helper(f, field, computer, step)
    if step == -1:
        step = make_step_helper(f, field, player, step)
        for mv in f:
            if step == -1 and step_ability(field, mv):
                step = mv
                break
    return make_step(field, computer, step)


def first_step(pl):
    print('# Make your step %s' % pl)
    try:
        step = int(input())
    except ValueError:
        print("Its not a number!")
        return False, 0
    return True, step


def who_goes_first(p1, p2, live=False):
    if p1 == X:
        if not live:
            print("The player goes first")
            safe_step(p1, field)
            computer_step(True)
        else:
            print("The player number one goes first")
            safe_step(p1, field, False)
            safe_step(p2, field, False)
    if p2 == X and not live:
        print("The computer goes first")
        computer_step(True)
    if p2 == X and live:
        print("The player number two goes first")
        safe_step(p2, field, False)
    return True


def safe_step(pl, fields, comp=True):
    victory, step = False, False
    while not step:
        tmp = False
        while not tmp:
            f_step = first_step(pl)
            tmp = f_step[0]
        step, victory = make_step(fields, pl, f_step[1])
        if not comp: draw_field(fields)
        if not step: print('You entered the wrong number or the place is already taken. Try again')
    return victory


def playing_with_computer(pl, comp):
    who_is_who_mes(pl, comp, True)
    r = ''
    while field.count(X) + field.count(O) != len(field):
        draw_field(field)
        if field.count(X) + field.count(O) == 0:
            tmp = who_goes_first(pl, comp, False)
            if not tmp:
                continue
        else:
            victory = safe_step(pl, field)
            if victory:
                r = '%s You are the winner %s' % (win, win)
                break
            elif computer_step()[1]:
                r = '%s You loooose %s' % (lose, lose)
                break
            else:
                r = "Friendship between man and computer won!"
    draw_field(field)
    print(r)


def playing_with_human(pl, pl2):
    who_is_who_mes(pl, pl2, False)
    r = ''
    draw_field(field)
    while field.count(X) + field.count(O) != len(field):
        if field.count(X) + field.count(O) == 0:
            tmp = who_goes_first(pl, pl2, True)
            if not tmp:
                continue
        else:
            victory = safe_step(pl, field, False)
            if victory:
                r = '%s %s the winner %s' % (win, pl, win)
                break
            if not field.count(X) + field.count(O) != len(field):
                break
            victory = safe_step(pl2, field, False)
            if victory:
                r = '%s %s the winner %s' % (win, pl2, win)
                break
            else:
                r = "Friendship won!"
    print(r)


def rand_symbol_choice():
    chars = (X, O)
    chars = (chars[::-1] if randint(0, 1) == 0 else chars)
    return chars


print(colored("To play with a computer, enter 1, to play with a person, enter 2, to exit enter \'exit\'", "blue"))
decision = input()
if decision == "1":
    player, computer = rand_symbol_choice()
    playing_with_computer(player, computer)
elif decision == "2":
    player, player2 = rand_symbol_choice()
    playing_with_human(player, player2)
elif decision == "exit":
    exit()
else:
    print('You entered the wrong number')
    exit()
