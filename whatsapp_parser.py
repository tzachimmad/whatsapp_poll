# -*- coding: utf-8 -*-

from collections import defaultdict
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def comming (output_file, msg):
    come = 0
    friend = 0
    for input_post in msg:
    	come = come + input_post.count("emojiordered0911")
    	come = come + input_post.count("7708431d.png")
    	come = come + input_post.count("3599ec59.png")
    	come = come - input_post.count("emojiordered0917")
    	come = come - input_post.count("f7ca681d.png")
    	come = come - input_post.count("289f84cc.png")
    	friend = friend + input_post.count("emojiordered0916")
    	friend = friend + input_post.count("49c7d331.png")
    	friend = friend - input_post.count("emojiordered0922")
    	friend = friend - input_post.count("66dfb6bb.png")
    if come>0:
    	come = 1
  ##      post = input_post.decode("utf-8")
    return come,friend

def print_to_csv(output_file,key,value):
    come,friend = comming(output_file,value)
    output_file.write(str(come))
    output_file.write(",")
    output_file.write(str(friend))
    output_file.write(",")
    output_file.write(key)
    output_file.write(",")
    output_file.write("\n")
    return come,friend

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

def create_csv_file(dico):
    ##dico = defaultdict(list)
    ##fill_dico(dico)
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
    return comma,friends