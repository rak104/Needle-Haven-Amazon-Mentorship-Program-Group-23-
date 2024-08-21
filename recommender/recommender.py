import pandas as pd
import numpy as np
import torch
from torch.autograd import variable
from tqdm import tqdm_notebook as tqdm
from torch.utils.data.dataset import Dataset
from torch.utils.data import DataLoader 
from sklearn.cluster import KMeans
from matrixfiltration import MatrixFactorization
from loader import Loader

class recommender():
    def __init__(self, ratings_df, n_users, n_items,  num_epochs= 128, lr= 1e-3, n_factors= 8):
        self.num_epochs = num_epochs
        self.lr = lr
        self.n_users = n_users
        self.n_items = n_items
        self.n_factors = n_factors

    def clusters(self):
        cuda = torch.cuda.is_available()

        print("Is running on GPU:", cuda)
        
        model = MatrixFactorization(self.n_users, self.n_items, self.n_factors)
        print(model)
        for name, param in model.named_parameters():
            if param.requires_grad:
                print(name, param.data)
        # GPU enable if you have a GPU...
        if cuda:
            model = model.cuda()
        
        # MSE loss
        loss_fn = torch.nn.MSELoss()
        
        # ADAM optimizier
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
        
        # Train data
        train_set = Loader()
        train_loader = DataLoader(train_set, 128, shuffle=True)

        for it in tqdm(range(self.num_epochs)):
            losses = []
            for x, y in train_loader:
                if cuda:
                    x, y = x.cuda(), y.cuda()
                else:
                    x, y = x.cpu(), y.cpu()
                    
                optimizer.zero_grad()
                outputs = model(x)
                loss = loss_fn(outputs.squeeze(), y.type(torch.float32))
                losses.append(loss.item())
                loss.backward()
                optimizer.step()
                
            print("iter #{}".format(it), "Loss:", sum(losses) / len(losses))

        # By training the model, we will have tuned latent factors for movies and users.
        c = 0
        uw = 0
        iw = 0 
        for name, param in model.named_parameters():
            if param.requires_grad:
                print(name, param.data)
                if c == 0:
                  uw = param.data
                  c +=1
                else:
                  iw = param.data
                #print('param_data', param_data)
        
        trained_movie_embeddings = model.item_factors.weight.data.cpu().numpy()
        
        kmeans = KMeans(n_clusters=10, random_state=0).fit(trained_movie_embeddings)

        sets = []
        for cluster in range(10):
          #print("Cluster #{}".format(cluster))
          movs = []
          now = []    
          for movidx in np.where(kmeans.labels_ == cluster)[0]:
            movid = train_set.idx2movieid[movidx]
            rat_count = ratings_df.loc[ratings_df['movieId']==movid].count()[0]
            movs.append((movie_names[movid], rat_count))
          for mov in sorted(movs, key=lambda tup: tup[1], reverse=True)[:10]:
              
            print("\t", mov[0])
            now.append(mov[0])
          sets.append(now)
        return sets  
    