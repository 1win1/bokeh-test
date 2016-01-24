import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource, gridplot
from bokeh.models import HoverTool, DatetimeTickFormatter

# Чтобы открыть Excel файл как объект:
# xlsfile = pd.ExcelFile('data/top100.xlsx', header=None)
# dframe = xlsfile.parse(header=None)
# dframe = dframe.rename(columns={30: 'Datetime'})

# Ускоряем загрузку скрипта с помощью преварительно сохранённого в файл DataFrame
# Сохранять с помощью dframe.to_pickle('data/dframe')
dframe = pd.read_pickle('data/dframe')

players = dframe[1].unique()
# print(len(players))

# Отбираем игры конкретного игрока, для примера
rand_counter = 0
player_match = dframe[dframe[1] == players[rand_counter]]
nickname = dframe[0][rand_counter]

# Получаем список героев по месяцам:
# uniq_heroes_names_month = player_match.set_index('Datetime').groupby(pd.TimeGrouper('M'))[4].unique()

# Получаем количество уникальных героев по месяцам: (объект pandas.core.series.Series)
uniq_heroes_month = player_match.set_index('Datetime').groupby(pd.TimeGrouper('M'))[4].apply(lambda x: len(x.unique()))


list_players = [dframe[dframe[1] == players[x]].set_index('Datetime').groupby(pd.TimeGrouper('M'))[4].
                apply(lambda x: len(x.unique())) for x in range(0, len(players))]
list_players_indexes = [list_players[x].keys() for x in range(0, len(list_players))]

list_uniq_heroes = [dframe[dframe[1] == players[x]].set_index('Datetime').groupby(pd.TimeGrouper('M'))[4].
                    apply(lambda x: len(x.unique())) for x in range(0, len(players))]

source = ColumnDataSource(
        data=dict(
            x=uniq_heroes_month.index,
            y=uniq_heroes_month,
            players=list_players,
            dates=list_players_indexes,
            nick=[nickname for x in range(len(uniq_heroes_month.index))],
            desc=[uniq_heroes_month[x] for x in range(len(uniq_heroes_month.index))],
            time=[uniq_heroes_month.keys()[x].strftime('%m-%Y') for x in range(len(uniq_heroes_month.index))],
            dframe=dframe[0].unique(),
            list_uniq_heroes=list_uniq_heroes,
            since=[list_players[0].keys()[0].strftime('%m-%Y') for x in range(len(uniq_heroes_month.index))],
            first_games=[list_players[x].keys()[0].strftime('%m-%Y') for x in range(0, len(players))],
        )
    )

hover = HoverTool(
        tooltips=[
            ("Index", "$index"),
            ("Date", "@time"),
            ("Nick:", "@nick"),
            ("Unique heroes:", "@desc"),
            ("Playing since:", "@since"),
        ]
    )

# Рисуем графики:
output_file("legend.html", title="legend.py example")
TOOLS = "pan, wheel_zoom, box_zoom, reset,save, box_select, crosshair"


def plotsomethingnew(plot_number=0, sources=list()):
    # Готовим данные:
    if not isinstance(sources, list):
        sources = []

    foo_nickname = []
    foo_datetime = []
    foo_fgames = []
    for i in range(0, len(list_players_indexes[plot_number])):
        foo_nickname.append(dframe[0].unique()[plot_number])
        foo_datetime.append(list_players_indexes[plot_number][i].strftime('%m-%Y'))
        foo_fgames.append([list_players[plot_number].keys()[0].strftime('%m-%Y')])

    new_source = ColumnDataSource(
        data=dict(
            x=list_players_indexes[plot_number],
            y=list_players[plot_number],
            time=foo_datetime,
            nick=foo_nickname,
            unique_heroes=list_uniq_heroes[plot_number],
            playing_since=foo_fgames,
        )
    )

    foo_hover = HoverTool(
            tooltips=[
                ("Index", "$index"),
                ("Date", "@time"),
                ("Nick:", "@nick"),
                ("Unique heroes:", "@unique_heroes"),
                ("Playing since:", "@playing_since"),
            ]
        )

    sources.append(new_source)


# Необходимые форматы для разных масштабов можно задать вучную, перечислив их в словаре:
    formats = {
        'hours': ["%b"],
        'days': ["%b-%y"],
    }

    # Создаём график:
    foo = figure(width=275, height=300, name="foo", x_axis_type="datetime",
                 title=(str(plot_number) + ' ' + str(foo_nickname[0])), tools=[foo_hover, TOOLS])
    foo.line('x', 'y', source=new_source)
    foo.title_text_font_size = '8pt'
    foo.xaxis.axis_label_text_font_size = '8pt'
    foo.xaxis.major_label_orientation = 0.785  # Pi/4
    foo.xaxis[0].formatter = DatetimeTickFormatter(formats=formats)
    # адаптивность не работает: http://bokeh.pydata.org/en/0.10.0/docs/user_guide/styling.html#responsive-dimensions
    return foo


output_file("legend.html", title="legend.py example")

plots = []
plots_row = []
plot_num = 0

# Строим таблицу и помещаем графики в ячейки
# Строим столько графиков, сколько уместится целыми рядами
for x in range(0, (len(players) // 5)):
    plots.append(plots_row)
    for y in range(0, 5):
        plots_row.append(plotsomethingnew(plot_num))
        plot_num += 1
    plots_row = []

grid_layout = gridplot(plots)
show(grid_layout)
