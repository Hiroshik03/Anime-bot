import asyncio
import json
import aiohttp
import parser_anime
import random
import discord
import anime_db as DB
import hui
from League_parse import summoner

bot = discord.Bot()
@bot.event
async def on_ready():
    print(f'Бот:{bot.user.display_name} готов!')
    print(f'Запущен на серверах:{bot.guilds}')
@bot.slash_command(name='roll', description='Роллит случайное число')
async def roll(ctx,at: int=0,to: int=100):
    await parser_anime.data_reader_on_year(2024)
    generate = random.randrange(start=at, stop=to)
    embed = discord.Embed(
        title="Rolled",
        description=f":slot_machine: {generate}",
        color=discord.Colour.blurple(),  # Pycord provides a class with default colors you can choose from
    )
    embed.set_author(name=f"{ctx.user.display_name}", icon_url=ctx.user.avatar.url)
    await ctx.respond(embed=embed)
@bot.slash_command(name='today_anime', description='Показывает вышедшее сегодня аниме')
async def today_anime(ctx):
    iteration = 1
    await ctx.respond("Вот список вышедших аниме")
    data = await parser_anime.data_reader()
    embed = discord.Embed(
        title="Anime",
        description=f"Вышедшие сегодня аниме",
        color=discord.Colour.blurple(),  # Pycord provides a class with default colors you can choose from
    )
    embed.set_author(name=f"{bot.user.display_name}", icon_url=bot.user.avatar.url)
    embed.set_image(url=data[iteration][2])
    embed.add_field(name=data[iteration][0],value=data[iteration][1])
    message = await ctx.channel.send(embed=embed)
    while True:
        await message.add_reaction("📄")
        await message.add_reaction("➡")
        await message.add_reaction("✖")
        def check(reaction, user):
            return (user == ctx.author and str(reaction.emoji) == '➡') or (user == ctx.author and str(reaction.emoji) == '📄') or (user == ctx.author and str(reaction.emoji) == '✖')
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        except:
            await message.delete()
            return
        match reaction.emoji:
            case "➡" :
                iteration+=1
                await message.delete()
                embed = discord.Embed(
                    title="Anime",
                    description=f"страница №{iteration}",
                    color=discord.Colour.blurple(),  # Pycord provides a class with default colors you can choose from
                )
                embed.set_image(url=data[iteration][2])
                embed.add_field(name=data[iteration][0], value=data[iteration][1])
                message = await ctx.channel.send(embed=embed)
            case "📄" :
                await message.delete()
                await ctx.channel.send ("Больше информации")
            case "✖":
                await message.delete()
                print("Выход")
                break
@bot.slash_command(name='search_anime_by_year', description='Поиск аниме по дате выхода', guild_ids=[1028741714401296444])
async def search_anime_by_year(ctx,year):
    iteration = 1
    qeue = 0
    chanel = ctx.channel
    list = await DB.anime_on_year(year)
    embed = discord.Embed(
        title="Anime",
        description=f"Топ аниме {year} года",
        color=discord.Colour.blurple(),
    )
    embed.add_field(name=f"**{list[qeue][1]}**", value=f"рейтинг {list[0][3]}🌟",inline=False)
    qeue+=1
    while qeue%10 != 0 and qeue!= len(list)-1:
        qeue+=1
        embed.add_field(name="-----------------------------",value='', inline=False)
        embed.add_field(name=f"**{list[qeue][1]}**", value=f"рейтинг {list[qeue][3]}🌟",inline=False)
    embed.set_author(name=f"{bot.user.display_name}", icon_url=bot.user.avatar.url)
    message = await ctx.channel.send(embed=embed)
    while True:
        await message.add_reaction("📄")
        if (qeue!= len(list)-1): await message.add_reaction("➡")
        await message.add_reaction("✖")
        def check(reaction, user):
            return (user == ctx.author and str(reaction.emoji) == '➡') or (user == ctx.author and str(reaction.emoji) == '📄') or (user == ctx.author and str(reaction.emoji) == '✖')
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        except:
            await message.delete()
            return
        match reaction.emoji:
            case "➡" :
                iteration+=1
                await message.delete()
                embed = discord.Embed(
                    title="Anime",
                    description=f"Топ аниме {year} года",
                    color=discord.Colour.blurple(),
                )
                embed.set_author(name=f"{bot.user.display_name}", icon_url=bot.user.avatar.url)
                qeue += 1
                embed.add_field(name=f"**{list[qeue][1]}**", value=f"рейтинг {list[qeue][3]}🌟",inline=False)
                while qeue % 10 != 0 and qeue != len(list)-1:
                    qeue += 1
                    embed.add_field(name="-----------------------------",value='', inline=False)
                    embed.add_field(name=f"**{list[qeue][1]}**", value=f"рейтинг {list[qeue][3]}🌟",inline=False)
                message = await chanel.send(embed=embed)
            case "📄" :
                await message.delete()
                view = discord.ui.View(timeout=10)
                view.add_item(hui.anime_selecting(list=list,iteration=iteration))
                await ctx.send('What is your favourite anime?', view=view)
                break
            case "✖":
                await message.delete()
                print("Выход")
                break
@bot.slash_command (name = 'summoner_info', description= 'Поиск призывателей')
async def summoner_info(
    ctx,
    region: discord.Option(str, choices=['ru','en']),
    name,
    tag
    ):
    try: 
        player = await summoner.find(region,name,tag)
        embed = discord.Embed(
        title=player.nick,
        description=f"",
        color=discord.Colour.blurple(),
        )
        embed.set_thumbnail(url=player.icon_url)
        embed.set_author(name=f"{bot.user.display_name}", icon_url=bot.user.avatar.url)
        embed.add_field(name="Уровень", value = player.level)
        embed.add_field(name="Ранг", value = f"{player.rank}\n")
        embed.add_field(name="Игры", value = player.win_lose)
        embed.add_field(name="Винрейт", value =player.winrate)
        #embed.set_image(url=player.rank_icon)
        await ctx.respond(embed=embed)
    except: await ctx.respond("Призыватель не найден :с")

bot.run("MTA5MjA2NDk4NDI2OTMyODQ1NA.G7gcjW.2_fc4lAJ_xuoZ_fRfAu7DV7LzTtCBVO9joVVcA")