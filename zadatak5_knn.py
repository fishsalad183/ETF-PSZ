import math
import typing
import numpy as np
import pandas as pd
import time
from sklearn.model_selection import train_test_split

class KNN:
    
    def __init__(self, n_neighbors: int, metric: str) -> None:
        self._k: int = n_neighbors
        match metric:
            case 'euclidean':
                self._distance_metric = KNN.euclidian_distance
            case 'manhattan':
                self._distance_metric = KNN.manhattan_distance
            case _:
                raise ValueError(f"Unknown metric: {metric}")
        
    def fit(self, xtrain: pd.DataFrame, ytrain: pd.Series):
        self._xtrain = xtrain
        self._ytrain = ytrain
        
    def predict(self, xtest: pd.DataFrame) -> list:
        # ret = np.empty(shape=(xtest.shape[0], 2))
        ret = []
        
        for i_test, row in xtest.iterrows():
            # start_time_iteration = time.time()
            
            # distances
            # start_time_dist = time.time()
            distances = self._compute_distances(row)
            # end_time_dist = time.time()
            # print(f"distance computation time: {end_time_dist - start_time_dist}")
        
            # vote
            # start_time_vote = time.time()
            votes = {}
            for ind, _ in sorted(distances.items(), key=lambda x: x[1])[:self._k]:
                yclass = self._ytrain[ind]
                votes[yclass] = votes.get(yclass, 0) + 1
            predicted_class = max(votes, key=votes.get)
            # end_time_vote = time.time()
            # print(f"voting computation time: {end_time_vote - start_time_vote} | predicted class: {predicted_class}")
            
            # np.append(ret, predicted_class)
            ret.append(predicted_class)
            
            # end_time_iteration = time.time()
            # print(f"single iteration time ({i_test}/{xtest.shape[0]}): {end_time_iteration - start_time_iteration}")
        
        return ret
    
    # def predict_single(self, vector: pd.Series):
    #     start_time_dist = time.time()
    #     distances = self._compute_distances(vector)
    #     end_time_dist = time.time()
    #     print(f"distance computation time: {end_time_dist - start_time_dist}")
    
    #     # vote
    #     start_time_vote = time.time()
    #     votes = {}
    #     for ind, _ in sorted(distances.items(), key=lambda x: x[1])[:self._k]:
    #         yclass = self._ytrain[ind]
    #         votes[yclass] = votes.get(yclass, 0) + 1
    #     predicted_class = max(votes, key=votes.get)
    #     end_time_vote = time.time()
    #     print(f"voting computation time: {end_time_vote - start_time_vote} | predicted class: {predicted_class}")
        
    #     return predicted_class
    
    # def _vote(self, distances: typing.Dict[int, float]):
    #     votes = {}
    #     for ind, _ in sorted(distances.items(), key=lambda x: x[1])[:self._k]:
    #         yclass = self._ytrain[ind]
    #         votes[yclass] = votes.get(yclass, 0) + 1
    #     return max(votes, key=votes.get)
    
    def _compute_distances(self, vector) -> typing.Dict[int, float]:
        distances = {}
        for i, row in self._xtrain.iterrows():
            distances[i] = self._distance_metric(vector, row)
        return distances

    @staticmethod
    def euclidian_distance(vector1, vector2) -> float:
        return math.sqrt(sum((val1 - val2)*(val1 - val2) for val1, val2 in zip(vector1, vector2)))
    
    @staticmethod
    def manhattan_distance(vector1, vector2) -> float:
        return sum(abs(val1 - val2) for val1, val2 in zip(vector1, vector2))

    @staticmethod
    def compute_k(data_count: int) -> int:
        return 2 * math.floor(math.sqrt(data_count) / 2) + 1    # odd integer closest to the square root of the data count