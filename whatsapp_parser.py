# -*- coding: utf-8 -*-

from collections import defaultdict
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


## each word is a tuple, if 1 is in front of it, than this word is distinct and cannot be found when 
##incorparated in other word, otherwise this word can be found even when part of other word
friend_only = [(0,"יבוא"), (0,"יגיע"),(0,"ברק ורע"),(0,"באים")]
me_only = [(0,"אבוא"), (0,"אגיע"), (0,"אהיה"),(0,"אבו מחר")]
agnostic = [(1,"בא"), (0,"מגיע"),(0,"להגיע"),]
no_words = [(1,"לא"),(1,"מי"),(0,"בספק"),(0,"מישהו"),(1,"שלא")]
separators = [(0,","), (0,".")]
first_msg_words = [(0,"אבוא"), (0,"אגיע"), (0,"אהיה"), (1,"בא"), (0,"מגיע"),(1,"באא"),(0,"אבו מחר")]
friends_words = [(0,"חבר")]
bringing_friend = [(0,"מביא"),(0,"פלוס")]
delimiters = [(0,","), (0,"."),(0,"?"),(0,"-"),(0,"/")]
me_word = [(1,"אני")]

def isBlank (msg, index):
    this_char = msg[index]
    if ord(this_char)==32:
        return True
    if ord(this_char)==160:
        return True
    for delimiter in delimiters:
        if this_char==delimiter[1]:
            return True
    return False

def get_pos_default(hey, needle):
    if needle in hey:
        return hey.find(needle)
    return -1

def get_pos_distinct(hey, needle):
    if needle in hey:
        pos = hey.find(needle)
        needle_sz = len(needle)
        hey_sz = len(hey)
        if needle_sz == hey_sz:
            return pos
        elif pos == 0:
            if isBlank(hey,needle_sz):
                return pos
        elif (pos + needle_sz) == hey_sz:
            if isBlank(hey,pos-1):
                return pos
        elif isBlank(hey,pos-1) and isBlank(hey,pos + needle_sz):
            return pos
    return -1

def get_pos (hey, needles):
    for input_needle in needles:
        needle = input_needle[1].decode("utf-8")
        pos = 1
        if input_needle[0] == 1:
            pos = get_pos_distinct(hey,needle)
        else:
            pos = get_pos_default(hey,needle)
        if pos != -1:
            return pos
    return -1

def friend_analysis (msg,prev):
    friend_pos = get_pos(msg,friends_words)
    if friend_pos>-1:
        bring_pos = get_pos(msg[:friend_pos],bringing_friend)
        if (bring_pos>-1):
            no_pos= get_pos(msg[:bring_pos],no_words)
            if no_pos == -1:
                return 1
    return analyze_post(msg, friend_only,prev,0)

#Return var1,var2
## var1==1 means comming, var2==1 means friend comming else post owner comming
## var1==-1 means not comming, var2==1 means friend not comming else post owner not comming

def analyze_post (msg,needles,prev,me):
    for needle in needles:
        stam_array = ["סתם"]
        stam_array[0]= needle
        come_pos = get_pos(msg, stam_array)
        if come_pos == -1:
            continue
        no_pos = get_pos(msg[:come_pos],no_words)
        if no_pos == -1:
            if get_pos(msg[:come_pos],me_word)>=0 and me==1:
                return 1
            elif me==0:
                return 1
        dot_pos = get_pos(msg[:come_pos],separators)
        if dot_pos > no_pos:
            if get_pos(msg[:come_pos],me_word)>=0 and me==1:
                return 1
            elif me==0:
                return 1
        else:
            if get_pos(msg[:come_pos],me_word)>=0 and me==1:
                return 0
            elif me==0:
                return 0
    return prev

def comming (output_file, msg):
    come = 0
    friend = 0
    first_msg  = msg[0].decode("utf-8")
    come = analyze_post(first_msg, first_msg_words,come,0)
    friend = friend_analysis(first_msg, friend)
    for input_post in msg:
        post = input_post.decode("utf-8")
        if (post == msg[0]) or ("Air" in post):
            continue
        come =  analyze_post(post,agnostic,come,1)
        friend = analyze_post(post,agnostic,friend,0)
        come = analyze_post(post,me_only,come,1)
        friend = friend_analysis(post,friend)
    output_file.write(str(come))
    output_file.write(",")
    output_file.write(str(friend))
    output_file.write(",")
    return come,friend

def print_to_csv(output_file,key,value):
    coming,friend = comming(output_file,value)
    output_file.write(key)
    output_file.write(",")
    for item in value:
        output_file.write(str(item))
        output_file.write(",")
    output_file.write("\n")
    return coming,friend

def print_header(output_file):
    today = datetime.date.today()
    time = datetime.datetime.now().time()
    minutes = datetime.time.min
    output_file.write("Updated,")
    output_file.write(str(today))
    output_file.write(",")
    output_file.write(str(time))
    output_file.write("\n\n")
    output_file.write("מגיע")
    output_file.write(",")
    output_file.write("מביא חבר")
    output_file.write(",")
    output_file.write("שחקן")
    output_file.write("\n")

def fill_dico(dico):
    print "Enter text please, after finished press enter and then ctrl+d (ctr+z on windows)\n"
    text = sys.stdin.read()
    key = "defult"
    for line in text.splitlines():
        if "]" in line:
            tmp = line.split ("]")
            key_with_msg = tmp[1].split(":")
            key = key_with_msg[0]
            msg = key_with_msg[1]
        else:
            msg = line
        dico[key].append(msg)

def create_csv_file():
    dico = defaultdict(list)
    fill_dico(dico)
    output_file = open("output.csv", 'w')
    print_header(output_file)
    comma = friends = 0
    for item in dico.items():
        cama, haver= print_to_csv(output_file,item[0],item[1])
        comma += cama
        friends += haver
    output_file.write(str(comma)+","+str(friends))
    output_file.close()
    print "Done creating local csv file output.csv "
