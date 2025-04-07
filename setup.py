from setuptools import setup, find_packages

# Чтение зависимостей из файла requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="telegram_monitoring",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Telegram Monitoring Bot using Telethon for monitoring channels with marker words",
    packages=find_packages(),  # Если структура проекта подразумевает пакеты
    install_requires=requirements,
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            # Предполагается, что функция main() находится в файле bot.py
            'telegram_monitor=bot:main',
        ],
    },
)
