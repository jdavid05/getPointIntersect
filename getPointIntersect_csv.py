#===============================================================
# getPointsIntersect.py
# Get points/lines that intersect with polygon/line and print
# out there attributes in console. Can be edited to update a
# csv, database, or spreadsheet.
# Joe Davidson
# Created: 220922
# Edited: 220922
#===============================================================
from arcgis.gis import GIS
from arcgis.geometry import filters
import re
import csv

class lib():
    #===============================================================
    # function: loginAgol
    # purpose : login to ArcGIS Online
    # inputs  : url to ArcGIS Online home, username, and password
    # outputs : connection to ArcGIS Online
    #===============================================================
    def loginAgol(web,usr,pas):
        gis = GIS(url=web, username=usr, password=pas)
        return gis
    #===============================================================
    # function: getPoly
    # purpose : Get the polygon layer used to compute intersects
    # inputs  : The feature ID for the polygon dataset, the where
    #           clause to query the data, the AGOL connection
    # outputs : Query result
    # notes   : Replace the number in polyFeatureLayer.layers[2] to
    #           select a different FC from the feature dataset
    #===============================================================
    def getPoly(ply,whr,gis):
        polyFeatureLayer = gis.content.get(ply)
        polyFeatures = polyFeatureLayer.layers[0]
        for f in polyFeatures.properties.fields:
            print(f['name'])
            sets = 1
        queryResult = polyFeatures.query(where=whr)
        print(len(queryResult))
        return queryResult
    #===============================================================
    # function: getPolyFeat
    # purpose : Get the polygon layer used to compute intersects
    # inputs  : The query result from getPoly and an iterable number
    # outputs : Polygon features
    # notes   : Replace the number in polyFeatureLayer.layers[i] to
    #           select a different FC from the feature dataset
    #===============================================================
    def getPolyFeat(queryResult,i):
        polyFeat = queryResult.features[i].geometry
        return polyFeat
    #===============================================================
    # function: getPoint
    # purpose : Get the point layer used to compute intersects
    # inputs  : The feature ID for the point dataset, the where
    #           clause to query the data, the polygon feature, and
    #           the AGOL connection
    # outputs : Query expression, Point features, AGOL connection
    # notes   : Replace the number in pointFeatureLayer.layers[1] to
    #           select a different FC from the feature dataset
    #===============================================================
    def getPoint(pnt,whr,polyFeat,gis):
        pointFeatureLayer = gis.content.get(pnt)
        pnts = pointFeatureLayer.layers[0]
        for f in pnts.properties.fields:
            print(f['name'])
            sets = 1
        query1 = pnts.query(where=whr, return_ids_only=True, geometry_filter=filters.intersects(polyFeat))
        query1 = str(query1).replace("{'objectIdFieldName': 'OBJECTID', 'objectIds': [","objectid in (")
        query1 = str(query1).replace("]}",") AND CONSTRUCTIONSTATUS = '10'")
        return query1, pnts
    #===============================================================
    # function: queryPoints
    # purpose : Query the points layer based on object ids
    # inputs  : The query expression from getPoint, the AGOL
    #           connection, the points dataset
    # outputs : None
    # notes   : Query expression can be chaged to
    #           pnts.query(where = query, out_fields='field1, field2'
    #           to select which fields are output
    #===============================================================
    def queryPoints(query1,gis,pnts):
        qRes = pnts.query(where = query1, out_fields='FACILITYID,METERSIZE,SERVICEADDRESS,ADDRESSUNIT')
        #print(str(qRes))
        return qRes
    #===============================================================
    # function: buildCsv
    # purpose : Build a csv from the intersects of the points and
    #           the poly
    # inputs  : The query expression from queryPoints and the iterable
    #           number
    # outputs : CSV(s)
    # notes   : Build one or more csvs from a query
    #===============================================================
    def buildCsv(qRes,i):
        # Create lists from each attribute
        xLst = re.findall(r'{"x": (.*?),',str(qRes), re.DOTALL)
        yLst = re.findall(r', "y": (.*?),',str(qRes), re.DOTALL)
        obId = re.findall(r'{"OBJECTID": (.*?),',str(qRes), re.DOTALL)
        fcId = re.findall(r'"FACILITYID": (.*?),',str(qRes), re.DOTALL)
        mtSz = re.findall(r'"METERSIZE": (.*?),',str(qRes), re.DOTALL)
        addr = re.findall(r'"SERVICEADDRESS": (.*?),',str(qRes), re.DOTALL)
        unit = re.findall(r'"ADDRESSUNIT": (.*?)}}',str(qRes), re.DOTALL)
        print(len(unit))
        print(len(obId))
        with open('report_systemMeterArea_'+str(i+1)+'.csv', mode='w',newline="") as c:
            header = ['x','y','objectid','facility id','meter size','address','unit']
            writer=csv.DictWriter(c,fieldnames=header)
            writer.writeheader()
            l = 0
            while l< len(unit):
                writer.writerow({'x':xLst[l],'y':yLst[l],'objectid':obId[l],'facility id':fcId[l].strip('"'),'meter size':mtSz[l].strip('"'),'address':addr[l].strip('"'),'unit':unit[l].strip('"')})
                l = l+1
        
        

if __name__ == '__main__':
    gis = lib.loginAgol('https://testMap.maps.arcgis.com/','username','password')
    queryResult = lib.getPoly('23345ukeuaeou434docfc342','testID is not null', gis)
    polyNum = len(queryResult)
    i = 0
    while i < polyNum:
        print(str(i))
        polyFeat = lib.getPolyFeat(queryResult,i)
        query1, pnts = lib.getPoint('foeu3242345oeuoeuoeue4','1=1',polyFeat,gis)
        qRes = lib.queryPoints(query1,gis,pnts)
        lib.buildCsv(qRes, i)
        i = i+1
