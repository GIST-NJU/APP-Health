import pandas as pd

df = pd.read_csv("data/release/58job_all_releases.csv")
print(df.head(2))

df=df.drop(df.columns[0],axis=0)
df=df.drop(df.columns[1],axis=0)
df=df.drop(df.columns[2],axis=0)
print(df.head(2))

df.to_csv('data/release/Wechat_all_releases.csv', encoding='utf-8',index=False)
exit()
