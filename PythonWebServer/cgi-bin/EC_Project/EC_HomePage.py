#! /usr/bin/python
import cgi,cgitb
cgitb.enable()
def main():
    form = cgi.FieldStorage()
    print "Content-type: text/html\n"
    if "username" in form:
        #print "<html><body>ERROR</body></html>"
        openHome(form.getvalue("username"))
    else:
        #print "<html><body>hi</body></html>"
        openHome("")
def openHome(username):
    #print "Content-type: text/html"
    html=""
    try:
        f = open("homePage.html","rU")
        html = f.read()
        f.close()
        #print "hi"
        import EC_ProcessFile
        html = html.replace("<!--USERNAME-->","<!--USERNAME-->%s"%(username))
        html = html.replace("<!--INPUT USERNAME-->",'<!--INPUT USERNAME--><input type=hidden name=username value="%s">'%(username))
        #print "hi2"
        d = EC_ProcessFile.makeGameDict().get(username,{})
        maxScore=0.0
        for i in d:
            if d[i]["score"]>maxScore:
                maxScore=d[i]["score"]
        html = html.replace("<!--TOTAL SCORE-->","<!--TOTAL SCORE-->%.1f"%(maxScore))
    except:
        html= "<html><body>ERROR</body></html>"
    print html
main()
