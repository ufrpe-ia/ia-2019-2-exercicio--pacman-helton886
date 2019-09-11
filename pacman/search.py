# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    # from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    stack = util.Stack()
    visitedList = []
    # coloca a estrutura inicial na pilha
    stack.push((problem.getStartState(),[],0))
    (state, toDirection, toCost) = stack.pop()
    # coloca o estado na lista de visitados
    visitedList.append(state)
    # enquanto nao encontrar a resolucao
    while not problem.isGoalState(state):
        successors = problem.getSuccessors(state)
        for son in successors:
            # se o filho nao foi visitado, coloque-o na pilha e coloca o estado atual em visitados
            if (not son[0] in visitedList):
                stack.push((son[0],toDirection + [son[1]],toCost + son[2]))
                visitedList.append(son[0])
        (state, toDirection, toCost) = stack.pop()
    return toDirection


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    DICA: Utilizar util.PriorityQueue
    *** YOUR CODE HERE ***
    """
    queue = util.Queue()
    visitedList = []
    #coloque a estrutura inicial para a fila
    queue.push((problem.getStartState(),[],0))
    (state,toDirection,toCost) = queue.pop()
    #coloque o ponto visitado na lista de pontos visitados
    visitedList.append(state)

    # se o filho nao foi visitado, coloque-o na fila e coloca o estado atual em visitados
    while not problem.isGoalState(state): 
        successors = problem.getSuccessors(state) 
        for son in successors:
            if not son[0] in visitedList: 
                queue.push((son[0],toDirection + [son[1]],toCost + son[2]))
                visitedList.append(son[0])
        (state,toDirection,toCost) = queue.pop()

    return toDirection

    
def uniformCostSearch(problem):
    """Search the node of least total cost first.
    *** YOUR CODE HERE ***
    """
    pQueue = util.PriorityQueue()
    visitedList = []

    #inicia a estrutura na fila colocando um peso 0 e coloca o primeiro valor na lista de visitados
    pQueue.push((problem.getStartState(),[],0),0)
    (state,toDirection,toCost) = pQueue.pop()
    visitedList.append((state,toCost))

    #adicione o estado se o sucessor nao foi visitado ou foi visitado mas com um custo menor que o anterir
    while not problem.isGoalState(state):
        successors = problem.getSuccessors(state)
        for son in successors:
            visitedExist = False
            total_cost = toCost + son[2]
            for (visitedState,visitedToCost) in visitedList:
                # se o sucessor n tiver sido visitado e tiver custo menor que o anterior
                if (son[0] == visitedState) and (total_cost >= visitedToCost):
                    visitedExist = True # ponto reconhecido visitado
                    break

            if not visitedExist:
                # empurre o estado com a prioriade do seu custo total e o coloca na lista de visitados
                pQueue.push((son[0],toDirection + [son[1]],toCost + son[2]),toCost + son[2])
                visitedList.append((son[0],toCost + son[2]))

        (state,toDirection,toCost) = pQueue.pop()

    return toDirection

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    pQueue = util.PriorityQueue()
    visitedList = []

    # inicia o estado inicial com prioridade 0 e o coloca como visitado
    pQueue.push((problem.getStartState(),[],0),0 + heuristic(problem.getStartState(),problem))
    (state,toDirection,toCost) = pQueue.pop()
    visitedList.append((state,toCost + heuristic(problem.getStartState(),problem)))

    while not problem.isGoalState(state):
        successors = problem.getSuccessors(state)
        for son in successors:
            visitedExist = False
            total_cost = toCost + son[2]
            for (visitedState,visitedToCost) in visitedList:
                # se o sucessor n tiver sido visitado e tiver custo menor que o anterior
                if (son[0] == visitedState) and (total_cost >= visitedToCost):
                    visitedExist = True
                    break
            if not visitedExist:
                # coloca-o na fila de prioridades com o custo total e o adiciona como visitado
                pQueue.push((son[0],toDirection + [son[1]],toCost + son[2]),toCost + son[2] + heuristic(son[0],problem))
                visitedList.append((son[0],toCost + son[2]))

        (state,toDirection,toCost) = pQueue.pop()

    return toDirection



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
