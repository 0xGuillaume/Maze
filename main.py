import argparse
from curses import wrapper
from time import sleep, time
from maze import Maze


# Arguments terminal
parser = argparse.ArgumentParser(description="Labyrinthe - Projet Algo Maths ESGI")
parser.add_argument("-x", dest="x", type=int, required=True, 
        help="Saisir le nombre de lignes X du labyrinthe")
parser.add_argument("-y", dest="y", type=int, required=True, 
        help="Saisir le nombre de colonnes Y du labyrinthe")
parser.add_argument("-g", dest="g", action="store_true", 
        help="Affiche le graph de résolution du labyrinthe")
parser.add_argument("-m", dest="m", action="store_true", 
        help="Affiche un labytinthe")
parser.add_argument("-gen", dest="gen", action="store_true", 
        help="Génère un labyrinthe")
parser.add_argument("-s", dest="s", action="store_true", 
        help="Résoud un labyrinthe")
args = parser.parse_args()

class Display(Maze):
    """
    Gerer les affichages pour la présentation
    """
    
    def __init__(self, row:int, column:int):
        super().__init__(row, column)

        self._ms        = 0.2 # Terminal
        self._ms_solver = 0.5 # Terminal
        self._solver    = " 👣 "

    def graph(self) -> None:
        """Afficher le graph des solutions possibles"""

        print(f"\n\t[MAZE] Graph des possibilités :\n")
        for node in self._graph:
            print(f"\t{node}")
        print("\n")            
    
    def maze_screen(self) -> None:
        """Afficher le maze"""

        return print(self.maze_print())

    def maze(self, stdscr:object) -> None:
        """Afficher le maze"""

        stdscr.clear()
        stdscr.addstr(self.maze_print())
        stdscr.refresh()
        sleep(self._ms)

    def solver(self, stdscr:object) -> None:
        """Chemin pour résoudre le labyrinthe"""

        path = self._graph_solver()
        path = path[:-1]
        maze = self._maze
        maze_str = "\n"

        for r, row in enumerate(maze):
            for c, cell in enumerate(row):
                if (r, c) in path:
                    maze[r][c] = self._solver

                    for row in self._maze:
                        maze_str += f"\t{str(''.join(row))}\n"
                        #print(maze_str)

                    stdscr.clear()
                    stdscr.addstr(maze_str)
                    stdscr.refresh()
                    sleep(self._ms_solver)
                    maze_str = "\n"

        self.maze_screen()
        return path                    


# ===================================================================


def main(stdscr):
    """Fonction principale"""

    start_time = time()
    attempt = 0

    while True:
        show = Display(args.x, args.y)
       
        if args.gen:
            show.maze(stdscr)
        
        if show.is_solvable():
            # Graph
            if args.g:
                show.graph()

            # Maze
            if args.m:
                show.maze_screen()

            attempt += 1
            break
        else:
            attempt += 1

    message = ""

    if args.gen and args.s:
        path = show.solver(stdscr)
        message += f"Taille\t\t-\t10 x 10\nTentative(s)\t-\t{attempt}\nTemps écoulé\t-\t{'%s secondes' % (round(time() - start_time, 2))}\nChemin\t\t-\t{path}\n"

    elif args.gen and not args.s:
        print(show.maze_print())
        message += f"Taille\t\t-\t10 x 10\nTentative(s)\t-\t{attempt}\nTemps écoulé\t-\t{'%s secondes' % (round(time() - start_time, 2))}\n"
    
    elif args.s and not args.gen:
        path = show.solver(stdscr)
        message += f"Taille\t\t-\t10 x 10\nTentative(s)\t-\t{attempt}\nTemps écoulé\t-\t{'%s secondes' % (round(time() - start_time, 2))}\nChemin\t\t-\t{path}\n"

    print(message)


wrapper(main)
    

    

