#!/usr/bin/python3
import sys
import argparse
import http.client
import json
import time
import re
import string

class GreensnowConsole() :

    def __init__(self,inputfile,request_delay,regex_match,raw_data):
        self.inputfile = inputfile
        self.request_delay = request_delay
        self.regex_match = regex_match
        self.raw_data = raw_data
        self.controller = GreensnowController();

        self._check_ips();

    def _check_ips(self):

        if self.inputfile :
            with open(self.inputfile, 'r') as data:
                self._main_loop(data)
        else :
            data=self.raw_data.split('\n')
            self._main_loop(data)

    def _render_line(self,data) :
        if data.error == 1:
            print("|"+ip.center(17)+"|"+"Error".center(21)+"|")
        else :
            blocked = "N/A"
            country = "N/A"

            data.blocked = int(data.blocked)
            data.nb_attack = int(data.nb_attack)

            if int(data.blocked) == 0 and int(data.nb_attack) <= 0 :
                blocked = "OK"
            elif int(data.blocked) == 0 and int(data.nb_attack) >= 0 :
                blocked = "WARNING"
            else :
                blocked = "BLOCKED"

            if data.country :
                country=data.country

            print("|"+data.ip.center(17)+"|"+blocked.center(11)+"|"+country.center(9)+"|")

    def _main_loop(self,data):
        print("|"+"IP".center(17)+"|"+"State".center(11)+"|"+"Country".center(9)+"|")
        for line in data:
            if self.regex_match and not re.match(self.regex_match,line) :
                continue

            ips = re.findall(self.controller.ip_regex, line)
            for ip in ips:
                data=self.controller.check_ip(ip)
                self._render_line(self.controller.format_greensnow_api(ip,data))
                time.sleep(self.request_delay)



class GreensnowApiData() :

    def __init__(self,ip,blocked=0,first_report="",last_report="",nb_attack=0,country="",reverse="",error=0):
        self.ip=ip
        self.blocked=blocked
        self.first_report=first_report
        self.last_report=last_report
        self.nb_attack=nb_attack
        self.country=country
        self.reverse=reverse
        self.error=error

class GreensnowController() :

    def __init__(self):
        self.conn = http.client.HTTPConnection("api.greensnow.co")
        self.ip_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

    def check_ip(self,ip):
        self.conn.request("GET", "/"+ip.strip())
        return self.conn.getresponse()

    def format_greensnow_api(self,ip,response):
        if(response.status == 200 ) :
            data = response.read()
            try:
                j = json.loads(str(data,'utf-8'));

                blocked=0
                first_report=""
                last_report=""
                nb_attack=0
                country=""
                reverse=""

                if 'blocked' in j :
                    blocked = j['blocked']
                if 'first_report' in j :
                    first_report = j['first_report']
                if 'last_report' in j :
                    last_report = j['last_report']
                if 'nb_attack' in j :
                    nb_attack = j['nb_attack']
                if 'country' in j :
                    country = j['country']
                if 'reverse' in j :
                    reverse = j['reverse']

                return GreensnowApiData(ip,blocked,first_report,last_report,nb_attack,country,reverse)
            except ValueError:
                return GreensnowApiData(ip,error=1)
        else :
            return GreensnowApiData(ip,error=1)


class GreensnowCli() :

    def __init__(self):

        self.inputfile=""
        self.request_delay=1
        self.regex_match=""
        self.raw_data=""
        self.gui=""

        self.parse_args()

    def parse_args(self):
        parser = argparse.ArgumentParser(description="Simple unofficial Greensnow Python client.")
        parser.add_argument('-i', '--inputfile', metavar='inputfile', default="", type=str, help="File to check IPs.")
        parser.add_argument('-d', '--delay',dest='request_delay', metavar='request_delay', default=1, type=float, help="Delay between two requests.")
        parser.add_argument('--regex_match', metavar='regex_match', default="", type=str, help="The regex must match before being treat.")
        parser.add_argument('--raw_data', metavar='raw_data', default="", type=str, help="Direct ips input instead of input file. Ignore if inputfile is set.")

        args = parser.parse_args()

        if not args.inputfile and not args.raw_data :
            sys.stderr.write('error: %s\n' % "No input data")
            parser.print_help()
            sys.exit(2)

        self.inputfile=args.inputfile
        self.request_delay=args.request_delay
        self.regex_match=args.regex_match
        self.raw_data=args.raw_data

        GreensnowConsole(self.inputfile,self.request_delay,self.regex_match,self.raw_data)

if __name__ == "__main__":
    GreensnowCli()
