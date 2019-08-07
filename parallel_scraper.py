from celery import Celery
import requests
import json
import subprocess
import os
from tqdm import tqdm
import pandas as pd

FILENAME = "/tmp/euler_validators_full.csv"
CHUNK_SIZE = 1000
THREADS = 10

app = Celery('parallel_scraper', broker='redis://')

def get_start_block():
    os.system("touch {}".format(FILENAME))
    line = subprocess.check_output(['tail', '-1', FILENAME])
    try:
        return int(line.decode("utf-8").split(",")[0]) + 1
    except Exception as e:
        print(e)
        return 2

def parse(json_response):
    block_json = json_response["result"]["block"]
    item = {
        "block": int(block_json["header"]["height"]),
        "validators": [commit["validator_address"] for commit in block_json["last_commit"]["precommits"] if commit],
        "summary": json.dumps(json_response)
    }
    return item

def write(df):
    with open(FILENAME, 'a') as f:
        df.to_csv(f, header=False, index=False)
    
@app.task
def scrape(start_block, thread):
    blocks = []
    for block_index in range(start_block, start_block + CHUNK_SIZE):
        if block_index % THREADS != thread:
            continue
        url = "http://93.125.26.210:34657/block?height={}".format(block_index)
        response = requests.get(url).json()
        if "error" in response:
            block_index -= 1
            break
        block = parse(response)
        blocks.append(block)

    block_index += 1
    blocks_df = pd.DataFrame(blocks)
    write(blocks_df)
    scrape.delay(block_index, thread)

if __name__ == "__main__":
    start_block = get_start_block()
    print(start_block)
    for thread in range(THREADS):
        scrape.delay(start_block, thread)