#!/usr/bin/env/python

# PORTS TREE DEBLOBBING SCRIPT
# WTFPL, Jade Levesque

# Right now, it generates functional ports trees based
# on Whitelist/Blacklist & user input.

# TODO: Combine Blacklist and BlacklistI; Deblob local
#       package repositories; Fix rebranding & credit
#       in Makefiles; Fix date & time in Makefiles;
#       Allow for information on art asset licenses
#       for Free Culture trees 

import os
import shutil
from time import *
blacklist = [line.strip() for line in open("Blacklist")]
whitelist = [line.strip() for line in open("Whitelist")]

def deblobapp(grouptitle, app):
    shutil.rmtree("../%s/%s" % (grouptitle, app))
    print "%r Deleted" % app

def writelist(list, app): # adds whitelisted/blacklisted app to list
    open(list, 'a').write("\n"+app)
    print "%r added to %r" % (app, list)

def writelisti(list, app, grouptitle): # adds whitelisted/blacklisted app to list
    open(list, 'a').write("\n"+grouptitle+"/"+app)
    print "%r added to %r" % (app, list)

def writeindex():
    indexold = open("../INDEX", 'r+')
    indexnew = open("../INDEX.temp", 'a')
    listl = open("BlacklistI", 'r').read().splitlines()

    for line in indexold:
        for app in listl:
            if not app in line:
                indexnew.write(line)
    
def checkgroup(group, grouptitle):
    print "==== Checking %s ====" % grouptitle
    make = open("../%s/Makefile.temp" % grouptitle, 'w')
    make.truncate()
    make.close()
    
    make = open("../%s/Makefile.temp" % grouptitle, 'a')
    make.write("# $OpenBSD: Makefile,v 1.0 %s %s humanity Exp $\n\n" % (date, time))
    make.write("     SUBDIR =\n")

    entries = open("../%s/CVS/Entries.temp" % grouptitle, 'w')
    entries.truncate()
    entries.close()

    entries = open("../%s/CVS/Entries.temp" % grouptitle, 'a')
    
    for app in group:
        if app == "Makefile":
            print "Makefile Skipped"
        elif app == "Makefile.temp":
            print "Script Makefile Skipped"
        elif app == "CVS":
            print "CVS Skipped"
        elif app in blacklist:
            print "%s Failed" % app
            deblobapp(grouptitle , app)
        elif app in whitelist:
            print "%s Passed" % app
            make.write("     SUBDIR += %s\n" % app)
            entries.write("D/%s////\n" % app)
        else:
            print "%r Unlisted" % app
            app_free = ""
            while app_free != "f" and app_free != "n" and app_free != "?":
                app_free = raw_input("Is %r free or non-free? [f/n/?]: " % app)
                if app_free == "f":
                    print "%s is free, adding to Whitelist" % app
                    writelist("Whitelist", app)
                    make.write("     SUBDIR += %s\n" % app)
                    entries.write("D/%s////\n" % app)
                elif app_free == "n":
                    print "%s is non-free, adding to Blacklist" % app
                    writelist("Blacklist", app)
                    writelisti("BlacklistI", app, grouptitle)
                    print "%s Failed" % app
                    deblobapp(grouptitle, app)
                elif app_free == "?":
                    print "%s skipped" % app
    make.write("\n.include <bsd.port.subdir.mk>")
    make.close()
    entries.write("/Makefile/1.0/Wed July 8 %s %s//" % (time, timel[0]))
    entries.close()

indexnew = open("../INDEX.temp", 'w')
indexnew.truncate()
indexnew.close()
timel = localtime()
date = "%s/" % timel[0]
if timel[1] < 10:
    date += "0%s/" % timel[1]
else:
    date += "%s/" % timel[1]
if timel[2] < 10:
    date += "0%s" % timel[2]
else:
    date += "%s" % timel[2]
if timel[3] < 10:
    time = "0%s:" % timel[3]
else:
    time = "%s:" % timel[3]
if timel[4] < 10:
    time += "0%s:" % timel[4]
else:
    time += "%s:" % timel[4]
if timel[5] < 10:
    time += "0%s" % timel[5]
else:
    time += "%s" % timel[5]

groups = ["astro", "archivers", "audio", "benchmarks", "biology", "books",
          "cad", "chinese", "comms", "converters", "databases", "devel",
          "editors", "education", "emulators", "fonts", "games", "geo",
          "graphics", "infrastructure", "inputmethods", "japanese", "java",
          "korean", "lang", "mail", "math", "meta", "misc", "multimedia",
          "net", "news", "plan9", "print", "productivity", "security",
          "shells", "sysutils", "telephony", "tests", "textproc", "www",
          "x11"]

for group in groups:
    checkgroup(os.listdir("../%s" % group), "%s" % group)

#ls = os.listdir("./shells")
#tl = "shells"
#checkgroup(ls, tl)

writeindex()

indexnew.close()

print "Success: the ports tree has been deblobbed of all unholy software!"
print "Enjoy Pure Freedom(tm)!"
