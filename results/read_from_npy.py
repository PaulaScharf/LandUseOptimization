import numpy as np
import pandas as pd

default_directory = "./"

study_area = "2"

resX = np.load("./results/study" + study_area +"/resX.npy", allow_pickle=True)
resF = np.load("./results/study" + study_area +"/resF.npy", allow_pickle=True)

#print(resX[367])
pd.DataFrame(resX[52]).to_csv("./results/study" + study_area + "/sol52.csv")


# pd.DataFrame(res.X[367]).to_csv("./results/study1_367.csv")
