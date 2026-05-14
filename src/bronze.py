import os
import requests
import json
import boto3

def handler(event, context):
    user_email = os.environ.get('SEC_EMAIL')
    cik_padded = str(cik).zfill(10) 
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_padded}.json"
    
    headers = {
        'User-Agent': f'MyDataProject ({user_email})',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'data.sec.gov'
    }

    try:
        response = requests.get(url, headers=headers)
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
