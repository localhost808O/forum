import requests
from ast import literal_eval
from auth import auth


def test_auth():
    # login and get_jwt
    jwt, rt = auth()
    # logout имся
    url_logout = 'http://localhost:8080/api/auth/logout/'
    data4 = {"refresh_token":f"{rt}"}
    message4 = requests.post(url_logout, json=data4)
    print(message4.text)
    ## проверка работы logout а
    url5 = 'http://localhost:8080/api/auth/get_jwt/'
    data5 = {"nickname" : "Nikitos228",        
            "refresh_token" : f'{rt}'}
    message5 = requests.post(url5, json=data5)
    assert message5.text == '{"error": "wrong RT"}', "Не работает logout"
    print("message5.text == ", message5.text)
    ## # пробуем повторно зарегестрировать пользователя
    '''1- с темже НИКом '''
    url_signUp = 'http://localhost:8080/api/auth/signup/'
    dataX = {"nickname" : "Nikitos228",
        "password" : "10000",
        "profile" : {
        "name" : "sergey"}}
    messageX = requests.post(url_signUp, json=dataX)
    assert messageX.text != '{"success": "you can login"}', "Регистрация пользователя с повторяющимся ником!!"
    print("messageX.text == ", messageX.text)
    # пробуем логинимся с неправильным паролем
    url_signIn = 'http://localhost:8080/api/auth/signin/'
    data = {"nickname" : "Nikitos228",
        "password" : "wrongPswd"}
    message = requests.post(url_signIn, json=data)
    print("message.text == ", message.text)
    assert message.text == '{"error": "wrong password"}', "можно зайти с неправильным паролем!"


test_auth()
