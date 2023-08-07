from flask import Flask , jsonify, request
from flask_cors import CORS, cross_origin
from joblib import load
import pandas as pd
import numpy as np
from datetime import datetime

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/jugador/*": {"origins": "http://localhost"}})

# Cargar el archivo CSV de jugadores en lista
players_data = pd.read_csv("base_jugadores.csv")
#cargar modelos
loaded_model_overall = load('Modelos\model_overall.joblib')
loaded_model_potential = load('Modelos\model_potential.joblib')
loaded_model_attacking = load('Modelos\model_attacking.pkl')
loaded_model_defensive = load('Modelos\model_defensive.pkl')
# Obtener la fecha actual
current_date = datetime.now()
players_data['birthday'] = pd.to_datetime(players_data['birthday'])
players_data['Age'] = (current_date - players_data['birthday']).dt.days // 365
etiquetas_en_espanol = {
        'player_api_id': 'ID_Jugador',
        'player_name': 'Nombre_Jugador',
        'Age': 'Edad',
        'birthday': 'Fecha_Nacimiento',
        'date': 'Fecha_modificacion',
        'preferred_foot': 'Pie_Preferido',
        'crossing': 'Centros',
        'finishing': 'Finalización',
        'heading_accuracy': 'Precisión_Cabeceo',
        'short_passing': 'Pase_Corto',
        'volleys': 'Voleas',
        'dribbling': 'Regate',
        'curve': 'Efecto',
        'free_kick_accuracy': 'Precisión_Tiros_Libres',
        'long_passing': 'Pase_Largo',
        'ball_control': 'Control_Balón',
        'acceleration': 'Aceleración',
        'sprint_speed': 'Velocidad_Sprint',
        'agility': 'Agilidad',
        'reactions': 'Reacciones',
        'balance': 'Equilibrio',
        'shot_power': 'Potencia_Tiro',
        'jumping': 'Salto',
        'stamina': 'Resistencia',
        'strength': 'Fuerza',
        'long_shots': 'Tiros_Largos',
        'aggression': 'Agresión',
        'interceptions': 'Intercepciones',
        'positioning': 'Posicionamiento',
        'vision': 'Visión',
        'penalties': 'Penales',
        'marking': 'Marcaje',
        'standing_tackle': 'Entradas_Pie_Fijo',
        'sliding_tackle': 'Entradas_Deslizamiento',
        'overall_rating': 'Calificación_Global',
        'potential': 'Potencial',
        'attacking_work_rate': 'Tasa_Trabajo_Atacante',
        'defensive_work_rate': 'Tasa_Trabajo_Defensivo'
}
etiquetas_en_ingles = {
    'ID_Jugador': 'player_api_id',
    'Nombre_Jugador': 'player_name',
    'Edad': 'Age',
    'Fecha_Nacimiento': 'birthday',
    'Fecha_modificacion': 'date',
    'Pie_Preferido': 'preferred_foot',
    'Centros': 'crossing',
    'Finalización': 'finishing',
    'Precisión_Cabeceo': 'heading_accuracy',
    'Pase_Corto': 'short_passing',
    'Voleas': 'volleys',
    'Regate': 'dribbling',
    'Efecto': 'curve',
    'Precisión_Tiros_Libres': 'free_kick_accuracy',
    'Pase_Largo': 'long_passing',
    'Control_Balón': 'ball_control',
    'Aceleración': 'acceleration',
    'Velocidad_Sprint': 'sprint_speed',
    'Agilidad': 'agility',
    'Reacciones': 'reactions',
    'Equilibrio': 'balance',
    'Potencia_Tiro': 'shot_power',
    'Salto': 'jumping',
    'Resistencia': 'stamina',
    'Fuerza': 'strength',
    'Tiros_Largos': 'long_shots',
    'Agresión': 'aggression',
    'Intercepciones': 'interceptions',
    'Posicionamiento': 'positioning',
    'Visión': 'vision',
    'Penales': 'penalties',
    'Marcaje': 'marking',
    'Entradas_Pie_Fijo': 'standing_tackle',
    'Entradas_Deslizamiento': 'sliding_tackle',
    'Calificación_Global': 'overall_rating',
    'Potencial': 'potential',
    'Tasa_Trabajo_Atacante': 'attacking_work_rate',
    'Tasa_Trabajo_Defensivo': 'defensive_work_rate'
}

#metodo para listar todos los jugadores
@app.route('/jugadores', methods=['GET'])
def get_players():
    # Calcular la edad a partir de la fecha de nacimiento
    players_data['birthday'] = pd.to_datetime(players_data['birthday'])
    players_data['Age'] = (current_date - players_data['birthday']).dt.days // 365
    
    # Seleccionar las columnas necesarias
    selected_columns = ['player_api_id', 'player_name', 'Age']
    players_info = players_data[selected_columns]
    
    # Convertir los datos a formato JSON y devolverlos
    players_json = players_info.to_dict(orient='records')
    
    # Cambiar las etiquetas en el JSON
    etiquetas_en_espanol3 = {
        'player_api_id': 'ID',
        'player_name': 'Nombre_Jugador',
        'Age': 'Edad',
        'overall_rating': 'Calificación_Global',
        'potential': 'Potencial',
        'attacking_work_rate': 'Tasa_Trabajo_Atacante',
        'defensive_work_rate': 'Tasa_Trabajo_Defensivo',
        'date': 'Fecha_modificacion'
    }
    
    players_json_con_etiquetas = []
    for player in players_json:
        player_con_etiquetas = {etiquetas_en_espanol3[column]: value for column, value in player.items()}
        players_json_con_etiquetas.append(player_con_etiquetas)
    
    return jsonify(players_json_con_etiquetas)


#Metodo para listar un jugador y que me de todos los detalles del mismo 
@app.route('/jugador/<int:player_id>/detalle', methods=['GET'])
def get_player(player_id):
    player_info = players_data[players_data['player_api_id'] == player_id]
    
    if player_info.empty:
        return jsonify({"error": "Jugador no encontrado"}), 404
    
    player_dict = player_info.iloc[0].to_dict()
    
    
    selected_player_info = {column: player_dict[column] for column in etiquetas_en_espanol.keys()}
    
    
    player_json_con_etiquetas = {etiquetas_en_espanol[column]: value for column, value in selected_player_info.items()}
   
    
    return jsonify(player_json_con_etiquetas)

#metodo para que me de el resumen del jugador 
@app.route('/jugador/<int:player_id>', methods=['GET'])
def get_player_detalle(player_id):
    player_info = players_data[players_data['player_api_id'] == player_id]
    
    if player_info.empty:
        return jsonify({"error": "Jugador no encontrado"}), 404
    
    player_dict = player_info.iloc[0].to_dict()
    etiquetas_en_espanol2 = {
        'player_api_id': 'ID',
        'player_name': 'Nombre_Jugador',
        'Age': 'Edad',
        'overall_rating': 'Calificación_Global',
        'potential': 'Potencial',
        'attacking_work_rate': 'Tasa_Trabajo_Atacante',
        'defensive_work_rate': 'Tasa_Trabajo_Defensivo',
        'date': 'Fecha_modificacion'
    }
    
    selected_player_info = {column: player_dict[column] for column in etiquetas_en_espanol2.keys()} 
    player_json_con_etiquetas = {etiquetas_en_espanol2[column]: value for column, value in selected_player_info.items()}
    return jsonify({'msg':'prediccion nueva', 'datos': player_json_con_etiquetas})


#metodo para predecir y para que ingrese nuevos jugadores
@app.route('/jugador', methods=['POST'])
def prediccion():
    global players_data
    # Obtener los datos del nuevo jugador desde la solicitud POST
    new_player_data = request.json
    new_player_data = {etiquetas_en_ingles[column]: value for column, value in new_player_data.items()}
    new_player_df = pd.DataFrame([new_player_data])
    variables_opA = ['crossing', 'finishing', 'heading_accuracy', 'short_passing', 'volleys','dribbling','curve', 'free_kick_accuracy', 'long_passing', 'ball_control', 'acceleration', 'sprint_speed', 'agility', 'reactions', 'balance', 'shot_power']
    variables_attacking = ['crossing', 'finishing', 'heading_accuracy', 'short_passing', 'volleys', 'dribbling', 'curve', 'free_kick_accuracy', 'long_passing', 'ball_control']
    variables_defensive = ['interceptions', 'positioning', 'marking', 'standing_tackle', 'sliding_tackle']
    # Realizar predicciones con los modelos
    player_overrall = new_player_df[variables_opA]
    player_attacking = new_player_df[variables_attacking]
    player_defensive = new_player_df[variables_defensive]

    new_player_df['overall_rating'] = loaded_model_overall.predict(player_overrall)[0]
    new_player_df['potential'] = loaded_model_potential.predict(player_overrall)[0]
    new_player_df['attacking_work_rate'] = loaded_model_attacking.predict(player_attacking)[0]
    new_player_df['defensive_work_rate'] = loaded_model_defensive.predict(player_defensive)[0]
    new_player_df['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #busca en la base de datos a la persona 

    player_id = int(new_player_data['player_api_id'])
    player_info_idx = players_data[players_data['player_api_id'] == player_id].index
    print(players_data.loc[player_info_idx].shape)
    print(new_player_df.shape)
    if player_info_idx.empty:
        new_player_df['player_api_id'] = player_id
        players_data = players_data.append(new_player_df, ignore_index=True)
        player_info_idx = players_data[players_data['player_api_id'] == player_id].index
    else:
        # Si el jugador existe, actualizar sus atributos
        players_data.loc[player_info_idx, new_player_df.columns] = new_player_df.values

    player_info = players_data.loc[player_info_idx]
    player_dict = player_info.iloc[0].to_dict()
    etiquetas_en_espanol1 = {
        'player_api_id': 'ID',
        'player_name': 'Nombre_Jugador',
        'Age': 'Edad',
        'overall_rating': 'Calificación_Global',
        'potential': 'Potencial',
        'attacking_work_rate': 'Tasa_Trabajo_Atacante',
        'defensive_work_rate': 'Tasa_Trabajo_Defensivo',
        'date': 'Fecha_modificacion'
    }
    
    selected_player_info = {column: player_dict[column] for column in etiquetas_en_espanol1.keys()} 
    player_json_con_etiquetas = {etiquetas_en_espanol1[column]: value for column, value in selected_player_info.items()}
    players_data.to_csv('base_jugadores.csv', index=False )
    return jsonify({'msg':'prediccion nueva', 'datos': player_json_con_etiquetas})



if __name__ == '__main__':
    app.run()
