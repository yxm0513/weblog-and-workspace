from flask import Flask, render_template
#from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

import setting
app.config.from_object(setting)


# debug tool
#toolbar = DebugToolbarExtension(app)

app.jinja_env.add_extension("jinja2.ext.do")

#app.jinja_options = app.jinja_options.copy()
#app.jinja_options['extensions'].extend('jinja2.ext.do')

# add modules
from view import index
from view import admin
from view import test

app.register_module(index.mod)
app.register_module(admin.mod, url_prefix='/admin')
app.register_module(test.mod, url_prefix='/test')