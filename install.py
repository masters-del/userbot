import os
import subprocess
import sys
import time

# Функция для запуска системных команд
def sh(command):
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except:
        return False

def setup():
    print("\n" + "="*40)
    print("🚀  STUPID USERBOT - AUTO INSTALLER  🚀")
    print("="*40 + "\n")

    # 1. Проверка среды (Termux или PC)
    is_termux = os.path.exists("/data/data/com.termux")
    
    print(f"🔍 Определена система: {'Termux' if is_termux else 'PC'}")
    time.sleep(1)

    # 2. Установка системных зависимостей
    if is_termux:
        print("📦 Обновление и установка системных пакетов...")
        sh("pkg update -y && pkg upgrade -y")
        sh("pkg install git python ffmpeg libjpeg-turbo -y")
    else:
        print("📦 Проверка Git...")
        if not sh("git --version"):
            print("❌ Git не найден! Установи его: https://git-scm.com")
            return

    # 3. Установка библиотек Python
    print("\n📚 Установка зависимостей Python...")
    libs = ["telethon", "python-dotenv", "gtts", "requests", "pillow"]
    sh(f"{sys.executable} -m pip install --upgrade pip")
    sh(f"{sys.executable} -m pip install {' '.join(libs)}")

    # 4. Клонирование репозитория (если запускается не из папки бота)
    if not os.path.exists("main.py"):
        print("\n📂 Клонирование репозитория...")
        repo_url = input("Введите ссылку на ваш GitHub репозиторий: ").strip()
        sh(f"git clone {repo_url} bot_temp")
        sh("cp -r bot_temp/* . && rm -rf bot_temp")

    # 5. Создание .env файла
    if not os.path.exists(".env"):
        print("\n🔑 Настройка доступа (API ID/Hash брать на my.telegram.org):")
        api_id = input("Введите API_ID: ").strip()
        api_hash = input("Введите API_HASH: ").strip()
        with open(".env", "w", encoding="utf-8") as f:
            f.write(f"API_ID={api_id}\nAPI_HASH={api_hash}\n")
        print("✅ Файл конфигурации .env создан!")
    else:
        print("\n✅ Конфигурация .env уже существует.")

    print("\n" + "="*40)
    print("🎉 УСТАНОВКА ЗАВЕРШЕНА УСПЕШНО!")
    print("="*40)
    print("\nКоманда для запуска бота:")
    print("👉 python main.py")
    print("\n" + "="*40)

if __name__ == "__main__":
    setup()