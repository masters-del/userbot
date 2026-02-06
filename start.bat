@echo off
title UserBot Starter v6.2
chcp 65001 >nul
color 0b

echo 🔍 Проверка и установка библиотек...
:: Авто-установка всех нужных либ
python -m pip install --upgrade pip
pip install telethon python-dotenv gtts requests pillow

cls
echo ✅ Библиотеки проверены! Запускаю бота...
echo ---------------------------------------
python main.py
pause