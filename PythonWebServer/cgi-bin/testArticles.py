#! /usr/bin/python
import cgi, cgitb
cgitb.enable()
import os

HTML_HEADER = "Content-type: text/html\n\n<html>\n<body>\n"

def main():
    path = "C:/Users/annca/Desktop/PythonWebServer/cgi-bin/articles/"
    s = ""
    for filename in os.listdir(path):
        f = open(path + filename, "rU")
        s += f.read() + "\n<br>"
        f.close()
    #f = open("C:/Users/annca/Desktop/PythonWebServer/cgi-bin/articles/article1.txt", "rU")
    #s = f.read()
    f.close()
    f = open("C:/Users/annca/Desktop/PythonWebServer/html-stuff/testArticlesHome.html", "rU")
    s2 = f.read()
    f.close()
    #print os.getcwd()
    print (HTML_HEADER + s + s2[s2.rindex("<body>")::])

main()
