import os
import re
import json
import time
from datetime import datetime

INPUT_JSON_DIR = '../json/'
OUTPUT_JSON_DIR = '../json/merged_json_7/'

if __name__ == '__main__':

    total_begin_time = datetime.now()
    total_tweets = {}
    json_file_paths = {}
    company_code_pattern = "tweets_(.*?)_page"

    for file in os.listdir(INPUT_JSON_DIR):
        if not file.endswith(".json"):
            continue
        company_code = re.search(company_code_pattern, file).group(1)

        if company_code not in json_file_paths:
            json_file_paths[company_code] = []

        json_file_paths[company_code].append(INPUT_JSON_DIR + file)

    for key in json_file_paths.keys():
        print(f'Files to merge with {key} code: {len(json_file_paths[key])}')
        begin_time = datetime.now()

        tweets_about_company = {'data': []}

        for file_path in json_file_paths[key]:
            with open(file_path) as json_file:
                file_data = json.load(json_file)

            tweets_about_company['data'] += file_data['data']

        milliseconds = int(round(time.time() * 1000))
        file_name = f'{OUTPUT_JSON_DIR}tweets_{key}_merged_{milliseconds}.json'
        with open(file_name, "w") as write_file:
            json.dump(tweets_about_company, write_file, indent=4, sort_keys=True)
        total_tweets[key] = len(tweets_about_company["data"])
        print(f'Files merged, {total_tweets[key]} tweets')

        end_time = datetime.now()
        print(f'took {(end_time-begin_time).total_seconds()}s')

    print(f'All files merged, total {sum(total_tweets.values())} tweets')
    total_end_time = datetime.now()
    print(f'whole app took {(total_end_time - total_begin_time).total_seconds()}s')