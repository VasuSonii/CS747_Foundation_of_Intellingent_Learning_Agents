"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the base Algorithm class that all algorithms should inherit
from. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)

We have implemented the epsilon-greedy algorithm for you. You can use it as a
reference for implementing your own algorithms.
"""

import numpy as np
import math
# Hint: math.log is much faster than np.log for scalars
class Algorithm:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon = horizon
    
    def give_pull(self):
        raise NotImplementedError
    
    def get_reward(self, arm_index, reward):
        raise NotImplementedError

# Example implementation of Epsilon Greedy algorithm
class Eps_Greedy(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # Extra member variables to keep track of the state
        self.eps = 0.1
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
    
    def give_pull(self):
        if np.random.random() < self.eps:
            return np.random.randint(self.num_arms)
        else:
            return np.argmax(self.values)
    
    def get_reward(self, arm_index, reward):
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value

# START EDITING HERE
# You can use this space to define any helper functions that you need
def KL_divergence(a, b):
    if(a == b):
        return 0
    elif(b == 1):
        return float('inf')
    elif a == 0:
        return (1-a)*math.log((1-a)/(1-b))
    elif a == 1:
        return a*math.log(a/b)
    else:
        kl = a*math.log(a/b) + (1-a)*math.log((1-a)/(1-b))
        return kl
def binary_search(l,r,target,p):
    while True:
        if abs(l-r) < 0.001:
            break
        mid = (l+r)/2
        val = KL_divergence(p,mid)
        if val < target:
            l = mid
        elif val > target:
            r = mid
        if val == target:
            break
    return l 
# END EDITING HERE

class UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # START EDITING HERE
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
        self.ucb_values = np.zeros(num_arms)
        self.time = 0
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        self.time += 1
        if self.time < self.counts.size:
            return self.time
        return np.argmax(self.ucb_values)
        #raise NotImplementedError
        # END EDITING HERE  
        
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n-1)/n)*value + (1/n)*reward
        self.values[arm_index] = new_value
        if self.time >= self.counts.size:
            self.ucb_values = self.values + np.sqrt((2*math.log(self.time))/self.counts)
        # raise NotImplementedError
        # END EDITING HERE


class KL_UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        self.values = np.zeros(num_arms)
        self.counts = np.zeros(num_arms)
        self.kl_ucb = np.zeros(num_arms)
        self.time = 0
        # START EDITING HERE
   
    def give_pull(self):
        # START EDITING HERE
        self.time += 1
        if self.time < self.counts.size:
            return self.time
        return np.argmax(self.kl_ucb)
        # raise NotImplementedError
        # END EDITING HERE

    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        new_value = (n-1)*self.values[arm_index]/n + reward*(1/n)
        self.values[arm_index] = new_value
        if self.time >= self.counts.size:
         for i in range(self.counts.size):
             l = self.values[i]
             r = 1
             target =(math.log(self.time))/self.counts[i]
             self.kl_ucb[i] = binary_search(l,r,target,self.values[i])
        # END EDITING HERE

class Thompson_Sampling(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.heads = np.zeros(num_arms)
        self.counts = np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        betas = np.zeros(self.heads.size)
        betas = np.random.beta(self.heads+1, self.counts-self.heads+1,self.heads.size)
        return np.argmax(betas)
        # raise NotImplementedError
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.counts[arm_index] += 1
        if(reward == 1):
            self.heads[arm_index] += 1
        # raise NotImplementedError
        # END EDITING HERE
