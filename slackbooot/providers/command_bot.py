import re
import asyncio
import operator

from butterfield import Bot


class CommandBot(Bot):

    def __init__(self, *args, **kwargs):
        super(CommandBot, self).__init__(*args, **kwargs)
        self.listen(self.message_handler)
        self.command_handlers = []

    async def message_handler(self, bot, message: 'message'):
        if 'subtype' in message:
            return

        text = message['text']

        for commands, coro in self.command_handlers:
            regexp = r'^\s*%s\s*' % (r'\s*'.join(commands))
            pattern = re.compile(regexp)
            match = pattern.match(text)
            if not match:
                continue
            prefix = match.group(0)

            param = text[len(prefix):].strip()

            return asyncio.ensure_future(coro(param, bot, message))

    def listen_on_command(self, commands, coro):
        self.command_handlers.append((commands, coro))
        self.command_handlers.sort(key=operator.itemgetter(0), reverse=True)
