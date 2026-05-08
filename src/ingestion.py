import os
import requests
import json

def lambda_handler(event, context):
    user_email = os.environ.get('SEC_EMAIL')
    cik = event.get('cik', '0000320193') 
    
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    
    headers = {
        'User-Agent': f'MyDataProject ({user_email})',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'data.sec.gov'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Contoh: Log nama perusahaan ke CloudWatch
        print(f"Ingestion sukses: {data.get('name')}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Data ingested successfully',
                'company': data.get('name'),
                'ticker': data.get('tickers')[0] if data.get('tickers') else None
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
