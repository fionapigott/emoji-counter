This is a quick python script to count emoji in Tweets. 

The script uses emoji\_dict.py as a list of all of the emoji, there may be some missing.

Usage: Run python emoji\_dict.py to create emoji\_dict.pkl. After emoji\_dict.pkl is created there is no need to run this again, except to update the dictionary.

Then:
cat tweet\_file.json | python find\_emoji.py

The script expects a json payload, one record per line, and counts emoji in the "body" field.

example\_tweet\_ids.txt is a file of ids for Tweet containing emoji. Most of the emoji in emoji\_dict are covered here. Try using twurl to get these Tweets from the public Twitter API.

Credit to http://apps.timwhitlock.info/emoji/tables/unicode and, of course, unicode.org.

Doesn't include skin tone modifiers or new emoji (yet).

Feel free to use/modify. No guarantees of anything.
