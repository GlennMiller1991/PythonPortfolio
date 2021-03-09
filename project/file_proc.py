from project import app, os

file_proc_errors = {0: 'Файл обработан',
                    1: 'Ошибка удаления файла',
                    2: 'Ошибка открытия шаблона обработки',
                    3: 'Вы выбрали неверный файл',
                    4: 'Ошибка обработки файла',
                    5: 'Загруженный файл не соответствует шаблону',
                    6: 'Совпадение шаблона',
                    7: 'Отсутствие файла',
                    8: 'Ошибка формирования строки',
                    9: 'Ошибка записи файла',
                    10: 'Обработка не реализована',
                    }

def exl_file_proc(filename):
    # на PythonAnywhere функционал этой функции несет полезную нагрузку
    # Некоторые данные для быстроты написания были жостко вшиты в код
    # Данные эти могут содержать информацию не для посторонних глаз
    # Поэтому страница, на которой используется эта функция, была защищена паролем
    return filename, 10

    
def template_file_proc(filename):
    return filename, 10
