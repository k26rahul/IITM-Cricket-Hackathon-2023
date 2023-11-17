import numpy as np
import pandas as pd
from mymodelfile import MyModel

import os

ball_by_ball = pd.read_csv('./Data/IPL_Ball_by_Ball_2008_2022.csv')
matches_result = pd.read_csv('./Data/IPL_Matches_Result_2008_2022.csv')

a_model = MyModel()
a_model.fit([ball_by_ball, matches_result])

files = os.listdir('./FilesUsed')
total_error = 0
for file in files:
    if 'test_file_matchid' in file:
        match_no = file[-6:-4]

        if int(match_no) < 20:
            continue

        X_file_name = './FilesUsed/' + file
        y_file_name = './FilesUsed/' + 'test_file_labels_matchid_' + match_no + '.csv'

        X = pd.read_csv(X_file_name).drop(columns=['Unnamed: 0'])
        y = pd.read_csv(y_file_name)['actual_runs']

        print(match_no, X_file_name, y_file_name)

        y_pred = a_model.predict(X)
        y_real = y.to_numpy().astype(int)

        error = np.abs(y_real - y_pred).sum()
        total_error += error

        print(y_real, y_pred, error, '\n')
        print(pd.DataFrame(list(zip(y_real, y_pred)),
              columns=['Actual', 'Predicted']).to_markdown())

print('total_error:', total_error)
