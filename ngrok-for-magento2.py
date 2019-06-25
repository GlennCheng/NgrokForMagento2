#!/usr/bin/python3

import sys
import subprocess
import requests
import json
import time
import os
import signal
import atexit
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-l", "--localDomain", help="rewrite ngrok domain to local domain.", required=True)
parser.add_argument("-r", "--restoreDomain", help="restore domain when exit.", required=True)
args = parser.parse_args()

class const:
    def get_original_baseurl(self, url='localhost'):
        return url


def set_ngrok_baseurl(tunnel_url, tunnel_url_https):
    subprocess.check_call(['php','bin/magento','config:set','web/unsecure/base_url',tunnel_url+'/'],stdout=subprocess.PIPE)
    subprocess.check_call(['php','bin/magento','config:set','web/secure/base_url',tunnel_url_https+'/'],stdout=subprocess.PIPE)
    subprocess.check_call(['php','bin/magento','config:set','web/secure/base_link_url',tunnel_url_https+'/'],stdout=subprocess.PIPE)
    subprocess.check_call(['php','bin/magento','cache:flush'],stdout=subprocess.PIPE)
    print('setup the base url to '+tunnel_url_https)


def set_original_baseUrl(url):
    base_url = const.get_original_baseurl(const, url)
    subprocess.check_call(['php','bin/magento','config:set','web/unsecure/base_url','http://'+base_url+'/'],stdout=subprocess.PIPE)
    subprocess.check_call(['php','bin/magento','config:set','web/secure/base_url','https://'+base_url+'/'],stdout=subprocess.PIPE)
    subprocess.check_call(['php','bin/magento','config:set','web/secure/base_link_url','https://'+base_url+'/'],stdout=subprocess.PIPE)
    subprocess.check_call(['php','bin/magento','cache:flush'],stdout=subprocess.PIPE)
    print('restore BaseUrl to '+base_url)


def kill_child():
    if child_pid is None:
        pass
    else:
        os.kill(child_pid, signal.SIGTERM)
    print('killed subprocess.')


def sigint_handler(signum, frame):
    print('restore BaseUrl...')
    set_original_baseUrl(args.restoreDomain)
    print('kill subprocess...')
    kill_child()
    print('Done & exit, Bye!')
    exit()

def get_ngrok_tunnel_json(host='localhost', port='4040'):
    localhost_url = "http://"+host+":"+port+"/api/tunnels" #Url with tunnel details
    tunnel_url = requests.get(localhost_url).text #Get the tunnel information
    j = json.loads(tunnel_url)
    return j


signal.signal(signal.SIGINT, sigint_handler)

if __name__ == '__main__':

    signal.signal(signal.SIGINT, sigint_handler)

    ngrokprocess = subprocess.Popen(['ngrok','http','http://'+args.localDomain],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

    time.sleep(3) # to allow the ngrok to fetch the url from the server

    j = get_ngrok_tunnel_json()
    tunnel_url_https = j['tunnels'][0]['public_url']
    tunnel_url = j['tunnels'][1]['public_url'] #Do the parsing of the get

    print(tunnel_url)
    set_ngrok_baseurl(tunnel_url, tunnel_url_https)

    # Here you can get the PID
    global child_pid
    child_pid = ngrokprocess.pid

    # Now we can wait for the child to complete
    #(output, error) = ngrokprocess.communicate()
    ngrokprocess.communicate()

    atexit.register(set_original_baseUrl)
    atexit.register(kill_child)


