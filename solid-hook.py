#!/usr/bin/python
import urllib
import requests
import tldextract
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import sys
import dns
import dns.resolver
import time

name_server="ns.example.com"
headers = {'X-IPM-Username':'<username b64>','X-IPM-Password':'<password b64>'}
url ="https://{host}/rest/{action}/WHERE/{query}"
url2 ="https://{host}/rest/{action}"
#
# Return zone id of a  given zone
#
def get_zoneId(zone_name,dns_name='smart.local.com',dnsview_name='internet'):
    query = urllib.quote_plus("dnszone_name='{}' AND dnsview_name='{}' AND dns_name='{}'".format(zone_name,dnsview_name,dns_name))
    data={'host':name_server,'action':'dns_zone_list','query':query}
    q_url = url.format(**data)
    r = requests.get(q_url, headers=headers, verify=False)
    try:
        return json.loads(r.text)[0]["dnszone_id"]
    except:
        return None

def get_txt_rr(dnszone_id,domain):
    rr_full_name = '_acme-challenge.'+domain
    query = urllib.quote_plus("dnszone_id='{}' AND rr_type='TXT' AND rr_full_name = '{}'".format(dnszone_id,rr_full_name))
    data={'host':name_server,'action':'dns_rr_list','query':query}
    q_url = url.format(**data)
    r = requests.get(q_url, headers=headers, verify=False)
    try:
        parsed = json.loads(r.text)
        return parsed
    except:
        return None



def create_rr(dnszone_id,domain,token,dns_name='smart.local.com'):
    rr_full_name = '_acme-challenge.'+domain
    data={'host':name_server,'action':'dns_rr_add'}

    payload={
             'dns_name':dns_name,
             'rr_name':rr_full_name,
             'rr_type':'TXT',
             'dnszone_id':dnszone_id,
             'dnszone_site_id':dnszone_id,
             'rr_value1':token,
             'rr_ttl': 60,
             'force_update': 1

             }

    q_url = url2.format(**data)
    r = requests.post(q_url, data=json.dumps(payload, indent=4, sort_keys=True), headers=headers, verify=False)
    try:
        parsed = json.loads(r.text)
        return parsed
    except:
        return None

def delete_rr(rr_id):
    query = urllib.quote_plus("rr_id={}".format(rr_id))
    data={'host':name_server,'action':'dns_rr_delete'}
    payload={ 'rr_id':rr_id }

    q_url = url2.format(**data)
    r = requests.delete(q_url, data=json.dumps(payload, indent=4, sort_keys=True), headers=headers, verify=False)

    try:
        print r.text
        parsed = json.loads(r.text)
    except:
        return None

def wait_ns(ns,domain,token):
    my_resolver = dns.resolver.Resolver()
    my_resolver.nameservers = [ns]
    while 1:
        time.sleep(60)
        try:
            answers = my_resolver.query("_acme-challenge." + domain, 'TXT')
            for rdata in answers:
                for txt_string in rdata.strings:
                    print "TXT Record Retrieved: '{0}'".format(txt_string)
                    if token.strip() == txt_string.strip():
                        time.sleep(60)
                        return
        except Exception, ex:
            print "No TXT was found"

if __name__ == "__main__":

    hook = sys.argv[1]
    print("hook: {0}".format(hook))

    domain = sys.argv[2]
    print("domain: {0}".format(domain))
    if hook != 'invalid_challenge':
        txt_challenge = sys.argv[4]
        print("txt_challenge: {0}".format(txt_challenge))

    ext = tldextract.extract(domain)
    dnszone_id = get_zoneId(ext.domain+'.'+ext.suffix)
    print "zoneid: {0}\n domain: {1} ".format(dnszone_id,ext.domain+'.'+ext.suffix)
    
    if hook == "deploy_challenge":
        rr = get_txt_rr(dnszone_id,domain)
        if rr:
            delete_rr(rr[0]["rr_id"])
        create_rr(dnszone_id,domain,txt_challenge)
        wait_ns('8.8.8.8',domain,txt_challenge) #First time can be boring...
    elif hook == "clean_challenge":
        rr = get_txt_rr(dnszone_id,domain)
    #In order to increase next time generation do not remove record
    #    if rr: 
    #        delete_rr(rr[0]["rr_id"])
    print "---end---"
