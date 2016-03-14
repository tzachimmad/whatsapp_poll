# -*- coding: utf-8 -*-

from collections import defaultdict
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_pos (hey, needles):
    for needle in needles:
        if needle in hey:
            return hey.find(needle)
    return hey.__len__()


def comming (output_file, msg):
    come = 1
    friend = 0
    if "לא" in msg[0]:
        come = 0
    for post in msg:
        if (post == msg[0]) or ("Air" in post):
            continue
        position = str(post).__len__()
        if "חבר" in post:
            if ("בא" in post) or ("מגיע" in post) or ("מביא" in post):
                friend = 1
                position = get_pos (post, {"בא","מגיע","מביא"})
                if ("לא" in post[:position]) or ( "מישהו" in post[:position]) or ("מי" in post[:position]):
                    friend = 0
        if ("אבוא" in post) or ("אגיע" in post):
            position = get_pos (post, {"אבוא","אגיע"})
            if "לא" not in post[:position]:
                come = 1
            else:
                come = 0
        if ("בא" in post) or ("יגיע" in post) or ("יבוא" in post) or ("מגיע" in post):
            position = get_pos (post, {"בא","יגיע","יבוא","מגיע"})
            if "אני" in post[:position]:
                come = 1
                if "לא" in post[:position]:
                    come = 0
            else:
                friend = 1
                if ("לא" in post[:position]) or ("מי" in post[:position]) or ("מישהו" in post[:position]):
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