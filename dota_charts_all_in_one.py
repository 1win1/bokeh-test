import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, FixedTicker
from random import randint

"""Этот скрипт строит общий график зависимости числа уникальных героев
от числа проведённых игр, сгруппированных сотнями для всех игроков из dataframe.
Результат записывается в dota_charts_all_in_one.html"""

# Чтобы открыть Excel файл как объект:
# xlsfile = pd.ExcelFile('data/allpick29-01-16.xlsx', header=None)
# dframe = xlsfile.parse(header=None)
# dframe = dframe.rename(columns={30: 'Datetime'})

# Ускоряем загрузку скрипта с помощью преварительно сохранённого в файл DataFrame
# Сохранять с помощью dframe.to_pickle('data/dframe29-01-16')
dframe = pd.read_pickle('data/dframe29-01-16')

players = dframe[1].unique()

list_players = []
# Считаем уникальными ID, а не никнеймы, так как может получиться, что ник поменяли в процессе парсинга данных
for x in range(len(dframe[1].unique())):
    player_dframe = dframe[dframe[1] == players[x]]

    # Отсортируем значения
    player_dframe = player_dframe.sort_values(by='Datetime')

    # Добавим счётчик всех матчей этого игрока
    player_dframe['Сounter'] = [x for x in range(len(player_dframe))]

    # Создаём индекс для группировки
    # TODO: Сделать это красиво и в одну строчку:
    if len(player_dframe) > 100:
        groupper = [item for sublist in [[x for y in range(100)] for x in range(len(player_dframe) // 100)]
                for item in sublist]
        groupper += [groupper[-1] + 1 for x in range(len(player_dframe) - len(groupper))]
    else:
        groupper = [item for sublist in [[x for y in range(len(player_dframe))] for x in range(1)]
                for item in sublist]
        groupper += [groupper[-1] + 1 for x in range(len(player_dframe) - len(groupper))]

    # Добавляем в конец столбец с индексом для группировки (индекс 33, можно добавить название столбца)
    # (от SettingWithCopyWarning можно избавиться, установив df.is_copy = True, но я не уверен, что это лучший путь)
    player_dframe[len(player_dframe.columns)+1] = groupper
    # Добавляем запись в список
    list_players.append(player_dframe)

# Данные для оси y
list_unique_heroes = [list_players[x].set_index('Datetime').groupby(33)[4].apply(lambda x: len(x.unique()))
                      for x in range(len(players))]
# Данные для оси x
# list_unique_heroes_indexes = list([list_players[x][33].unique() for x in range(0, len(list_players))])
list_unique_heroes_indexes = list([list_players[x][33].unique()*100+100 for x in range(0, len(list_players))])

# Рисуем графики:
TOOLS = "pan, wheel_zoom, box_zoom, reset,save, box_select, crosshair"

# Задаём выходной файл:
output_file("dota_charts_all_in_one.html", title="Общий выбор героев")

plots = []
plots_row = []
plot_num = 0

nicknames = []
for x in range(len(players)):
    nicknames.append(list(dframe[dframe[1] == dframe[1].unique()[x]][0])[-1])

p1_hover = HoverTool(
            tooltips=[
                ("Index", "$index"),
            ]
        )

p1 = figure(width=1200, height=1200, name="foo",
                 title="All in one", tools=[p1_hover, TOOLS])


for x in range(len(players)):
    # player_data = dframe[dframe[1] == players[x]]
    nickname = list(dframe[dframe[1] == dframe[1].unique()[x]][0])[-1]
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    p1.line(list_unique_heroes_indexes[x], list_unique_heroes[x], legend=nickname, color=color)
show(p1)

