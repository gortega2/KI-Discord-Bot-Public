import discord
from discord import app_commands
from discord.ext import commands
import KIBot as KI
from discord_token import TOK as TOKEN #ENTER YOUR OWN DISCORD BOT TOKEN, OTHERWISE IT WON'T FUNCTION
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())





async def send_message(message, user_message, is_private):
    try:
        response = "```\n" + str(KI.send_response(user_message)) + "\n```"
        print(response)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

    


def get_response(message:str) -> str:
    p_message = message.lower()

    return


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event

    async def on_ready():
        print(f'{client.user} is now running!')

    
    @client.event 
    async def on_message(message):
        #TODO: Add slash commands
        #TODO: Create a !help command
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)


def command_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    fd_help_description = 'Bot will return you the frame data of a specified move.' \
     + '\nUSAGE: !fd [CHARACTER] [NORMAL/SPECIAL/COMMAND] (not case sensitive)' \
     + "\nJumping moves is notated with J.[COMMAND] (J.HK for example)" \
     + "\nTarget combos or rekkas is notated with > (Wulf st.lp>st.mp>st.hp, Hisako qcf+p>HP)"



    d_bot = commands.Bot(command_prefix='!', intents=intents)
    @d_bot.event
    async def on_ready():
        print(f'{d_bot.user} is now running!')

    @d_bot.command(name='fd', description=fd_help_description,)
    async def frame_data(ctx, name: str = commands.parameter(description='Name of the character'),
                          command: str = commands.parameter(description="Command notation of the move (Ex. 5HK, Cl.HK, QCB+HK)")):
        try:
            bot_testing_id = 643251292545875978
            print(ctx.message.channel.id)
            print(ctx.message.content)
            print(f'Name: {name}, Command: {command}')
            if ctx.message.channel.id == bot_testing_id:
                response = "```\n" + str(KI.send_response(name, command)) + "\n```"
                print(response)
                await ctx.send(response)
        except Exception as error:
            print(f"There was an error: {error}")

    d_bot.run(TOKEN)
            
        

        



