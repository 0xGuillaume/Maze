import collections
from colorama import Fore
from random import randrange


class Maze:
    """
    Description:
        - 1. Génère un labyrinthe
        - 2. Tente de le résoudre
        - 3. Si aucun chemin n'est trouvé, retourne à l'étape 1.
    """
    def __init__(self, row:int, column:int):

        # Configuration du labyrinthe
        self._wall      = " 🌳 " #"w"
        self._cell      = " 📍 " #"c"
        self._start     = " 🏁 " #"s"
        self._exit      = " 🏳️ " #"x"
        self._maze      = [[self._wall for _ in range(column)] for _ in range(row)]
        self._empty     = list()
        self._graph     = list()

        # GPS Labyrtinthe
        self._y_start   = randrange(0, len(self._maze[0]))
        self._y_exit    = randrange(0, len(self._maze[0]))

        # Lancement automatique
        self._maze      = self._flipping_wall()
        self._maze      = self._random_start_exit()
        self._graph     = self._graph_init()
        self.maze_print()
        
        
    def _random_start_exit(self) -> list:
        """Définir une entrée et une sortie"""

        maze = self._maze
        maze[0][self._y_start] = self._start
        maze[-1][self._y_exit] = self._exit

        return maze 

    def _flipping_wall(self) -> list:
        """Transforme aléatoirement les murs en cellules vides"""

        for r_, row in enumerate(self._maze):
            for c_, cell in enumerate(row):
                if bool(randrange(2)):
                    self._maze[r_][c_] = self._cell
                    self._empty.append([r_, c_])
        return self._maze

    def _is_valid(self, cursor:list) -> list:
        
        x, y        = cursor[0], cursor[1]
        maze        = self._maze
        children    = list()
        maze_blocks = (self._cell, self._start, self._exit)

        # Check : Droite - Est vide
        if not y + 1 >= len(maze[x]) and maze[x][y + 1] in maze_blocks:
            children.append((x, y + 1))

        # Check : Gauche - Est vide
        if not y - 1 < 0 and maze[x][y - 1] in maze_blocks:
            children.append((x, y - 1))

        # Check : Haut - Est vide
        if not x + 1 >= len(maze) and maze[x + 1][y] in maze_blocks:
            children.append((x + 1, y))

        # Check : Bas - Est vide
        if not x - 1 < 0 and maze[x - 1][y] in maze_blocks:
            children.append((x - 1, y))
        
        return children

    def maze_print(self) -> list:
        """Affiche le labyrtinthe"""

        maze_str = "\n"
        for row in self._maze:
            maze_str += f"\t{str(''.join(row))}\n"
        maze_str += "\n"
        
        return maze_str

    def _graph_init(self) -> list:
        """Dessine un graph avec les cellules non vides et voisins vides (cellule vide)"""

        maze, graph = self._maze, self._graph

        for x, row in enumerate(maze):
            for y, cell in enumerate(row):
                if cell == self._cell:
                    graph.append([(x, y), self._is_valid([x, y])])

                if cell == self._start:
                    graph.insert(0, [(x, y), self._is_valid([x, y])])
                
                if cell == self._exit:
                    exit_node = [(x, y), self._is_valid([x, y])] 

        graph.append(exit_node)        
    
        return graph

    def _graph_first_move(self) -> tuple:
        """Premier mouvement"""
        
        ways = self._graph[0][1]
        
        for way in ways:
            for node in self._graph[1:]:
                if way in node[1]:
                    return way

    def _graph_solver(self) -> list:
        """Resolution du graphique > Chemin"""
        
        graph = self._graph
        path, visited, queue = list(), list(), list()

        # Premier mouvement en mémoire
        first_move = self._graph_first_move()
        queue.append(first_move)
        visited.append(first_move)

        while queue:
            try:
                if path[-1] == graph[-1][0]:
                    break
            except IndexError:
                pass

            # Coordonnées sur lesquelles on effectue le test 
            cursor = queue.pop()

            for node in graph[1:]:
                
                # Si le noeud a déjà été visité, on passe au suivant
                if node[0] in visited:
                    continue

                if cursor in node[1]:
                    visited.append(node[0])
                    queue.append(node[0])

            # Ajout de la cellule au chemin de résolution
            path.append(cursor)

        return path

    def _graph_is_solvable(self) -> bool:
        """On tente de voir si le graph est solvable"""

        path    = self._graph_solver()
        exit_   = (len(self._maze) - 1, self._y_exit)  

        if not path or path[-1] != exit_:
            return False

        else:
            return True
    
    def is_solvable(self) -> bool:
        """Vrai ou Faux : Si on peut résoudre le labyrinthe"""

        return self._graph_is_solvable()

    def solution(self) -> list:
        """Retourne la solution du labyrinthe"""

        return self._graph_solver()

