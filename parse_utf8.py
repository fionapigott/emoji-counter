import fileinput
import ujson as json
import pickle
from collections import defaultdict

#unicode_markers = {'\xc2':2, '\xe2':3, '\xe3':3, '\xf0':4}
emoji_dict = pickle.load(open("emoji_dict_2.pkl","r"))
unicode_markers = pickle.load(open("unicode_markers.pkl","r"))

# Initialize counters and results dicts
used_emojis = defaultdict(int)
tweets_with_this_emoji = defaultdict(int)
total_emoji_used = 0
total_tweets_with_emoji = 0
total_tweets = 0
emoji_per_tweet = defaultdict(int)

# Count things!
for line in fileinput.FileInput():
    try:
        body = json.loads(line)["body"].encode('utf-8')
    except (ValueError, KeyError):
        continue
    body_chars = [] 
    i = 0
    len_body = len(body)
    while i < len_body:
        byte = body[i]
        if byte in unicode_markers:
            body_chars.append(body[i:i+unicode_markers[byte]])
            i = i+unicode_markers[byte]
        else:
            body_chars.append(byte)
            i = i+1
    j = 0
    emoji_in_tweet = []
    len_body_chars = len(body_chars)
    while j < len_body_chars:
        char = body_chars[j]
        start_byte = char[0]
        # if it's an emoji and it's in the dict
        if char in emoji_dict:
            # set emoji_found to the character we just read
            emoji_found = char
            # get the info from the emoji dict
            char_info = emoji_dict[char]
            look_for_modifiers = char_info["look_for_modifiers"]
            found_a_modifier = False
            # see if it has modifiers around it so we can count both chars as one
            if look_for_modifiers:
                modifiers_possible_before = char_info["modifiers_possible_before"]
                modifiers_possible_after = char_info["modifiers_possible_after"]
                # check for after modifiers
                if (j != len_body_chars - 1) and len(modifiers_possible_after) > 0:
                    if body_chars[j+1] in modifiers_possible_after:
                        emoji_found = char + body_chars[j+1]
                        # Debugging
                        #print char, [char]
                        #print body_chars[j+1], [body_chars[j+1]]
                        #print emoji_found
                        #print "***************"
                        j += 1 # skip the next character because we found it
                        look_for_modifiers = False
                        found_a_modifier = True
                # check for before modifiers
                if (j != 0) and look_for_modifiers and len(modifiers_possible_before) > 0:
                    if body_chars[j-1] in modifiers_possible_before:
                        emoji_found = body_chars[j-1] + char
                        found_a_modifier = True
                        # Debugging
                        #print body_chars[j-1], [body_chars[j-1]]
                        #print char, [char]
                        #print emoji_found
                        #print "***************"
            if char_info["can_stand_alone"] or found_a_modifier:    
                emoji_in_tweet.append(emoji_found)
        j += 1
    len_emoji_in_tweet = len(emoji_in_tweet)
    for emoji in emoji_in_tweet:
        used_emojis[emoji] += 1
    for emoji in set(emoji_in_tweet):
        tweets_with_this_emoji[emoji] += 1
    emoji_per_tweet[len_emoji_in_tweet] += 1
    total_emoji_used += len_emoji_in_tweet
    total_tweets_with_emoji += int(bool(len_emoji_in_tweet))
    total_tweets += 1
    
    # Debugging
    if len(emoji_in_tweet) == 0:
        print body
        print body_chars
    #print body
    #for x,y in used_emojis.items():
    #    print x, y
    #print total_emoji_used
    #print total_tweets_with_emoji
    #print total_tweets
    #print "************************************************************"

print "************************************************************"
emoji_table = []
for emoji in used_emojis.keys():
    emoji_table.append([emoji, str(used_emojis[emoji]), str(tweets_with_this_emoji[emoji])])
print "Emoji, utf-8 byte seq, number of appearances (twice in one Tweet = 2), number of Tweets with this emoji (twice in one Tweet = 1)"
for line in sorted(emoji_table, key = lambda x:int(x[1]), reverse = True):
    print line[0] + " , " + str([line[0]]).strip("][").ljust(34," ") + " , " + line[1] + " , " + line[2]
print "\n"
print "Number of emoji X, number of Tweets with X emoji"
for count, num_tweets in sorted(emoji_per_tweet.items()):
    print str(count) + " , " + str(num_tweets)
print '\n'
print "Total emoji used: {}".format(total_emoji_used)
print "Total Tweets with emoji: {}".format(total_tweets_with_emoji)
print "Total Tweets processed: {}".format(total_tweets)
print "Fraction of Tweets with at least one emoji: {}".format(float(total_tweets_with_emoji)/float(total_tweets))
print "************************************************************"

# Debugging/ testing print
#print "************************************************************"
#print "used_emojis"
#for emoji,count in sorted(used_emojis.items(), key = lambda x:x[1], reverse = True)[0:10]:
#    print emoji, count
#print ".\n.\n.\n"
#for emoji,count in sorted(used_emojis.items(), key = lambda x:x[1], reverse = True)[-10:]:
#    print emoji, count
#print "tweets_with_this_emoji"
#for emoji,count in sorted(tweets_with_this_emoji.items(), key = lambda x:x[1], reverse = True)[0:10]:
#    print emoji, count
#print ".\n.\n.\n"
#for emoji,count in sorted(tweets_with_this_emoji.items(), key = lambda x:x[1], reverse = True)[-10:]:
#    print emoji, count
#print "emoji_per_tweet"
#for count, num_tweets in sorted(emoji_per_tweet.items())[0:10]:
#    print count, num_tweets
#print "Total emoji used: {}".format(total_emoji_used)
#print "Total Tweets with emoji: {}".format(total_tweets_with_emoji)
#print "Total Tweets processed: {}".format(total_tweets)
#print "************************************************************"
