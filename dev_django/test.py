import requests

url = f'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?fields=avg_interest_rate_amt,%20record_date&filter=record_date:gte:2032-01-01,security_type_desc:eq:Marketable,security_desc:eq:Treasury%20Bills'


response = requests.request("GET", url).json()

print(response['data'] == [])