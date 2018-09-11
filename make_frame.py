import json

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


with open('test.json', 'r') as f:
    data = json.load(f)

all_data = []

for month in data['MonthCollection']:
    df = pd.DataFrame(month['Days'])
    df['Month'] = month['Month']
    df['SiteId'] = month['SiteId']
    all_data.append(df)

all_data = pd.concat(all_data, ignore_index=True)

all_data['DateTime'] = pd.to_datetime(all_data['DayNumber'] + ' ' + all_data['Month'])
all_data['FlowValue'] = pd.to_numeric(all_data['FlowValue'], errors='coerce')

fig, ax = plt.subplots(figsize=(8,6))
all_data.groupby('SiteId').plot.line(x='DateTime', y='FlowValue', ax=ax)

plt.show()
