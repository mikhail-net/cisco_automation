# Fonctions d'affichage avec couleurs
RED = '\033[31m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
END = '\033[0m'

def show_result(result):
    print(YELLOW + result + END)

def show_info(info):
    print(RED + info + END)

def show_input(input):
    return "{0}{1}{2}".format(YELLOW, input, END)

def show_cisco():
    return "{0}cisco~# {1}".format(RED, END)
