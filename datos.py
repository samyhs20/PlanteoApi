import pandas as pd 
from sklearn.model_selection import train_test_split

players_data = pd.read_csv("file_train_models\Player.csv", sep=",")
players_data_attributes = pd.read_csv("file_train_models\Player_Attributes.csv", sep=",")
#players_data_attributes = players_data_attributes[]

data_playes_match = pd.merge(players_data, players_data_attributes, left_on='player_api_id', right_on='player_api_id')
# Ordenar el DataFrame por 'nombre' y 'fecha' en orden descendente
df_sorted = data_playes_match.sort_values(by=['player_api_id', 'date'], ascending=[True, False])
# Convertir la columna 'fecha' a tipo datetime
data_playes_match['date'] = pd.to_datetime(data_playes_match['date'])
# Eliminar filas duplicadas basadas en el nombre manteniendo la primera (la más reciente)
df_unique = df_sorted.drop_duplicates(subset=['player_api_id'], keep='first')
variables_use =['player_api_id', 'player_name','birthday','date', 'preferred_foot', 'crossing', 'finishing', 'heading_accuracy',
       'short_passing', 'volleys', 'dribbling', 'curve', 'free_kick_accuracy','long_passing', 'ball_control', 'acceleration', 'sprint_speed',
       'agility', 'reactions', 'balance', 'shot_power', 'jumping', 'stamina','strength', 'long_shots', 'aggression', 'interceptions', 'positioning',
       'vision', 'penalties', 'marking', 'standing_tackle', 'sliding_tackle', 'overall_rating', 'potential','attacking_work_rate', 'defensive_work_rate']
use_data = df_unique[variables_use]

# Eliminar filas con valores nulos
use_data_cleaned = use_data.dropna()

# Dividir los datos en 80% de entrenamiento y 20% de prueba
train_data, test_data = train_test_split(use_data, test_size=0.2, random_state=42)
print("Conjunto de entrenamiento:")
print(train_data)
print("Conjunto de prueba:")
print(test_data)
test_data.to_csv('base_jugadores.csv', index=False )
