from django.http import HttpResponse
from elementsoap.ElementSOAP import *
from django.utils.html import escape
from pprint import pprint, pformat

class PrepaService(SoapService):
    url = "http://wss.prepa.com/services/BreakdownReport.BreakdownReportHttpSoap11Endpoint/"
    def getBreakdownsSummary(self):
        action = "urn:getBreakdownsSummary"
        request = SoapRequest("")
        response = self.call(action, request)

        response_dict = {}
        for result in response:
            r1TownOrCity = result.find('{http://ws.breakdown.prepa.com}r1TownOrCity').text
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
            r2Area = result.find('{http://ws.breakdown.prepa.com}r2Area').text
            r3Status = result.find('{http://ws.breakdown.prepa.com}r3Status').text
            r4LastUpdate = result.find('{http://ws.breakdown.prepa.com}r4LastUpdate').text
            response_dict[r2Area] = {'status': r3Status, 'last_update': r4LastUpdate}

        return response_dict

def update(request):
    prepa = PrepaService()
    response = prepa.getBreakdownsSummary()
    output = ""
    total_num_breaks = 0

    for town, num_breaks in response.iteritems():
        output += "\n%s has %d breakdowns" % (town, num_breaks)
        total_num_breaks += num_breaks
        response2 = prepa.getBreakdownsByTownOrCity(town)

        for area, breakdown in response2.iteritems():
            output += "\n\t%s (%s) %s" % (area, breakdown['status'], breakdown['last_update'])

    output += "\n\n\t\t\tTotal breakdowns: %d" % total_num_breaks
    return HttpResponse("<pre>%s</pre>" % output)
