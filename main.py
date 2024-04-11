import telebot
import requests
from datetime import datetime, timezone, timedelta

bot = telebot.TeleBot('6455915723:AAG9v7ybCFo9ITXabfR4Bpuqyi7XCGrHjUw')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот погоды, отправь мне название города, и я скажу тебе погоду.")

@bot.message_handler(func=lambda message: True)
def send_weather(message):
    city = message.text
    weather_api_key = '08f3286fcbcf8355e18456dda983aad8'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&appid={weather_api_key}&units=metric'
    response = requests.get(url)
    weather_data = response.json()

    if weather_data['cod'] == 200:
        description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        pressure = weather_data['main']['pressure']
        visibility = weather_data['visibility'] / 1000
        sunrise = weather_data['sys']['sunrise']
        sunset = weather_data['sys']['sunset']

        moscow_tz = timezone(timedelta(hours=3))
        sunrise = datetime.utcfromtimestamp(weather_data['sys']['sunrise']).replace(tzinfo=timezone.utc).astimezone(moscow_tz)
        sunset = datetime.utcfromtimestamp(weather_data['sys']['sunset']).replace(tzinfo=timezone.utc).astimezone(moscow_tz)
        message_to_send = f"Погода в {city}:\nОписание: {description}\nТемпература: {temperature}°C\nВлажность: {humidity}%\nСкорость ветра: {wind_speed} м/с\nДавление: {pressure} гПа\nВидимость: {visibility} км\nВосход солнца: {sunrise}\nЗакат солнца: {sunset}"
        bot.reply_to(message, message_to_send)
    else:
        bot.reply_to(message, "Извините, не могу получить данные о погоде для этого города.")

bot.polling()