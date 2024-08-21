import pandas as pd
import numpy as np
import torch
from torch.autograd import variable
from tqdm import tqdm_notebook as tqdm
from torch.utils.data.dataset import Dataset
from torch.utils.data import DataLoader 
from sklearn.cluster import KMeans



class user():
    def __init__(self, user_id):
        self.user_id = user_id

    def recommend(self, sets, product_id, timing):
        if timing > 1:
            for i in range(len(sets)):
                for j in range(len(sets[0])):
                    if product_id == sets[i][j]:
                        return sets[i]
        return 