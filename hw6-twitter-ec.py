#########################################
##### Name: Hiroyuki Makino         #####
##### Uniqname: mhiro               #####
#########################################

from requests_oauthlib import OAuth1
import json
import requests

import secrets as secrets # file that contains your OAuth credentials


CACHE_FILENAME = "twitter_cache.json"
CACHE_DICT = {}

client_key = secrets.TWITTER_API_KEY
client_secret = secrets.TWITTER_API_SECRET
access_token = secrets.TWITTER_ACCESS_TOKEN
access_token_secret = secrets.TWITTER_ACCESS_TOKEN_SECRET

oauth = OAuth1(client_key,
            client_secret=client_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret)

def test_oauth():
    ''' Helper function that returns an HTTP 200 OK response code and a 
    representation of the requesting user if authentication was 
    successful; returns a 401 status code and an error message if 
    not. Only use this method to test if supplied user credentials are 
    valid. Not used to achieve the goal of this assignment.'''

    url = "https://api.twitter.com/1.1/account/verify_credentials.json"
    auth = OAuth1(client_key, client_secret, access_token, access_token_secret)
    authentication_state = requests.get(url, auth=auth).json()
    return authentication_state


def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 


def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params

    AUTOGRADER NOTES: To correctly test this using the autograder, use an underscore ("_") 
    to join your baseurl with the params and all the key-value pairs from params
    E.g., baseurl_key1_value1
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string
    '''
    #TODO Implement function
    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = baseurl + connector + connector.join(param_strings)
    return unique_key

def make_request(baseurl, params):
    '''Make a request to the Web API using the baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param:value pairs
    
    Returns
    -------
    dict
        the data returned from making the request in the form of 
        a dictionary
    '''
    #TODO Implement function
    response = requests.get(baseurl, params=params, auth=oauth)
    ret = json.loads(response.text)
    return ret


def make_request_with_cache(baseurl, hashtag, count):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.

    AUTOGRADER NOTES: To test your use of caching in the autograder, please do the following:
    If the result is in your cache, print "fetching cached data"
    If you request a new result using make_request(), print "making new request"

    Do no include the print statements in your return statement. Just print them as appropriate.
    This, of course, does not ensure that you correctly retrieved that data from your cache, 
    but it will help us to see if you are appropriately attempting to use the cache.
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    hashtag: string
        The hashtag to search for
    count: integer
        The number of results you request from Twitter
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    params ={"q": hashtag.lower(), "count": count}
    unique_key = construct_unique_key(baseurl, params)

    if unique_key in CACHE_DICT.keys():
        print('fetching cached data')
        return CACHE_DICT[unique_key]
    else: 
        print("making new request")
        retrieved_dict = make_request(baseurl, params)
        CACHE_DICT[unique_key] = retrieved_dict
        save_cache(CACHE_DICT)
        return CACHE_DICT[unique_key]


def find_most_common_cooccurring_hashtag(tweet_data, hashtag_to_ignore):
    ''' Finds the hashtag that most commonly co-occurs with the hashtag
    queried in make_request_with_cache().

    Parameters
    ----------
    tweet_data: dict
        Twitter data as a dictionary for a specific query
    hashtag_to_ignore: string
        the same hashtag that is queried in make_request_with_cache() 
        (e.g. "#MarchMadness2021")

    Returns
    -------
    string
        the hashtag that most commonly co-occurs with the hashtag 
        queried in make_request_with_cache()

    '''
    # TODO: Implement function 
    dict_hashtags = dict()
    list_tweets = tweet_data["statuses"]

    for tweet in list_tweets:
        list_hashtags = tweet['entities']['hashtags']
        for hashtag in list_hashtags:
            hashtag_ = '#' + hashtag['text']
            if hashtag_ not in dict_hashtags.keys():
                dict_hashtags[hashtag_] = 1
            else:
                dict_hashtags[hashtag_] += 1
    dict_hashtags.pop(hashtag_to_ignore)

    return max(dict_hashtags, key=dict_hashtags.get)

    ''' Hint: In case you're confused about the hashtag_to_ignore 
    parameter, we want to ignore the hashtag we queried because it would 
    definitely be the most occurring hashtag, and we're trying to find 
    the most commonly co-occurring hashtag with the one we queried (so 
    we're essentially looking for the second most commonly occurring 
    hashtags).'''

def find_top3_most_common_cooccurring_hashtags(tweet_data, hashtag_to_ignore):
    ''' Finds the hashtags that top 3 most commonly co-occurs with the hashtag
    queried in make_request_with_cache().

    Parameters
    ----------
    tweet_data: dict
        Twitter data as a dictionary for a specific query
    hashtag_to_ignore: string
        the same hashtag that is queried in make_request_with_cache() 
        (e.g. "#MarchMadness2021")

    Returns
    -------
    strings
        the hashtags that top 3 most commonly co-occurs with the hashtag 
        queried in make_request_with_cache()

    '''
    # TODO: Implement function 
    dict_hashtags = dict()
    list_tweets = tweet_data["statuses"]

    for tweet in list_tweets:
        list_hashtags = tweet['entities']['hashtags']
        for hashtag in list_hashtags:
            hashtag_ = '#' + hashtag['text'].lower()
            if hashtag_ not in dict_hashtags.keys():
                dict_hashtags[hashtag_] = 1
            else:
                dict_hashtags[hashtag_] += 1
    dict_hashtags.pop(hashtag_to_ignore.lower())
    top3 = sorted(dict_hashtags.items(), key=lambda x:x[1], reverse=True)[:3]
    return top3[0][0] + ", " + top3[1][0] + " and " + top3[2][0]


def find_top10_most_common_cooccurring_words(tweet_data):
    ''' Finds the words that top 10 most commonly co-occurs with the hashtag
    queried in make_request_with_cache().

    Parameters
    ----------
    tweet_data: dict
        Twitter data as a dictionary for a specific query
    hashtag_to_ignore: string
        the same hashtag that is queried in make_request_with_cache() 
        (e.g. "#MarchMadness2021")

    Returns
    -------
    list
        a list of tuples of the words that top 100 most commonly co-occurs with the hashtag 
        and the frequencies
    '''
    # TODO: Implement function 
    dict_words = dict()
    list_tweets = tweet_data["statuses"]

    stopwords_file = open('stopwords.json', 'r')
    stopwords_contents = stopwords_file.read()
    stopwords = json.loads(stopwords_contents)
    stopwords_file.close()

    stopwords.append("rt")

    for tweet in list_tweets:
        list_words = tweet['text'].lower().split()
        for word in list_words:
            if word not in stopwords:
                if word not in dict_words.keys():
                    dict_words[word] = 1
                else:
                    dict_words[word] += 1

    top10 = sorted(dict_words.items(), key=lambda x:x[1], reverse=True)[:10]
    return top10
    

if __name__ == "__main__":

    CACHE_DICT = open_cache()

    if not client_key or not client_secret:
        print("You need to fill in CLIENT_KEY and CLIENT_SECRET in secret_data.py.")
        exit()
    if not access_token or not access_token_secret:
        print("You need to fill in ACCESS_TOKEN and ACCESS_TOKEN_SECRET in secret_data.py.")
        exit()

    baseurl = "https://api.twitter.com/1.1/search/tweets.json"
    count = 100

    while True:
        hashtag = input('Enter a hashtag (e.g., #MarchMadness2021), or "exit" to quit: ')
        if hashtag == 'exit':
            print('Bye!')
            break
        elif hashtag[0] != '#':
            print('Include # at the beginning.')
        else:
            tweet_data = make_request_with_cache(baseurl, hashtag, count)
            if len(tweet_data["statuses"]) == 0:
                print("No results")
            else:
                top3_most_common_cooccurring_hashtags = find_top3_most_common_cooccurring_hashtags(tweet_data, hashtag)
                print()
                print("The top 3 most commonly cooccurring hashtag with {} are {}.".format(hashtag, top3_most_common_cooccurring_hashtags))
                top10_most_common_cooccurring_words = find_top10_most_common_cooccurring_words(tweet_data)
                print()
                print("The top 10 most commonly occurring words are")
                print(top10_most_common_cooccurring_words)

