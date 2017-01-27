#! /usr/bin/python

# We'll print these strings at the appropriate time
HTML_HEADER = 'Content-type: text/html\n\n'

Top_HTML = '''
<html><body>
<center><table border="1">
<tr><td><b>The answers...</b></td></tr>
'''

Bottom_HTML = '</center></table></body></html>'

Nothing_Requested = '<tr><td>No answers were requested</td></tr>'

Bad_Arithmetic = '<tr><td>Error: We needed two numbers to work on, and NO DIVIDING BY ZERO!</td></tr>'

Bad_String = '<tr><td>Error: We needed a string for string processing!</td></tr>'


# We need these library modules to retrieve the user's answers
import cgi

# We need this module to debug Python program bugs
import cgitb
cgitb.enable()

def main():

    print HTML_HEADER
    print Top_HTML

    # ask the library function to retrieve all answers and put them
    #   into a dictionary
    form = cgi.FieldStorage()

    if not form.has_key('CheckArithmetic') and not form.has_key('CheckString'):
        # the user hasn't requested either arithmetic or string processing
        print Nothing_Requested
    else:
        if form.has_key('CheckArithmetic'):
            if not ArithmeticQuestionsAreGood(form):
                print Bad_Arithmetic
            else:
                question = 'The question is: '+form['FirstNum'].value+form['Operator'].value+form['SecondNum'].value
                fnum = int(form['FirstNum'].value)
                snum = int(form['SecondNum'].value)
                op = form['Operator'].value
                if op == '-':
                    answer = fnum - snum
                elif op == '+':
                    answer = fnum + snum
                elif op == '*':
                    answer = fnum * snum
                elif op == '/':
                    answer = fnum / snum
                print '<tr><td>'+question+'  The answer is: <b>'+str(answer)+'</b></td></tr>'
        if form.has_key('CheckString'):
            # Did the user provide a string?
            if not form.has_key('TheString'):
                print Bad_String
            else:
                s = form['TheString'].value
                rad = form['RadioString'].value
                if rad == 'Lower':
                    question = 'lower-case'
                    answer = s.lower()
                elif rad == 'Upper':
                    question = 'upper-case'
                    answer = s.upper()
                print '<tr><td>Convert "'+s+'" to '+question+': "'+answer+'"</td></tr>'
    print Bottom_HTML


def ArithmeticQuestionsAreGood(f):
    # Did the user actually provide numeric requests (or is either blank)?
    if not f.has_key('FirstNum') or not f.has_key('SecondNum'):
        return False
    s1=f['FirstNum'].value
    s2=f['SecondNum'].value
    if s1 == '' or s2 == '':
        return False
    # Are they numbers?
    if not s1.isdigit() or not s2.isdigit():
        return False
    op = f['Operator'].value
    num_s = int(s2)
    if num_s == 0 and op == '/':
        return False  # divide by zero?
    return True

# OK, run the main() function...
main()

                
