import discord
import os
from discord.ext import commands

from myserver import server_on

class stacia_bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.token = os.getenv("TOKEN")  # ใช้ os.getenv เพื่อดึงตัวแปรสภาพแวดล้อม
        super().__init__(command_prefix='.', *args, **kwargs)

bot = stacia_bot(owner_id=1249683591995326568, case_insensitive=True)

# Assume this is your server's data
total_donations = 1000  # Example total donation amount
total_items_purchased = 500  # Example total items purchased

@bot.event
async def on_ready():
    print(f'{bot.user} Is Ready')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1284570434842529802)  # Replace with your channel ID
    guild = member.guild
    member_count = guild.member_count  # Get the number of members in the guild

    # Send a greeting message first
    # await channel.send(f"🌟 **สวัสดี {member.mention}!**")

    # Create a more visually appealing embed
    embed = discord.Embed(
        title=f"**🌟 ยินดีต้อนรับสู่ {guild.name}! 🌟**",  # Show the server name
        description=(
            f"🎉 **ยินดีต้อนรับ {member.mention}!**\n\n"
            f"🧑 **รับยศได้ที่** <#1284098667162374146>\n"
            f"📜 **อ่านกฎ** <#1284716905294463061>\n"
            f"⚠️ **แจ้งบัค** <#1284720546738602117>\n\n"
            f"👤 **คุณคือสมาชิกคนที่ {member_count} ในเซิร์ฟนี้!**\n"
            f"💰 **ยอดการเติมเงินทั้งหมด: {total_donations} บาท**\n"
            f"🛒 **จำนวนสินค้าที่สั่งซื้อ: {total_items_purchased} ชิ้น**"
        ),
        color=discord.Color.gold(),
        timestamp=discord.utils.utcnow()
    )

    # เพิ่มรูปแบบการตกแต่ง
    embed.set_thumbnail(url=member.avatar.url if member.avatar else "https://message.style/cdn/images/20cbf772182f81672160169a1b9ecba5bdc8d74829ab72420002311ea67a3131.jfif")
    embed.set_image(url="https://i.pinimg.com/originals/2f/56/90/2f5690ee185f5345025b1a5b0bf2c8aa.gif")  # รูปแบนเนอร์หรือรูปภาพสวยๆ ด้านล่าง
    embed.set_footer(text="บอทนี้เขียนโดย https://www.facebook.com/alpharia.2024/")
    embed.add_field(name="🔗 เช็คสถานะ", value="[เข้าชมเว็บไซต์ของเรา!](https://example.com)", inline=False)

    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1284570434842529802)  # Replace with your channel ID
    guild = member.guild
    remaining_members = guild.member_count  # Get the number of remaining members

    # Send a farewell message first
    # await channel.send(f"😢 **ลาก่อน {member.mention}**")

    # Embed for member leaving
    embed = discord.Embed(
        title=f"**👋 {member.display_name} ออกจากเซิร์ฟเวอร์ {guild.name}!**",
        description=(
            f"😢 **{member.mention} ได้ลาออกจากเซิร์ฟเวอร์**\n\n"
            f"📉 **ตอนนี้ในเซิร์ฟเวอร์มีสมาชิกเหลือ {remaining_members} คน**"
        ),
        color=discord.Color.red(),
        timestamp=discord.utils.utcnow()
    )

    # เพิ่มรูปแบบการตกแต่ง
    embed.set_thumbnail(url=member.avatar.url if member.avatar else "https://message.style/cdn/images/20cbf772182f81672160169a1b9ecba5bdc8d74829ab72420002311ea67a3131.jfif")
    embed.set_image(url="https://media1.tenor.com/m/Vs9QNG3lQZUAAAAC/luffy-one-piece.gif")  # ใส่ลิงก์ของ GIF ที่ต้องการที่นี่
    embed.set_footer(text="บอทนี้เขียนโดย https://www.facebook.com/alpharia.2024/")
    
    await channel.send(embed=embed)

# Run the bot
if __name__ == "__main__":
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            bot.load_extension(f'cogs.{file[:-3]}')

    server_on()

    bot.run(os.getenv('TOKEN'))