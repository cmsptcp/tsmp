"""
Settings to be used
"""
API_KEY = 'qAUaPBCKrIPjgmBplbqyqAiP4'
API_KEY_SECRET = 'xcaYuwYJe8BVdRkudq25fSBio8BRn0CGX01Yl2VguuGPp1XV6G'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAACjzKAEAAAAA%2FXECVw0prWVtuHzrGWYDgF2MdvQ' \
               '%3DHM5rq9mcW8Dx6ah5do4EiwAohywcime701Z1QZUmH2yNKIaPPZ '
MAX_TWITTER_RESULTS = 20
MAX_TWITTER_RESULTS_HIGH_TIME = 80
TWEETS_TIME_SPANS_PER_HOUR = 5
DATE_TIME_STRING_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
RANDOM_TIME_SPAN_MAX = 240

JSON_FILES_LOCATION = '../json/'

# uwaga: giełda pracuje w określone dni od 9:30-4:00
# warto: 9-16 pobierać więcej tweetów, w pozostałe godziny mniej
# wtedy mamy 7 godzin giełdowych i 15 niegiełdowych
# w giełdowe tweety x5
# w niegiełdowe tweety x1
# 7 * 400 = 2800 (5*80)
# 15 * 100 = 1500 (5*20)


"""
Example companies, data taken from https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
"""
example_sp500_companies = {
    "AMZN": {
        "company_name": "Amazon.com Inc.",
        "gics_sector": "Consumer Discretionary",
        "gics_sub_industry": "Internet & Direct Marketing Retail",
        "keywords": ["$amzn", "amazon"],
        "anti_keywords": ["amazons", "rainforest"],
        "twitter_queries": ["(\"$amzn\" OR amazon OR @jeffbezos OR from:jeffbezos OR from:amazon "
                            "OR context:47.10026792024) -amazons -rainforest"],
        "twitter_people": ["@jeffbezos", "@amazon"],
        "twitter_anti_people": [],
        "context_domain_brand": "47.10026792024",
    },
    "AMD": {
        "company_name": "Advanced Micro Devices Inc",
        "gics_sector": "Information Technology",
        "gics_sub_industry": "Semiconductors",
        "keywords": ["$amd", "amd"],
        "anti_keywords": [],
        "twitter_queries": ["(\"$amd\" OR @lisasu OR from:lisasu OR from:amd OR context:47.10041873034)"],
        "twitter_people": ["@lisasu", "@amd"],
        "twitter_anti_people": [],
        "context_domain_brand": "47.10041873034",
    },
    "INTC": {
        "company_name": "	Intel Corp.",
        "gics_sector": "Information Technology",
        "gics_sub_industry": "Semiconductors",
        "keywords": ["$intc"],
        "anti_keywords": ["intel"],
        "twitter_queries": ["(\"$intc\" OR @bobswan OR @pgelsinger OR @intel OR context:47.10026332285 "
                            "OR from:bobswan OR from:pgelsinger OR from:intel)"],
        "twitter_people": ["@bobswan", "@pgelsinger", "@intel"],
        "twitter_anti_people": [],
        "context_domain_brand": "47.10026332285"
    },
    "MCD": {
        "company_name": "McDonald's Corp.",
        "gics_sector": "Consumer Discretionary",
        "gics_sub_industry": "Restaurants",
        "keywords": ["$mcd", "mcdonald"],
        "anti_keywords": [],
        "twitter_queries": ["(\"$mcd\" OR \"mcdonald's\" OR mcdonalds OR from:mcdonalds OR context:47.10026319212)"],
        "twitter_people": ["@mcdonalds"],
        "twitter_anti_people": [],
        "context_domain_brand": "47.10026319212"
    },
    "MSFT": {
        "company_name": "Microsoft Corp.",
        "gics_sector": "Information Technology",
        "gics_sub_industry": "Systems Software",
        "keywords": ["$msft", "microsoft"],
        "anti_keywords": [],
        "twitter_queries": ["(\"$msft\" OR microsoft OR @billgates OR from:billgates OR from:microsoft "
                            "OR context:47.10027232467)"],
        "twitter_people": ["@billgates", "@microsoft"],
        "twitter_anti_people": [],
        "context_domain_brand": "47.10027232467"
    },
    "NFLX": {
        "company_name": "Netflix Inc.",
        "gics_sector": "Communication Services",
        "gics_sub_industry": "Movies & Entertainment",
        "keywords": ["$nflx", "netflix"],
        "anti_keywords": [],
        "twitter_queries": ["(\"$nflx\" OR netflix OR @reedhastings OR from:reedhastings OR from:netflix "
                            "OR context:47.10026367762)"],
        "twitter_people": ["@reedhastings", "@netflix"],
        "twitter_anti_people": [],
        "context_domain_brand": "47.10026367762"
    },
    "PFE": {
        "company_name": "Pfizer Inc.",
        "gics_sector": "Health Care",
        "gics_sub_industry": "Pharmaceuticals",
        "keywords": ["$PFE", "pfizer"],
        "anti_keywords": [],
        "twitter_queries": ["(\"$pfe\" OR pfizer OR @albertbourla OR from:albertbourla OR from:pfizer "
                            "OR context:47.10032761422)"],
        "twitter_people": ["@albertbourla", "@pfizer"],
        "twitter_anti_people": [],
        "context_domain_brand": "47.10032761422"
    },
    "QCOM": {
        "company_name": "QUALCOMM Inc.",
        "gics_sector": "Information Technology",
        "gics_sub_industry": "Semiconductors",
        "keywords": ["$qcom", "qualcomm", "qualcom"],
        "anti_keywords": [],
        "twitter_queries": ["(\"$qcom\" OR qualcomm OR qualcom OR @cristianoamon OR from:cristianoamon "
                            "OR from:qualcomm OR context:47.10026948815)"],
        "twitter_people": ["@cristianoamon", "@qualcomm"],
        "twitter_anti_people": [],
        "context_domain_brand": "47.10026948815"
    },
    "SBUX": {
        "company_name": "Starbucks Corp.",
        "gics_sector": "Consumer Discretionary",
        "gics_sub_industry": "Restaurants",
        "keywords": ["$sbux", "starbucks"],
        "anti_keywords": [],
        "twitter_queries": ["(\"$sbux\" OR starbucks OR @kevin_johnson OR from:kevin_johnson OR from:starbucks "
                            "OR context:47.10026514830)"],
        "twitter_people": ["@kevin_johnson", "@starbucks"],
        "twitter_anti_people": [],
        "context_domain_brand": "47.10026514830"
    },
    "TSLA": {
        "company_name": "Tesla, Inc.",
        "gics_sector": "Consumer Discretionary",
        "gics_sub_industry": "Automobile Manufacturers",
        "keywords": ["$TSLA", "Tesla", "@elonmusk"],
        "anti_keywords": ["nikola", "nicola", "Nikola Tesla", "Nicola Tesla"],
        "twitter_queries": ["(\"$tsla\" OR tesla OR @elonmusk OR from:elonmusk OR from:tesla"
                            " OR context:47.10044199219) -nikola -nicola -@nictesla"],
        "twitter_people": ["@elonmusk", "@tesla"],
        "twitter_anti_people": ["@nictesla"],
        "context_domain_brand": "47.10044199219"
    }

}
