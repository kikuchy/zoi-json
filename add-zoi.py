#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import re
import json
import io

ZOI_JSON = "./zoi.json"

class ZoiEntry:
    def __init__(self, dic = None):
        if dic is None:
            dic = {}
            dic.src_url = ""
            dic.word = ""
            dic.image_url = ""
        
        self.src_url = dic.src_url
        self.word = dic.word
        self.image_url = dic.image_url

    def is_correct_entry(self):
        return self.is_src_correct() and self.is_image_correct() and self.is_word_correct()

    def is_image_correct(self):
        return re.match("^https://pbs.twimg.com/media/\w{15}\.(jpg|jpeg|png):large$", self.image_url)

    def is_src_correct(self):
        return re.match("^pic.twitter.com/\w{10}$", self.src_url)

    def is_word_correct(self):
        return self.word != ""

    def is_unique(self, existing_zois = []):
        if len(existing_zois) == 0:
            fp = open(ZOI_JSON, "r")
            existing_zois = json.load(fp)
            fp.close()
        repetitions = [ e for e in existing_zois if e["src"] == self.src_url or e["image"] == self.image_url ]
        return len(repetitions) == 0

    def to_dict(self):
        return {
                "word":     self.word,
                "image":    self.image_url,
                "src":      self.src_url
                }

def wizard(dic):
    entry = ZoiEntry(dic)
    while not entry.is_correct_entry():
        if not entry.is_image_correct():
            entry.image_url = raw_input("URL of zoi image > ")
        if not entry.is_src_correct():
            entry.src_url = raw_input("URL of zoi source tweet > ")
        if not entry.is_word_correct():
            entry.word = raw_input("Brief word expresses zoi image > ")
    return entry

def save_zoi(entry):
    fp = open(ZOI_JSON, "r")
    zois = json.load(fp)
    fp.close()
    zois.append(entry.to_dict())
    fp = open(ZOI_JSON, "w")
    fp.write(json.dumps(zois, indent = 4).decode("unicode_escape").encode("utf8"))
    fp.close()

def main():
    parser = OptionParser()

    parser.add_option("-s", "--src", dest = "src_url", default = "")
    parser.add_option("-w", "--word", dest = "word", default = "")
    parser.add_option("-i", "--image", dest = "image_url", default = "")

    (options, args) = parser.parse_args()

    entry = wizard(options)
    if entry.is_correct_entry() and entry.is_unique():
        save_zoi(entry)
        print "Successfully added new zoi entry: %(word)s" % { "word": entry.word }
        print "Please send pull request to update 'zoi-json' repository."
        print "https://github.com/kikuchy/zoi-json/pulls"
    else:
        print "This zoi is not unique: %(word)s" % { "word": entry.word }

if __name__ == "__main__":
    main()
