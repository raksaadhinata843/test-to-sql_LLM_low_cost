import os
import requests
import json
import boto3
import time

def get_all_ciks():
    ticker_url = "[https://www.sec.gov/files/company_tickers.json](https://www.sec.gov/files/company_tickers.json)"

def handler(event, context):
    user_email = os.environ.get('SEC_EMAIL')
    ciks = get_all_ciks()

    target_ciks = ciks[:10]

    for cik in target_ciks:
        fetch_and_save_to_s3(cik)
        time.sleep(0.1)
    
    headers = {
        'User-Agent': f'RaksaProject ({user_email})',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'data.sec.gov'
    }

    try:
        response = requests.get(ticker_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        print(f"Ingestion sukses: {data.get('name')}")

        s3 = boto3.client('s3')
        bucket_name = 'config-elt-bucket'
        file_name = f"bronze/sec_data_{cik_padded}.json"

        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(data),
            ContentType='application/json'
        )
        
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
