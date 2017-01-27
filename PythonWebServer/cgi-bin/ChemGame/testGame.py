#! /usr/bin/python
import cgi, cgitb
cgitb.enable()

attackNames={"Water":0,"Earth":1,"Fire":2,"Air":3}
names = ["Korra", "Kyoshi", "Roku", "Aang"]
attacks = ["Water", "Earth", "Fire","Air"]
avatars = {}
def main():
    print '''Content-type: text/html
<html>
<body>
hi
</body>
</html>
'''
