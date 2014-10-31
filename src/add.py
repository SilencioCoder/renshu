from lib.storage import Storage
import cgi


form = cgi.FieldStorage()
id = form.getvalue('id')

s = Storage()

result = s.get_id(id)
result = result[0]

html = ""

html += "Writing:"
html += "<ul>"
for w in result.writings:
    html += "<li>%s</li>" % w.content
html += "</ul>"

html += "Reading:"
html += "<ul>"
for r in result.readings:
    html += "<li>%s</li>" % r.content
html += "</ul>"

html += "Meaning:"
html += "<ul>"
for m in result.meanings:
    #if m.parts:
    #    html += "<li>%s</li>" % '; '.join([p.content for p in m.parts])
    html += "<li>%s</li>" % '; '.join([g.content for g in m.gloss])
html += "</ul>"

prompt = ""
if result.writings:
    prompt = result.writings[0].content
elif result.readings:
    prompt = result.readings[0].content

def get_first_gloss(input):
    for m in input.meanings:
        for g in m.gloss:
            if g.content:
                return g.content
    return ""

def get_first_reads(input):
    for r in input.readings:
        if r.content:
            return "(%s)" % (r.content,)
    return ""

answer = ("%s %s" % (get_first_gloss(result), get_first_reads(result))).strip(' ')

print "Content-type: text/html"
print ("""

<html>
    <head>
        <title>Kanji Flash</title>
        <meta charset="utf-8" />
        <link rel="stylesheet" type="text/css" href="css/main.css" />
        <script type="text/javascript" src="js/jquery-1.11.1.min.js"></script>
        <script>
            $(document).ready(function() {
                $('form').submit(function(event) {
                    event.preventDefault();
                    formdata = {
                        entry:$('#entry').val(),
                        prompt:$('#prompt').val(),
                        answer:$('#answer').val()
                    }
                    $.get("save.py", formdata, function(data) {
                        $('.result').html(data);
                    });
                });
            });
        </script>
    </head>
    <body>
        %s
        <form action="save.py">
            <input id="entry" name="entry" type="hidden" value="%s" />
            <label for="prompt">Prompt: </label>
            <input id="prompt" name="prompt" type="text" value="%s" />
            <br />
            <label for="answer">Answer: </label>
            <input id="answer" name="answer" type="text" value="%s" />
            <br />
            <input type="submit" value="Add to Flash Cards" />
        </form>
        <div class="result"></div>
    </body>
</html>

""" % (html, id, prompt, answer)).encode('utf8')