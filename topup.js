const express = require('express');
const bodyParser = require('body-parser');
const twvoucher = require('@fortune-inc/tw-voucher');

const app = express();
app.use(bodyParser.json());

app.post('/topup', async (req, res) => {
    const { code } = req.body;
    
    if (!code) return res.status(400).send('❌ | กรุณาระบุลิ้งอังเปา');
    
    try {
        const redeemed = await twvoucher('0638430912', code);
        // บันทึกข้อมูลลงฐานข้อมูลที่นี่
        res.send('✅ | เติมเงินจำนวน ' + redeemed.amount + ' แล้ว!');
    } catch (err) {
        res.status(400).send('❌ | ลิ้งอังเปาถูกใช้งานแล้ว');
    }
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
