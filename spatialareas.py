import pysal, json
from dbfpy.dbf import Dbf
from mysql.mysqldata import MySQLdata

class SpatialAreas(object):

    def __init__(self, filepath, outname, namelist, idlist, nb="queen", factor=2):
        """
        Initiation of modules
        """
        f=Dbf(filepath+".dbf")
        #Create mapping of locations to row id
        self.locations = dict()
        i=0
        for row in f:
            uid=unicode("".join([row[k] for k in idlist]))
            locnames = unicode(", ".join([row[k] for k in namelist]),"ascii","ignore")
            self.locations[i] = {outname:locnames,"id":uid}
            i+=1
        self.__dict__[outname]= self.locations
        self.outname = outname
        #Get Neightbor weights by queen, rook, knn, distance
        if nb=="queen":
            self.wt = pysal.queen_from_shapefile(filepath+".shp")
        elif nb=="rook":
            self.wt = pysal.rook_from_shapefile(filepath+".shp")
        elif nb=="knn":
            self.wt = pysal.knnW_from_shapefile(filepath+".shp", k=factor)
        elif nb=="distance":
            self.wt = pysal.threshold_binaryW_from_shapefile(filepath+".shp",k)

        #Create dictionary of neighbors for each region
        self.neighbors ={}
        for i,j in enumerate(self.wt):
            self.neighbors[self.locations[i]["id"]] = {self.outname:self.locations[i][self.outname]
                            ,"neighbors":dict([[self.locations[k]["id"],self.locations[k][self.outname]] for k in j.keys()])}

    def get_neighbor_pairs(self):
        pairs = []
        for i in self.neighbors:
            k= self.neighbors[i][self.outname]
            for j in self.neighbors[i]['neighbors']:
                pairs.append([i,k,j,self.neighbors[i]['neighbors'][j]])
        return pairs

    def get_neighbor_json(self):
        return json.dumps(self.neighbors, sort_keys=True)

    def get_census(self, table="spatial_data.fct_census_2010"):
        header, data = MySQLdata().getTable(table, condition ="where state != 'Puerto Rico'")
        data_filtered = []
        location_set =set([int(j['id']) for i,j in self.locations.iteritems()])

        for obs in data:
            if obs[0] in location_set: data_filtered.append(obs)
        return header, sorted(data_filtered)

if __name__=="__main__":
    state = SpatialAreas("/home/den/data/geo/state/tl_2011_us_state"
                   ,"state"
                   ,["NAME"]
                   ,["STUSPS"]
                   , nb="queen"
                   )
    print state.get_neighbor_json()
