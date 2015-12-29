import os
from slackbooot import run

TOKEN = os.environ.get('TOKEN')
run(TOKEN)
