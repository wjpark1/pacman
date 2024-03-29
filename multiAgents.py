# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newGhostPositions = successorGameState.getGhostPositions()

        "*** YOUR CODE HERE ***"
        score = 0
        foodPositions = newFood.asList()
        foodPositionsAndDistances = {}

        for foodPos in foodPositions:
        	distance = manhattanDistance(newPos, foodPos)
        	foodPositionsAndDistances[foodPos] = distance
        if len(foodPositionsAndDistances) > 1:
        	closestFoodPos = min(foodPositionsAndDistances, key=foodPositionsAndDistances.get)
        	oldPos = currentGameState.getPacmanPosition()
        	newClosestFoodDist = manhattanDistance(newPos, closestFoodPos)
        	oldClosestFoodDist = manhattanDistance(oldPos, closestFoodPos)
        	if newClosestFoodDist < oldClosestFoodDist:
        		score += 100
        	else:
        		score -= 100
        
        if newScaredTimes[0] == 0:
        	newGhostPositions = successorGameState.getGhostPositions()
        	newGhostPositionsAndDistances = {}
        	for newGhostPosition in newGhostPositions:
        		distance = manhattanDistance(newPos, newGhostPosition)
        		newGhostPositionsAndDistances[newGhostPosition] = distance
        	closestGhostPos = min(newGhostPositionsAndDistances, key=newGhostPositionsAndDistances.get)
        	oldPos = currentGameState.getPacmanPosition()
        	newClosestGhostDist = manhattanDistance(newPos, closestGhostPos)
        	oldClosestGhostDist = manhattanDistance(oldPos, closestGhostPos)
        	if oldClosestGhostDist <= 5:
        		if newClosestGhostDist > oldClosestGhostDist:
        			score += 50
        		else:
        			score -= 50
        return score + successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        print self.depth
        print self.evaluationFunction
        print gameState.getLegalActions(0)
        legalActions = gameState.getLegalActions(0)
        print gameState.generateSuccessor(0, legalActions[0])
        print gameState.getNumAgents()
        print gameState.isWin()
        print gameState.isLose()
        
        depth = self.depth
        numAgents = gameState.getNumAgents()
        legalActionUtilities = {}
        legalActions = gameState.getLegalActions(0)


        for legalAction in legalActions:
        	successorGameState = gameState.generateSuccessor(0, legalAction)
        	legalActionUtilities[legalAction] = maxValue(successorGameState, 0, 0)

        closestFoodPos = min(foodPositionsAndDistances, key=foodPositionsAndDistances.get)

        #for currentDepth in range(0,depth):
        #	for currentAgent in range(0,numAgents):
        return maxValue(gameState, 0, 0)

        def maxValue(state, currentAgent, currentDepth):
        	v = -sys.maxint - 1
        	for successor in state.generateSuccessor( ):
        		v = max(v, value(successor))
        		return v

        def value(state, currentAgent, currentDepth):
        	if state.isWin() or state.isLose() or currentDepth == depth:
        		utility = self.evaluationFunction(state)
        		return utility
        	if currentAgent == 0:
        		return maxValue(state, currentAgent, depth)
        	else:
        		return minValue(state, currentAgent, depth)

        def minValue(state, nextAgent, currentDepth):
        	v = sys.maxint
        	for successor in state.generateSuccessor( ):
        		v = min(v, value(successor))
        		return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectedValue(gameState, agent, depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            numGhosts = gameState.getNumAgents() - 1
            actions = gameState.getLegalActions(agent)
            actionNum = len(actions)
            val = 0
            for action in actions:
                nextState = gameState.generateSuccessor(agent, action)
                if (agent == numGhosts):
                    val += maxValue(nextState, depth - 1)
                else:
                    val += expectedValue(nextState, agent + 1, depth)
            return val / actionNum
        
        def maxValue(gameState, depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(0)
            val = -(float('inf'))
            for action in actions:
                prevValue = val
                nextState = gameState.generateSuccessor(0, action)
                val = max(val, expectedValue(nextState, 1, depth))
            return val

        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(0)
        move = Directions.STOP
        score = -(float('inf'))
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            prevScore = score
            score = max(score, expectedValue(nextState, 1, self.depth))
            if score > prevScore:
                move = action
        return move

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newGhostPositions = successorGameState.getGhostPositions()

    "*** YOUR CODE HERE ***"
    score = 0
    foodPositions = newFood.asList()
    foodPositionsAndDistances = {}

    for foodPos in foodPositions:
    	distance = manhattanDistance(newPos, foodPos)
    	foodPositionsAndDistances[foodPos] = distance
    if len(foodPositionsAndDistances) > 1:
    	closestFoodPos = min(foodPositionsAndDistances, key=foodPositionsAndDistances.get)
    	oldPos = currentGameState.getPacmanPosition()
    	newClosestFoodDist = manhattanDistance(newPos, closestFoodPos)
    	oldClosestFoodDist = manhattanDistance(oldPos, closestFoodPos)
    	if newClosestFoodDist < oldClosestFoodDist:
    		score += 100
    	else:
    		score -= 100
    
    if newScaredTimes[0] == 0:
    	newGhostPositions = successorGameState.getGhostPositions()
    	newGhostPositionsAndDistances = {}
    	for newGhostPosition in newGhostPositions:
    		distance = manhattanDistance(newPos, newGhostPosition)
    		newGhostPositionsAndDistances[newGhostPosition] = distance
    	closestGhostPos = min(newGhostPositionsAndDistances, key=newGhostPositionsAndDistances.get)
    	oldPos = currentGameState.getPacmanPosition()
    	newClosestGhostDist = manhattanDistance(newPos, closestGhostPos)
    	oldClosestGhostDist = manhattanDistance(oldPos, closestGhostPos)
    	if oldClosestGhostDist <= 5:
    		if newClosestGhostDist > oldClosestGhostDist:
    			score += 50
    		else:
    			score -= 50
    return score + successorGameState.getScore()
    

# Abbreviation
better = betterEvaluationFunction

