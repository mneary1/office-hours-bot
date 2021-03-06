import logging

from discord import Message, Guild, Client, Member


logger = logging.getLogger(__name__)


def name(member: Member):
    return member.nick if member.nick else member.display_name


def is_bot_mentioned(message: Message, client: Client) -> bool:
    users_mentioned_in_role = []
    for role in message.role_mentions:
        users_mentioned_in_role.extend(role.members)

    if client.user in message.mentions or client.user in users_mentioned_in_role:
        return True

    return False


supported_commands = []


def command_class(cls):
    supported_commands.append(cls)


async def handle_message(message: Message, client: Client):
    if not message.guild:
        return  # this is a DM to the bot TODO: add DM commands
    for cmd_class in supported_commands:
        if await cmd_class.is_invoked_by_message(message, client):
            command = cmd_class(message, client)
            await command.handle()
            return


class Command:
    def __init__(self, message: Message = None, client: Client = None):
        if not message:
            raise ValueError("You must issue a command with a message or guild")
        self.message: Message = message
        self.guild: Guild = message.guild
        self.client = client

    async def handle(self):
        raise AttributeError("Must be overwritten by command class")

    @staticmethod
    async def is_invoked_by_message(message: Message, client: Client):
        pass


## DO NOT MOVE THIS CODE
# The following imports all the modules in command so that they can be added to the
# command interpreter.
import pkgutil

__all__ = []
for loader, module_name, is_pkg in  pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module