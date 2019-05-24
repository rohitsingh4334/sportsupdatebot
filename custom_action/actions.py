from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from datetime import datetime

import requests
from rasa_core_sdk import Action

logger = logging.getLogger(__name__)

API_URL = "https://cricapi.com/api/matches?apikey=KRAteAAoYOcW6vEfxottDRBcaFf1"
API_KEY = "GENERATE_KEY_GO_TO: https://cricapi.com/"


class ApiAction(Action):
    def name(self):
        return "action_match_news"

    def run(self, dispatcher, tracker, domain):
        sport_type = tracker.get_slot('group')

        if sport_type == 'cricket':
            res = requests.get(API_URL)
            if res.status_code == 200:
                data = res.json()["matches"]
                recent_match = data[0]
                upcoming_match = data[1]
                upcoming_match["date"] = datetime.strptime(upcoming_match["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                next_date = upcoming_match["date"].strftime("%d %B %Y")

                out_message = """Quick info:\n1.The match between {} and {} was recently held and {} won.
                """.format(recent_match["team-1"], recent_match["team-2"], recent_match["winner_team"])

                dispatcher.utter_message(out_message)

                out_message = "2.The next match is {} vs {} on {}".format(
                    upcoming_match["team-1"], upcoming_match["team-2"], next_date)

                dispatcher.utter_message(out_message)
        elif sport_type == 'tennis':
            dispatcher.utter_message('coming soon...................')
        elif sport_type == 'football':
            dispatcher.utter_message('api is not working............ :X')
        else:
            dispatcher.utter_message("not able to catch entity")
        return []
