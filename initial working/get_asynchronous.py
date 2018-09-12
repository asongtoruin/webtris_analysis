from datetime import datetime
import asyncio
import json
import os

from aiohttp import ClientSession
import pandas as pd


def create_dataframe(data):
    all_data = []

    for month in data['MonthCollection']:
        df = pd.DataFrame(month['Days'])
        df['Month'] = month['Month']
        df['SiteId'] = month['SiteId']
        df['DateTime'] = pd.to_datetime(df['DayNumber'] + ' ' + df['Month'])
        all_data.append(df)

    return pd.concat(all_data, ignore_index=True)


async def fetch(url, session, params):
    async with session.get(url, params=params) as response:
        print(response.url)
        return await response.json()


async def bound_fetch(sem, url, session, params):
    # Getter function with semaphore.
    async with sem:
        # return await fetch(url, session, params)
        async with session.get(url, params=params) as response:
            print(response.url)
            return await response.json()


async def run(sites):
    url = r'http://webtris.highwaysengland.co.uk/api/v1.0/reports/monthly'
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(50)

    # Create client session that will ensure we don't open new connection
    # per each request.
    async with ClientSession() as session:
        for site in sites:
            params = dict(
                sites=site, start_date=13092008, end_date=10092018,
                page=1, page_size=2000
            )

            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(
                bound_fetch(sem, url, session, params)
            )
            tasks.append(task)

        return await asyncio.gather(*tasks)

print(datetime.now())

sites = (115,668,714,911,1704,2618,3187,3523,3636,4506,4668,4940,5923,
         7097,7106,7107,7110,7111,7118,7119,7124,7125,7126,7127,7130,
         7131,7132,7157,7158,8349,8350,8351,8352,8353,8354,8355,8356,
         8687,8688,8689,8690,8778,8779,8780,8781,8782,8783,8784,8785,
         8786,8787,8788,8789,8790,8791,8792,8793,8794,8795,8796,8797,
         8798,8799,8800,8801,8802,8803,8804,8805,8806,8807,8808,8809,
         8810,8811,8812,8813,8814,8815,8816,8817,8818,8835,8836,8837,
         8838,8841,8842,8843,8844,8845,8846,8847,8848,8849,8850,8860,
         8861,8862,8863,8864,9139,9140,9142,9144,9145,9264,9265,10253,
         10254,10255,10256,14377,14378)

loop = asyncio.get_event_loop()

future = asyncio.ensure_future(run(sites))
results = loop.run_until_complete(future)

for i, res in enumerate(results):
    try:
        create_dataframe(res).to_csv(
            os.path.join('Outputs', 'results_{}.csv'.format(i)), index=False
        )
    except TypeError:
        with open(os.path.join('Outputs', 'ERROR_{}.json'.format(i)), 'w') as f:
            json.dump(res, f, indent=4)


print(datetime.now())