ENCODED_WRAPPER = """
<!DOCTYPE html>
<html lang="{{ lang }}">
    <head>
        <title>{{ title }}</title>
        <meta charset="{{ encoding }}" />
        <meta name="viewport" content="{{ viewport }}" />
        <link rel="stylesheet" href="/style.css" />
        {% if inject_jetbrains_font %}
        <style>
            @font-face {
                font-family: WuiBaseFont;
                src: url("/font.ttf");
            }

            html,
            body {
                font-family: WuiBaseFont;
            }
        </style>
        {% endif %}
        <script src="/script.js"></script>
    </head>
    <body></body>
</html>

""".lstrip()
