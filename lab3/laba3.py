import os
import datetime
import pandas as pd
import urllib.request
from spyre import server
import matplotlib.pyplot as plt
import seaborn as sns


def vhi_data(province_id, start_year=2000, end_year=2024):

    storage_directory = "lab2"
    if not os.path.exists(storage_directory):
        os.makedirs(storage_directory)
    

    existing_files = []
    for file in os.listdir(storage_directory):
        if file.startswith(f"VHI_ID_{province_id}_") and file.endswith(".csv"):
            existing_files.append(file)
    
    if existing_files:
        return
    

    download_url = (
        f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?"
        f"country=UKR&provinceID={province_id}&year1={start_year}&year2={end_year}&type=Mean"
    )
    vhi_data = urllib.request.urlopen(download_url)
    

    current_date = datetime.datetime.now().strftime("%d-%m-%Y")
    current_time = datetime.datetime.now().strftime("%H-%M-%S")
    filename = f"VHI_ID_{province_id}_{current_date}_{current_time}.csv"
    

    file_path = os.path.join(storage_directory, filename)
    with open(file_path, 'wb') as output_file:
        output_file.write(vhi_data.read())
    
for province_id in range(1, 28):

    vhi_data(province_id, 1982, 2024)

def read_files(directory):
    files = os.listdir(directory)
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    data_frame = pd.DataFrame()
    
    for i in range(len(files)):
        file_path = os.path.join(directory, files[i])

        province_id = int(files[i].split('_')[2])
        
        if province_id in [12, 20]:
            continue
        
        df = pd.read_csv(file_path, header=1, names=headers)
        
        df = df.drop(df.loc[df['VHI'] == -1].index)
        
        df['area'] = i + 1
        
        df['Year'] = df['Year'].str.replace('<tt><pre>', '', regex=False)
        
        df = df.drop(df[df['Year'] == '</pre></tt>'].index)

        df.drop('empty', axis = 1, inplace=True)
        
        df['Year'] = df['Year'].astype(int)

        df['Week'] = df['Week'].astype(int)
        
        data_frame = pd.concat([data_frame, df], ignore_index=True)
    
    return data_frame

directory = "lab2"
vhi_data_frame = read_files(directory)

province_indexes = {
    1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21,
    11: 9, 13: 10, 14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16,
    21: 17, 22: 18, 23: 6, 24: 1, 25: 2, 26: 7, 27: 5
}
vhi_data_frame["area"].replace(province_indexes, inplace = True)




class VHI3(server.App):
    title = "NOAA. Logo National Oceanic and Atmospheric Administration"
    inputs = [
        {
            'type': 'dropdown',
            'label': 'Unit',
            'options': [
                {'label': 'VHI', 'value': 'VHI'},
                {'label': 'TCI', 'value': 'TCI'},
                {'label': 'VCI', 'value': 'VCI'},
            ],
            'variable_name': 'index',
            'action_id': 'update'
        },
        {
            'type': 'dropdown',
            'label': 'Province',
            "options": [
                {"label": "Вінницька", "value": 1},
                {"label": "Волинська", "value": 2},
                {"label": "Дніпропетровська", "value": 3},
                {"label": "Донецька", "value": 4},
                {"label": "Житомирська", "value": 5},
                {"label": "Закарпатська", "value": 6},
                {"label": "Запорізька", "value": 7},
                {"label": "Івано-Франківська", "value": 8},
                {"label": "Київська", "value": 9},
                {"label": "Кіровоградська", "value": 10},
                {"label": "Луганська", "value": 11},
                {"label": "Львівська", "value": 12},
                {"label": "Миколаївська", "value": 13},
                {"label": "Одеська", "value": 14},
                {"label": "Полтавська", "value": 15},
                {"label": "Рівненська", "value": 16},
                {"label": "Сумська", "value": 17},
                {"label": "Тернопільська", "value": 18},
                {"label": "Харківська", "value": 19},
                {"label": "Херсонська", "value": 20},
                {"label": "Хмельницька", "value": 21},
                {"label": "Черкаська", "value": 22},
                {"label": "Чернівецька", "value": 23},
                {"label": "Чернігівська", "value": 24},
                {"label": "Республіка Крим", "value": 25},
            ],
            'variable_name': 'area',
            'action_id': 'update'
        },
        {
            'type': 'text',
            'label': 'Year 1982-2024',
            'variable_name': 'year',
            'value': '1982-2024', 
            'action_id': 'update'
        },
        {
            'type': 'text',
            'label': 'Week (1-52)',
            'variable_name': 'week',
            'value': '1-52',
            'action_id': 'update'
        }
    ]
    tabs = ['Table', 'Plot']

    controls = [{
        "type": "hidden",
        "label": "get data",
        "id": "update"
    }]

    outputs = [
        {
            'id': 'table_output',
            'type': 'table',
            'control_id': 'update',
            'tab': 'Table'
        },
        {
            'id': 'plot_output',
            'type': 'plot',
            'control_id': 'update',
            'tab': 'Plot'
        }
    ]

    def table_output(self, params):
        week_range = params['week'].split('-')
        week_range_1 = int(week_range[0])
        week_range_2 = int(week_range[1])

        year_range = params['year'].split('-')
        year_range_1 = int(year_range[0])
        year_range_2 = int(year_range[1])

        index = params['index']
        table = vhi_data_frame[['Year', 'Week', index, 'area']][(vhi_data_frame['Year'].between(year_range_1, year_range_2)) & (vhi_data_frame['Week'].between(week_range_1, week_range_2))
                                                                & (vhi_data_frame['area'] == int(params['area']))]
        return table

    def plot_output(self, params):
        y = params['index']
        table = self.table_output(params)
        plt.figure(figsize=(15, 8))
        plt.title(f'{y} залежність від часу')
        plt.ylabel(y)
        plt.xlabel('week')
        sns.set_style('ticks')
        graph = sns.lineplot(data=table, x='Week', y=y)
        return graph

app = VHI3()
app.launch()