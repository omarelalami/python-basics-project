class infrastructures:

    def __init__(self,id_infra,infra_type,length,nb_houses):
        self.id_infra = id_infra
        self.infra_type = infra_type
        self.length = length
        self.nb_houses = nb_houses

    def difficulty_infra(self):
        
        return self.length / self.nb_houses

    
    def list_infra(self):
        pass
    

    def infra_repair(self):
        pass