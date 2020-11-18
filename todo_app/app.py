from flask import Flask, render_template, url_for, redirect, request
from .data.session_items import get_items, add_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items = get_items()
    return render_template('index.html', items = items)

@app.route('/', methods = ['POST'])
def new_item():
    field_name = request.form['field_name']
    add_item(field_name)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
