import os
from slackbooot import run

TOKEN = os.environ.get('TOKEN')
PORT = os.environ.get('PORT')
run(TOKEN, PORT)
