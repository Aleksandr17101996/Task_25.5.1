from typing import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Создание драйвера Google Chrome
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(10)
driver.get('https://petfriends.skillfactory.ru/login')

# Находим поля email и пароль
email = driver.find_element(By.ID, 'email')
password = driver.find_element(By.ID, 'pass')

# Заполняем найденные поля значениями
email.send_keys('TestingEmail@mail.ru')
password.send_keys('12345')

# Нажимаем Войти
enter = driver.find_element(By.CLASS_NAME, 'btn-success')
enter.click()

# Нажимаем на span
navbar = driver.find_element(By.CLASS_NAME, 'navbar-toggler-icon')
navbar.click()

# Нажимаем на вкладку "Мои питомцы"
mine = driver.find_element(By.LINK_TEXT, 'Мои питомцы')
mine.click()

# Находим статистику пользователя
block_pet = driver.find_element(By.CLASS_NAME, 'left').text

# Высчитываем число питомцев из статистики
count_pet = int(block_pet.split('\n')[1][-1])


table = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr"))
)
# Находим число записей в таблице
size_table = len(table)

# Сравниваем полученные значения числа питомцев
assert count_pet == size_table, 'Значения из статистики и из таблицы различаются'

driver.implicitly_wait(10)
# Находим все изображения внутри таблицы
images = driver.find_elements(By.XPATH, "//th/img")
count_of_img = 0
for i in images:
    if i.get_attribute('src') != '':    # Если поле источник не пустое, то картинка есть
        count_of_img += 1

# Если четное число питомцев, то сравниваем с size_table пополам, если нечетное, то пополам + 1
if size_table % 2 == 0:
    assert count_of_img >= size_table/2, 'Больше чем у половины питомцев отсутствует фото'
else:
    assert count_of_img >= int(size_table/2) + 1, 'Больше чем у половины питомцев отсутствует фото'

# Создаем словарь информации о каждом питомце
info_dict = dict()
k = 0
for i in table:
    info_dict[k] = i.text.split()
    k += 1

# Проверяем, что у всех питомцев есть имя, возраст и порода
for i in info_dict:
    assert len(info_dict[i]) == 4, 'У питомца под номером {} заполнены не все значения'.format(i+1)


list_names = [] # Формируем пустой список для имён
for i in info_dict:
    list_names.append(info_dict[i][0].lower())  # Складываем в этот список имена

# Проверяем, что у всех питомцев различные имена
assert len(list_names) == len(set(list_names)), 'Не у всех питомцев разные имена'

# Сформировали словарь картинок с их источником
img_dict = dict()
n = 0
for i in images:
    img_dict[n] = i.get_attribute('src')
    n += 1

result_list = []
for i in info_dict:
    info_dict[i].insert(0, img_dict[i]) # Добавили к исходной информации информацию о картинках
    result_list.append(info_dict[i])    # Положили результат в список всех информаций

# Формируем список уникальных информаций о питомцах
unique_data = [list(x) for x in set(tuple(x) for x in result_list)]

# Проверяем, есть ли одинаковые элементы в списке
assert len(unique_data) == len(result_list), 'В перечне питомцев есть два одинаковых'