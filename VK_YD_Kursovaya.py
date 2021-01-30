# Курсовая работа Подузов Сергей
# Нужно написать программу, которая будет:
#
# 1. Получать фотографии с профиля. Для этого нужно использовать метод photos.get.
# 2. Сохранять фотографии максимального размера(ширина/высота в пикселях) на Я.Диске.
# 3. Для имени фотографий использовать количество лайков.
# 4. Сохранять информацию по фотографиям в json-файл с результатами.

# Обязательные требования к программе:
# Использовать REST API Я.Диска и ключ, полученный с полигона.
# Для загруженных фотографий нужно создать свою папку.
# Сохранять указанное количество фотографий(по умолчанию 5) наибольшего размера (ширина/высота в пикселях) на Я.Диске
# Сделать прогресс-бар или логирование для отслеживания процесса программы.
# Код программы должен удовлетворять PEP8.


import requests
import time
import os
import datetime
import json

# Токен VK

token = ''
# Токен YD
TOKEN_Y = ''

import requests
import os

HEADERS = {
    "Authorization": f"OAuth {TOKEN_Y}"
}


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
        self.owner_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']

    def get_fotos_profile(self, user_id=None):
        if user_id is None:
            user_id = self.owner_id
        fotos_url = self.url + 'photos.get'
        fotos_params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'count': 1000,
            'rev': 0,
            'extended': 1
            # 1 — будут возвращены дополнительные поля likes, comments, tags, can_comment, reposts. По умолчанию: 0.

        }
        res = requests.get(fotos_url, params={**self.params, **fotos_params})
        return res.json()

    def get_fotos_wall(self, user_id=None):
        if user_id is None:
            user_id = self.owner_id
        fotos_url = self.url + 'photos.get'
        fotos_params = {
            'owner_id': user_id,
            'album_id': 'wall',
            'count': 1000,
            'rev': 0,
            'extended': 1
            # 1 — будут возвращены дополнительные поля likes, comments, tags, can_comment, reposts. По умолчанию: 0.
        }
        res = requests.get(fotos_url, params={**self.params, **fotos_params})
        return res.json()


def is_digit(string):
    """Проверка ввода цифр"""
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def getting_id_vk(question1, question2):
    """Ввод ID пользователя"""

    active = True
    while active:
        num_id = input(question1)
        if is_digit(num_id) == True:
            if num_id.count('.') == 0:
                num_id = int(num_id)
                return num_id
            else:
                print(question2)
                continue
        else:
            print(question2)
            continue


def getting_id(question1, question2, max_num):
    """Ввод Цифр пользователем пользователя"""

    active = True
    while active:
        num_id = input(question1)
        if is_digit(num_id) == True:
            if num_id.count('.') == 0:
                num_id = int(num_id)
                if num_id <= max_num:
                    return num_id
            else:
                print(question2)
                continue
        else:
            print(question2)
            continue


def getting_name_dir():
    """Вводим имя новой папке на Яндекс диске"""
    active1 = True
    while active1:
        new_yandex_dir = input(
            "Ведите имя нового или существующего каталога в Яндекс диск, для копирования туда файлов с жеского диска компьютьера: ")
        new_yandex_dir = new_yandex_dir.strip()

        new_yandex_dir = new_yandex_dir.split(' ')

        if (len(new_yandex_dir) > 1 or len(new_yandex_dir[0]) == 0):
            print('Вы ввели имя с ошибкой, повторите')
            continue
        else:
            return new_yandex_dir[0]


# Создание яндекс диска
def creating_dir_yandexdisk(yandex_dir):
    try:

        response = requests.get(
            "https://cloud-api.yandex.net/v1/disk/resources",
            params={
                "path": yandex_dir,  # Запись c именем

            },
            headers=HEADERS
        )

        answer = response.json()['_embedded']['path']
        print("Такой каталого уже существует")
        dir = True

    except:

        print("Такого каталога еще не существует, и он будет создан!")
        dir = False

    # Если каталога не существует dir==False, то создаем его в яндекс Диске в корне
    if dir == False:
        response = requests.put(
            "https://cloud-api.yandex.net/v1/disk/resources",
            params={
                "path": yandex_dir,  # Запись c именем

            },
            headers=HEADERS
        )

        answer = response.json()
        print("Создан каталог в Яндекс Диске: ", yandex_dir)


# Функция - которая на входе берет req по get.fotos и на ывыходе делает список словарь с данными по фото
def gettin_foto_list_from_request_profile(req):
    req_num = req['response']['count']
    req_foto_datas = req_num = req['response']['items']  # список фото с информаций
    info_json_data = []  # Файл для записи информации о файлах

    for foto in req_foto_datas:
        foto_dict = {}
        foto_date = foto['date']  # знаем дату фото
        foto_date_likes = foto['likes']['count']
        foto_size_list = foto['sizes']  # Списиок фото разного качествао в списке

        last_foto = foto_size_list[-1]
        # Создаем элементы словаря фото
        foto_dict['url'] = last_foto['url']
        foto_dict['size'] = last_foto['type']
        foto_dict['likes'] = foto_date_likes
        foto_dict['date'] = foto_date
        foto_dict['height'] = last_foto['height']
        foto_dict['width'] = last_foto['width']
        info_json_data.append(foto_dict)

    num_foto = len(info_json_data)

    # Сортируем по width  вначале более большие фото width
    newlist_foto = sorted(info_json_data, key=lambda k: k['width'], reverse=True)

    return newlist_foto


# Эта функция анализирует json, создает папку на YD и копирует туда фото
def analyzong_and_copying_fotos(req):
    # анализируем список по req и вынимаем информацию из него
    newlist_foto = gettin_foto_list_from_request_profile(req)

    len_fotos = len(newlist_foto)  # Выясняем кол-во фото
    print("Количество фотографий равно: ", len_fotos)

    # Спрашиваем пользователя сколько требуется фотографий:
    input_foto_num = getting_id("Введите кол-во фотографий, которое надо загрузить: ",
                                "Ввели с ошибкой, введите заново: ", len_fotos)

    # Загрузка файлов на яндекс диск

    # спрашиваем имя нового катлога на яндекс диске
    Yandex_dir = getting_name_dir()

    # Создание каталога на яндекс Диске
    creating_dir_yandexdisk(Yandex_dir)

    like_list = []  # проверяем, списко нгазваний из лайков

    output_file = []

    n = 0  # Текущий номер фотографии
    for foto in newlist_foto:

        output_dict = {}  # формируем выходной словарь по фото тип {"file_name": "34.jpg","size": "z"}
        n = n + 1
        if n > int(input_foto_num):
            break
        else:
            if foto['likes'] not in like_list:
                foto_name = str(foto['likes']) + '.jpg'
                like_list.append(foto['likes'])
            else:
                # Преобразуем дату в формат %Y-%m-%d %H-%M-%S
                data_time = str(datetime.datetime.fromtimestamp(foto['date']))
                data_time = data_time.replace(":", "-")

                foto_name = str(foto['likes']) + '-' + data_time + '.jpg'

            foto_path = '/'.join([Yandex_dir, foto_name])
            foto_url = foto['url']

            response2 = requests.post(
                "https://cloud-api.yandex.net/v1/disk/resources/upload",
                params={
                    "path": foto_path,  # Запись c именем
                    "url": foto_url,  # Атрибут перезаписи файла
                },
                headers=HEADERS
            )

            # Через 5 секунду провереяем статус загрузки фотографий
            time.sleep(5)

            response3 = requests.get(response2.json()['href'],
                                     headers=HEADERS,
                                     )

            if (response3.json()['status'] == 'failed'):
                print("Фото номер ", str(n), "из ", str(int(input_foto_num)), "с именем ", foto_name,
                      "  не загружен, статус failed ")
            elif (response3.json()['status'] == 'in-progress'):
                print("Фото номер ", str(n), "из ", str(int(input_foto_num)), "с именем ", foto_name,
                      "  не загружен, статус in-progress ")
                # даем еще 7 секунда
                time.sleep(7)
                response4 = requests.get(response2.json()['href'],
                                         headers=HEADERS,
                                         )

                if (response4.json()['status'] == 'failed'):
                    print("Фото номер ", str(n), "из ", str(int(input_foto_num)), "с именем ", foto_name,
                          "  не загружен, статус failed ")
                elif (response4.json()['status'] == 'in-progress'):
                    print("Фото номер ", str(n), "из ", str(int(input_foto_num)), "с именем ", foto_name,
                          "  не загружен, статус in-progress ")
                elif (response4.json()['status'] == 'success'):
                    print("Фото номер ", str(n), "из ", str(int(input_foto_num)), "с именем ", foto_name,
                          "загружен, статус success ")
                    output_dict['file_name'] = foto_name
                    output_dict['size'] = foto['size']
                    output_file.append(output_dict)
            elif (response3.json()['status'] == 'success'):
                print("Фото номер ", str(n), "из ", str(int(input_foto_num)), "с именем ", foto_name,
                      "загружен, статус success ")
                output_dict['file_name'] = foto_name
                output_dict['size'] = foto['size']
                output_file.append(output_dict)

    # Сохраняем json на локальном компьютере в текущем каталоге
    print("Будет сохранет файл JSON - output_file.json: ")
    print(output_file)
    with open(r'output_file.json', 'w') as f:
        json.dump(output_file, f)

    # Сохраняем json в папке на яндекс диске
    foto_path = '/'.join([Yandex_dir, 'output_file.json'])

    response5 = requests.get(
        "https://cloud-api.yandex.net/v1/disk/resources/upload",
        params={
            # "path": file_name_urel,  # Запись c именем
            "path": foto_path,  # Запись c именем
            "overwrite": 'true'  # Атрибут перезаписи файла
        },
        headers=HEADERS
    )
    response5.raise_for_status()
    href = response5.json()['href']
    upload_response = requests.put(href, json=output_file, headers=HEADERS)


def main():
    # starting_condition()
    vk_client = VkUser(token, '5.77')

    choice = True
    while choice:
        print \
            ("""
                        Курсовая  работа по первому увроню Python "АПИ".
                Введите команду 0-2:
                    0 - Завершить работу
                    1 - Скопировать фотографии со своего профиля из VK на Яндекс иск
                    2 - Скопировать фотографии с любого открытого профиля из VK на Яндекс иск                    
                """)

        choice = input("Ваш выбор: ")
        print()
        # выход
        if choice == "0":
            print("До свидания.")
            break

        elif choice == "1":
            choice1 = True
            while choice1:
                print \
                    ("""
                            Копируем фотографии со своего профиля из VK на Яндекс иск.
                    Введите команду 0-2: 
                        0 - Вернуться обратно
                        1 - Скопировать с profile (аватарок) VK на Яндекс иск
                        2 - Скопировать с wall (стены) VK на Яндекс иск

                                """)

                choice1 = input("Ваш выбор: ")
                print()
                # обратно
                if choice1 == "0":
                    break
                elif choice1 == "1":
                    # Делаем запрос к API VK по  фото в profile
                    req = vk_client.get_fotos_profile()  # Мой ID 25554
                    # анализируем список по req и вынимаем информацию из него
                    analyzong_and_copying_fotos(req)

                elif choice1 == "2":
                    # Делаем запрос к API VK по  фото в wall
                    req = vk_client.get_fotos_wall()  # Мой ID 25554
                    # анализируем список по req и вынимаем информацию из него
                    analyzong_and_copying_fotos(req)


                else:
                    print("Извините, в меню нет пункта")
                    continue

        elif choice == "2":
            choice2 = True
            while choice2:
                print \
                    ("""
                            Копируем фотографии с любого профиля из VK на Яндекс иск.
                    Введите команду 0-2: 
                        0 - Вернуться обратно
                        1 - Скопировать с profile (аватарок) VK на Яндекс иск
                        2 - Скопировать с wall (стены) VK на Яндекс иск

                                """)

                choice2 = input("Ваш выбор: ")
                print()
                # обратно
                if choice2 == "0":
                    break
                elif choice2 == "1":
                    num_id = getting_id_vk("Введите ID пользователя цифрами: ", "Вы ввели с ошибкой, повторите ввод: ")
                    # Делаем запрос к API VK по  фото в profile
                    req = vk_client.get_fotos_profile(str(num_id))
                    # анализируем список по req и вынимаем информацию из него
                    try:
                        analyzong_and_copying_fotos(req)
                    except:
                        print("Ошибка", req['error']['error_msg'])



                elif choice2 == "2":
                    num_id = getting_id_vk("Введите ID пользователя цифрами: ", "Вы ввели с ошибкой, повторите ввод: ")
                    # Делаем запрос к API VK по  фото в wall
                    req = vk_client.get_fotos_wall(str(num_id))
                    # анализируем список по req и вынимаем информацию из него
                    try:
                        analyzong_and_copying_fotos(req)
                    except:
                        print("Ошибка", req['error']['error_msg'])


                else:
                    print("Извините, в меню нет пункта")
                    continue






        else:
            print("Извините, в меню нет пункта")
            continue


main()




