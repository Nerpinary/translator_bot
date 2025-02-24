#!/bin/bash

mkdir -p temp

echo "🚀 Запуск бота..."

cleanup() {
    echo "👋 Бот остановлен $(date '+%Y-%m-%d %H:%M:%S')"
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "✅ Бот запущен $(date '+%Y-%m-%d %H:%M:%S')"
python3 run.py

echo "❌ Бот завершил работу $(date '+%Y-%m-%d %H:%M:%S')"