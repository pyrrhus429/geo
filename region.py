from spatialareas import SpatialAreas
import numpy as np
import pysal
import random, csv

"""
Contruct regions based on given demographics
"""

class Region(SpatialAreas):
    def __init__(self, filepath, outname, namelist, idlist, nb="queen", factor=2):
        super(Region,self).__init__(filepath, outname, namelist, idlist, nb="queen", factor=2)
    
    def loc2row(self,idname):
        """Reverse lookup of row number by some location name, e.g, state, county"""
        loc2row ={}
        for i,j in self.locations.items():
            loc2row[j[idname]]=i
        return loc2row

    def get_attr(self,f,region,*args):
        """Makes a dict of attr data pulled from csv"""
        attr = csv.DictReader(open(f,'rb'),quotechar='"')
        data = {}
        for row in attr:
            row_dict={}
            for i in args:
                try:
                    row_dict[i]=float(row[i])
                except:
                    row_dict[i]=row[i]
            data[row[region]] = row_dict
        return data

    def map_wt2data(self, idname, data):
        """Align wt to external data"""
        loc2row = self.loc2row(idname)
        wt2data = []
        for i,j in enumerate(self.wt):
            try:
                x = [v for k,v in data[self.locations[i][idname]].items()]
                wt2data.append([i, self.locations[i][idname], j, x])
            except:
                x=[0,0]
                wt2data.append([i, self.locations[i][idname], j, x])
        return wt2data

    def build_region(self, dataid, data, floor, floor_col, initial):
        wt = []
        pci = []
        floor_list=[]
        for i,j,w,x in self.map_wt2data(dataid,data):
            wt.append(w)
            pci.append(x)
            floor_list.append(x[floor_col])

        pci_array=np.array(pci)
        print pci_array[0]
        r=pysal.Maxp(state.wt,pci_array, floor=floor,floor_variable=np.array(floor_list), initial=initial)
        regions = []
        for i in r.regions:
            regions.append(sorted([state.locations[j]['id'] for j in i]))
        r.inference()
        return r, regions

if __name__=="__main__":
    state = Region("/home/den/data/geo/state/state48/state48"
                   ,"state"
                   ,["NAME"]
                   ,["STUSPS"]
                   , nb="queen"
                   )
    """
    j=state.wt[1]
    for i in j:
        print state.locations[i]
    print state.loc2row('state')
    """

    data=state.get_attr("/home/den/data/census/state_example.csv"
                        ,'State'
                        , 'Population'
                        , 'pct_male'
                        ,'age_median'
                        ,'pct_white'
                        ,'pct_renters')

    i,j = state.build_region('state', data, 10000000,4,999)
    for k in j:
        print k

