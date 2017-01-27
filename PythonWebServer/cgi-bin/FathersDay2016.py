import urllib2,random
def main():
    people=["Richard Feynman", "Bill Evans", "Leonhard Euler"]
    print "Welcome to the Inspirational Quote Machine!"
    quotes=main2()
    while True:
        ans = raw_input('''Enter nothing to exit, 0 for a random quote, 1 for a Richard Feynman quote, 2 for a Bill Evans quote, 3 for a Leonhard Euler quote.
''')
        if ans.isdigit() and 0<=int(ans)<=len(people):
            num=int(ans)
            ans=raw_input("Enter a word to randomly insert into your quote. ")
            quote=""
            author=people[num-1]
            if num==0:
                allQuotes=giantQuoteList(quotes)
                quote= allQuotes[random.randint(0,len(allQuotes)-1)]+"\n"
            else:
                quote= editQuotes(quotes,author)[author][random.randint(0,len(quotes[author])-1)]
            #print quote
            newQuote=quote[:quote.find("\n\t - %s"%(author))]
            #print newQuote
            start='"'
            end='"'
            if '"' in newQuote:
                newQuote=newQuote[1:-1]
            newQuote=newQuote.split()
            index=random.randint(0,len(newQuote)-1)
            puncts=""
            if newQuote[index][-1] in "!.?,;:-":
                puncts=newQuote[index][-1]
                newQuote[index]=newQuote[index][:-1]
            if index>0 and newQuote[index-1] in ".?!":
                ans = ans.capitalize()
            newQuote[index]=ans+puncts
            newQuote=start+" ".join(newQuote)+end
            quote= newQuote + quote[quote.rfind("\n\t - "):]
            print quote
        elif ans=="":
            print "Bye!"
            return
        else:
            print "Your input was invalid!"
def giantQuoteList(quotes):
    allQuotes=[]
    for author in quotes.keys():
        for i in range(len(quotes[author])):
            quote=quotes[author][i].replace("\n\t - %s"%(author),"")
            quote='%s \n\t - %s'%(quote,author)
            allQuotes.append(quote)
    return allQuotes
def editQuotes(quotes,author):
    for i in range(len(quotes[author])):
        #print quotes[author][i]
        quotes[author][i]=quotes[author][i].replace("\n\t - %s"%(author),"")
        quotes[author][i]=('%s \n\t - %s'%(quotes[author][i],author))
        #print quotes[author][i]
    return quotes
def main2():
    html=""
    response = urllib2.urlopen("https://www.goodreads.com/author/quotes/1429989.Richard_Feynman")
    html = response.read()
    quotes={}
    quotes["Richard Feynman"] = processQuotes(html)
    #print quotes
    quotes["Bill Evans"]=processBillEvans()
    response = urllib2.urlopen("https://www.goodreads.com/author/quotes/186483.Leonhard_Euler")
    html=response.read()
    quotes["Leonhard Euler"]=processQuotes(html)
    return quotes
def processQuotes(html):
    quoteList=[]
    while html.find('<div class="quoteText">')>0:
       # print html[html.find('<div class="quoteText">'):]
        #print html.find('<div class="quoteText">')
        #print html[html.find('<div class="quoteText">'):].find("&rdquo;")
        quote=html[html.find('<div class="quoteText">')+len('<div class="quoteText">'):]
        quote=quote[:quote.find("&rdquo;")]
        if "&ldquo;" in quote:
            quote=quote[quote.find("&ldquo;")+len("&ldquo;"):]
        quoteList.append(quote)
        html=html[html.find('<div class="quoteText">')+len('<div class="quoteText">'):]
    return quoteList

def processBillEvans():
    html = urllib2.urlopen('http://www.billevanswebpages.com/billquotes.html').read()
    allQuotes=[]
    html=html[html.find("</p>",html.find('<p align="left">')):]
    while html.find("<hr>")>0:
        quote = html[html.find("<hr"):html.find("<hr",html.find("<hr")+3)]
        quote=quote[quote.find("<em>")+len("<em>"):quote.rfind("</em>")]
        if "&quot;" in quote:
            quote=quote[quote.find("&quot;")+len("&quot;"):quote.rfind("&quot;")]
        if ">" in quote:
            quote = quote[quote.find(">")+1:]
        quote=" ".join(quote.split("\n\t"))
        quote=quote.replace("&quot;",'"')
        quote=quote.replace("&#146;","'")
        allQuotes.append(quote)
        html=html[html.find("<hr")+len("<hr"):]
    return allQuotes


main()
