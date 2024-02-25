import pandas as pd
from infrastructures import Infrastructures
from batiment import Batiment

if __name__ == '__main__':
    df = pd.read_csv('reseau_en_arbre.csv')

    infra_remplacer = df.loc[df['infra_type'] == 'a_remplacer']
    df_inf = infra_remplacer[['infra_id', 'infra_type', 'longueur', 'nb_maisons', 'id_batiment']]

    df_infra_unq = df_inf.drop_duplicates(subset='infra_id')
    df_bat_unq = df_inf.drop_duplicates(subset='id_batiment')

    obj_infra = [Infrastructures(row['infra_id'], row['infra_type'], row['longueur'],
                                  df_inf.groupby('infra_id')['nb_maisons'].sum().loc[row['infra_id']])
                 for _, row in df_infra_unq.iterrows()]

    dict_diff = {}

    for _, bat in infra_remplacer.iterrows():
        for i in range(len(obj_infra)):
            if obj_infra[i].search_infra(bat['infra_id']):
                if bat['id_batiment'] not in dict_diff:
                    dict_diff[bat['id_batiment']] = [obj_infra[i].difficulty_infra()]
                else:
                    dict_diff[bat['id_batiment']].append(obj_infra[i].difficulty_infra())

    objs_batiment = [Batiment(row['id_batiment'], dict_diff[row['id_batiment']])
                     for _, row in infra_remplacer.iterrows()]

    diff_batiment = {}

    for o_batiment in objs_batiment:
        diff_batiment[o_batiment.id_batiment] = o_batiment.difficulty_maison()

    data_batiment = pd.DataFrame(list(diff_batiment.items()), columns=['Batiment', 'difficulté'])
    data_batiment = data_batiment.sort_values(by='difficulté')

final_list = []
print(data_batiment.tail())
print(data_batiment)

while not data_batiment.empty:
    print('#' * 30)

    batiment_a_supprimer = data_batiment.iloc[0, 0]
    final_list.append(batiment_a_supprimer)

    infra_remplacer = infra_remplacer.loc[~(infra_remplacer['id_batiment'] == batiment_a_supprimer)]

    df_inf = infra_remplacer[['infra_id', 'infra_type', 'longueur', 'nb_maisons', 'id_batiment']]

    df_infra_unq = df_inf.drop_duplicates(subset='infra_id')
    df_bat_unq = df_inf.drop_duplicates(subset='id_batiment')

    obj_infra = [Infrastructures(row['infra_id'], row['infra_type'], row['longueur'],
                                  infra_remplacer.groupby('infra_id')['nb_maisons'].sum().loc[row['infra_id']])
                 for _, row in infra_remplacer.iterrows()]

    dict_diff = {}

    for _, bat in infra_remplacer.iterrows():
        for i in range(len(obj_infra)):
            if obj_infra[i].search_infra(bat['infra_id']):
                if bat['id_batiment'] not in dict_diff:
                    dict_diff[bat['id_batiment']] = [obj_infra[i].difficulty_infra()]
                else:
                    dict_diff[bat['id_batiment']].append(obj_infra[i].difficulty_infra())

    obj_batiment = [Batiment(row['id_batiment'], dict_diff[row['id_batiment']])
                    for _, row in infra_remplacer.iterrows()]

    diff_batiment = {}

    for o_batiment in obj_batiment:
        diff_batiment[o_batiment.id_batiment] = o_batiment.difficulty_maison()

    data_batiment = pd.DataFrame(list(diff_batiment.items()), columns=['Batiment', 'difficulté'])
    data_batiment = data_batiment.sort_values(by='difficulté')

    print(len(data_batiment))

print(final_list)
