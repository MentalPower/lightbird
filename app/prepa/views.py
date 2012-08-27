from django.http import HttpResponse
from elementsoap.ElementSOAP import *
from django.utils.html import escape
from django.db import connection
from django.utils import timezone
from pprint import pprint, pformat
from models import Scan, Town, Area, Status, Event, Action
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
    time_start = datetime.now()
    prepa = PrepaService()
    response = prepa.getBreakdownsSummary()
    output = "\t\tScan time %s\n" % datetime.now()
    total_num_towns = 0
    total_num_breaks = 0
    scan_object = Scan()
    scan_object.save()

    for town, num_breaks in response.iteritems():
        (town_object,is_new) = Town.objects.get_or_create(name=town, defaults={'scan_added': scan_object})
        output += "\n%s has %d breakdowns" % (town, num_breaks)
        total_num_towns += 1
        total_num_breaks += num_breaks
        response2 = prepa.getBreakdownsByTownOrCity(town)

        for area, breakdown in response2.iteritems():
            (area_object,is_new) = Area.objects.get_or_create(town=town_object, name=area, defaults={'scan_added': scan_object})
            (status_object,is_new) = Status.objects.get_or_create(name=breakdown['status'], defaults={'scan_added': scan_object})
            (event_object,is_new) = Event.objects.get_or_create(area=area_object, scan_last_seen__id__gt=scan_object.id-3, defaults={'scan_added': scan_object, 'scan_last_seen': scan_object})
            event_object.scan_last_seen = scan_object
            event_object.save()

            (action_object,is_new) = Action.objects.get_or_create(event=event_object, status=status_object, defaults={'scan_added': scan_object, 'scan_last_seen': scan_object})
            action_object.scan_last_seen = scan_object
            action_object.save()

            output += "\n\t%s (%s) %s" % (area, breakdown['status'], breakdown['last_update'])

    time_end = datetime.now()
    time_taken = time_end - time_start

    scan_object.num_towns = total_num_towns
    scan_object.num_breakdowns = total_num_breaks
    scan_object.time_taken = time_taken.total_seconds()
    scan_object.save()
    output += "\n\n\t\t\tTotal towns: %d" % total_num_towns
    output += "\n\t\t\tTotal breakdowns: %d" % total_num_breaks

    if settings.DEBUG:
        output += "\n\n\n\n" + pformat(connection.queries)

    return HttpResponse("<pre>%s</pre>" % output)
