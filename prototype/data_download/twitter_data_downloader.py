# based on https://developer.twitter.com/en/docs/tutorials/analyze-past-conversations
import json

import pytz
import requests
import app_config as cfg
import time
from datetime import datetime, timedelta
import os
import logging as log
import random
import tsmp_decorators

"""
 Step 1: Identify which past conversation you wish to study
   I wish to study conversations related to: Dow Jones most important companies
   How to build a query?
   https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-rule
"""

"""
 Step 2: Authenticate and connect to the recent search endpoint to receive Tweets
   Recent reach endpoint:
   https://developer.twitter.com/en/docs/twitter-api/tweets/search/introduction
   https://developer.twitter.com/en/docs/twitter-api/tweets/search/quick-start
   https://github.com/twitterdev/Twitter-API-v2-sample-code
   https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/master/
   ...Recent-Search/recent_search.py
   https://github.com/twitterdev/search-tweets-python

   Query elements:
       https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/
       ...build-a-rule
       limitations:
           - max 512 characters
           - all operators can be negated, negated operators cannot be used alone
           - negation of each individual operator is recommended
           - twitter does not distinguish between cases in search (capital letters)
       operators:
           - logical: {AND|OR|NOT}
               * space between operators means AND i.e. >snow day #NoSchool<
               * OR i e. >grumpy OR cat OR #meme<
               * "-" means NOT i.e. >cat #meme -grumpy<
               * parentheses can be used to group operators >(grumpy cat) OR (#meme has:images)<
           - standalone:
               * keyword
               * emoji
               * "exact phrase match"
               * #
               * @
               * from:
               * to:
               * url:
               * retweets_of:
               * context:
               * entity:
               * conversation_id:
           - non-standalone
               * is: {retweet|quote|verified}
               * has: {hashtag|links|mentions|media|images|videos}
               * lang: {pl|en|...}
   Optional query parameters:
       https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent
       CSL - comma-separated list
       * end_time UTC date YYYY-MM-DDTHH:mm:ssZ (ISO 8601 / RFC 3339), 30s as default
       * expansions as enum CSL (attachments.poll_ids, attachments.media_keys, author_id, entities.mentions.username,
                             geo.place_id, in_reply_to_user_id, referenced_tweets.id, referenced_tweets.id.author_id)
       * max_results as integer 10-100
       * media.fields as enum CSL (duration_ms, height, media_key, preview_image_url, type, url, width,
                                   public_metrics, non_public_metrics, organic_metrics, promoted_metrics)
       * next_token string (pulled directly from response provided by the API)
       * place.fields as enum CSL (contained_within, country, country_code, full_name, geo, id, name, place_type)
       * poll.fields as enum CSL (duration_minutes, end_datetime, id, options, voting_status)
       * since_id string (return results with TweetID greater than given, start_time would be ignored)
       * start_time date YYYY-MM-DDTHH:mm:ssZ (ISO 8601 / RFC 3339), up to 7 days ago as default
       * tweet.fields as enum CSL (attachments, author_id, context_annotations, conversation_id, created_at, entities,
                                   geo, id, in_reply_to_user_id, lang, non_public_metrics, public_metrics,
                                   organic_metrics, promoted_metrics, possibly_sensitive, referenced_tweets,
                                   reply_settings, source, text, withheld)
       * until_id string (return results with TweetID less than given)
       * user.fields as enum CSL (created_at, description, entities, id, location, name, pinned_tweet_id,
                                  profile_image_url, protected, public_metrics, url, username, verified, withheld)

   curl "https://api.twitter.com/2/tweets/search/recent?query=python&max_results=10&tweet.fields=created_at,
         lang,conversation_id" -H "Authorization: Bearer $BEARER_TOKEN"

"""


def auth():
    return cfg.BEARER_TOKEN


def create_default_query(company):
    query: str = company.get('twitter_queries')[0]
    query += ' -is:quote'
    query += ' -is:retweet lang:en'
    # query += ' -is:retweet is:verified lang:en'
    return query


def create_default_url(query: str, max_results=cfg.MAX_TWITTER_RESULTS, start_time_iso=None,
                       end_time_iso=None, next_token=None):
    """
     * end_time UTC date YYYY-MM-DDTHH:mm:ssZ (ISO 8601 / RFC 3339), 30s as default
     * expansions as enum CSL (attachments.poll_ids, attachments.media_keys, author_id, entities.mentions.username,
                               geo.place_id, in_reply_to_user_id, referenced_tweets.id, referenced_tweets.id.author_id)
     * max_results as integer 10-100
     * media.fields as enum CSL (duration_ms, height, media_key, preview_image_url, type, url, width,
                                 public_metrics, non_public_metrics, organic_metrics, promoted_metrics)
     * next_token string (pulled directly from response provided by the API)
     * place.fields as enum CSL (contained_within, country, country_code, full_name, geo, id, name, place_type)
     * poll.fields as enum CSL (duration_minutes, end_datetime, id, options, voting_status)
     * since_id string (return results with TweetID greater than given, start_time would be ignored)
     * start_time date YYYY-MM-DDTHH:mm:ssZ (ISO 8601 / RFC 3339), up to 7 days ago as default
     * tweet.fields as enum CSL (attachments, author_id, context_annotations, conversation_id, created_at, entities,
                                 geo, id, in_reply_to_user_id, lang, non_public_metrics, public_metrics,
                                 organic_metrics, promoted_metrics, possibly_sensitive, referenced_tweets,
                                 reply_settings, source, text, withheld)
     * until_id string (return results with TweetID less than given)
     * user.fields as enum CSL (created_at, description, entities, id, location, name, pinned_tweet_id,
                                profile_image_url, protected, public_metrics, url, username, verified, withheld)
    """
    expansions = 'expansions=attachments.poll_ids,attachments.media_keys,author_id,' \
                 'entities.mentions.username,geo.place_id,in_reply_to_user_id,' \
                 'referenced_tweets.id,referenced_tweets.id.author_id'
    media_fields = 'media.fields=duration_ms,height,media_key,preview_image_url,type,' \
                   'url,width,public_metrics'
    place_fields = 'place.fields=contained_within,country,country_code,full_name,geo,id,' \
                   'name,place_type'
    poll_fields = 'poll.fields=duration_minutes,end_datetime,id,options,voting_status'
    tweet_fields = 'tweet.fields=attachments,author_id,context_annotations,conversation_id,' \
                   'created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,' \
                   'possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld'
    user_fields = 'user.fields=created_at,description,entities,id,location,name,' \
                  'pinned_tweet_id,profile_image_url,protected,public_metrics,url,' \
                  'username,verified,withheld'

    url = f'https://api.twitter.com/2/tweets/search/recent?query={query}&{expansions}&{media_fields}' \
          f'&{place_fields}&{poll_fields}&{tweet_fields}&{user_fields}&max_results={max_results}'

    if start_time_iso is not None:
        url += f'&start_time={start_time_iso}'

    if end_time_iso is not None:
        url += f'&end_time={end_time_iso}'

    if next_token is not None:
        url += f'&next_token={next_token}'
    log.info(f'Url length = {len(url)}, query length = {len(query)}')

    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)

    log.info(f'status_code: {response.status_code}')
    if response.status_code != 200:
        log.warning(f'Request returned an error: status code:{response.status_code}, {response.text}')
        raise Exception(response.status_code, response.text)

    return response.json()


def generate_random_date_times(start_time, end_time):
    date_times = [start_time.strftime(cfg.DATE_TIME_STRING_FORMAT)]
    date_time = start_time
    max_end_time = end_time - timedelta(seconds=12)
    while date_time < end_time:
        date_time += timedelta(minutes=12)
        generated_date_time = date_time + timedelta(
            seconds=random.randint(-1 * cfg.RANDOM_TIME_SPAN_MAX, cfg.RANDOM_TIME_SPAN_MAX))
        if generated_date_time > max_end_time:
            generated_date_time = max_end_time
        date_times.append(generated_date_time.strftime(cfg.DATE_TIME_STRING_FORMAT))
    log.info(f'Generated list of time periods to be checked: {date_times}')
    return date_times


def is_stock_market_open(time_to_be_checked):
    if type(time_to_be_checked) == str:
        tmp_time = datetime.strptime(time_to_be_checked, cfg.DATE_TIME_STRING_FORMAT)
        utc_time = pytz.utc.localize(tmp_time)
    else:
        utc_time = time_to_be_checked

    est_time = utc_time.astimezone(pytz.timezone("America/New_York"))
    weekday = est_time.weekday()
    if (9 <= est_time.hour <= 16) and weekday < 5:
        log.info(f'Day: {weekday}, Time: {time_to_be_checked} == {est_time} EST is inside or near stock market '
                 f'opening hours')
        return True
    log.info(f'Day: {weekday}, Time: {time_to_be_checked} == {est_time} EST is outside stock market opening hours')
    return False


# @tsmp_decorators.time_it
def download_tweets_for_company(key, company_data, limit_tweets=cfg.MAX_TWITTER_RESULTS, start_time_iso=None,
                                end_time_iso=None):
    company_name = company_data.get('company_name')
    log.info(f'Company name: {company_name}, stock code: {key}')

    query = create_default_query(company_data)
    log.info(f'Twitter api query={query}')

    url = create_default_url(query, max_results=limit_tweets, start_time_iso=start_time_iso, end_time_iso=end_time_iso)
    log.info(f'Twitter api url = {url}')

    bearer_token = auth()
    headers = create_headers(bearer_token)
    log.info(f'Twitter api headers={headers}')

    next_token = 'First run'
    sleep_count = 0
    page_count = 0
    downloaded_tweets = 0

    while downloaded_tweets < limit_tweets and next_token is not None:
        try:
            json_response = connect_to_endpoint(url, headers)

        except Exception as error:
            log.warning(error)

            if sleep_count > 15:
                log.warning('Very long waiting... going to next company')
                break

            if error.args[0] == 429:
                sleep_time = 120

            else:
                sleep_time = 2

            log.warning(f'Error {error.args[0]}')
            log.warning(f'Waiting {sleep_time} seconds')
            time.sleep(sleep_time)

            sleep_count += 1
            continue

        sleep_count = 0

        if "result_count" not in json_response.get("meta"):
            log.warning(f'broken response?? no result_count - stopping queries for company {key}')
            break

        results_count = json_response.get("meta").get("result_count")
        if results_count == 0:
            log.info(f'results_count == 0: stopping queries for company {key}')
            break

        milliseconds = int(round(time.time() * 1000))
        log.info(milliseconds)

        page_count += 1
        file_name = f'{cfg.JSON_FILES_LOCATION}tweets_{key}_page{page_count}_{milliseconds}.json'
        with open(file_name, "w") as write_file:
            json.dump(json_response, write_file, indent=4, sort_keys=True)
            log.info(f'File saved as: {os.path.realpath(write_file.name)}')

            downloaded_tweets += results_count
            log.info(f'result_count: {results_count}')
            log.info(f'newest_id: {json_response.get("meta").get("newest_id")}')
            log.info(f'oldest_id: {json_response.get("meta").get("oldest_id")}')

            if "next_token" not in json_response.get("meta"):
                log.info(f'no next_token - finished queries for company {key}')
                break
            else:
                next_token = json_response.get("meta").get("next_token")
                log.info(f'next_token: {next_token}')
                url = create_default_url(query, max_results=limit_tweets, next_token=next_token,
                                         start_time_iso=start_time_iso, end_time_iso=end_time_iso)

    return downloaded_tweets


# @tsmp_decorators.time_it
def twitter_data_download(companies_dict):
    # initialize log file
    milliseconds = int(round(time.time() * 1000))
    utc_now = pytz.utc.localize(datetime.utcnow())
    week_ago_utc = (utc_now - timedelta(days=7))
    utc_now = utc_now - timedelta(seconds=11)

    log.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename=f'{cfg.JSON_FILES_LOCATION}twitter_data_downloader_{milliseconds}.log',
                    level=log.DEBUG)
    log.info('Twitter data downloader started...')
    log.info(f'Number of companies: {len(companies_dict)}')

    no_downloaded_tweets = 0

    for key in sorted(companies_dict, reverse=True):

        time_marks = generate_random_date_times(week_ago_utc, utc_now)
        log.info(f'Length of time_marks tab: {len(time_marks)}')
        company_data = companies_dict.get(key)
        company_tweets = 0
        for i in range(0, len(time_marks) - 1):
            time_span_start = time_marks[i]
            time_span_end = time_marks[i + 1]
            if is_stock_market_open(time_span_start):
                result = download_tweets_for_company( \
                    key, company_data, cfg.MAX_TWITTER_RESULTS_HIGH_TIME, time_span_start, time_span_end)
                log.info(f'download_tweets_for_company called with parameters: key:{key}, '
                         f'max_results: {cfg.MAX_TWITTER_RESULTS_HIGH_TIME}, start: {time_span_start}, '
                         f'end: {time_span_end}')
            else:
                result = download_tweets_for_company(key, company_data, cfg.MAX_TWITTER_RESULTS, time_span_start,
                                                     time_span_end)
                log.info(f'download_tweets_for_company called with parameters: key:{key}, '
                         f'max_results: {cfg.MAX_TWITTER_RESULTS}, start: {time_span_start}, end: {time_span_end}')
            no_downloaded_tweets += result
            company_tweets = 0
        log.info(f'Data downloading for {key} finished: {company_tweets} tweets were downloaded, '
                 f'for all companies: {no_downloaded_tweets}')
    log.info(f'Data downloading finished. {no_downloaded_tweets} tweets downloaded')


if __name__ == '__main__':
    twitter_data_download(cfg.example_sp500_companies)

# Step 3: Analyzing the data for past conversations
#
