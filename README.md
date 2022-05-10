# :art: **Minecraft-Art in Game** :art:
Converting a **Photo** to **Minecraft Art in Game**
## :ledger: **Description** :ledger:
The program generates from the original photo an art consisting of Minecraft game blocks.
## :snake: **Специально для курса Master of Python** :snake:
### :nut_and_bolt: **Проблема** :nut_and_bolt:
*Первая версия* этого проекта включала *максимально топорное* определение выходных значений на основе входных данных, а именно текстуру блока на основе входного цвета, с помощью стандартной библиотеки *python* ***webcolors***. Для более грамотного решения данной задачи было необходимо использовать **машинное обучение**. <br/>
**Главная цель** данного проекта - это генерация изображения в игровом мире майнкрафта с использованием средств *minecraft-api*. Одна из основных целей - это предсказать какая текстура будет использована для изображения пикселя исходного изображения, для дальнейшей генерации её в мире *Maincraft'а*.
### :package: **Данные** :package:
Чтобы обучить модель понадобился *набор данных*, который включал в себя **4** необходимых переменных, **3** из которых значения цвета в *RGB* формате и *номер текстуры*, что относиться к этому цвету. 
<br/>
![img](https://user-images.githubusercontent.com/104269586/167304383-79ddce87-bada-437f-b79c-09637725d44d.jpg)
<br/>
Так как на просторах интернета ничего подобного не было найдено - набор данных собирался вручную. К каждой текстуре был подобран *диапазон* ближайших цветов путём перевода средннего значения цвета текстуры в *HEX* представление, простыми словами в ***web*** цвет, и нахождению ближайших к этому цвету *hex* значений.
```python
import csv
from webcolors import rgb_to_hex, hex_to_rgb

def add_bd(list): #функция добавления данных в набор
    with open("bd_blockrgb_mc.csv", mode="a", encoding='utf-8') as fbd:
        fbd_writer = csv.writer(fbd, delimiter = ",", lineterminator="\r")
        fbd_writer.writerow(list)
        
for i in range(218):
    img = Image.open('srt2\{}.png'.format(i)) #Загрузка усреднённого по цвету изображения текстуры
    im = img.load()
    rgb = im[0, 0] # Получения значения цвета
    a = int('0x' + rgb_to_hex(rgb)[1:], 16)
    add_bd(rgb[0], rgb[1], rgb[2], i)
    #--------------------------------Добавлени диапазона цветов относящихся к текстуре блока--------------------------------
    add_bd(hex_to_rgb('#' + hex(a + 1)[2:])[0], hex_to_rgb('#' + hex(a + 1)[2:])[1], hex_to_rgb('#' + hex(a + 1)[2:])[2], i)
    add_bd(hex_to_rgb('#' + hex(a + 2)[2:])[0], hex_to_rgb('#' + hex(a + 2)[2:])[1], hex_to_rgb('#' + hex(a + 2)[2:])[2], i)
    add_bd(hex_to_rgb('#' + hex(a + 3)[2:])[0], hex_to_rgb('#' + hex(a + 3)[2:])[1], hex_to_rgb('#' + hex(a + 3)[2:])[2], i)
    add_bd(hex_to_rgb('#' + hex(a + 4)[2:])[0], hex_to_rgb('#' + hex(a + 4)[2:])[1], hex_to_rgb('#' + hex(a + 4)[2:])[2], i)
    add_bd(hex_to_rgb('#' + hex(a + 5)[2:])[0], hex_to_rgb('#' + hex(a + 5)[2:])[1], hex_to_rgb('#' + hex(a + 5)[2:])[2], i)
    add_bd(hex_to_rgb('#' + hex(a - 1)[2:])[0], hex_to_rgb('#' + hex(a - 1)[2:])[1], hex_to_rgb('#' + hex(a - 1)[2:])[2], i)
    add_bd(hex_to_rgb('#' + hex(a - 2)[2:])[0], hex_to_rgb('#' + hex(a - 2)[2:])[1], hex_to_rgb('#' + hex(a - 2)[2:])[2], i)
    add_bd(hex_to_rgb('#' + hex(a - 3)[2:])[0], hex_to_rgb('#' + hex(a - 3)[2:])[1], hex_to_rgb('#' + hex(a - 3)[2:])[2], i)
    add_bd(hex_to_rgb('#' + hex(a - 4)[2:])[0], hex_to_rgb('#' + hex(a - 4)[2:])[1], hex_to_rgb('#' + hex(a - 4)[2:])[2], i)
    add_bd(hex_to_rgb('#' + hex(a - 5)[2:])[0], hex_to_rgb('#' + hex(a - 5)[2:])[1], hex_to_rgb('#' + hex(a - 5)[2:])[2], i)
```
### :wrench: **Предобработка** :wrench:
Как таковой предобработки нет, ибо всё это было продумано при создании набора данных для обучения. Вся оставшаяся предобработка это разделение на обучающую выборку и проверочную.
```python
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.tree import DecisionTreeRegressor

modeltree = DecisionTreeRegressor()
bd = pd.read_csv('my_super_dataset_3.csv')
x = bd[['r', 'g', 'b']]
y = bd[['block_nom']]
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.2)
modeltree.fit(x_train, y_train)
predtree = modeltree.predict(x_test)
joblib.dump(modeltree, 'new_db_learn8.pkl')
err = mean_absolute_percentage_error(y_test, predtree)
print('Error ', err)
```
### :penguin: **Модель машинного обучения** :penguin:
Конечной стала модель **new_db_learn8** - *DecisionTreeRegressor*. В ней было учтено большинсво ошибок и в конечном результате она достигла минимальной ошибки в **1.3%**. Также есть ещё 2 модели, предыдущие версии с чуть большей ошибкой, но координально несколько другой предсказывающей особенностью. Из трёх возможных вариантов: ***Линейной регрессии, Дерева регрессий и Классификации*** было выбрано использование именно ***Дерева регрессий***, так как при использовании линейной регрессии выходные значения - дроби, что при округлении дают огромные ошибки от десятков миллионов процентов, а при классификации происходит предсказание из сотен возможных вариантов, что даёт большую задержку в выполнении программы. *DecisionTreeRegressor* же позволяет получать целые числа, не требующие округления, что исключает необходимость дополнительной обработки, что в свою очередь в челом **состовляет более качественную работу и маленькую задержку в выполнении кода.**
### :chart_with_downwards_trend: **Метрики работы моделей - процент ошибки:** :chart_with_downwards_trend:
+ new_db_learn6 **2.1%**
+ new_db_learn7 **1.9%**
+ new_db_learn8 **1.3%**
## :bulb: Features :bulb:
+ The program runs on a *sklearn regression tree model* trained on a self-made dataset
+ Python *version 3.8*
+ The model reached a minimum error of *1.3%*
+ Multithreading applied
+ There is a setting for the *height* of the final image in Minecraft blocks, the *width* changes proportionally (It should be noted that the larger the height, the longer the code will be executed and max height 256.)
## :floppy_disk: Setup for Windows :floppy_disk:
+ Clone this repository
+ Install all the dependencies from **requirements.txt** via pip install -r requirements.txt **or** run **pip install.bat**
+ Run **start.bat**
+ Go to **Minecraft** and connect to *localhost* with port *11111*
+ Run **main.py**
+ Write something to the chat
## :cookie: Result :cookie:
**Input:**
<br/>
![Image](https://user-images.githubusercontent.com/104269586/166220919-783d2ac3-6501-4fe6-a3b1-a44961eade68.jpg)
<br/>
**Output:**
![Image](https://user-images.githubusercontent.com/104269586/166220948-86e18f3c-b322-4af5-a613-ed55f977387c.png)
## :shipit: END :shipit:
We created these Minecraft-Arts in the Minecraft world using the Minecraft-Api. We have achieved our goal! :relaxed:
