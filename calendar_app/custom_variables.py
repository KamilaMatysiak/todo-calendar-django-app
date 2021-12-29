months = {
    1: "Styczeń",
    2: "Luty",
    3: "Marzec",
    4: "Kwiecień",
    5: "Maj",
    6: "Czerwiec",
    7: "Lipiec",
    8: "Sierpień",
    9: "Wrzesień",
    10: "Październik",
    11: "Listopad",
    12: "Grudzień"
}

colors_calendar = {'1': {'background': '#ac725e', 'foreground': '#1d1d1d'},
                   '2': {'background': '#d06b64', 'foreground': '#1d1d1d'},
                   '3': {'background': '#f83a22', 'foreground': '#1d1d1d'},
                   '4': {'background': '#fa573c', 'foreground': '#1d1d1d'},
                   '5': {'background': '#ff7537', 'foreground': '#1d1d1d'},
                   '6': {'background': '#ffad46', 'foreground': '#1d1d1d'},
                   '7': {'background': '#42d692', 'foreground': '#1d1d1d'},
                   '8': {'background': '#16a765', 'foreground': '#1d1d1d'},
                   '9': {'background': '#7bd148', 'foreground': '#1d1d1d'},
                   '10': {'background': '#b3dc6c', 'foreground': '#1d1d1d'},
                   '11': {'background': '#fbe983', 'foreground': '#1d1d1d'},
                   '12': {'background': '#fad165', 'foreground': '#1d1d1d'},
                   '13': {'background': '#92e1c0', 'foreground': '#1d1d1d'},
                   '14': {'background': '#9fe1e7', 'foreground': '#1d1d1d'},
                   '15': {'background': '#9fc6e7', 'foreground': '#1d1d1d'},
                   '16': {'background': '#4986e7', 'foreground': '#1d1d1d'},
                   '17': {'background': '#9a9cff', 'foreground': '#1d1d1d'},
                   '18': {'background': '#b99aff', 'foreground': '#1d1d1d'},
                   '19': {'background': '#c2c2c2', 'foreground': '#1d1d1d'},
                   '20': {'background': '#cabdbf', 'foreground': '#1d1d1d'},
                   '21': {'background': '#cca6ac', 'foreground': '#1d1d1d'},
                   '22': {'background': '#f691b2', 'foreground': '#1d1d1d'},
                   '23': {'background': '#cd74e6', 'foreground': '#1d1d1d'},
                   '24': {'background': '#a47ae2', 'foreground': '#1d1d1d'}
                   }
colors_event = {'1': {'background': '#a4bdfc', 'foreground': '#1d1d1d', 'name': 'gray'},   # real name: Perano
                '2': {'background': '#7ae7bf', 'foreground': '#1d1d1d', 'name': 'salad'}, # real name: Riptide
                '3': {'background': '#dbadff', 'foreground': '#1d1d1d', 'name': 'purple'},      # real name: Mauve
                '4': {'background': '#ff887c', 'foreground': '#1d1d1d', 'name': 'pink'},        # real name: Salmon
                '5': {'background': '#fbd75b', 'foreground': '#1d1d1d', 'name': 'yellow'},      # real name: Dandelion
                '6': {'background': '#ffb878', 'foreground': '#1d1d1d', 'name': 'orange'},      # real name: Macaroni And Cheese
                '7': {'background': '#46d6db', 'foreground': '#1d1d1d', 'name': 'cyan'},        # real name: Medium Turquoise
                '8': {'background': '#e1e1e1', 'foreground': '#1d1d1d', 'name': 'grey'},        # real name: Gainsboro
                '9': {'background': '#5484ed', 'foreground': '#1d1d1d', 'name': 'blue'},        # real name: Cornflower Blue
                '10': {'background': '#51b749', 'foreground': '#1d1d1d', 'name': 'green'},      # real name: Fruit Salad
                '11': {'background': '#dc2127', 'foreground': '#1d1d1d', 'name': 'red'},        # real name: Alizarin
                }
vtodo_colors_event = {
    'blue': '9',
    'orange': '6',
    'green': '10',
    'purple': '3',
    'red': '11',
    'gray': '1',
    'salad': '2',
    'pink': '4',
    'yellow': '5',
    'cyan': '7',
    'grey': '8',

}

COLORS = [(c, c) for c in vtodo_colors_event.keys()]
print(COLORS)
timezone = 'Europe/Warsaw'
