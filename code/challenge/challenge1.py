# -*- coding: utf-8 -*-

# http://www.pythonchallenge.com/pc/def/map.html

import string

def mai():
    alist = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj"
    # str_new = ""
    # for i in alist:
    #     i = chr(ord(i)+2)
    #     str_new = str_new+i
    # str_new_new = str_new.replace("\"", " ")
    # str_new_new1 = str_new_new.replace("{", "a")
    # str_new_new2 = str_new_new1.replace("|", "m")
    # str_new_new3 = str_new_new2.replace("0",".")
    # print str_new_new3

    mapping=str.maketrans(string.ascii_lowercase,string.ascii_lowercase[2:]+string.ascii_lowercase[:2])
    blist = alist.translate(mapping)
    print(blist)
    str_url = "map"
    new_url = str_url.translate(mapping)
    print(new_url)

if __name__ == '__main__':
    mai()