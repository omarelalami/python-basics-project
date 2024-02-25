import pandas as pd
from infrastructures import infrastructures
from batiment import batiment

if __name__ == '__main__':
    df = pd.read_csv('reseau_en_arbre.csv')

    infra_remplacer = df.loc[df['infra_type'] == 'a_remplacer']
    df_inf = infra_remplacer[['infra_id', 'infra_type', 'longueur', 'nb_maisons','id_batiment']]

    df_infra_unq = df_inf.drop_duplicates(subset='infra_id')
    df_bat_unq = df_inf.drop_duplicates(subset='id_batiment')

    # df_infra_unq.to_csv('nom_du_fichier.csv', index=False)

   
   

    obj_infra = [infrastructures(row['infra_id'], row['infra_type'], row['longueur'],
                                  df_inf.groupby('infra_id')['nb_maisons'].sum().loc[row['infra_id']])
                 for index, row in df_infra_unq.iterrows()]

    dict_diff = {}




    
    for index, bat in df_bat_unq.iterrows():
        for i in range(len(obj_infra) - 1):
            if obj_infra[i].search_infra(bat['infra_id']):
                if bat['id_batiment'] not in dict_diff:
                    dict_diff[bat['id_batiment']] = [obj_infra[i].difficulty_infra()]
                else:
                    dict_diff[bat['id_batiment']].append(obj_infra[i].difficulty_infra())

    # print(dict_diff)

    obj_batiment = [batiment(row['id_batiment'], dict_diff[row['id_batiment']]).difficulty_maison()
                 for index, row in df_bat_unq.iterrows()]
    
    print(dict_diff.values().sort())



    # print(obj_infra[0].difficulty_infra())
    # print(df_infra_unq)
    # print(df.head(30))
