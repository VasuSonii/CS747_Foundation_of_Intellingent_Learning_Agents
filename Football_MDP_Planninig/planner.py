#python code for task1 
import numpy as np
import argparse
import pulp

def Value_Policy(T, R, gamma, S, Policy):
    Vpi = np.zeros(S)
    Vpi_1 = np.zeros(S)
    eps = 1e-12
    while True:
        Vpi_1 = Vpi.copy()
        for i in range(S):
            Vpi[i] = np.sum(T[i, int(Policy[i])] * (R[i, int(Policy[i])] + gamma * Vpi_1))
        if abs(np.max(Vpi - Vpi_1)) < eps and abs(np.max(Vpi_1-Vpi)) < eps:
            break
    Qpi = np.sum(np.multiply(T, (R + gamma * Vpi)), axis=2)
    return Vpi, Qpi 


def PolicyIteration(T, R, S, gamma):
    Policy = np.zeros(S)
    Pre_Policy = np.zeros(S)
    V, Q = Value_Policy(T, R, gamma, S, Policy)
    while True:
        Pre_Policy = Policy.copy()
        IA = [] 
        for i in range(S):
            indices = np.where(Q[i] > V[i])
            indices = list(indices[0])
            IA.append(indices)
        for i in range(S):
            if len(IA[i])>0:
                Policy[i] = np.argmax(Q[i])
        V, Q = Value_Policy(T, R, gamma, S, Policy)
        if np.array_equal(Pre_Policy,Policy):
          break

    return Policy

def LinearProgramming(T,R,gamma,S,A):
    problem = pulp.LpProblem("LP", pulp.LpMinimize)
    num_vars = S
    V = [pulp.LpVariable(f"V{i}") for i in range(num_vars)]
    problem += pulp.lpSum(V[s] for s in range(S))

    for s in range(S):
        for a in range(A): 
            problem += V[s] >= pulp.lpSum(T[s][a][s_prime] * (R[s][a][s_prime] + gamma * V[s_prime])for s_prime in range(S))

    problem.solve(pulp.PULP_CBC_CMD(msg=False))
    optimal_Vs = [V[s].varValue for s in range(S)]
    Vs = np.array(optimal_Vs)    
    As = np.argmax(np.sum(T*(R+gamma*Vs),axis=2),axis = 1)
    return Vs,As


def ValueIteration(T, R, gamma, S, A,endstate):
    Vt = np.zeros(S)
    At = np.zeros(S)
    Vt_1 = np.zeros(S)
    eps = 1e-10
    sum = 0
    while(True): 
        Vt_1 = Vt.copy()
        for i in range(S):
            if i not in endstate:  
                Vt[i] = np.max(np.sum(T[i]*(R[i]+gamma*Vt_1),axis=1))
                At[i] = np.argmax(np.sum(T[i]*(R[i]+gamma*Vt_1),axis=1))
            else:
                Vt[i] = 0
                At[i] = -1     
        if(abs(np.max(Vt-Vt_1))<eps and abs(np.max(Vt_1-Vt))<eps):
            break
    return Vt,At

def ReadFile(mdppath):
    States = 0
    Actions = 0
    T = None
    R = None
    gamma = 0
    mtype = "not-specified"
    endstate = -1

    with open(mdppath, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(' ')
            parts = [i for i in parts if i != '']
            if parts[0] == 'numStates':
                States = int(parts[1])
            elif parts[0] == 'numActions':
                Actions = int(parts[1])
                T = np.zeros((States, Actions, States))
                R = np.zeros(shape = (States, Actions, States), dtype = np.float32)
            elif parts[0] == 'transition':
                s1, ac, s2 = map(int, parts[1:4])
                p = float(parts[5])
                r = float(parts[4])
                T[s1,ac,s2] = p
                R[s1,ac,s2] = r
            elif parts[0] == 'mdptype':
                mtype = parts[1]
            elif parts[0] == 'discount':
                gamma = float(parts[1])
            elif parts[0] == 'end':
                endstate = parts[1:]

    return States, Actions, T, R, gamma, mtype, endstate

def ReadPolicy(policypath,States):
    P = np.zeros(States)
    N = []
    with open(policypath, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(' ')
            parts = [i for i in parts if i != '']
            N.append(int(parts[0]))  
    P = np.array(N)
    return P
if __name__ == "__main__":
        
    parse = argparse.ArgumentParser()
    parse.add_argument("--mdp", type=str, help="MDP file path to be entered")
    parse.add_argument("--algorithm", type=str, help="Algorithm to be executed", default = 'vi')
    parse.add_argument("--policy", type=str, help="Policy for Value Function")
    argument = parse.parse_args()
    mdppath = argument.mdp
    algorithm = argument.algorithm
    policypath = argument.policy
    States, Actions, T, R, gamma, mtype, endstate = ReadFile(mdppath)
    if policypath != None:
        Policy = ReadPolicy(policypath,States)
        Vpi,Qpi = Value_Policy(T,R,gamma,States,Policy)
        for i in range(States):
            print(Vpi[i], " ", Policy[i]) 
    elif algorithm == 'vi':
        Vt, At = ValueIteration(T,R,gamma,States,Actions,endstate)
        for i in range(States):
            print(Vt[i], " ", int(At[i]))

    elif algorithm == 'hpi':
        Policy = PolicyIteration(T,R,States,gamma)
        Vt,Qt = Value_Policy(T,R,gamma,States,Policy)
        for i in range(States):
            print(Vt[i], " ", int(Policy[i]))

    elif algorithm == 'lp':
        Vt,At = LinearProgramming(T,R,gamma,States,Actions)
        for i in range(States):
            print(Vt[i]," ",At[i])
    

