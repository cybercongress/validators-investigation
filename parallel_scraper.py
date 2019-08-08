from celery import Celery
import requests
import json
import subprocess
import os
from tqdm import tqdm
import pandas as pd
from config import *

FILENAME = "/tmp/euler_validators_full.csv"
CHUNK_SIZE = 1000
THREADS = 10

app = Celery('parallel_scraper', broker='redis://')

def first_run():
    client = app.connection().channel().client
    length = client.llen("celery")
    return length == 0

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
        if block_index > LAST_BLOCK:
            return
        if block_index % THREADS != thread:
            continue
        url = "http://{}:{}/block?height={}".format(NODE_HOST, NODE_PORT, block_index)
        try:
            response = requests.get(url).json()
            if "error" in response:
                raise requests.exceptions.ConnectionError()
        except requests.exceptions.ConnectionError:
            block_index -= 1
            break

        block = parse(response)
        blocks.append(block)

    block_index += 1
    blocks_df = pd.DataFrame(blocks)
    write(blocks_df)
    scrape.delay(block_index, thread)

if __name__ == "__main__":
    if first_run():
        print("Filling the empty queue...")
        for thread in range(THREADS):
            scrape.delay(FIRST_BLOCK, thread)
