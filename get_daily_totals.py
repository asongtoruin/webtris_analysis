import json

import requests

stoke_sites = (6810,6811,8419,8420,8421,8422,8423,8424,8425,8426,8438,8994,)
               # 8995,8996,8998,8999,9000,9016,9099,9100,9279,9280,9283,9284)

r = requests.get(r'http://webtris.highwaysengland.co.uk/api/v1.0/reports/monthly',
                 params=dict(
                     sites=','.join(map(str, stoke_sites)),
                     start_date=13092008, end_date=10092018, page=1,
                     page_size=2000)
                 )

response = r.json()

with open('test.json', 'w') as f:
    json.dump(response, f, indent=4)
