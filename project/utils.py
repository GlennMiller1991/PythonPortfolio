from project import os, app
from flask import Markup

def swoper_logic(original_text, to_russian) -> str:
    changed_text =''

    english_to_russian = {
                        "`":"ё", "~":"Ё", "@":'"', "#":"№", ";":"$", "^":":", "&":"?",
                        "q":"й", "Q":"Й", "w":"ц", "W":"Ц", "e":"у", "E":"У", "r":"к", "R":"К", "t":"е", "T":"Е", "y":"н", "Y":"Н",
                        "u":"г", "U":"Г", "i":"ш", "I":"Ш", "o":"щ", "O":"Щ", "p":"з", "P":"З", "[":"х", "{":"Х", "]":"ъ", "}":"Ъ", "\\":"\\", "|":"/",
                        "a":"ф", "A":"Ф", "s":"ы", "S":"Ы", "d":"в", "D":"В", "f":"а", "F":"А", "g":"п", "G":"П", "h":"р", "H":"Р",
                        "j":"о", "J":"О", "k":"л", "K":"Л", "l":"д", "L":"Д", ";":"ж", ":":"Ж", "'":"э", "\"":"Э",
                        "z":"я", "Z":"Я", "x":"ч", "X":"Ч", "c":"с", "C":"С", "v":"м", "V":"М", "b":"и", "B":"И",
                        "n":"т", "N":"Т", "m":"ь", "M":"Ь", ",":"б", "<":"Б", ".":"ю", ">":"Ю", "/":".", "?":","
                        }

    russian_to_english = {
                        "ё":"`", "Ё":"~", "\"":"@", "№":"#", "ж":";", ":":"^", "?":"&", "й":"q", "Й":"Q", "ц":"w", "Ц":"W", "у":"e",
                        "У":"E", "к":"r", "К":"R", "е":"t", "Е":"T", "н":"y", "Н":"Y", "г":"u", "Г":"U", "ш":"i", "Ш":"I", "щ":"o",
                        "Щ":"O", "з":"p", "З":"P", "х":"[", "Х":"{", "ъ":"]", "Ъ":"}", "\\":"\\", "/":"|", "ф":"a", "Ф":"A", "ы":"s",
                        "Ы":"S", "в":"d", "В":"D", "а":"f", "А":"F", "п":"g", "П":"G", "р":"h", "Р":"H", "о":"j", "О":"J", "л":"k",
                        "Л":"K", "д":"l", "Д":"L", "Ж":":", "э":"'", "Э":"\"", "я":"z", "Я":"Z", "ч":"x", "Ч":"X", "с":"c", "С":"C",
                        "м":"v", "М":"V", "и":"b", "И":"B", "т":"n", "Т":"N", "ь":"m", "Ь":"M", "б":",", "Б":"<", "ю":".", "Ю":">",
                        ".":"/", ",":"?"
                        }

    if to_russian:
        dict_to_compare = english_to_russian
    else:
        dict_to_compare = russian_to_english
        
    for letter in original_text:
        if letter in dict_to_compare:
            changed_text = changed_text + dict_to_compare.get(letter)
        else:
            changed_text = changed_text + letter

    return changed_text

def clear_instance_path():
    try:
        for f in os.listdir(app.instance_path):
            if f != 'err_log':
                try:
                    os.remove(os.path.join(app.instance_path, f))
                except:
                    with open(os.path.join(app.instance_path, 'err_log'), 'r+w') as error_file:
                        error_file.write('ошибка удаления файла {} в {}\n'.format(f, datetime.utcnow()))
    except:
        pass

def tag_replace(s):
    # Принимает объект Markup.escape

    # paragraph
    a = Markup.escape('[p]')
    b = Markup('<p>')
    s = s.replace(a, b)
    a = Markup.escape('[/p]')
    b = Markup('</p>')
    s = s.replace(a, b)
    
    # bold 
    a = Markup.escape('[b]')
    b = Markup('<b>')
    s = s.replace(a, b)
    a = Markup.escape('[/b]')
    b = Markup('</b>')
    s = s.replace(a, b)

    # italic
    a = Markup.escape('[i]')
    b = Markup('<i>')
    s = s.replace(a, b)
    a = Markup.escape('[/i]')
    b = Markup('</i>')
    s = s.replace(a, b)

    # strike
    a = Markup.escape('[s]')
    b = Markup('<s>')
    s = s.replace(a, b)
    a = Markup.escape('[/s]')
    b = Markup('</s>')
    s = s.replace(a, b)

    # details
    a = Markup.escape('[d]')
    b = Markup('<details>')
    s = s.replace(a, b)
    a = Markup.escape('[/d]')
    b = Markup('</details>')
    s = s.replace(a, b)

    # code
    a = Markup.escape('[c]')
    b = Markup('<code>')
    s = s.replace(a, b)
    a = Markup.escape('[/c]')
    b = Markup('</code>')
    s = s.replace(a, b)

    # pre
    a = Markup.escape('[pre]')
    b = Markup('<pre>')
    s = s.replace(a, b)
    a = Markup.escape('[/pre]')
    b = Markup('</pre>')
    s = s.replace(a, b)
    return s
    
if __name__ == '__main__':
    text_to_swop = input('type text: ')
    print(swoper_logic(text_to_swop, True))
    input()
