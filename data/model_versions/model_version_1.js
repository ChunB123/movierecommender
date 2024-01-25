const fs = require('fs');

const numNeighbors = 20;
const threshold = 0;

//Reading the file
const infoFile = "../data/info/info.json"
let info = JSON.parse(fs.readFileSync(infoFile, 'utf-8'));
let training_data_version = info["training_data_version"].toString();

const matrixFile = "../data/training_data_versions/data_" + training_data_version + ".txt";
const usersFile = "../data/training_data_versions/users_" + training_data_version + ".txt";
const moviesFile = "../data/training_data_versions/movies_" + training_data_version + ".txt";
const recommendationFile = "../data/training_data_versions/recommendation_versions/recommendation_user_" + training_data_version + ".json";

const matrixData = fs.readFileSync(matrixFile, 'utf-8').split("\n");
const usersData = fs.readFileSync(usersFile, 'utf-8').split("\n");
const users = getUsers(usersData);
const numUsers = users.length;
const moviesData = fs.readFileSync(moviesFile, 'utf-8').split("\n");
const movies = getMovies(moviesData);
const numMovies = movies.length;
let results = getRatings(matrixData)
const ratings = results[0]
const average_ratings = results[1]


const prediction = calculateRatings();
console.log(prediction);
const jsonString = JSON.stringify(prediction, null, 2);

fs.writeFile(recommendationFile, jsonString, (err) => {
    if (err) {
        console.error('An error occurred:', err);
        return;
    }
    console.log('JSON saved to output.json');
});

function sim(posU1, posU2){
    let numerator = 0;
    let denominator = 0;
    let firstDenom = 0;
    let secondDenom = 0;

    for(let i = 0; i < numMovies; i++){        
        if(ratings[posU1][i] != -1 && ratings[posU2][i] != -1){            
            numerator += (ratings[posU1][i] - average_ratings[posU1]) * (ratings[posU2][i] - average_ratings[posU2]);
            firstDenom += Math.pow((ratings[posU1][i] - average_ratings[posU1]), 2);
            secondDenom += Math.pow((ratings[posU2][i] - average_ratings[posU2]), 2);
        }
    }

    if(numerator == 0){
        return 0
    }

    denominator = Math.sqrt(firstDenom) * Math.sqrt(secondDenom);

    return numerator/denominator;
}

function pred(pos, sims, average){
    let numerator = 0;
    let denominator = 0;

    for(let i= 0; i < sims.length; i++){
        numerator += (sims[i].sim * (ratings[sims[i].pos][pos] - average_ratings[sims[i].pos]));
        denominator += sims[i].sim;
    }
    
    if(numerator == 0){
        return average;
    }

    return (average + numerator/denominator);
}

function calculateRatings(){
    let recommendedMovies = {}
    console.log(numUsers)

    for(let i = 0; i < numUsers; i++){
        console.log("userID: ", i)
        let tempRow = []

        for(let j = 0; j < numMovies; j++){
            if(ratings[i][j] == -1){
                let sims = [];
                
                for(let k = 0; k < numUsers; k++){
                    if((k != i) && (ratings[k][j] != -1)){
                        let tempSim = sim(i, k);

                        if(tempSim > threshold){
                            let obj = {pos: k, sim: tempSim};
                            sims.push(obj);
                        }
                    }
                }
                sims = getNeighbors(sims);
                tempRow.push({name: movies[j], score: pred(j, sims, average_ratings[i])});
            }
        }
        tempRow = processPredictions(tempRow);
        recommendedMovies[users[i]] = tempRow;
    }

    return recommendedMovies;
}

function processPredictions(predictions){
    predictions.sort(function (a, b) {
        return (b.score - a.score);
    });

    let result = [];
    for(let i = 0; i < 20; i++){
        result.push(predictions[i].name);
    }
    return result;
}

//Get Neighbors
function getNeighbors(sims){
    sims.sort(function (a, b) {
        return (b.sim - a.sim);
    });

    sims = sims.slice(0, numNeighbors);
    return sims;
}

//Initial functions
function getUsers(data) {
    let users = [];
    for(let i = 0; i < data.length - 1; i++){
        users.push(Number(data[i]))
    }
    return users;
}

function getMovies(data){
    return data.slice(0, data.length -1);
}

function getRatings(data) {
    let ratings = [];
    let average_ratings = [];

    for(let i = 0; i < data.length; i++){
        let sum = 0;
        let cnt = 0;
        let row = [];
        
        let tempRow = data[i].split(' ');
        for(let j = 0; j < tempRow.length; j++){
            rate = Number(tempRow[j]);
            row.push(rate)
            if(rate != -1){
                sum += rate;
                cnt ++;
            }
        }

        ratings.push(row);
        average_ratings.push(sum/cnt);
    }

    return [ratings, average_ratings];
}