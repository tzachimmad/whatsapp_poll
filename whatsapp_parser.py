# -*- coding: utf-8 -*-

from collections import defaultdict
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

friend_only = {"יבוא", "יגיע"}
first_msg_friend_associated = {"מביא"}
me_only = {"אבוא", "אגיע", "אהיה"}
agnostic = {"בא", "מגיע"}
no_words = {"לא"," מי ", "מישהו"}
separators = {",", "."}
first_msg_words = {"אבוא", "אגיע", "אהיה", "בא", "מגיע"}

def get_pos (hey, needles):
    for needle in needles:
        if needle in hey:
            return hey.find(needle)
    return -1

def friend_analysis (msg):
    friend_pos = msg.find("חבר")
    if friend_pos>-1:
        bring_pos = msg[:friend_pos].find("מביא")
        if (bring_pos>-1):
            no_pos= get_pos(msg[:bring_pos],no_words)
            if no_pos == -1:
                return [1,0]
    return analyze_post(msg, friend_only)

def analyze_post (msg,needles):
    for needle in needles:
        come_pos = msg.find(needle)
        if come_pos == -1:
            continue
        no_pos = get_pos(msg[:come_pos],no_words)
        if no_pos == -1:
            if ("אני") in msg[:come_pos]:
                return [1,0]
            else:
                return [1,1]
        dot_pos = get_pos(msg[:come_pos],separators)
        if dot_pos > no_pos:
            if ("אני") in msg[:come_pos]:
                return [1,0]
            else:
                return [1,1]
        else:
            if ("אני") in msg[:come_pos]:
                return [-1,0]
            else:
                return [-1,1]
    return [0,0]

def comming (output_file, msg):
    tmpA = 0
    tmpB = 0
    come = 0
    friend = 0
    come, tmpB = analyze_post(msg[0], first_msg_words)
    friend, tmpB = friend_analysis(msg[0])
    for post in msg:
        if (post == msg[0]) or ("Air" in post):
            continue
        tmpA , tmpB = analyze_post(post,agnostic)
        if tmpA == 1 and tmpB == 0:
            come =1
        if tmpA == 1 and tmpB == 1:
            friend = 1
        if tmpA == -1:
            if tmpB == 0:
                come = 0
            else:
                friend = 0
        tmpA , tmpB = analyze_post(post,me_only)
        if tmpA:
            come =1
        if tmpA == -1:
            come = 0
        tmpA , tmpB = friend_analysis(post)
        if tmpA:
            friend = 1
        if tmpA == -1:
            friend = 0
    if come == -1:
        come = 0
    if friend == -1:
        friend = 0
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