from lib.storage import Storage
import cgi
import re

form = cgi.FieldStorage()
subj = form.getvalue('subj')

s = Storage()

def is_alpha(s):
    p = '^[a-zA-Z\s]*$'
    if re.match(p, s):
        return True
    return False

if subj.isdigit():
    result = s.get_id(subj)
elif not is_alpha(subj):
    result = s.search_writing(subj, 10)
else:
    result = s.search_meaning(subj, 10)

html = ''
html += '<table class="result">'

if result:
    for item in result:

        html += '<tr>'

        html += '<td class="main">'
        if item.writings:
            html += item.writings[0].content
        else:
            html += item.readings[0].content
        html += '<br />'
        html += '<a href="add.py?id=%s" class="lnk" target="_blank">Add</a>' % item.id
        html += '</td>'

        html += '<td>'
        for i in range(len(item.meanings)):
            m = item.meanings[i]
            if m.parts:
                html += '<div class="pos fade">p: %s</div>' % ', '.join([p.content for p in m.parts])
            html += '<div class="detail"><span class="fade">%s.</span> %s</div>' % (i+1, '; '.join([g.content for g in m.gloss]))
        if item.writings[1:]:
            html += '<div class="detail">%s</div>' % '; '.join([w.content for w in item.writings[1:]])
        rindex = 0 if item.writings else 1
        html += '<div class="detail">%s</div>' % '; '.join([r.content for r in item.readings[rindex:]])
        html += '</td>'

        html += '</tr>'

        """
        html += '<table>'
        html += '<tr>'

        rowspan = len(r.meanings)

        html += '<td rowspan="%s">' % (rowspan,)

        if r.writings:
            html += r.writings[0].content

        html += '</td>'
        html += '</tr>'

        html +=
        html += '</table>'

        for w in r.writings:
            html += w.content
            html += ';'
        """

html += '</table>'

print "Content-type: text/html"

print ("""

%s

""" % html).encode('utf8')