#! /usr/bin/python
import cgi, cgitb
cgitb.enable()

def makeFile():
    print "Content-type: text/html\n<html><body>"
    form =cgi.FieldStorage()
    if "threadName" in form and "category" in form:
        f = open("Saved_Threads/%s/%s.txt"%(form.getvalue("category"), form.getvalue("threadName")), "w")
        f.write("hi")
        f.close()
    print "</body></html>"
makeFile()
