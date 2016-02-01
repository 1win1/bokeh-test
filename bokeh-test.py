from bokeh.plotting import figure, show, output_file, vplot, output_notebook
from bokeh.models import HoverTool
from datetime import date
# import operator

"""Этот скрипт выводит 2 графика зависимости числа убийств (K) от месяца игры для одного игрока
с группировками по дням и месяцам соответственно.
Данные берутся из текстового файла, а результат записывается в kills_by_time.html"""

# # output_notebook()
# def convertdatetime(x):
#     return np.array(x, dtype=np.datetime64)

# получаем сырые данные из текстового файла
kills = {}
deaths = {}
assists = {}

file = open('data/txt/Dedein test data.txt', 'r')
# file = open('data/txt/Insane test data.txt', 'r')
# -------------------------------------
for line in file:  # use line here
    # дата находится в столбце 19, KDA в 9-11
    string_date = line.split('\t')[19].strip()
    string_nick = line.split('\t')[0]
    string_id = line.split('\t')[1]
    string_date = date(int(string_date.split('-')[2]), int(string_date.split('-')[1]), int(string_date.split('-')[0]))
    # print(string_date, type(string_date))

    string_kills = int(line.split('\t')[9])
    string_assists = int(line.split('\t')[10])
    string_deaths = int(line.split('\t')[11])

    if kills.get(string_date):
        kills[string_date] += int(string_kills)
    else:
        kills[string_date] = int(string_kills)

    if deaths.get(string_date):
        deaths[string_date] += int(string_deaths)
    else:
        deaths[string_date] = int(string_deaths)

    if assists.get(string_date):
        assists[string_date] += int(string_assists)
    else:
        assists[string_date] = int(string_assists)

# -------------------------------------
file.close()

# Складываем результаты по месяцам
month_kills = {}
for item in sorted(kills):
    month_kills[item.strftime("%m-%Y")] = month_kills.get(item.strftime("%m-%Y"), 0) + int(kills[item])

TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select, hover"

hover = HoverTool(
        tooltips=[
            ("kills", "$x"),
        ]
    )

list_dates = []
list_kills = []
for item in sorted(kills):
    list_dates.append(item)
    list_kills.append(kills[item])

m_list_dates = []
m_list_kills = []
for item in sorted(month_kills):
    # print(item)
    m_list_dates.append(date(int(item.split('-')[1]), int(item.split('-')[0]), 1))
    m_list_kills.append(month_kills[item])

# График с группировкой по дням
plot1 = figure(width=1395, height=300, title="Kills by days. Player: " + str(string_nick) + " Id: " + str(string_id),
               x_axis_type="datetime", tools=TOOLS)
plot1.xaxis.axis_label = 'Date'
plot1.yaxis.axis_label = 'Kills'

plot1.circle(list_dates, list_kills, legend="Зависимость kills от даты")
plot1.line(list_dates, list_kills, legend="Зависимость kills от даты")

# Второй график с группировкой по месяцам
plot_m = figure(width=1395, height=300, title="Kills by months",
                x_axis_type="datetime", tools=TOOLS)
plot_m.xaxis.axis_label = 'Date'
plot_m.yaxis.axis_label = 'Kills'

plot_m.circle(sorted(m_list_dates), m_list_kills, legend="Зависимость kills от даты")
plot_m.line(sorted(m_list_dates), m_list_kills, legend="Зависимость kills от даты")

# Задаём выходной файл:
output_file("kills_by_time.html", title="Зависимость числа убийств от времени")

p = vplot(plot1, plot_m)
show(p)  # open a browser

# Сортировка словаря со статистикой по датам
# sorted_kills = dict(enumerate(sorted(kills.items(), key=operator.itemgetter(1), reverse=True), 1))
