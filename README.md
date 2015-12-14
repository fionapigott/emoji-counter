This is a quick python script to count emoji in Tweets. 

Credit to http://apps.timwhitlock.info/emoji/tables/unicode and, of course, unicode.org.

There is also a pretty helpful (for understanding character encodings) Stack Overflow post here: 
http://stackoverflow.com/questions/700187/unicode-utf-ascii-ansi-format-differences

And webpage:
http://csharpindepth.com/Articles/General/Unicode.aspx

I have taken the emoji data from http://www.unicode.org/Public/emoji/2.0/emoji-data.txt (emoji\_data.txt), parsed the modifiers to add skin tone modifiers, and added regional country letter indicators (to detect flags). If this page is updated you should be able to copy it and update the dict.

Run parse\_unicode\_tables.py to create the emoji dictionary that we use to count emoji. Edit the encoding (top of the file) to create a UTF-8 vs UTF-32 encoded dictionary (right now it creates a UTF-8 dictionary). 
The parse\_unicode\_tables.py assigns a unique ID to each emoji in the dict, so that you can chose which characters to count (uncomment print statements at the end to see a table of all of the emoji being recorded and thier modifiers).
The dictionaries are saved as pickled files emoji\_dict\_utf-{8,32}.pkl. Running for UTF-8 will also save unicode\_markers\_utf-8.pkl (a dictionary of marker bytes in utf-8).

Then run:
cat tweet\_fie.json | python parse\_utf8.py (if you created a UTF-8 dict)
Or
cat tweet\_fie.json | python parse\_utf32.py (if you created the UTF-32 dict)

They both do exactly the same thing, just use different inputs and parse the strings differently. No huge speed difference. I've added them both as two examples of solving the problem.

Old version (don't use, this is a very silly way to solve the problem):
find\_emoji.py, emoji\_dict.py

All scripts expect a json payload, one record per line, and count emoji in the "body" field.

example\_tweet\_ids.txt is a file of ids for Tweet containing emoji. Most of the emoji in emoji\_dict are covered here. Try using twurl to get these Tweets from the public Twitter API.

Feel free to use/modify. No guarantees of anything.
