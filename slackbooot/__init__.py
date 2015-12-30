import butterfield

from .providers.command_bot import CommandBot
from .bots.commands.gif_commands import find_gif, gif_trends
from .bots.commands.build_commands import BuildCommand


def run(token, port):
    b = CommandBot(token)
    b.listen_on_command(['gif'], find_gif)
    b.listen_on_command(['gif', 'trends'], gif_trends)
    b.listen_on_command(['build'], BuildCommand(b, port=port))

    butterfield.run(b)
