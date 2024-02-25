

class Batiment:
    def __init__(self, id_batiment,list_infra) :
         
         self.id_batiment = id_batiment
         self.list_infra = list_infra

        
    def difficulty_maison(self):
         
         return sum(self.list_infra)
      


    def list_batiment(self):
         pass
    
    def batiment_byid(self):
         pass
    

    def batiment_repair(self):
         pass