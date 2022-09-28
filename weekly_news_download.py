import os
import argparse
from datetime import datetime
from google.cloud import storage

def upload_to_bucket(blob_name, path_to_file, bucket_name):
    """ Upload data to a bucket"""
    storage_client = storage.Client.from_service_account_json('my-cloud-keys.json')
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)
    return blob.public_url

def download_from_bucket(blob_name, destination_file_name, bucket_name):
    """ Download data from a bucket """
    storage_client = storage.Client.from_service_account_json('my-cloud-keys.json')
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(destination_file_name)
    return blob.public_url

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--currdate', type=str, default=None)
    config = parser.parse_args()

    if config.currdate is None:
        config.currdate = str(datetime.now()).split(' ')[0].strip()
    config.currdate="2022-09-25"

    if not os.path.exists(f"./{config.currdate}"):
        os.makedirs(f"./{config.currdate}")

    files_to_download = [f"news_labelled_{config.currdate}_shortlist.xlsx", f"news_labelled_{config.currdate}_shortlist.xlsx", 
        f"news_labelled_{config.currdate}_masterlist.xlsx", f"news_labelled_{config.currdate}_world_shortlist.xlsx", 
        f"keywords_{config.currdate}.xlsx", f"event_clusters_{config.currdate}.xlsx"]
    for filename in files_to_download:
        result = download_from_bucket(f"{config.currdate}/{filename}", f"{config.currdate}/{filename}", bucket_name="wwf-cmu")
        print(filename, result)