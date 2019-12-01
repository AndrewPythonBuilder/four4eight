import constants, base_w
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Contact, KeyboardButton, ChatMember, ChatAction, InlineQueryResultArticle, InputTextMessageContent, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, InlineQueryHandler
import logging
import random
import datetime
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
updater = Updater(token=constants.token)
dispatcher = updater.dispatcher

job_queue = updater.job_queue

def start(bot, update):
    message = update.message
    if message.chat.id == constants.admin:
        bottons = [['Обновить очки']]
        keyboard = ReplyKeyboardMarkup(bottons, resize_keyboard=True)
        bot.send_message(message.chat.id, 'Привет, красавчик!)))', reply_markup= keyboard)
    else:
        bot.send_message(message.chat.id, 'Приветстую, мои друзья по кругу, и Димка!')

def answer_questions(bot, update):
    message = update.message
    text = ''
    flag = True
    if message.chat.id == constants.admin:
        if message.text == 'Завершить':
            base_w.set_balls()
            bottons = [['Обновить очки']]
            keyboard = ReplyKeyboardMarkup(bottons, resize_keyboard=True)
            bot.send_message(message.chat.id, 'Работа закончена', reply_markup= keyboard)
            bot.send_message(-186360476, 'Жеребьевка окончена')

    else:
        for i in constants.name:
            if i in str(message.text).lower():
                text += random.choice(constants.hello)+message.from_user.first_name + '.\n'

                if ('тише' in str(message.text).lower()) or ('заткнись' in str(message.text).lower()):
                    k = base_w.talkative_off()
                    text += 'Обидно так-то...\nВероятность того, что я скажу что-нибудь теперь равняется '+ str(k/50) + '\n'

                elif ('громче' in str(message.text).lower()) or ('болтай' in str(message.text).lower()):
                    k = base_w.talkative_on()
                    text += 'Благодарю, любезный, '+ message.from_user.first_name + '!\nВероятность того, что я скажу что-нибудь теперь равняется '+ str(k/50) + '\n'

                if ('думаешь' in str(message.text).lower()) or ('дум' in str(message.text).lower()):
                    text += random.choice(constants.thinking) + '\n'

                if 'статистик' in str(message.text).lower():
                    a = base_w.statistics()
                    text += a

                flag = False

        answer_the_question = base_w.get_answer(message.text)

        if answer_the_question != '*':
            text += answer_the_question + '\n'

        if ((random.randint(0, base_w.tallkative_is()) > 50) and (text != '')) or ('Да пошел ты по кругу' in text):
            bot.send_message(message.chat.id, text)

        if flag != False:
            base_w.set_answer_and_questions(message.text)

def button_answers(bot, update):
    query = update.callback_query
    if 'Me' == str(query.data):
        bot.send_message(-186360476, query.from_user.first_name + ' ++ к рейтингу')
        base_w.add_balls(query.from_user.id)
    else:
        bot.send_message(-186360476, query.from_user.first_name + ', эх ты, какашка')
        base_w.reduse_balls(query.from_user.id)

def who_will(bot, update):
    base_w.reset_balls()
    text = 'Кто сегодня будет мыть посуду сегодня?'
    x = base_w.who_today()
    if  x == []:
        buttons = [[InlineKeyboardButton('Я', callback_data='Me'),InlineKeyboardButton('Не я', callback_data='Not_Me')]]
        keyboard = InlineKeyboardMarkup(buttons)
        bot.send_message(-186360476, text, reply_markup=keyboard)
        bottons = [['Завершить']]
        keyboard = ReplyKeyboardMarkup(bottons, resize_keyboard=True)
        bot.send_message(constants.admin, 'Стартовала жеребьевка', reply_markup=keyboard)
    else:
        text+= '\n' + x[0] + ' и ' + x[1]
        buttons = [
            [InlineKeyboardButton('Ладно', callback_data='Me'), InlineKeyboardButton('В другой раз', callback_data='Not_Me')]]
        keyboard = InlineKeyboardMarkup(buttons)
        bot.send_message(-186360476, text + '\nИтак, '+x[2]+' можешь не голосовать, или ответь "В другой раз".\nТы и так молодец!)', reply_markup=keyboard)
        bottons = [['Завершить']]
        keyboard = ReplyKeyboardMarkup(bottons, resize_keyboard=True)
        bot.send_message(constants.admin, 'Стартовала жеребьевка' , reply_markup=keyboard)


def time_job(bot, update, job_queue):
    t = datetime.time(18,00,10,0)
    job_queue.run_daily( who_will, t, days=tuple(range(7)), context=update)

updater.dispatcher.add_handler(CallbackQueryHandler(button_answers))
updater.dispatcher.add_handler(CommandHandler('notify', time_job, pass_job_queue=True))
start_handler = CommandHandler('start', start)
answer_handler = MessageHandler(Filters.all, answer_questions)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(answer_handler)
updater.start_polling(timeout=5, clean=True)