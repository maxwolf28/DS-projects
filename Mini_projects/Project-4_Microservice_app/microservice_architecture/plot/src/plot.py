import time

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

while True:
    try:
        df = pd.read_csv("logs/metric_log.csv")
    except:
        print("file is no exist")
        continue
    try:
        fig, ax = plt.subplots(figsize=(12,8))
        sns_plot  = sns.histplot(df['absolute_error'], kde=True, color="orange", ax=ax)
        fig.savefig('logs/error_distribution.png')
        del fig
        del df
        time.sleep(0.5)
    except:
        print("error building plot")
            