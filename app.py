from flask import (Flask, render_template, redirect, request, url_for, flash)
import logging
import short_url
from uuid import  uuid4
import os

app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)


@app.route('/', methods=["GET", "POST"])
def home_page():
    domain = os.environ.get("DOMAIN", "localhost")
    protocol = os.environ.get("PROTOCOL", "http")

    if request.method == 'POST':
        url = str(request.form.get('url'))
        encoded_hash = short_url.encode_url(uuid4().int)
        logging.info(url)
        return redirect(url_for('shortened_url', url=f"{protocol}://{domain}/{encoded_hash}"))
    else:
        return render_template("index.html"), 200


@app.route('/result')
def shortened_url():
    url = request.args.get('url')
    logging.info(f"short {url}")
    return render_template('result.html', url=url), 200


@app.route('/<hash>')
def redirect_url(hash):
    with open('url_list.p') as f:
        url_list = pickle.load(f)
    for item in url_list:
        if hash == item[1]:
            return redirect(item[0])
    flash("<strong>Redirect failed:</strong> shortened url does not exist. Enter a url to shorten below.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
