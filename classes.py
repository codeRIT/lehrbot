from typing import Callable, List
from discord.channel import TextChannel
from discord.guild import Guild
from discord.member import Member
from discord.role import Role


def check_admin(func: Callable[[Member, TextChannel], None]):
    async def wrapper(caller: Member, channel: TextChannel, *args, **kwargs):
        if not caller.guild_permissions.administrator:
            await channel.send(
                caller.mention + " You must be an administrator "
                                 "to call this command."
            )
        else:
            await func(caller, channel, *args, **kwargs)
    return wrapper


@check_admin
async def makeclass(caller: Member, channel: TextChannel, name: str) -> None:
    guild: Guild = caller.guild
    await guild.create_role(
        name="Class-" + name,
        mentionable=True,
        reason="Requested by " + caller.mention
    )

    await channel.send(
        caller.mention + ' Class role "{}" has been created.'.format(name)
    )


@check_admin
async def deleteclass(caller: Member, channel: TextChannel, name: str) -> None:
    guild: Guild = caller.guild
    roles: List[Role] = guild.roles

    role: Role  # doesn't do anything except type hints
    for role in roles:
        if role.name == "Class-" + name:
            await role.delete(reason="Requested by " + caller.mention)
            await channel.send(
                caller.mention +
                ' Class role "{}" has been deleted.'.format(name)
            )
            return

    # only runs if the class doesn't exist
    await channel.send(
        caller.mention + ' Class role "{}" does not exist.'.format(name)
    )
