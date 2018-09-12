import pandas as pd
import requests

r = requests.get(r'http://webtris.highwaysengland.co.uk/api/v1.0/sites')

df = pd.DataFrame(r.json()['sites'])
df.to_csv(r'C:\Users\ruszkowskia\Desktop\webTRIS.csv', index=False)
