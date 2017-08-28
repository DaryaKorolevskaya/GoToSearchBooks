import telebot
import requests

tokenbot = "406696396:AAFDf1SIqBuRZodIXwYN1iNEUFYnfRIacvs"
token = "7fd81a935ced84e8a86eb239f7a9657733d050b1db9a1ba840a3ee9d82b92f811cff2647ad5efcc157f40"
url = "https://api.vk.com/method/{method}?{params}&access_token={token}&v={version}"
method = "docs.search"
v = 5.68

bot = telebot.TeleBot(token=tokenbot)

data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user = message.chat.id
    bot.send_message(user, "Привет! Я найду книгу, которая тебе нужна. Напиши ее автора и название!")

@bot.message_handler(content_types=["text"])
def find(message):
    user = message.chat.id
    query = message.text
    data[user] = query[:10]
    params = "q={0}&count=5&offset={1}"
    bot.send_message(user, "А теперь подожди минуточку...")
    # скачиваем ссылки по нужному нам запросу
    items = []
    for i in range(0, 11):
        print("downloading - {}".format(i))
        response = requests.get(url.format(method=method, version=v, params=params.format(query, 0), token=token))
        result = response.json()
        count = result['response']['count']
        items += result['response']['items']

    # выводим ссылки на скачивание
    i=0
    g=0
    for item in items[:11]:
      print(item['ext'])
      if item['ext'] == "fb2" or item['ext'] == "pdf":
          if g==0:
              bot.send_message(user, "Вот, что я нашел:")
              g=1
          i+=1
          print(item)
          bot.send_message(user, item['title'])
          bot.send_message(user, item['url'])
          if i > 2:
              break
    if i==0:
        bot.send_message(user, "Прости, к сожалению, я не нашел такой книги :(")

bot.polling(none_stop=True)