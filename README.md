
# 🛒 Korzinka Telegram Bot

Bu Telegram bot "Korzinka" (do‘kon) uchun ishlab chiqilgan. Bot mahsulotlarni ko‘rish, buyurtma berish va ularni boshqarish imkonini beradi.

---

## 📁 Loyihaning Tuzilishi

```
korzinka_bot/
│
├── main.py                 # Botning asosiy fayli
├── config.example.py       # Namuna konfiguratsiya fayli (foydalanuvchi tomonidan sozlanishi kerak)
├── requirements.txt        # Zarur Python kutubxonalar ro‘yxati
└── README.md               # Loyihaga oid hujjat (ushbu fayl)
```

---

## 🚀 Ishga Tushurish

### 1. Repozitoriyani Klon Qiling

```bash
git clone https://github.com/yourusername/korzinka_bot.git
cd korzinka_bot
```

### 2. Virtual Muhit Yaratish (ixtiyoriy, ammo tavsiya etiladi)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate    # Windows
```

### 3. Kutubxonalarni O‘rnatish

```bash
pip install -r requirements.txt
```

### 4. `config.py` faylini yaratish

Repo ichida `config.py` mavjud emas. Iltimos, quyidagicha `config.py` faylini yarating va ma’lumotlarni to‘ldiring:

```python
# config.py
BOT_TOKEN = "YOUR_BOT_TOKEN"
ADMINS = [123456789]  # Telegram ID raqamlari
```
> **Eslatma:** `config.example.py` faylidan nusxa olib foydalanishingiz mumkin.

---

## 🔑 Funksiyalar

- 📦 Mahsulotlarni ko‘rish
- 🛍 Buyurtma qilish
- 🧑‍💼 Admin panel orqali buyurtmalarni ko‘rish va boshqarish
- 📊 Interaktiv tugmalar va bot interfeysi

---

## 👨‍💻 Dasturchi

- [Imomaliyev Javohir]
- [Joxa2047]

---

## 📜 Litsenziya

Ushbu loyiha MIT litsenziyasi asosida tarqatiladi.
