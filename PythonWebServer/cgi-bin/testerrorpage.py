import cgi, cgitb, forumUtilities, accountUtilities, linkToForumHome
cgitb.enable()
HTML_HEADER = "Content-type: text/html\n"
HTML_HEADER2 = '''
<html>
<head></head>
<body>
'''
def main():
    try:
        x = 1/0
        import accountUtilities
        accountUtilities.makeUserFile(1) #returns True or False
    except:
        print HTML_HEADER
        print HTML_HEADER2
        print "An unknown error occured!"
        print "</body></html>"
"""def meh():
    thing = [12,23,23,4,23,43]
    for i in range(len(thing)-1,-1,-1):
        print thing[i]"""
main()
