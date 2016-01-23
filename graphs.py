import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool, CustomJS
from bokeh.models.widgets import Select
from bokeh.io import vform

# Open the excel file as an object
# xlsfile = pd.ExcelFile('data/top100.xlsx', header=None)
# dframe = xlsfile.parse(header=None)
# dframe = dframe.rename(columns={30: 'Datetime'})

# Ускоряем загрузку скрипта с помощью преварительно сохранённого в файл DataFrame
# Сохранять с помощью dframe.to_pickle('data/dframe')
dframe = pd.read_pickle('data/dframe')

players = dframe[1].unique()
# print(len(players))

# Отбираем игры конкретного игрока, для примера
# rand_counter = randint(1, len(players))
rand_counter = 0

player_match = dframe[dframe[1] == players[rand_counter]]
nickname = dframe[0][rand_counter]
# print(len(player_match))

# player_match.set_index('Datetime').groupby(pd.TimeGrouper('M'))[0].apply(lambda x: x.count())
# player_match.set_index('Datetime').groupby(pd.TimeGrouper('M'))[4].apply(lambda x: len(x.unique()))

# Получаем список героев по месяцам:
uniq_heroes_names_month = player_match.set_index('Datetime').groupby(pd.TimeGrouper('M'))[4].unique()

# Получаем количество уникальных героев по месяцам: (объект pandas.core.series.Series)
uniq_heroes_month = player_match.set_index('Datetime').groupby(pd.TimeGrouper('M'))[4].apply(lambda x: len(x.unique()))

# Рисуем графики:
output_file("legend.html", title="legend.py example")
TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select, crosshair"

list_players = [dframe[dframe[1] == players[x]].set_index('Datetime').groupby(pd.TimeGrouper('M'))[4].apply(lambda x: len(x.unique())) for x in range(0, len(players))]
list_players_indexes = [list_players[x].keys() for x in range(0, len(list_players))]

list_uniq_heroes = [dframe[dframe[1] == players[x]].set_index('Datetime').groupby(pd.TimeGrouper('M'))[4].apply(lambda x: len(x.unique())) for x in range(0, len(players))]

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

# График с группировкой по месяцам
plot1 = figure(width=1000, height=600, name="foo", title="Unique heroes per month",
               x_axis_type="datetime", tools=[hover, TOOLS])
plot1.xaxis.axis_label = 'Date'
plot1.yaxis.axis_label = 'Heroes'


plot1.circle('x', 'y', size=10, source=source)
plot1.line('x', 'y', source=source)
# show(plot1)

select_callback = CustomJS(args=dict(source=source), code="""
    var data = source.get('data');
    var f = cb_obj.get('value').split('\t', 1)
    x = data['x']
    y = data['y']

    nickname = new Array();
    datetime = new Array();
    fgames = new Array();
    for (i = 0; i < data['dates'][f].length; i++) {
            nickname.push(data['dframe'][f])
            datetime.push(new Date(data['dates'][f][i]))
            fgames.push(data['first_games'][f])
        }
    data['nick'] = nickname
    data['x'] = data['dates'][f]
    data['y'] = data['players'][f]
    data['desc'] = data['list_uniq_heroes'][f]
    var date = new Date(data['dates'][f][0]);
    data['time'] = datetime
    data['since'] = fgames
    source.trigger('change');
""")

select = Select(title="Player:", value="None", options=[str(x)+ '\t' + dframe[0].unique()[x] for x in range(0, len(players))], callback=select_callback)

layout = vform(select,  plot1)
output_file("legend.html", title="legend.py example")
show(layout)

