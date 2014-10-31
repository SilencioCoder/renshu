from lib.storage import Storage
import cgi

print "Content-type: text/plain"

form = cgi.FieldStorage()
entry = form.getvalue('entry')
prompt = form.getvalue('prompt')
answer = form.getvalue('answer')

if not entry.isdigit():
    print """
    Incorrect entry id.
    """
else:
    try:
        s = Storage()
        s.save(entry, prompt, answer)
        print """
        Sucessfully added.
        """
    except Exception as e:
        print """
        %s %s %s %s
        """ % (e, entry, prompt, answer)