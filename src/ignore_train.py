# Data processing
import pandas as pd
import numpy as np
import scipy.stats

# Similarity
from sklearn.metrics.pairwise import cosine_similarity  

def main():
    ratings = pd.read_csv("/home/tyang30/ml-latest/ratings.csv")  
    movies = pd.read_csv("/home/tyang30/ml-latest/movies.csv")
    

if __name__ == "__main__":
    main()