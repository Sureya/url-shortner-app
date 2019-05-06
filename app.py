from flask import (Flask, render_template, redirect, request, url_for, flash, g)
import logging
import short_url
import uuid
import os
import psycopg2

app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)
short_url.DEFAULT_BLOCK_SIZE = 4


@app.before_request
def before_request():
   g.db =psycopg2.connect(user="developer", password="developer", host="127.0.0.1", port="5432",
                          database="exercises")

   g.cursor = g.db.cursor()
   g.domain = os.environ.get("DOMAIN", "localhost:5000")
   g.protocol = os.environ.get("PROTOCOL", "http")


@app.teardown_request
def teardown_request(exception):
    g.cursor.close()
    g.db.close()


def persist_records(unqiue_id, url, result_url):
    sql = 'INSERT INTO serverless.short_url(uuid, url, result_url) VALUES(%s, %s, %s) '
    g.cursor.execute(sql, (unqiue_id, url, result_url))
    g.db.commit()


@app.route('/', methods=["GET", "POST"])
def home_page():
    if request.method == 'POST':
        url = request.form.get('url')
        logging.info(request.form)
        _id = int(str(uuid.uuid4().int)[:4])
        encoded_hash = short_url.encode_url(_id)
        result_url = f"{g.protocol}://{g.domain}/{encoded_hash}"
        persist_records(_id, url, result_url.replace("'", ""))
        logging.info(f"record updated in database, {result_url}")
        return redirect(url_for('shortened_url', url=result_url)), 200

    else:
        return render_template("index.html"), 200


@app.route('/result')
def shortened_url():
    url = request.args.get('url')
    return render_template('result.html', url=url), 200


# #  WIP ******
# @app.route('/<hash>')
# def redirect_url(hash):
#     with open('url_list.p') as f:
#         url_list = pickle.load(f)
#     for item in url_list:
#         if hash == item[1]:
#             return redirect(item[0])
#     flash("<strong>Redirect failed:</strong> shortened url does not exist. Enter a url to shorten below.")
#     return redirect(url_for('index'))
#

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
