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
        "*** YOUR CODE HERE ***"
        score=successorGameState.getScore()
        foodArray=newFood.asList()

        for i in foodArray:
          foodDist = util.manhattanDistance(i,newPos)
          if (foodDist)!=0:
                  score=score+(1.0/foodDist)
        
        for ghost in newGhostStates:
          ghostpos=ghost.getPosition()
          ghostDist = util.manhattanDistance(ghostpos,newPos)
          if (abs(newPos[0]-ghostpos[0])+abs(newPos[1]-ghostpos[1]))>1:	
            score=score+(1.0/ghostDist)
        
        return score

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
        """
        "*** YOUR CODE HERE ***"
        numberOfGhosts = gameState.getNumAgents() - 1
        def maxLevel(gameState, depth):
          currentDepth = depth + 1
          if gameState.isWin() or gameState.isLose() or currentDepth == self.depth:
            return self.evaluationFunction(gameState)
          maxValue = -99999

          actions = gameState.getLegalActions(0)
          for action in actions:
            successor = gameState.generateSuccessor(0, action)
            maxValue = max(maxValue, minLevel(successor, currentDepth, 1))
          return maxValue
        
        def minLevel(gameState, depth, agentIndex):
          minValue = 99999
          if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
          for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == numberOfGhosts:
              minValue = min(minValue, maxLevel(successor, depth))
            else:
              minValue = min(minValue, minLevel(successor, depth, agentIndex+1))
          return minValue

        currentScore = -99999
        returnAction = ''

        for action in gameState.getLegalActions(0):
          nextState = gameState.generateSuccessor(0, action)
          score = minLevel(nextState, 0, 1)
          if score > currentScore:
            returnAction = action
            currentScore = score

        return returnAction
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numberOfGhosts = gameState.getNumAgents() - 1
        def maxLevel(gameState, depth, alpha, beta):
          currentDepth = depth +1
          maxValue = -99999
          if gameState.isWin() or gameState.isLose() or currentDepth == self.depth:
            return self.evaluationFunction(gameState)
          alpha1 = alpha

          for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            maxValue = max(maxValue, minLevel(successor, currentDepth, 1, alpha1, beta))
            if maxValue > beta:
              return maxValue
            alpha1 = max(alpha1, maxValue)

          return maxValue
            
        def minLevel(gameState,depth, agentIndex, alpha, beta):
          minValue= 99999
          if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
          beta1 = beta

          for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            if agentIndex==numberOfGhosts:
              minValue = min(minValue, maxLevel(successor, depth, alpha, beta1))
              if minValue < alpha:
                return minValue
              beta1 = min(beta1, minValue)
            else:
              minValue = min(minValue, minLevel(successor, depth, agentIndex+1, alpha, beta1))
              if minValue < alpha:
                return minValue
              beta1 = min(beta1, minValue)

          return minValue

        alpha = -99999
        beta = 99999
        currentScore = -99999
        returnAction = ''

        for action in gameState.getLegalActions(0):
          nextState = gameState.generateSuccessor(0, action)
          score = minLevel(nextState, 0, 1, alpha, beta)
          if score > currentScore:
            currentScore = score
            returnAction = action
          if score > beta:
            return returnAction
          alpha = max(alpha, score)

        return returnAction
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
        def maxLevel(gameState, depth):
          currentDepth = depth + 1
          maxValue = -99999

          if gameState.isWin() or gameState.isLose() or currentDepth == self.depth:
            return self.evaluationFunction(gameState)
          for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            maxValue = max(maxValue, expectLevel(successor, currentDepth, 1))

          return maxValue 

        def expectLevel(gameState, depth, agentIndex):
          if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
          totalExpectedValue = 0
          actions= gameState.getLegalActions(agentIndex)
          numberOfActions = len(actions)

          for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == (gameState.getNumAgents() - 1):
              expectedValue = maxLevel(successor, depth)
            else:
              expectedValue = expectLevel(successor, depth, agentIndex + 1)
            totalExpectedValue = totalExpectedValue + expectedValue
          if numberOfActions == 0:
            return 0

          return float(totalExpectedValue)/float(numberOfActions)

        currentScore = -99999
        returnAction = ''

        for action in gameState.getLegalActions(0):
          nextState = gameState.generateSuccessor(0, action)
          score = expectLevel(nextState, 0, 1)
          if score > currentScore:
            returnAction = action
            currentScore = score

        return returnAction
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    numberOfPowerPellets = len(currentGameState.getCapsules())

    foodList = newFood.asList()
    foodDistance = [0]
    for pos in foodList:
      foodDistance.append(manhattanDistance(newPos, pos))

    ghostPos = []
    for ghost in newGhostStates:
      ghostPos.append(ghost.getPosition())
    ghostDistance = [0]
    for pos in ghostPos:
      ghostDistance.append(manhattanDistance(newPos, pos))
    
    score = 0
    numberOfNoFoods = len(newFood.asList(False))
    sumScaredTimes = sum(newScaredTimes)
    sumGhostDistance = sum(ghostDistance)
    reciprocalFoodDistance = 0
    if sum(foodDistance) > 0:
      reciprocalFoodDistance = 1.0 / sum(foodDistance)
    
    score += currentGameState.getScore() + reciprocalFoodDistance + numberOfNoFoods

    if sumScaredTimes > 0:
      score += sumScaredTimes + (-1 * numberOfPowerPellets) + (-1 * sumGhostDistance)
    else:
      score += sumGhostDistance + numberOfPowerPellets

    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

