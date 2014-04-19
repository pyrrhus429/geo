File Edit Options Buffers Tools Python Help
import sys, csv
from spatialareas import SpatialAreas


def getCounties():
    return SpatialAreas("/directory/20120426_census/map/tl_2010_us_county10/tl_2010_us_county10"
                   ,"county"
                   ,["NAME10"]
                   ,["STATEFP10","COUNTYFP10"])

def getStates():
    return SpatialAreas("/directory/20120426_census/map/tl_2010_us_state10/tl_2010_us_state10"
                   ,"state"
                   ,["NAME10"]
                   ,["STUSPS10"])

def getZip3():
    return SpatialAreas("/directory/20120426_census/map/zip3/zip3"
                   ,"zip3"
                   ,["ZIP3"]
                   ,["ZIP3"])

def getZip3_2000():
    return SpatialAreas("/directory/20120426_census/map/zip3_2000/zip3_2000"
                   ,"zip3"
                   ,["NAME"]
                   ,["ZCTA3"])



if __name__=="__main__":
    zip3 = getZip3_2000()
    dir = ""
    f = open(dir + sys.argv[1],"wt")
    writer = csv.writer(f)
    writer.writerow(["i","i_code","j","j_code"])
    writer.writerows(zip3.get_neighbor_pairs())
