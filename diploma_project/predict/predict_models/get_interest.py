from datetime import datetime
from dateutil.relativedelta import relativedelta

import requests
import pandas as pd

reference_date = (datetime.now() + relativedelta(months=-6)).strftime('%Y-%m-%d')

url = f'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?fields=avg_interest_rate_amt,%20record_date&filter=record_date:gte:{reference_date},security_type_desc:eq:Marketable,security_desc:eq:Treasury%20Bills'
data = requests.get(url).json()
print(data['data'])
df = pd.json_normalize(data['data'])

print(df)