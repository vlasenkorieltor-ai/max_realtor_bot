cat > bot.py << 'EOF'
import asyncio
import logging
import json
import os
from datetime import datetime
from maxapi import Bot, Dispatcher
from maxapi.types import MessageCreated

logging.basicConfig(level=logging.INFO)

TOKEN = 'f9LHodD0cOKKBxoiRXKlgLzK50BZM3nGlDZ3NpFXA_J0mNYO2K4cYX0uhx6JszEVNt5GgG7HawMp8CUGyfPi'

CHAT_IDS = {
    "Мир Квартир Сочи": -73368178474297,
    "Мир Домов Сочи": -73381264702777,
    "Мир земли Сочи": -73381239668025,
}

STATE_FILE = os.path.expanduser("~/bot_replied.json")

def load_replied():
    if not os.path.exists(STATE_FILE):
        return set()
    try:
        with open(STATE_FILE, 'r') as f:
            data = json.load(f)
        today = datetime.now().date().isoformat()
        return {tuple(item) for item in data if item[0] == today}
    except:
        return set()

def save_replied(replied_set):
    with open(STATE_FILE, 'w') as f:
        json.dump([list(item) for item in replied_set], f)

replied = load_replied()

# ========== РАСПИСАНИЕ (полные тексты) ==========
SCHEDULE = [
    # МИР КВАРТИР СОЧИ
    (8, "Мир Квартир Сочи", '''*"МИНИСТЕРСКИЕ ОЗЕРА"*
«КОМФОРТ» квартал 
✅ *КОЛ-ВО КОМНАТ* - 1-к.;
✅ *ПЛОЩАДЬ* - 36м2;
✅ *ЭТАЖ*- 16 эт.;
✅ *РЕМОНТ*- Чистовая под Ваш проект;
💰 *ЦЕНА: 8'500'000₽*

Отдел продаж Министерские Озера: 
89891229902 - Мессенджер Макс. 89952269902 - Мой номер телефона'''),

    (12, "Мир Квартир Сочи", '''*"МИНИСТЕРСКИЕ ОЗЕРА"*
«КОМФОРТ» квартал 
✅ *КОЛ-ВО КОМНАТ* - 2-к.;
✅ *ПЛОЩАДЬ* - 60м2;
✅ *ЭТАЖ*- 1эт.;
✅ *РЕМОНТ*- С ремонтом, мебелью и техникой;
💰 *ЦЕНА: 14'900'000₽*

Отдел продаж Министерские Озера: 
89891229902 - Мессенджер Макс. 89952269902 - Мой номер телефона'''),

    (16, "Мир Квартир Сочи", '''*"МИНИСТЕРСКИЕ ОЗЕРА"*
«КОМФОРТ» квартал 
✅ *КОЛ-ВО КОМНАТ* - ЕВРО 3-к.;
✅ *ПЛОЩАДЬ* - 70м2;
✅ *ЭТАЖ*- Средний;
✅ *РЕМОНТ*- С качественным ремонтом, премиальной мебелью и техникой;
💰 *ЦЕНА: 17'500'000₽*

Отдел продаж Министерские Озера: 
89891229902 - Мессенджер Макс. 89952269902 - Мой номер телефона'''),

    (18, "Мир Квартир Сочи", '''*ЗАВОКЗАЛЬНЫЙ РАЙОН*
*АРЕДА* До жд вокзала 10 минут, пешком. До Альпийского квартала 5 минут пешком. 

* 3 комнатная  110 м2 * 4 световые точки 
* Этаж-* 2 этаж 
* СТАТУС КВАРТИРА*
* НОВЫЙ ДОМ*
* ПОД ВАШ ДИЗАЙНЕРСКИЙ ПРОЕКТ*
* НЕТ ОБРЕМЕНЕНИЙ*

*Цена 16.000.000  

89891229902 - Мессенджер Макс. 89952269902 - Мой номер телефона'''),

    (19, "Мир Квартир Сочи", '''*ЗАВОКЗАЛЬНЫЙ РАЙОН*
*АРЕДА* До жд вокзала 10 минут, пешком. До Альпийского квартала 5 минут пешком. 

* студия  23,3 м2*
* Этаж-1* отдельный вход 
* СТАТУС КВАРТИРА*
* НОВЫЙ ДОМ*
* ПОД ВАШ ДИЗАЙНЕРСКИЙ ПРОЕКТ*
* НЕТ ОБРЕМЕНЕНИЙ*

*Цена 6'000'000₽* 

89891229902 - Мессенджер Макс. 89952269902 - Мой номер телефона'''),

    # МИР ДОМОВ СОЧИ
    (12, "Мир Домов Сочи", '''Продаю дом на улице восточная, ст Ветеран 24 центральный Сочи. Хороший ремонт. 
135 м2, баня, бомбический вид, 5 соток земли, участок не требует вложений, 
Все документы в полном порядке. Проходит ипотека. 
Коммуникации - центральные, септик 
Цена ниже себестоимости, за такие деньги в этом месте - в Сочи такое построить не реально 
Цена: 15 млн (1 млн - 50 на 50) 

89891229902 - Мессенджер Макс. 89952269902 - Мой номер телефона'''),

    # МИР ЗЕМЛИ СОЧИ
    (13, "Мир земли Сочи", '''Добрый день! В базу отличное предложение для инвесторов в Сочи.

* Участок 42 сотки в пос. Сергей-Поле (Сочи)* Шикарный вид на море 
*💰 Цена: 45 000 000 руб.
* *Комиссия: 5 000 000 руб. (50/50)*

Ключевые преимущества:
• Разрешенное использование: ИЖС и Предпринимательство.
• Планировка: Уже разделен на 7 лотов по ~5.1 сотки.
• Вид: Панорамный, открывается вид на море.
• Коммуникации: Полностью готовы — свет 120 кВт, вода, газ у границы.
• Документы: Получены ГПЗУ и геология — стройка "с колес".
• Подъезд: Асфальтированная дорога.

89891229902 - Мессенджер Макс. 89952269902 - Мой номер телефона'''),
]

# Ночное сообщение (ссылки во все группы)
NIGHT_MSG = '''🔗 *ССЫЛКИ-ПРИГЛАШЕНИЯ В ГРУППЫ MAX*

🏢 Мир квартир: https://max.ru/join/fy-vBgJWR2a2aN9ZiLsAcvfD1qo6LEP5w51qybUUVSw

🏡 Мир домов: https://max.ru/join/nImAIra_dpgUG_2eClDEqmQquzYYrppt0nzseHB6v44

🌍 Мир Земли: https://max.ru/join/ZMByvivzr_Fsyiz27cBeL3mocuCmtjcjJ4s95kBqs0Y

💰 Мир квартир Сочи до 7млн: https://max.ru/join/9JjPoM0VobwF7e9U_PcGiTo_3aWdCDwWD0zgifaJBqg

📢 Запросы Сочи: https://max.ru/join/wpy1rD0853qUBsIf6KfgoOEWTNsrjq0Xcl5SeBkKXPs

📲 89952269902 - Роман'''

for hour in [23, 0, 1, 2]:
    for group in ["Мир Квартир Сочи", "Мир Домов Сочи", "Мир земли Сочи"]:
        SCHEDULE.append((hour, group, NIGHT_MSG))

SCHEDULE.sort(key=lambda x: x[0])

def get_current_hour():
    return datetime.now().hour

def get_current_date():
    return datetime.now().date().isoformat()

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message_created()
async def handle(event: MessageCreated):
    hour = get_current_hour()
    date = get_current_date()
    
    # ПРАВИЛЬНОЕ ПОЛУЧЕНИЕ ID ЧАТА (из отладки)
    if not hasattr(event, 'chat') or not hasattr(event.chat, 'chat_id'):
        print("❌ Не удалось получить ID чата")
        return
    chat_id = event.chat.chat_id
    
    for h, group_name, text in SCHEDULE:
        if h == hour and chat_id == CHAT_IDS.get(group_name):
            key = (date, hour, chat_id)
            if key in replied:
                return
            try:
                await event.message.answer(text)
                replied.add(key)
                save_replied(replied)
                print(f"✅ {datetime.now().strftime('%Y-%m-%d %H:%M')} | {group_name}")
            except Exception as e:
                print(f"❌ Ошибка при отправке: {e}")
            return

async def main():
    print("=" * 60)
    print("🤖 РИЭЛТОР БОТ ЗАПУЩЕН (исправленная версия с event.chat.chat_id)")
    print("=" * 60)
    print(f"📁 Файл состояния: {STATE_FILE}")
    print(f"📅 Загружено записей за сегодня: {len(replied)}")
    print("📅 РАСПИСАНИЕ (бот отвечает на ПЕРВОЕ сообщение в час):")
    last_hour = None
    for h, g, _ in SCHEDULE:
        if h != last_hour:
            print(f"   {h:02d}:00")
            last_hour = h
        print(f"       → {g}")
    print("=" * 60)
    print("🛡️ Состояние сохраняется в файл и очищается по дням")
    print("=" * 60)
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
EOF
