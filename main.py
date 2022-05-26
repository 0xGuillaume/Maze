from curses import wrapper
from time import sleep
from maze import Maze


class Display(Maze):
    """
    Gerer les affichages pour la présentation
    """
    
    def __init__(self, row:int, column:int):
        super().__init__(row, column)

        # Terminal
        self._ms = 0.2

    def graph(self) -> None:
        """Montre le graph"""

        print(f"\n\t[MAZE] Graph des possibilités :\n")
        for node in self._graph:
            print(f"\t{node}")
        print("\n")            
    
    def maze(self, stdscr:object) -> None:
        """Afficher le maze"""

        stdscr.clear()
        stdscr.addstr(self.maze_print())
        stdscr.refresh()
        sleep(self._ms)
            

# ===================================================================

def main(stdscr):
    """Fonction de test"""

    attempt = 0

    while True:
        #maze = Maze(10, 10)
        show = Display(10, 10)
        show.maze(stdscr)
        
        if show.is_solvable():
            print(show.maze_print())
            attempt += 1
            break
        else:
            attempt += 1
    print(f"Taille : 1000, 1000 - Nombre de tentative : {attempt}")

if __name__ == "__main__":
    #maze = Maze(5, 5)
    #show = Display(5, 5)
    #wrapper(show.maze)
    wrapper(main)
    

