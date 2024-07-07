import discord
import anime_db
import parsetest
class anime_selecting(discord.ui.Select):
    def __init__(self, list,iteration):
        options =[]
        for i in range(iteration*10):
            options.append(discord.SelectOption(label=list[i][1], description='Your favourite anime', emoji='🟦'))
        super().__init__(placeholder='Pick your colour', min_values=1, max_values=1, options=options)
    async def callback(self,interaction):
        anime = await anime_db.on_name_finder(self.values[0])
        more_info = await parsetest.more_info(anime[0][4])
        embed = discord.Embed(
        title=f"{anime[0][1]}",
        description=f"",
        color=discord.Colour.blurple(),
        )
        #embed.set_author(name=f"{bot.user.display_name}", icon_url=bot.user.avatar.url)
        embed.set_image(url=anime[0][2])
        embed.add_field(name="Жанр:",value=anime[0][6])
        embed.add_field(name="Рейтинг",value=anime[0][3])
        if more_info[0][3]=="None":
            embed.add_field(name="Серии", value=more_info[0][1])
        else:
            embed.add_field(name="Серии", value=more_info[0][1])
            embed.add_field(name="Статус",value=more_info[0][3])
        embed.add_field(name="Описание",value=more_info[0][2])
        await interaction.response.send_message(embed=embed)