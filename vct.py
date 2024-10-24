import requests
import json
import gzip
import shutil
import time
import os
from io import BytesIO

S3_BUCKET_URL = "https://vcthackathon-data.s3.us-west-2.amazonaws.com"

# (game-changers, vct-international, vct-challengers)
LEAGUE = "game-changers"

# (2022, 2023, 2024)
YEAR = 2022

def download_gzip_and_write_to_json(file_name, valid_file_name = None):
    if os.path.isfile(f"{file_name}.json"):
        return False

    remote_file = f"{S3_BUCKET_URL}/{file_name}.xml.gz"
    response = requests.get(remote_file, stream=True)

    if response.status_code == 200:
        gzip_bytes = BytesIO(response.content)
        with gzip.GzipFile(fileobj=gzip_bytes, mode="rb") as gzipped_file:
            with open(f"{file_name}.xml", 'wb') as output_file:
                shutil.copyfileobj(gzipped_file, output_file)
            print(file_name, " written")
        return True
    elif response.status_code == 404:
        print("404")
        return False
    else:
        print(response)
        print(f"Failed to download {file_name}")
        return False


def download_esports_files():
    directory = f"fandom"

    if not os.path.exists(directory):
        os.makedirs(directory)

    esports_data_files = ["valorant_esports_pages", "valorant_pages"]
    for file_name in esports_data_files:
        download_gzip_and_write_to_json(f"{directory}/{file_name}")


if __name__ == "__main__":
    download_esports_files()