import math
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class KNN:
    
    def __init__(self, df: pd.DataFrame) -> None:
        self.k: int = 2 * math.floor(math.sqrt(df.shape[0]) / 2) + 1    # self.k = odd integer closest to the square root of the number of entries
        pass

    def scale(self, df: pd.DataFrame) -> pd.DataFrame:
        scaler = StandardScaler()
        scaler.fit(df.drop('TARGET CLASS', axis=1))
        scaled_features = scaler.transform(df.drop('TARGET CLASS'), axis=1)
        df_feat = pd.DataFrame(scaled_features, columns=df.columns[:-1])
        return df_feat

    def train(self, df: pd.DataFrame):
        X = self.scale(df)
        y = df['TARGET CLASS']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    @staticmethod
    def euclidian_distance(vector1, vector2) -> float:
        return math.sqrt(sum((val1 - val2)**2 for val1, val2 in zip(vector1, vector2)))
    
    @staticmethod
    def manhattan_distance(vector1, vector2) -> float:
        return sum(abs(val1 - val2) for val1, val2 in zip(vector1, vector2))
