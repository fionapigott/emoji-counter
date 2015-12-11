# Author: Fiona Pigott

import fileinput
# if you can't get ujson to install, try 'import json' (slower, but works)
import ujson as json
import pickle
from collections import defaultdict

# load the pickled emoji dictionary
emoji_dict = pickle.load(open("emoji_dict.pkl","r"))

# parse out the dictionary so that we separate the emoji by byte length. 
# We use the byte length later when checking the emoji strings against the Tweet body
emoji_dict_by_byte = defaultdict(dict)
for emoji in emoji_dict.keys():
    emoji_dict_by_byte[len(emoji)][emoji] = emoji_dict[emoji]
emoji_sets_by_byte = {}
for length in emoji_dict_by_byte.keys():
    emoji_sets_by_byte[length] = set([tuple(s) for s in emoji_dict_by_byte[length].keys()])

# Initialize counters and results dicts
num_tweets_with_emoji = 0
num_tweets = 0
num_emoji_per_tweet = defaultdict(int)
used_emojis = defaultdict(int)
tweets_with_this_emoji = defaultdict(int)

# read in stdin line by line
for line in fileinput.FileInput():
    try:
        num_emoji_in_tweet = 0
        # read in each Tweet and get the 'body' field. 
        # If your Tweets aren't JSON formatted and are just 1 Tweet body/line
        # you could simply use: body = line.encode("utf-8")
        body = json.loads(line)["body"].encode("utf-8")
        # For each possible emoji length
        for length in emoji_sets_by_byte:
            # create a list of all byte sequences of 'length' in the Tweet body
            sequences = zip(*[body[x:] for x in range(0,length)])
            # find the set intersection of the sequences in 'body' and emoji sequences
            intersect_chars = list(emoji_sets_by_byte[length].intersection(sequences))
            # If there is an intersection
            if len(intersect_chars) > 0:
                # tally up how many emoji were in that Tweet
                num_emoji_in_tweet += len(intersect_chars)
                # get how many times each specific emoji was used in this Tweet
                for emoji_tuple in intersect_chars:
                    used_emojis[emoji_tuple] += sequences.count(emoji_tuple)
                    tweets_with_this_emoji[emoji_tuple] += 1
                    #if emoji_tuple == ('\xf0', '\x9f', '\x92', '\xae'): #('\xf0', '\x9f', '\x98', '\x82'):
                    #    print "************************************************"
                    #    print json.loads(line)["body"].strip()#, json.loads(line)["id"]
        # increment the # of Tweets with emoji
        num_tweets_with_emoji += int(num_emoji_in_tweet > 0)
        # tally up how many emoji were in that Tweet
        num_emoji_per_tweet[num_emoji_in_tweet] += 1
        # increment the total # of Tweets that we have read
        num_tweets += 1
    # if the JSON is invalid, pass
    except (KeyError, ValueError):
        pass

# the number of Tweets with no emoji at all
num_emoji_per_tweet[0] = num_tweets - num_tweets_with_emoji

# print results to stdout
print "\n***************** Counts of all emoji ********************** \n"
for emoji_tuple, count in sorted(used_emojis.items(), key = lambda x:x[1], reverse = True):
    print "".join(emoji_tuple) + " , " + str(count)

# print results to stdout
print "\n***************** Counts of Tweets with certain emoji ********************** \n"
for emoji_tuple, count in sorted(tweets_with_this_emoji.items(), key = lambda x:x[1], reverse = True):
    print "".join(emoji_tuple) + " , " + str(count)

print "\n****************** Emoji per Tweet ************************* \n"
print "number_of_emojis_x, count_of_Tweets_with_x_emojis"
for emojis, count in sorted(num_emoji_per_tweet.items(), key = lambda x:x[0], reverse = False):
    print str(emojis) + " , " + str(count)

print "\n***************** Number of Tweets with at least 1 emoji**** \n"
print num_tweets_with_emoji

print "\n***************** Number of Tweets ************************* \n"
print num_tweets

print "\n************************************************************ \n"
