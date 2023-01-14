from api import PetFriends
from settings import *
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово "key" """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key; затем запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступные значения параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Cat_Boy', animal_type='кот',
                                     age='4', pet_photo='images/Cat_Boy.jpg'):
    """Проверка возможности добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверка возможности удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список своих питомцев пустой, добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Cat_Man", "кот", "9", "images/Cat_Man.JPG")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, что статус ответа равен 200, и что в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Cat_Boy', animal_type='Кот', age=5):
    """Проверка возможности обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем, что статус ответа = 200, и что имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, пользователь получает уведомление с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_post_new_pet_simple(name='Sima_cat', animal_type='кошка', age='4'):
    # тестируем добавление питомца без фото
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_new_pet_simple (auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_update_post_pets_set_photo(pet_photo='images/Sima_cat.JPG'):
    """Проверяем возможность добавления фото к питомцу"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то обновляем данные питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.post_pets_set_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200, и что фото питомца добавлено
        assert status == 200
        assert result['pet_photo'] is not ''

    else:
        # Если список питомцев пуст, то выводим сообщение с текстом об отсутствии питомцев в своем списке
        raise Exception("There is no my pets")

def test_get_api_key_for_invalid_user_invalid_email(email = invalid_email, password = invalid_password):
    """" Проверяем, что запрос ключа от несуществующего пользователя с неверным паролем
    возвращает статус 403"""
    status, result = pf.get_api_key(email, password)
    # Проверяем статус:
    assert status == 403

def test_get_api_key_for_invalid_user(email = invalid_email, password = valid_password):
    """" Проверяем, что запрос ключа от несуществующего пользователя с верным паролем
    возвращает статус 403"""
    status, result = pf.get_api_key(email, password)
    # Проверяем статус:
    assert status == 403

def test_get_api_key_for_invalid_password(email = valid_email, password = invalid_password):
    """" Проверяем, что запрос ключа от существующего пользователя с неверным паролем
    возвращает статус 403"""
    status, result = pf.get_api_key(email, password)
    # Проверяем статус:
    assert status == 403

def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем, что запрос всех питомцев с неправильным api ключом возвращает статус 403.
    Для этого запрашиваем список всех питомцев с invalid_key, который сохранен в settings.
    Доступное значение параметра filter - 'my_pets' либо '' """
    status, result = pf.get_list_of_pets(invalid_key, filter)
    # Проверяем статус:
    assert status == 403

def test_post_new_pet_simple_with_invalid_age_format(name='Beowulf', animal_type='beowulf', age='abc'):
    """Проверяем, что нельзя добавить питомца с буквами в поле age"""
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_new_pet_simple(auth_key, name, animal_type, age)
    ###############Внимание - баг! #############
    # Статус ответа = 200 вместо ожидаемого 400 (поле age предполагает в формате целое число)
    assert status == 200


def test_post_new_pet_simple_with_none_age_format(name='Beowulf', animal_type='beowulf', age=''):
    """Проверяем, что нельзя добавить питомца с пустым значением в поле age"""
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_new_pet_simple(auth_key, name, animal_type, age)
    ###############  Внимание - баг! #############
    # Статус ответа = 200 вместо ожидаемого 400 (поле age предполагает в формате целое число)
    assert status == 200

def test_post_new_pet_simple_with_invalid_name_format(name=' ', animal_type='beowulf', age='5'):
    """Проверяем, что нельзя добавить питомца с пустым полем имени"""
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_new_pet_simple(auth_key, name, animal_type, age)
    ###############   Внимание - баг! #############
    # Статус ответа = 200 вместо ожидаемого 400 (поле age предполагает в формате целое число)
    assert status == 200

def test_failed_update_post_pets_set_photo_with_invalid_format(pet_photo='images/TonyRobbins.jfif'):
    """Проверяем невозможность добавления фото в некорректном формате"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то обновляем данные питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.post_pets_set_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200, и что фото питомца добавлено
        assert status == 200
        assert result['pet_photo'] is not ''

    else:
        # Если список питомцев пуст, то выводим сообщение с текстом об отсутствии питомцев в своем списке
        raise Exception("There is no my pets")

    ############   Внимание - баг! #############
    # Статус ответа = 200 вместо ожидаемого 400 (В документации допустимые форматы
    # "The file should be in JPG, JPEG or PNG format"
