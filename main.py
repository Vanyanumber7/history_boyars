import sqlite3
import matplotlib.pyplot as plt


def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i])


def translation(year1, year2, type, cur):
    years_info = {
        'boyars': {'name': 'Бояре', 'print': 'бояр', 1532: 12, 1547: 20, 1558: 34, 'color': ['green', 'red', 'purple']},
        'okolnichi': {'name': 'Окольничие', 'print': 'окольничих', 1532: 3, 1547: 7, 1558: 15,
                      'color': ['darkgreen', 'orangered', 'darkviolet']}}
    data = cur.execute(
        """SELECT arrived, gone FROM {} WHERE year<={} AND year>= {}""".format(type, year2, year1)).fetchall()
    print(data)
    arv, gone = sum(map(lambda x: x[0], data)), sum(map(lambda x: x[1], data))
    y = [arv, gone, abs(arv - gone)]
    print(y)
    x = ["Прибыло", "Убыло", "Разница с пред. периодом"]
    plt.bar(x, y, color=years_info[type]['color'])
    addlabels(x, y)
    plt.title(f"{years_info[type]['name']} {year1}-{year2}")
    plt.ylabel("Количество человек")
    per_cent = round((years_info[type][year1 - 1] + arv - gone) / years_info[type][year1 - 1] * 100)
    if per_cent < 100:
        plt.xlabel(
            f"Численность {years_info[type]['print']} сократилась на {100 - per_cent}% отношению к пред. периоду")
    elif per_cent > 100:
        plt.xlabel(
            f"Численность {years_info[type]['print']} увеличилась на {per_cent - 100}% по отношению к пред. периоду")
    else:
        plt.xlabel(
            f"Численность {years_info[type]['print']} не изменилась по отношению к пред. периоду")
    plt.show()


def derivative(year1, year2, type, cur):
    years_info = {'boyars': {'name': 'Бояре', 'print': 'бояр', 1532: 12, 1547: 20, 1558: 34, 'color': 'darkblue'},
                  'okolnichi': {'name': 'Окольничие', 'print': 'окольничих', 1532: 3, 1547: 7, 1558: 15, 'color': 'gold'}}
    data = cur.execute(
        """SELECT year, arrived, gone FROM {} WHERE year<={} AND year>= {}""".format(type, year2, year1)).fetchall()
    y = list(map(lambda x: x[1] - x[2], data))
    x = list(map(lambda x: x[0], data))
    plt.plot(x, y, color=years_info[type]['color'])
    plt.plot(x, [0] * len(x), color='gray')
    plt.title(f"Измение числа {years_info[type]['print']} за год в {year1}-{year2} годах")
    plt.ylabel("Изменение числа людей")
    plt.xlabel("Год")
    plt.show()


con = sqlite3.connect('boyars.db')
cur = con.cursor()
derivative(1548, 1558, 'okolnichi', cur)
