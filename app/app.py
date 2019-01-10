#  -*- encoding: utf-8 -*-

import logging

from flask import Flask, request, jsonify

from app.common.constants_and_variables import AppVariables, AppConstants

app_variables = AppVariables()
app_constants = AppConstants()

app = Flask(__name__)


# @celery.task
# def update_stats(athlete_id):
#     with app.app_context():
#         process_stats = ProcessStats()
#         calc_stats = process_stats.process(athlete_id)
#         print(calc_stats)


@app.route("/")
def home():
    # update_stats(11591902)
    # update_stats.delay(11591902)
    # hello.delay()
    return "OK"


@app.route("/stats/<telegram_username>", methods=['POST'])
def stats(telegram_username):
    if request.method == 'POST':
        return telegram_username


@app.route('/webhook', methods=['GET', 'POST'])
def strava_webhook():
    if request.method == 'POST':
        message = request.json
        logging.info("Received webhook event: {event}".format(event=message))

        return jsonify(''), 200

    elif request.method == 'GET':
        hub_challenge = request.args.get('hub.challenge')
        logging.info("Hub Challenge ID: {hub_challenge}".format(hub_challenge=hub_challenge))
        return jsonify({'hub.challenge': hub_challenge}), 200


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    app.run(host=app_variables.app_host, port=int(app_variables.app_port))
