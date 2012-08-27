from django.http import HttpResponse
from elementsoap.ElementSOAP import *
from django.utils.html import escape
from django.db import connection
from django.utils import timezone
from pprint import pprint, pformat
from models import Town, Area, Event, Status, Action
from datetime import datetime
from django.conf import settings

class PrepaService(SoapService):
    url = "http://wss.prepa.com/services/BreakdownReport.BreakdownReportHttpSoap11Endpoint/"
    def getBreakdownsSummary(self):
        action = "urn:getBreakdownsSummary"
        request = SoapRequest("")
        response = self.call(action, request)

        response_dict = {}
        for result in response:
            r1TownOrCity = result.find('{http://ws.breakdown.prepa.com}r1TownOrCity').text.strip()
            r2TotalBreakdowns = int(result.find('{http://ws.breakdown.prepa.com}r2TotalBreakdowns').text)
            response_dict[r1TownOrCity] = r2TotalBreakdowns
        return response_dict
    def getBreakdownsByTownOrCity(self, townOrCity):
        action = "urn:getBreakdownsByTownOrCity"
        request = SoapRequest("{http://ws.breakdown.prepa.com}getBreakdownsByTownOrCity")
        SoapElement(request, "townOrCity", "string", townOrCity)
        response = self.call(action, request)

        response_dict = {}
        for result in response:
            r2Area = result.find('{http://ws.breakdown.prepa.com}r2Area').text.strip()
            r3Status = result.find('{http://ws.breakdown.prepa.com}r3Status').text.strip()
            r4LastUpdate = datetime.strptime(result.find('{http://ws.breakdown.prepa.com}r4LastUpdate').text.strip(), "%m/%d/%Y %H:%M %p")
            response_dict[r2Area] = {'status': r3Status, 'last_update': r4LastUpdate}

        return response_dict

def update(request):
    prepa = PrepaService()
    response = prepa.getBreakdownsSummary()
    output = ""
    total_num_breaks = 0

    for town, num_breaks in response.iteritems():
        (town_object,is_new) = Town.objects.get_or_create(name=town)
        output += "\n%s has %d breakdowns" % (town, num_breaks)
        total_num_breaks += num_breaks
        response2 = prepa.getBreakdownsByTownOrCity(town)

        for area, breakdown in response2.iteritems():
            (area_object,is_new) = Area.objects.get_or_create(town=town_object, name=area)
            (status_object,is_new) = Status.objects.get_or_create(name=breakdown['status'])
            output += "\n\t%s (%s) %s" % (area, breakdown['status'], breakdown['last_update'])

    output += "\n\n\t\t\tTotal breakdowns: %d" % total_num_breaks

    if settings.DEBUG:
        output += "\n\n\n\n" + pformat(connection.queries)

    return HttpResponse("<pre>%s</pre>" % output)
