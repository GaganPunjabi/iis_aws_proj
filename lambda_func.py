from io import StringIO , BytesIO   
import boto3
import pandas as pd
from urllib.parse import unquote_plus



def lambda_handler(event, context):
    """Read file from s3 on trigger."""
    s3 = boto3.client("s3")
    output_bucketname = "output123123"
    if event:
        file_obj = event["Records"][0]
        bucketname = str(file_obj["s3"]["bucket"]["name"])
        filename = unquote_plus(str(file_obj["s3"]["object"]["key"]))
        fileObj = s3.get_object(Bucket=bucketname, Key=filename)
        df = pd.read_csv(fileObj['Body'], sep=',')
        df.rename(columns={"Direction": "Category"}, inplace=True)
        df_filtered = df[~ df['Category'].isin(["Imports", "Exports"])]
        df_filtered['Current_Match'] = pd.to_datetime(df_filtered['Current_Match'])
        df_filtered = df_filtered.sort_values(by="Current_Match")
        csv_buffer = StringIO()
        df_filtered.to_csv(csv_buffer, sep=',', encoding='utf-8', index=False)
        buffer_to_upload = BytesIO(csv_buffer.getvalue().encode())
        s3.put_object(Body=buffer_to_upload, Bucket=output_bucketname, Key=(filename.split('.csv')[0] + '_output.csv'))



        print(df_filtered.groupby('Country').Value.agg('sum'))
        print(df_filtered.groupby('Commodity').Value.agg('mean'))