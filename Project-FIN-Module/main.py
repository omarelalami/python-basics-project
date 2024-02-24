import pandas as pd
from infrastructures import  infrastructures
from batiment import batiment

if __name__ == '__main__':
    df = pd.read_csv('reseau_en_arbre.csv')
    
    infra_remplacer = df.loc[df['infra_type'] == 'a_remplacer']
    df_inf = infra_remplacer[['infra_id', 'infra_type', 'longueur', 'nb_maisons']]

    df_infra_unq = df_inf.drop_duplicates(subset='infra_id')
    
    # df_infra_unq.to_csv('nom_du_fichier.csv', index=False)


    
    
    obj_infra = [infrastructures(row['infra_id'], row['infra_type'], row['longueur'], 
                             df_infra_unq.groupby('infra_id')['nb_maisons'].sum().loc[row['infra_id']]) 
             for index, row in df_infra_unq.iterrows()]

    
    print(obj_infra[0].difficulty_infra())

     

    

    # print(df_infra_unq)
    
    

    # print(df.head(30))
