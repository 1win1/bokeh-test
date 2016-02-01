import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource, gridplot
from bokeh.models import HoverTool, FixedTicker

# Чтобы открыть Excel файл как объект:
# xlsfile = pd.ExcelFile('data/allpick29-01-16.xlsx', header=None)
# dframe = xlsfile.parse(header=None)
# dframe = dframe.rename(columns={30: 'Datetime'})

# Ускоряем загрузку скрипта с помощью преварительно сохранённого в файл DataFrame
# Сохранять с помощью dframe.to_pickle('data/dframe29-01-16')
dframe = pd.read_pickle('data/dframe29-01-16')

players = dframe[1].unique()
# print(len(players))

# Получаем количество уникальных героев по месяцам: (объект pandas.core.series.Series)
# uniq_heroes_month = player_match.set_index('Datetime').groupby(pd.TimeGrouper('M'))[4].
# apply(lambda x: len(x.unique()))

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


def plotsomethingnew(plot_number=0, sources=list()):
    # Готовим данные:
    if not isinstance(sources, list):
        sources = []

    foo_nickname = []
    for i in range(0, len(list_unique_heroes[plot_number])):
        foo_nickname.append(dframe[0].unique()[plot_number])

    # На будущее - для шкал
    # ticker = []
    # for t in range(max(list_unique_heroes[0])+1):
    #     ticker.append(t)

    new_source = ColumnDataSource(
        data=dict(
            x=list_unique_heroes_indexes[plot_number],  # list(pandas.core.series.Series)
            y=list_unique_heroes[plot_number],  # pandas.core.series.Series
            nick=foo_nickname,
            unique_heroes=list_unique_heroes[plot_number],
        )
    )

    foo_hover = HoverTool(
            tooltips=[
                ("Index", "$index"),
                ("Nick:", "@nick"),
                ("Unique heroes:", "@unique_heroes"),
                # ("Playing since:", "@playing_since"),
            ]
        )
    sources.append(new_source)

    # Создаём график:
    foo = figure(width=275, height=300, name="foo",
                 title=(str(plot_number) + ' ' + str(foo_nickname[0])), tools=[foo_hover, TOOLS])
    foo.line('x', 'y', source=new_source)
    foo.title_text_font_size = '8pt'
    foo.xaxis.axis_label_text_font_size = '8pt'
    foo.xaxis.major_label_orientation = 0.785  # Pi/4

    # TODO: Сделать одинаковый масштаб шкалы Y
    # foo.yaxis.ticker = FixedTicker(ticks=ticker)
    # foo.responsive=True
    # адаптивность не работает: http://bokeh.pydata.org/en/0.10.0/docs/user_guide/styling.html#responsive-dimensions
    return foo

# Задаём выходной файл:
output_file("dota_charts_hundreds.html", title="Выбор героев по сотням матчей")

plots = []
plots_row = []
plot_num = 0

# Строим таблицу и помещаем графики в ячейки
# Строим столько графиков, сколько уместится целыми рядами
for x in range(0, (len(players) // 5)):
    plots.append(plots_row)
    for xi in range(0, 5):
        plots_row.append(plotsomethingnew(plot_num))
        plot_num += 1
    plots_row = []

grid_layout = gridplot(plots)
show(grid_layout)


for x in range(len(players)):
    for each in range(len(list_unique_heroes[x])):
        print(players[x], list_unique_heroes_indexes[x][each], list_unique_heroes[x][each])
