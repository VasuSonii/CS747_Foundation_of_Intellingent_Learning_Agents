import argparse
import numpy as np




def MapState():
    mydict = {}
    s = 0
    P = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16']
    B = ['1','2']
    for i in P:
      for j in P:
        for k in P:
          for e in B:
            mydict[s] =i+j+k+e 
            s += 1
    return mydict




def Read_file(filepath):
    Statemap = MapState()
    with open(filepath, 'r') as file:
        lines = file.readlines()
        for i,line in enumerate(lines):
            if i > 8191:
                break
            parts = line.strip().split(' ')
            parts = [i for i in parts if i != '']
            print(Statemap[i], parts[1], parts[0])



if __name__ == "__main__": 
    parse = argparse.ArgumentParser()
    parse.add_argument("--value-policy", type=str, help="Optimal Policy for the agent")
    parse.add_argument("--opponent", type=str, help="Location of Opponent policy file")
    argument = parse.parse_args()
    filepath = argument.value_policy
    Read_file(filepath)
