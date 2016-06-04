from django.conf import settings
import requests;

class LegiscanService():
    base_url = 'http://api.legiscan.com/'
    base_params = { 'key': settings.LEGISCAN_API_KEY }

    @staticmethod
    def getMasterList(state):
        params = { 'op': 'getMasterList', 'state': state }
        params.update(LegiscanService.base_params)
        response = requests.get(LegiscanService.base_url, params)
        response.raise_for_status()
        return response.json()