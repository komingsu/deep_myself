def count_dense_plot(dataframe, tg):
    import pandas as pd
    import matplotlib.pyplot as plt
    df = dataframe.copy()
    target = tg
    
    for i in df.columns:
        if (df[i].dtype == "int64" or df[i].dtype == "float64"):
            df = df.drop([i], axis=1)
    
    df_target = df[[target]].copy()
    df = df.drop([target], axis=1)
    df_length = len(df.columns)
    df = pd.concat([df, df_target], axis=1)
    df["id"] = 1
    for i in df.columns[:df_length]:
        temp = df.groupby([i, target])["id"].count().unstack().T.copy()
        temp = temp/df[i].value_counts()
        bc = temp.T.plot.bar(rot=0, xlabel=f"{i}")