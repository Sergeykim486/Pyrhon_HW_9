import telebot, functions, random, time
bot = telebot.TeleBot('5891684002:AAF9GzovRLlRapruKpGQLvFxoVGVeuwgB4I')

score = {
    'player': 0,
    'tab': 0,
    'bot': 0
}
firststep = 0
lasttake = 28
curmes = ''

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global firststep
    mark = functions.buttons('Новая игра')
    bot.send_message(message.chat.id, 'Добро пожаловать в CANDYS', reply_markup=mark)
    bot.register_next_step_handler(message, newgame)

@bot.message_handler(content_types=['text'])
def newgame(message):
    global score, firststep, lasttake, curmes
    if message.text == 'Новая игра':
        score = {
            'player': 0,
            'tab': 117,
            'bot': 0
        }
        firststep = random.randint(1, 2)
        curmes = bot.send_message(message.chat.id, functions.showscore(score), reply_markup=functions.newgamebuttons(lasttake, score))
        if firststep == 2:
            bot.send_message(message.chat.id, 'Бот делает первый ход')
            score = functions.botstep(score)
            time.sleep(2)
            bot.edit_message_text(chat_id = message.chat.id, message_id = curmes.id, text = functions.showscore(score), reply_markup=functions.newgamebuttons(lasttake, score))

@bot.callback_query_handler(func=lambda call: True)

def playerstep(call):
    global lasttake, score, curmes
    command = call.data
    if score['tab'] < 28:
        maxcandys = int(score['tab'])
        lasttake = maxcandys
    else:
        maxcandys = 28
    if score['tab'] > 0:
        if call.data == '+':
            if lasttake < maxcandys:
                lasttake += 1
            else:
                lasttake = 1
            bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = curmes.id, reply_markup = functions.newgamebuttons(lasttake, score))
        elif call.data == '-':
            if lasttake > 1:
                lasttake -= 1
            else:
                lasttake = maxcandys
            bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = curmes.id, reply_markup = functions.newgamebuttons(lasttake, score))
        elif call.data == 'take':
            score['tab'] -= lasttake
            score['player'] += lasttake + score['bot']
            score['bot'] = 0
            print(f'i take {lasttake} candys')
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = curmes.id, text = functions.showscore(score), reply_markup = functions.newgamebuttons(lasttake, score))
            if score['tab'] > 0:
                score = functions.botstep(score)
                time.sleep(2)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = curmes.id, text = functions.showscore(score), reply_markup = functions.newgamebuttons(lasttake, score))
            else:
                if score['bot'] == 0:
                    bot.send_message(call.message.chat.id, 'ПОЗДРАВЛЯЮ!\nВы выйграли')
                    bot.edit_message_text(chat_id = call.message.chat.id, message_id = curmes.id, text = functions.showscore(score), reply_markup = functions.buttons('Новая игра'))
                elif score['player'] == 0:
                    bot.send_message(call.message.chat.id, 'УВЫ!\nБот выйграл')
                    bot.send_message(call.message.chat.id, functions.showscore(score), reply_markup = functions.buttons('Новая игра'))
                bot.register_next_step_handler(message, newgame)

bot.polling(none_stop=True, interval=0)