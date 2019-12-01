import sqlite3
import random

def add_balls(texts):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE promizh SET balls=:balls WHERE name_is=:name_is', {'name_is': texts, 'balls': 1})
    conn.commit()
    cursor.close()
    conn.close()


def reduse_balls(texts):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE promizh SET balls=:balls WHERE name_is=:name_is', {'name_is': texts, 'balls': 0})
    conn.commit()
    cursor.close()
    conn.close()

def reset_balls():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE promizh SET balls=:balls', {'balls': 0})
    conn.commit()
    cursor.close()
    conn.close()

def admin_is_add(first_name, count_is):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE promizh SET count_is=:count_is WHERE first_name=:first_name', {'first_name': first_name, 'count_is': count_is})
    conn.commit()
    cursor.close()
    conn.close()

def statistics():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM main_table')
    t = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    a = ''
    for i in t:
        a += str(i[0]) + ': ' + str(i[2]) +'\n'
    return a

def who_today():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM main_table')
    t = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    a = []
    if (int(t[0][2]) > int(t[1][2])) and ((int(t[1][2]) >= int(t[2][2])) or (int(t[0][2]) >= int(t[2][2]))):
        a.append(str(t[1][0]))
        a.append(str(t[2][0]))
        a.append(str(t[0][0]))
    elif (int(t[1][2]) > int(t[0][2])) and ((int(t[0][2]) >= int(t[2][2])) or (int(t[1][2]) >= int(t[2][2]))):
        a.append(str(t[0][0]))
        a.append(str(t[2][0]))
        a.append(str(t[1][0]))
    elif (int(t[2][2]) > int(t[0][2])) and ((int(t[0][2]) >= int(t[1][2])) or (int(t[2][2]) >= int(t[1][2]))):
        a.append(str(t[1][0]))
        a.append(str(t[0][0]))
        a.append(str(t[2][0]))
    return a

def set_balls():
    a = 0
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM promizh')
    t = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    for i in t:
        if i[1] == 1:
            conn = sqlite3.connect('base.db')
            cursor = conn.cursor()
            cursor.execute('SELECT count_is FROM main_table WHERE name_is=:name_is', {'name_is': i[0]})
            x = cursor.fetchone()[0]
            count_is = x + i[1]
            cursor.execute('UPDATE main_table SET count_is=:count_is WHERE name_is=:name_is',
                           {'name_is': i[0], 'count_is': count_is})
            conn.commit()
            cursor.close()
            conn.close()
            a +=1

    if a == 1:
        for i in t:
            if i[1] == 1:
                conn = sqlite3.connect('base.db')
                cursor = conn.cursor()
                cursor.execute('SELECT count_is FROM main_table WHERE name_is=:name_is', {'name_is': i[0]})
                x = cursor.fetchone()[0]
                count_is = x + i[1]
                cursor.execute('UPDATE main_table SET count_is=:count_is WHERE name_is=:name_is',
                               {'name_is': i[0], 'count_is': count_is})
                conn.commit()
                cursor.close()
                conn.close()

    reset_balls()

def talkative_off():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT count_of FROM talkative')
    t = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    if t > 50:
        count_of = t - 10
    else:
        count_of = 50
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE talkative SET count_of=:count_of',
                   {'count_of': count_of})
    conn.commit()
    cursor.close()
    conn.close()
    return count_of - 50

def talkative_on():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT count_of FROM talkative')
    t = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    if t < 100:
        count_of = t + 10
    else:
        count_of = 100
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE talkative SET count_of=:count_of',
                   {'count_of': count_of})
    conn.commit()
    cursor.close()
    conn.close()
    return count_of - 50

def tallkative_is():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT count_of FROM talkative')
    t = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return t

def get_answer(question):
    q = str(question).replace('!','').replace('@','').replace('#','').replace('$','').replace('%','').replace('^','').replace('&','').replace('*','').replace('(','').replace(')','').replace('_','').replace('-','').replace('+','').replace('=','').replace('?','').replace('/','').replace(':','').replace(';','').replace('<','').replace('>','').replace('{','').replace('}','').replace('[','').replace(']','').replace('|','').replace('.','').replace(',','')
    qw = q.lower().split(' ')
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT questions FROM answers_questions')
    t = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    last = ''
    for i in t:
        n = 0
        xz = str(i[0]).split(' ')
        for j in qw:
            for l in xz:
                if l == j:
                    n += 1
                    break

        if n // len(xz) * 100 > 60:
            last = i
            break
    end_is = '*'

    if last != '':
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute('SELECT answers FROM answers_questions WHERE questions=:questions', {'questions':last[0]})
        z = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()

        end_is = random.choice(z)

    return end_is[0]

def set_answer_and_questions(question):
    q = str(question).replace('!','').replace('@','').replace('#','').replace('$','').replace('%','').replace('^','').replace('&','').replace('*','').replace('(','').replace(')','').replace('_','').replace('-','').replace('+','').replace('=','').replace('?','').replace('/','').replace(':','').replace(';','').replace('<','').replace('>','').replace('{','').replace('}','').replace('[','').replace(']','').replace('|','').replace('.','').replace(',','')
    qw = q.lower()
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE answers_questions SET answers=:answers WHERE answers=:answers_', {'answers_': 'None', 'answers':question})
    cursor.execute('INSERT INTO answers_questions (answers, questions) VALUES (?, ?)', ('None', qw))
    conn.commit()
    cursor.close()
    conn.close()
