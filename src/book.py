print "Content-type: text/html"
print """

<html>
    <head>
        <title>Kanji Flash</title>
        <link rel="stylesheet" type="text/css" href="css/main.css" />
        <script type="text/javascript" src="js/jquery-1.11.1.min.js"></script>
        <script>
            $(document).ready(function() {
                $('form').submit(function(event) {
                    event.preventDefault();
                    $.get("list.py", {subj:$('#subj').val()}, function(data) {
                        $('.result').html(data);
                    });
                });
            });
        </script>
    </head>
    <body>
        <form action="test.py">
            <input id="subj" name="subj" type="text" />
            <input type="submit" value="Search" />
        </form>
        <div class="result"></div>
    </body>
</html>

"""