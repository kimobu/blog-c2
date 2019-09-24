# Blog C2

This is a proof of concept for using a blog and its comments for malware command and control
    
## Installation
Start the server
`docker build -t blog`
`docker run -dit --restart unless-stopped blog`

Drop the client.py script onto the victim computer and then run it

## Command and Controlling
1. Visit the blog's page and login (default creds are: botherder/abc123!!!)
2. Create a new blog post with the body of the blog being the command you want to run
3. The client script will periodically check in. If it detects a new blog post, it will parse it, run the command from the post, and post a comment to the blog with the command's output
