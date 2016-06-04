from django.conf import settings
import requests;

class LegiscanService():
    base_url = 'http://api.legiscan.com/'
    base_params = { 'key': settings.LEGISCAN_API_KEY }

    @staticmethod
    def getMasterList(state=None, session=None):
        params = { 'op': 'getMasterList' }
        params.update(LegiscanService.base_params)
        if state is not None: params.update({ 'state': state })
        if session is not None: params.update({ 'id': session })
        response = requests.get(LegiscanService.base_url, params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def getBill(bill_id, state):
        params = {'op': 'getBill', 'bill_id':bill_id,'state':state}
        params.update(LegiscanService.base_params)
        response = requests.get(LegiscanService.base_url, params)
        response.raise_for_status()
        return repsonse.json()

    @staticmethod
    def getBillText(doc_id):
         params = {'op': 'getBillText','doc_id':doc_id}
         params.update(LegiscanService.base_params)
         response = requests.get(LegiscanService.base_url, params)
         response.raise_for_status()
         return response.json()

    @staticmethod
    def getAmedment(amendment_id):
         params = {'op': 'getAmendment', 'amendment_id':amendment_id}
         params.update(LegiscanService.base_params)
         response = requests.get(LegiscanService.base_url, params)
         response.raise_for_status()
         return response.json()
    @staticmethod
    def getSupplement(supplement_id):
         params = {'op': 'getSupplement', 'supplement_id':supplement_id}
         params.update(LegiscanService.base_params)
         response = requests.get(LegiscanService.base_url, params)
         response.raise_for_status()
         return response.json()
    @staticmethod
    def getRoll(roll_call_id):
         params = {'op': 'getSupplement', 'supplement_id':supplement_id}
         params.update(LegiscanService.base_params)
         response = requests.get(LegiscanService.base_urls, params)
         response.raise_for_status()
         return response.json()

    @staticmethod
    def getSponser(people_id):
         params = {'op': 'getSponser', 'people_id':people_id}
         params.update(LegiscanService.base_params)
         response = response.get(LegiscanService.base_urls, params)
         response.raise_for_status()
         return response.json()