import fileinput
import pickle
from collections import defaultdict

# Set the encoding that we want the results in:
## utf 8
encoding = "utf-8"
start_byte = 0
start_bytes = ""
# utf 32
#encoding = "utf-32"
#start_byte = 4
#start_bytes = "\xff\xfe\x00\x00"
# ############################################

emoji_dict = defaultdict(list)
emoji_dict_with_info = {}

uid = 0

for line in fileinput.FileInput("emoji_data.txt"):
    # If the line starts with "#", it's a comment:
    if line[0] == "#" and line.strip() != "":
        continue
    # else, it's an emoji
    else:
        code_point_data = [x.strip() for x in line.split("#")[0].split(";")]
    # if it's one of these weird cases, deal with it later:
    # the regional letter indicator range, for one
    if code_point_data in ["1F1E6..1F1FF"]:
        continue
    # parse the range of code points 
    if ".." in code_point_data[0]:
        char_range = code_point_data[0].split("..")
        range_list = [unichr(x) for x in range(int(char_range[0],16), int(char_range[1],16)+1)]
    else:
        try:
            range_list = [unichr(int(code_point_data[0],16))]
        except ValueError:
            # print line
            continue
    # store the emoji
    for emoji in range_list:
        emoji_dict[code_point_data[1]].append(emoji.encode(encoding)[start_byte:])

# You can count however many emoji of whatever type that you like
# But for some reason emoji_dict["Emoji"] incodes some #s, ignore them with len(emoji) > 1
for emoji in set(emoji_dict["Emoji_Presentation"] + emoji_dict["Emoji"]):
    if len((start_bytes + emoji).decode(encoding).encode("utf-8")) > 1:
        emoji_dict_with_info[emoji] = {
                "modifiers_possible_before": [],
                "modifiers_possible_after": [],
                "can_stand_alone": True,
                "look_for_modifiers": False,
                "name": str(uid) 
                }
        #print uid
        uid += 1
# add the modifiers
for emoji in emoji_dict["Emoji_Modifier_Base"]:
    for modifier in emoji_dict["Emoji_Modifier"]:
        try:
            emoji_dict_with_info[emoji]["modifiers_possible_after"].append(modifier)
            emoji_dict_with_info[emoji]["look_for_modifiers"] = True
        # These guys weren't in the original set, ignore them or uncomment and include them
        except KeyError:
            #emoji_dict_with_info[emoji] = {
            #        "modifiers_possible_before": [],
            #        "modifiers_possible_after": [modifier],
            #        "can_stand_alone": True,
            #        "look_for_modifiers": True,
            #        "name": str(uid)
            #        }
            #uid += 1
            pass

# I'm going to add all possible combinations of the regional letter codes (for flags)
#"1F1E6..1F1FF"
flag_range_list = [unichr(x) for x in range(int("1F1E6",16), int("1F1FF",16)+1)]
for letter_1 in flag_range_list:
    emoji_dict_with_info[letter_1.encode(encoding)[start_byte:]] = {
            "modifiers_possible_after": [x.encode(encoding)[start_byte:] for x in flag_range_list],
            "modifiers_possible_before": [],
            "can_stand_alone": False,
            "look_for_modifiers": True,
            "name": str(uid)
            }
    uid += 1

# I'm going to add the "number" + "combining enclosing keycap character"
keycap = "\xe2\x83\xa3"
numbers = ["\x23", "\x30", "\x31", "\x32", "\x33", "\x34", "\x35", "\x36", "\x37", "\x38", "\x39"]
emoji_dict_with_info[keycap.decode("utf-8").encode(encoding)[start_byte:]] = {
        "modifiers_possible_after": [],
        "modifiers_possible_before": [x.decode("utf-8").encode(encoding)[start_byte:] for x in numbers],
        "can_stand_alone": False,
        "look_for_modifiers": True,
        "name": str(uid)
        }

# if the encoding is utf-8, we will need this
if encoding == "utf-8":
    unicode_markers = {}
    for emoji in emoji_dict_with_info:
        if len(emoji) > 1:
            unicode_markers[emoji[0]] = len(emoji)
    pickle.dump(unicode_markers, open("unicode_markers_{}.pkl".format(encoding),"w"))

# Dump the dictionary
pickle.dump(emoji_dict_with_info, open("emoji_dict_{}.pkl".format(encoding),"w"))
print "Dictionary of emoji created at emoji_dict_{}.pkl".format(encoding)
print "Encoding is {}".format(encoding)

# Debugging
## print the entire thing, so you know what you're dealing with
## you could use the ids to selectively not count emoji, or selectively count emoji
#print "emoji, byte string in {}, id, with before modifiers, with after modifiers".format(encoding)
#for emoji in [x[0] for x in sorted(emoji_dict_with_info.items(), key = lambda x: int(x[1]["name"]))]:
#    print((start_bytes + emoji).decode(encoding).encode("utf-8") + " , " + 
#        str([emoji]).strip("][") + " , " +
#        emoji_dict_with_info[emoji]["name"] + " , " + 
#        " ".join([(start_bytes + emoji + m).decode(encoding).encode("utf-8") for m in emoji_dict_with_info[emoji]["modifiers_possible_after"]]) + " , " + 
#        " ".join([(start_bytes + emoji + m).decode(encoding).encode("utf-8") for m in emoji_dict_with_info[emoji]["modifiers_possible_before"]]))

