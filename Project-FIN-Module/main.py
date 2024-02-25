import pandas as pd
from infrastructures import Infrastructures
from batiment import Batiment

def process_infra_dataframe(df):
    df_infra = df[['infra_id', 'infra_type', 'longueur', 'nb_maisons', 'id_batiment']]
    df_infra_unique = df_infra.drop_duplicates(subset='infra_id')

    infrastructures_list = [
        Infrastructures(row['infra_id'], row['infra_type'], row['longueur'],
                        df_infra.groupby('infra_id')['nb_maisons'].sum().loc[row['infra_id']])
        for _, row in df_infra_unique.iterrows()
    ]

    dict_difficulty = {}
    for _, bat_row in df.iterrows():
        for i, infra in enumerate(infrastructures_list):
            if infra.search_infra(bat_row['infra_id']):
                dict_difficulty.setdefault(bat_row['id_batiment'], []).append(infra.difficulty_infra())

    return dict_difficulty

def process_batiment_dataframe(dict_difficulty):
    batiment_objects = [Batiment(bat_id, dict_difficulty[bat_id]) for bat_id in dict_difficulty]

    difficulty_batiment = {bat_object.id_batiment: bat_object.difficulty_maison() for bat_object in batiment_objects}

    data_batiment = pd.DataFrame(list(difficulty_batiment.items()), columns=['Batiment', 'Difficulté'])
    return data_batiment.sort_values(by='Difficulté')

def main():
    try:
        df = pd.read_csv('reseau_en_arbre.csv')
    except FileNotFoundError:
        print("File 'reseau_en_arbre.csv' not found.")
        return

    infra_to_replace = df.loc[df['infra_type'] == 'a_remplacer']
    final_list = []

    while not infra_to_replace.empty:
        dict_difficulty = process_infra_dataframe(infra_to_replace)
        data_batiment = process_batiment_dataframe(dict_difficulty)

        building_to_remove = data_batiment.iloc[0, 0]
        final_list.append(building_to_remove)

        infra_to_replace = infra_to_replace.loc[~(infra_to_replace['id_batiment'] == building_to_remove)]

    print(final_list)

if __name__ == '__main__':
    main()
