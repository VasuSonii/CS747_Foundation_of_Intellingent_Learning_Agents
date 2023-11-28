"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the MultiBanditsAlgo class. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, set_pulled, reward): This method is called 
        just after the give_pull method. The method should update the 
        algorithm's internal state based on the arm that was pulled and the 
        reward that was received.
        (The value of arm_index is the same as the one returned by give_pull 
        but set_pulled is the set that is randomly chosen when the pull is 
        requested from the bandit instance.)
"""

import numpy as np
import math
# START EDITING HEREi
# You can use this space to define any helper functions that you need
# END EDITING HERE


class MultiBanditsAlgo:
    def __init__(self, num_arms, horizon):
        # You can add any other variables you need here
        self.num_arms = num_arms
        self.horizon = horizon
        # START EDITING HERE
        self.counts1 = np.zeros(num_arms)
        self.counts2 = np.zeros(num_arms)
        self.heads1 = np.zeros(num_arms)
        self.heads2 = np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        betas1 = np.random.beta(self.heads1+1,self.counts1-self.heads1+1,self.heads1.size)
        betas2 = np.random.beta(self.heads2+1,self.counts2-self.heads2+1,self.heads2.size)
        betas = betas1 + betas2
        return np.argmax(betas)
        #raise NotImplementedError
        # END EDITING HERE
    
    def get_reward(self, arm_index, set_pulled, reward):
        # START EDITING HERE
        if set_pulled == 0:
            if reward == 1:
                self.heads1[arm_index] += 1
            self.counts1[arm_index] += 1
        else:
            if reward == 1:
                self.heads2[arm_index] += 1
            self.counts2[arm_index] += 1
        #raise NotImplementedError
        # END EDITING HERE

