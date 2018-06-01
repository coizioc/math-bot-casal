"""Displays a list of people whom the creator has outdpsed in Runescape via a bot interface in discord."""
import discord
from discord.ext import commands

RESOURCES_REPO = './subs/casal/resources/'
CASAL_FILE = f'{RESOURCES_REPO}casallist.txt'
MARKOV_MODULE_CREATOR_ID_FILE = f'{RESOURCES_REPO}markovcreatorid.txt'

with open(MARKOV_MODULE_CREATOR_ID_FILE, 'r') as f:
    MARKOV_MODULE_CREATORS_ID = int(f.readline())

PERMISSION_ERROR_STRING = f'Error: You do not have permission to use this command.'


def format_casal(casal_list):
    '''Takes in a list of people and outputs a formatted string to be displayed.'''
    header = '```\n-----------\nCasal List:\n-----------\n\n'

    names = ''
    for index, name in enumerate(casal_list, 1):
        names += f'{index}. {name}'

    footer = ("\n * indicates that this person was outdpsed in a pvm situation with more than two people.\n"
              "** indicates that this person is a nitpicky ass.\n\n"
              "Type '$casal help' for more information on what this is.```")

    out = header + names + footer

    return out


class Casal():
    """Defines Casal commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def casal(self, ctx):
        """Displays the Casal List."""
        with open(CASAL_FILE, 'r') as file:
            casal_list = file.readlines()
        await ctx.send(format_casal(casal_list))

    @casal.command(name='help')
    async def casal_help(self, ctx):
        """Explains what the Casal List is."""
        msg = ("```The Casal List is the list of people who have been outdpsed by Coizioc, a known shit pvmer. "
               "If a person is on this list, then logically, that person must be worse than her in every way "
               "possible. To get onto this list, she must have outdpsed you at least once. The reason as to why "
               "this occurs is irrelevant. It is called the Casal list because Casal is the first person she "
               "ever outdpsed.```")
        await ctx.send(msg)

    @casal.command(name='add', hidden=True)
    async def casal_add(self, ctx, name):
        """Adds a name to the Casal List."""
        if ctx.author.id == MARKOV_MODULE_CREATORS_ID:
            with open(CASAL_FILE, 'a+') as file:
                file.write(name.rstrip() + '\n')
            await ctx.send(f"{name} successfully added to the Casal List.")
        else:
            await ctx.send(PERMISSION_ERROR_STRING)

    @casal.command(name='remove', hidden=True)
    async def casal_remove(self, ctx, removed_name):
        """Removes a name from the Casal List."""
        if ctx.author.id == MARKOV_MODULE_CREATORS_ID:
            with open(CASAL_FILE, 'r+') as infile:
                casal_list = infile.read().splitlines()
            if removed_name in casal_list:
                try:
                    casal_list.remove(removed_name)
                    out = ''
                    for name in casal_list:
                        out += name + '\n'
                    with open(CASAL_FILE, 'w') as outfile:
                        outfile.write(out)
                    await ctx.send(f"{removed_name} successfully removed from the Casal List.")
                except Exception:
                    await ctx.send(f"Error: Unknown error.")
            else:
                await ctx.send(f"Error: {removed_name} not found.")
        else:
            await ctx.send(PERMISSION_ERROR_STRING)


def setup(bot):
    """Adds the cog to the bot."""
    bot.add_cog(Casal(bot))
