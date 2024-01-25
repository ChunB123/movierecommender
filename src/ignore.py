import numpy as np
import pandas as pd
from libreco.data import random_split, DatasetPure
from libreco.data import DatasetFeat

def main():
    data = pd.read_csv("/home/tyang30/data/movielens.csv")
    data = data.iloc[:, 1:] 
    data.columns = ["user","item","label","time","sex","age","occupation","genre1","genre2","genre3"]
    train_data, eval_data, test_data = random_split(data=data, multi_ratios=[0.8, 0.1, 0.1], seed=42)
    
    sparse_col = ["sex", "occupation", "genre1", "genre2", "genre3"]
    dense_col = ["age"]
    user_col = ["sex", "age", "occupation"]
    item_col = ["genre1", "genre2", "genre3"]
    
    train_data, data_info = DatasetFeat.build_trainset(train_data, user_col, item_col, sparse_col, dense_col)
    eval_data = DatasetFeat.build_evalset(eval_data)
    test_data = DatasetFeat.build_testset(test_data)
    print(train_data)  
#     model = WideDeep(
#         task="rating",
#         data_info=data_info,
#         loss_type="cross_entropy",
#         embed_size=16,
#         n_epochs=10,
#         lr=1e-3,
#         batch_size=2048,
#         num_neg=1,
#     )
    
#     model.fit(
#     train_data,
#     neg_sampling=False, #for rating, this param is false else True
#     verbose=2,
#     eval_data=eval_data,
#     metrics=["loss"],
# )

# # do final evaluation on test data
#     evaluate(
#         model=ncf,
#         data=test_data,
#         neg_sampling=False,
#         metrics=["loss"],
#     )
#     ncf.save("/home/tyang30/model", model_name="NCF")
if __name__ == "__main__":
    main()

