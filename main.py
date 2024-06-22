import os
os.system("pip install discord.py==1.7.3")
os.system("pip install intensity-logger==0.1.2")
import discord, json
from discord.ext import commands
from intensity_logger import Logger

logger = Logger()
os.system("cls") if os.name == "nt" else os.system("clear")

class AutoPrune(commands.Cog):
    def __init__(self, discord_bot, target_server_id, wall_role_id, is_wall_role_enabled, prune_reason):
        self.discord_bot = discord_bot
        self.target_server_id = target_server_id
        self.wall_role_id = wall_role_id
        self.is_wall_role_enabled = is_wall_role_enabled
        self.prune_reason = prune_reason

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug("Auto Prune Enabled Successfully")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.guild is None or after.id != self.discord_bot.user.id or after.guild.id != self.target_server_id:
            return
        if before.roles != after.roles:
            await self.handle_role_change(before, after)

    async def handle_role_change(self, before, after):
        guild = after.guild
        bot_member = guild.get_member(self.discord_bot.user.id)
        if bot_member.guild_permissions.administrator or bot_member.guild_permissions.kick_members:
            try:
                if self.is_wall_role_enabled:
                    wall_role = guild.get_role(self.wall_role_id)
                    if wall_role and any(role.position > wall_role.position for role in after.roles):
                        roles = [role for role in guild.roles if len(role.members) > 0]
                        pruned_count = await guild.prune_members(days=1, roles=roles, reason=self.prune_reason)
                        logger.success(f"Pruned {pruned_count} members")
                    else:
                        return
                else:
                    roles = [role for role in guild.roles if len(role.members) > 0]
                    pruned_count = await guild.prune_members(days=1, roles=roles, reason=self.prune_reason)
                    logger.success(f"Pruned {pruned_count} members")
            except discord.errors.HTTPException as e:
                if e.status == 429:
                    logger.ratelimit("Rate limited: Max number of prune requests reached. Try again later.")
                else:
                    logger.error(f"HTTP Exception: {e.status} - {e.text}")
            except discord.errors.Forbidden:
                logger.error("Missing Permissions: Bot cannot prune members.")
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
        else:
            logger.warning("Bot does not have the required permissions to prune members.")

def main():
    with open("data.json", "r") as file:
        data = json.load(file)
    token = data["token"]
    target_server_id = data["target_server_id"]
    wall_role_id = data["wall_role_id"]
    is_wall_role_enabled = data["is_wall_role_enabled"]
    prune_reason = data["prune_reason"]
    intents = discord.Intents.all()
    discord_bot = commands.Bot(command_prefix="idk", help_command=None, self_bot=True, intents=intents)
    discord_bot.add_cog(AutoPrune(discord_bot, target_server_id, wall_role_id, is_wall_role_enabled, prune_reason))
    discord_bot.run(token, reconnect=True, bot=False)

if __name__ == "__main__":
    main()
