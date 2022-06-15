import math
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class KNN:
    
    def __init__(self, n_neighbors: int, metric: str) -> None:
        self._k: int = n_neighbors
        match metric:
            case 'euclidian':
                self._distance_metric = KNN.euclidian_distance
            case 'manhattan':
                self._distance_metrci = KNN.manhattan_distance
            case _:
                raise ValueError(f"Unknown metric: {metric}")
        
    def fit(self, xtrain: pd.DataFrame, ytrain: pd.DataFrame):
        self._xtrain = xtrain
        self._ytrain = ytrain
        
    def predict(self, xtest: pd.DataFrame):
        pass    # TODO: implement

    @staticmethod
    def euclidian_distance(vector1, vector2) -> float:
        return math.sqrt(sum((val1 - val2)**2 for val1, val2 in zip(vector1, vector2)))
    
    @staticmethod
    def manhattan_distance(vector1, vector2) -> float:
        return sum(abs(val1 - val2) for val1, val2 in zip(vector1, vector2))

    @staticmethod
    def compute_k(data_count: int) -> int:
        return 2 * math.floor(math.sqrt(data_count) / 2) + 1    # odd integer closest to the square root of the data count