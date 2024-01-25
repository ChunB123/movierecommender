import pandas as pd
import numpy as np
import math
import json

numNeighbors = 20
threshold = 0

flag = 50

matrix_ratings = []
average_ratings = []

users = []
movies = []

def _removeLabels(df):
    df.columns.name = None
    df.index.names = ['']
    return df

#Retrive average rating for each user from the matrix
def getRatings():
    global matrix_ratings
    global average_ratings

    for row in matrix_ratings:
        sum = 0
        cnt = 0

        for rating in row:
            if not rating == -1:
                sum += rating
                cnt += 1
        average_ratings.append(sum / cnt)
    
    average_ratings = np.array(average_ratings, dtype = float)

#Calculate similarity between two users
def simimilarity(posU1, posU2, newAverage):
    numerator = 0
    denominator = 0
    firstDenom = 0
    secondDenom = 0

    for i in range(len(movies)):
        if not matrix_ratings[posU1][i] == -1 and not matrix_ratings[posU2][i] == -1:
            numerator += (matrix_ratings[posU1][i] - newAverage) * (matrix_ratings[posU2][i] - average_ratings[posU2])
            firstDenom += pow(matrix_ratings[posU1][i] - newAverage, 2)
            secondDenom += pow(matrix_ratings[posU2][i] - average_ratings[posU2], 2)
        
    denominator = math.sqrt(firstDenom) * math.sqrt(secondDenom)
    
    if numerator == 0:
        return 0
    
    return numerator/denominator

#Predicte the rating for user i on item j
def prediction(pos, sims, newAverage):
    numerator = 0
    denominator = 0
    
    for i in range(len(sims)):    
        numerator += sims[i][0] * (matrix_ratings[sims[i][1]][pos] - average_ratings[sims[i][1]])
        denominator += sims[i][0]

    if numerator == 0:
        return newAverage

    return newAverage + numerator/denominator

#Sort the similarity in descending order and get most similar top n neighbors
def getNeighbours(sims):
    sims = sorted(sims, key=lambda x: x[0], reverse=True)
    
    sims = sims[0: numNeighbors]
    return sims

#Calculate new average for user i
def calNewAve(posU):
    sum = 0
    cnt = 0

    for j in range(len(movies)):
        if not matrix_ratings[posU][j] == -1:
            sum += matrix_ratings[posU][j]
            cnt += 1
    
    if sum == 0:
        return 0
    
    return sum / cnt

#Evaluation: MAE, Precision, Recall, and F1-Score
def eval():
    global matrix_ratings
    new_ratings = []

    for i in range(len(users)):
        print(i)
        tempRow = []

        for j in range(len(movies)):
            if not matrix_ratings[i][j] == -1:
                sims = []
                tempRating = matrix_ratings[i][j]
                matrix_ratings[i][j] = -1
                newAverage = calNewAve(i)

                for k in range(len(users)):
                    if not k == i and not matrix_ratings[k][j] == -1:
                        tempSim = simimilarity(i, k, newAverage)
                        if tempSim > threshold:
                            tup = (tempSim, k)
                            sims.append(tup)
                sims = getNeighbours(sims)
                tempRow.append(prediction(j, sims, newAverage))
                matrix_ratings[i][j] = tempRating
            else:
                tempRow.append(-1)
        new_ratings.append(tempRow)
    
    new_ratings = np.array(new_ratings, dtype=float)

    sum = 0
    cnt = 0

    truePos = 0
    falsePos = 0
    falseNeg = 0

    for i in range(len(users)):
        for j in range(len(movies)):
            if not matrix_ratings[i][j] == -1:
                sum += abs(matrix_ratings[i][j] - new_ratings[i][j])
                cnt += 1
                if matrix_ratings[i][j] > flag and new_ratings[i][j] > flag:
                    truePos += 1
                elif matrix_ratings[i][j] <= flag and new_ratings[i][j] > flag:
                    falsePos += 1
                elif matrix_ratings[i][j] > flag and new_ratings[i][j] <= flag:
                    falseNeg += 1

    mae = sum / cnt
    precision = truePos / (truePos + falsePos)
    recall = truePos / (truePos + falseNeg)

    f1score = (2 * precision * recall) / (precision + recall)

    return mae, precision, recall, f1score

def main(df):
    global matrix_ratings
    global users
    global movies
    global threshold
    global numNeighbors

    outfile_MAE = "MAE.json"

    merged_df = df.pivot(index='userid', columns='movieid', values='rating')
    merged_df = merged_df.fillna(-1)
    merged_df = _removeLabels(merged_df)

    matrix_ratings = merged_df.to_numpy()
    print(matrix_ratings)

    users = list(merged_df.index.values)
    movies = list(merged_df.columns.values)

    result = {}
    # result = {
    #     "Threshold" : {},
    #     "NumOfNeighbors" : {}
    # }

    getRatings()
    mae, precision, recall, f1score = eval()
    print(mae, precision, recall, f1score)
    result["MAE"] = mae
    result["Precision"] = precision
    result["Recall"] = recall
    result["F1Score"] = f1score

    with open("../data/evaluations/eval_user_result.txt", "w") as outfile: 
        json_str = json.dumps(result)
        outfile.write(json_str)

    
    # bestT = 0
    # bestTMAE = 101

    # bestN = 0
    # bestNMAE = 101

    # while threshold <= 1:
    #     mae, precision, recall, f1score = eval()
    #     print(mae)
    #     result["Threshold"][threshold] = mae

    #     if mae < bestTMAE:
    #         bestTMAE = mae
    #         bestT = threshold

    #     threshold += 0.01
    
    # threshold = 0

    # while numNeighbors < len(users):
    #     mae, precision, recall, f1score = eval()
    #     print(mae)
    #     result["NumOfNeighbors"][numNeighbors] = mae
        
    #     if mae < bestTMAE:
    #         bestNMAE = mae
    #         bestN = threshold

    #     numNeighbors += 1

    # print(bestT, bestTMAE)
    # print(bestN, bestNMAE)

    # with open("result.json", "w") as outfile: 
    #     json.dump(result, outfile)
    
if __name__ == '__main__':
    data_path = "../data/logs/logs_advanced.csv"
    df = pd.read_csv(data_path, names = ['userid', 'movieid', 'rating'])
    print(df)
    main(df)