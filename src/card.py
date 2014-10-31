from lib.storage import Storage
import cgi


print "Content-type: text/html"

form = cgi.FieldStorage()

box = form.getvalue('box')
s = Storage()
entries = s.retrieve(box, 1)
if entries:
    sample = entries[0]
else:
    sample = 'No entries found.'

print """

<html>
    <head>
        <title>Kanji Flash</title>
        <link rel="stylesheet" type="text/css" href="css/main.css" />
    </head>
    <body>
        %s
    </body>
</html>

""" % (sample,)