import frontmatter # https://github.com/eyeseast/python-frontmatter
import os
import jinja2
import markdown


TEMPLATE = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="A layout example with a side menu that hides on mobile, just like the Pure website.">
        <title>Responsive Side Menu &ndash; Layout Examples &ndash; Pure</title>
        <link rel="stylesheet" href="https://unpkg.com/purecss@2.0.5/build/pure-min.css"/>
        <link rel="stylesheet" href="css/template.css" />
        <link rel="stylesheet" href="https://jouw.us/css_prime" />
    </head>
    <body>

    <div id="layout">
        <!-- Menu toggle -->
        <a href="#menu" id="menuLink" class="menu-link">
            <!-- Hamburger icon -->
            <span></span>
        </a>

        <div id="menu">
            <div class="pure-menu">
                <a class="pure-menu-heading" href="#company">{{ static_details['site_name'] }}</a>

                <ul class="pure-menu-list">
                    {% for link in static_details['side_bar'] %}
                    <li class="pure-menu-item"><a href="/{{link.lower()}}" class="pure-menu-link">{{link}}</a></li>
                    {% endfor %}
                </ul>
            </div>
        </div>

        <div id="main">
            <div class="header">
        <h1> {{title}} </h1>
            <h2>By: {{author}}</h2>
        </div>

        <div class="content">
        <h2 class="content-subhead">Written on: {{date}} - Updated last: {{last_update}}</h2>
        <hr>
        <p>
            {{content}}
        </p>

        <div class="pure-g">
            {% for photo in photos %}
            <div class="pure-u-1-4">
                <img class="pure-img-responsive" src="photos/{{photo}}" alt="{{photo}}">
            </div>
            {% endfor %}
        </div>

    </div>
        </div>
    </div>

    <script src="https://jouw.us/js_prime"></script>

    </body>
    </html>
"""
static_details = {"site_name": "My Site", "side_bar": ["Home", "Tags", "About"]}

def render_pages():
    path = os.path.join(os.getcwd(), "markdown_content")
    md_files = os.listdir(path)

    for item in md_files:
        post = frontmatter.load(os.path.join(path, item))
        title = post['title']
        date = post['date']
        last_update = post['last_update']
        author = post['author']
        photos = post['photos']
        content = post.content

        extensions = ['extra', 'smarty']
        html = markdown.markdown(content, extensions=extensions, output_format='html5')
        doc = jinja2.Template(TEMPLATE).render(title=title, date=date, last_update=last_update, author=author, content=html, static_details=static_details, photos=photos)
        keepcharacters = ('_', '-') # Allows periods, hyphens or underbars to remain
        no_ext = item[:-3]
        filename = "".join(c for c in no_ext if c.isalnum() or c in keepcharacters).rstrip()
        
        with open("site/{}.html".format(filename.lower()), 'w') as f:
            f.write(doc)


render_pages()