import os
import subprocess
import sys
import time

# Функция для запуска системных команд
def sh(command):
    try:
        # Добавляем флаг игнорирования системных пакетов для новых Linux/Mac
        if "--break-system-packages" not in command and "pip install" in command:
            if not os.name == 'nt': # Если не Windows
                command += " --break-system-packages"
        subprocess.run(command, shell=True, check=True)
        return True
    except:
        return False

def setup():
    print("\n" + "="*45)
    print("🚀  STUPID USERBOT v9.3 - AUTO INSTALLER  🚀")
    print("="*45 + "\n")

    # 1. Проверка среды (Termux, Mac или PC)
    is_termux = os.path.exists("/data/data/com.termux")
    is_mac = sys.platform == "darwin"
    
    print(f"🔍 Система: {'Termux' if is_termux else 'MacOS' if is_mac else 'Windows/Linux'}")
    time.sleep(1)

    # 2. Установка системных зависимостей
    if is_termux:
        print("📦 [Termux] Установка системных пакетов...")
        sh("pkg update -y && pkg upgrade -y")
        # Добавлены зависимости для сборки тяжелых библиотек
        sh("pkg install git python clang make libffi openssl binutils ffmpeg -y")
    else:
        print("📦 Проверка Git...")
        if not sh("git --version"):
            print("❌ Git не найден! Установи его: https://git-scm.com")
            return

    # 3. Установка библиотек Python (ОБНОВЛЕННЫЙ СПИСОК)
    print("\n📚 Установка зависимостей Python...")
    # Добавлены: google-generativeai, colorama
    libs = ["telethon", "python-dotenv", "google-generativeai", "gtts", "colorama", "requests", "pillow"]
    
    sh(f"{sys.executable} -m pip install --upgrade pip")
    print(f"⏳ Устанавливаю: {', '.join(libs)}...")
    sh(f"{sys.executable} -m pip install {' '.join(libs)}")

    # 4. Клонирование репозитория
    if not os.path.exists("main.py"):
        print("\n📂 Клонирование репозитория...")
        repo_url = input("Введите ссылку на ваш GitHub репозиторий: ").strip()
        if sh(f"git clone {repo_url} bot_temp"):
            # Команда для перемещения файлов зависит от ОС
            move_cmd = "move bot_temp\\* ." if os.name == 'nt' else "cp -r bot_temp/* . && rm -rf bot_temp"
            sh(move_cmd)
        else:
            print("❌ Ошибка при клонировании!")

    # 5. Создание .env файла (автоматическая настройка)
    if not os.path.exists(".env"):
        print("\n🔑 Настройка доступа (API ID/Hash брать на my.telegram.org):")
        api_id = input("Введите API_ID: ").strip()
        api_hash = input("Введите API_HASH: ").strip()
        with open(".env", "w", encoding="utf-8") as f:
            f.write(f"API_ID={api_id}\nAPI_HASH={api_hash}\n")
        print("✅ Файл конфигурации .env создан!")
    else:
        print("\n✅ Конфигурация .env уже существует.")

    print("\n" + "="*45)
    print("🎉 УСТАНОВКА ЗАВЕРШЕНА УСПЕШНО!")
    print("👉 Теперь просто напиши: python main.py")
    print("="*45)

if __name__ == "__main__":
    setup()