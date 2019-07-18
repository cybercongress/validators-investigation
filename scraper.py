import scrapy
import json

class EulerSpider(scrapy.Spider):
    name = "euler"

    start_urls = [
        "http://93.125.26.210:34657/block?height={}".format(i)
        for i in range(2, 3665415) # 0 is prohibited, for 1 there are no validators
    ]

    custom_settings = {
        "CONCURRENT_REQUESTS": 100
    }

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        block_json = json_response["result"]["block"]

        item = {
            "block": int(block_json["header"]["height"]),
            "validators": [commit["validator_address"] for commit in block_json["last_commit"]["precommits"] if commit],
            "summary": json.dumps(json_response)
        }

        return item