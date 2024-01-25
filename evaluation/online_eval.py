import os
import sys
import time
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils import compute_occupation_sim, check_coverage, compute_user_dist, compute_recommedation_overlap

def online_eval():
    while True:
        compute_occupation_sim()
        check_coverage()
        
        compute_user_dist(35723,32880)
        overlap_moreeq2 = compute_recommedation_overlap(35723,32880)
        
        compute_user_dist(175634,137114)
        overlap_lesseq2 = compute_recommedation_overlap(175634,137114)
        
        with open(f"{os.path.dirname(__file__)}/../data/eval_online_result.txt",'r') as infile:
            result = json.load(infile)
        result["Sample recommendation overlap between proximate users "] = overlap_moreeq2
        result["Sample recommendation overlap between distant users "] = overlap_lesseq2
        
        with open(f"{os.path.dirname(__file__)}/../data/eval_online_result.txt",'w') as outfile:
            json.dump(result,outfile,indent=2)
        
        time.sleep(2)

if __name__ == "__main__":
    online_eval()