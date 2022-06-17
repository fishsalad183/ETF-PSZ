import math
import typing
import numpy as np
import pandas as pd
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
        ret = []
        
        for i_test, row in xtest.iterrows():
            distances = self._compute_distances(row)
        
            # vote
            votes = {}
            for ind, _ in sorted(distances.items(), key=lambda x: x[1])[:self._k]:
                yclass = self._ytrain[ind]
                votes[yclass] = votes.get(yclass, 0) + 1
            predicted_class = max(votes, key=votes.get)

            ret.append(predicted_class)
        
        return ret
    
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