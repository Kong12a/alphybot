import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, InputText
import requests
import mysql.connector

# เชื่อมต่อกับฐานข้อมูล MySQL
try:
    db = mysql.connector.connect(
        host="bhfzkcw6h9o6pheqvmm7-mysql.services.clever-cloud.com",
        user="ucvmfdraedrvbjuy",
        password="lc0bkqgnudvsyA2ZdGa1",
        database="bhfzkcw6h9o6pheqvmm7"
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

class AddUserModal(Modal):
    def __init__(self):
        super().__init__(title="【 Create 】")
        self.add_item(InputText(label="USERNAME (RANDOM = อุ่นชื่อ)", placeholder="username 3-20 character", required=True))
        self.add_item(InputText(label="PASSWORD (เว้นว่างเพื่อลุ้น)", placeholder="password 1-20 character", required=False, style=discord.InputTextStyle.short))
        self.add_item(InputText(label="AMOUNT (สูงสุด 100 ID/ครั้ง)", placeholder="amount (maximum 100)", required=True))

    async def callback(self, interaction: discord.Interaction):
        username = self.children[0].value
        password = self.children[1].value
        amount = self.children[2].value
        await interaction.response.send_message(f"เพิ่มผู้ใช้สำเร็จ!\nUsername: {username}\nPassword: {password or 'สุ่ม'}\nAmount: {amount}", ephemeral=True)

class DonationBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="top_donors", description="Displays the top 10 donors")
    async def top_donors(self, ctx):
        try:
            cursor.execute("SELECT username, amount FROM topups ORDER BY amount DESC LIMIT 10")
            results = cursor.fetchall()

            description = "\n".join([f"**{i+1}.** {row[0]} - **{row[1]:,}** บาท" for i, row in enumerate(results)])
            embed = discord.Embed(title="🏆 อันดับการเติมเงินสูงสุด 10 อันดับ 🏆", description=description, color=discord.Color.green())
            embed.set_thumbnail(url="https://i.imgur.com/4M34hi2.png")
            embed.set_footer(text="ระบบนี้ถูกพัฒนาโดยทีมงาน", icon_url="https://i.imgur.com/AfFp7pu.png")
            embed.set_image(url="https://i.pinimg.com/originals/2f/56/90/2f5690ee185f5345025b1a5b0bf2c8aa.gif")
            view = View(timeout=None)

            # ปุ่มเพิ่มผู้ใช้
            button_user = Button(label="เพิ่มผู้ใช้", style=discord.ButtonStyle.green, emoji="👤")
            async def button_user_callback(interaction):
                await interaction.response.send_modal(AddUserModal())
            button_user.callback = button_user_callback
            view.add_item(button_user)

            # ปุ่มเติมเงิน
            button_topup = Button(label="เติมเงิน", style=discord.ButtonStyle.blurple, emoji="💰")
            async def button_topup_callback(interaction):
                await interaction.response.send_modal(TopUpModal())
            button_topup.callback = button_topup_callback
            view.add_item(button_topup)

            # ปุ่มทดสอบเติมเงิน
            button_test_topup = Button(label="ทดสอบเติมเงิน", style=discord.ButtonStyle.red, emoji="🔧")
            async def button_test_topup_callback(interaction):
                await interaction.response.send_modal(TestTopUpModal())
            button_test_topup.callback = button_test_topup_callback
            view.add_item(button_test_topup)

            # ปุ่มเมนู
            button_menu = Button(label="เมนู", style=discord.ButtonStyle.gray, emoji="📜")
            async def button_menu_callback(interaction):
                await interaction.response.send_message("เมนูหลัก: [กดที่นี่](https://example.com/menu)", ephemeral=True)
            button_menu.callback = button_menu_callback
            view.add_item(button_menu)

            await ctx.respond(embed=embed, view=view)
        except mysql.connector.Error as err:
            await ctx.respond(f"❌ การดึงข้อมูลจากฐานข้อมูลล้มเหลว: {err}", ephemeral=True)

class TopUpModal(Modal):
    def __init__(self):
        super().__init__(title="เติมเงิน")
        self.add_item(InputText(label="กรุณากรอกรหัสอังเปา", placeholder="รหัสอังเปา", required=True))

    async def callback(self, interaction: discord.Interaction):
        code = self.children[0].value
        try:
            response = requests.post('https://alphybot.onrender.com/topup', json={'code': code})
            result = response.text
            print(result)  # พิมพ์ค่าที่ได้รับจาก API
            response.raise_for_status()  # ตรวจสอบรหัสสถานะ HTTP
            if response.status_code == 200:
                amount = int(result.split('จำนวน ')[1].split(' แล้ว!')[0])
                print(amount)
                username = interaction.user.name
                
                # บันทึกข้อมูลลง MySQL
                cursor.execute("INSERT INTO topups (username, amount) VALUES (%s, %s)", (username, amount))
                db.commit()

                await interaction.response.send_message(f"✅ เติมเงินสำเร็จ! จำนวนเงินที่เติม: {amount} บาท", ephemeral=True)
            else:
                await interaction.response.send_message(f"❌ ลิ้งค์อังเปาไม่ถูกต้องหรือถูกใช้งานแล้ว", ephemeral=True)
        except requests.RequestException as e:
            await interaction.response.send_message(f"❌ การเชื่อมต่อ API ล้มเหลว: {e}", ephemeral=True)

class TestTopUpModal(Modal):
    def __init__(self):
        super().__init__(title="ทดสอบเติมเงิน")
        self.add_item(InputText(label="จำนวนเงินที่ต้องการเติม (บาท)", placeholder="จำนวนเงิน", required=True))

    async def callback(self, interaction: discord.Interaction):
        amount = self.children[0].value
        username = interaction.user.name
        
        # บันทึกข้อมูลลง MySQL
        try:
            cursor.execute("INSERT INTO topups (username, amount) VALUES (%s, %s)", (username, amount))
            db.commit()
            await interaction.response.send_message(f"✅ ทดสอบเติมเงินสำเร็จ! จำนวนเงินที่เติม: {amount} บาท", ephemeral=True)
        except mysql.connector.Error as err:
            await interaction.response.send_message(f"❌ การบันทึกข้อมูลล้มเหลว: {err}", ephemeral=True)

def setup(bot):
    bot.add_cog(DonationBot(bot))

