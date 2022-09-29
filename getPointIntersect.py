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
    # outputs : Polygon features
    # notes   : Replace the number in polyFeatureLayer.layers[2] to
    #           select a different FC from the feature dataset
    #===============================================================
    def getPoly(ply,whr,gis):
        polyFeatureLayer = gis.content.get(ply)
        polyFeatures = polyFeatureLayer.layers[2]
        queryResult = polyFeatures.query(where=whr)
        polyFeat = queryResult.features[0].geometry
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
        pnts = pointFeatureLayer.layers[1]
        query1 = pnts.query(where=whr, return_ids_only=True, geometry_filter=filters.intersects(polyFeat))
        query1 = str(query1).replace("{'objectIdFieldName': 'OBJECTID', 'objectIds': [","objectid in (")
        query1 = str(query1).replace("]}",")")
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
        qRes = pnts.query(where = query1)
        print(str(qRes))
        

if __name__ == '__main__':
    gis = lib.loginAgol('https://testMapping.maps.arcgis.com/','username','password')
    polyFeat = lib.getPoly('4434244dhaeuttuoaeudhtdse','OBJECTID=9', gis)
    query1, pnts = lib.getPoint('34234deuaeot3234eueou5','1=1',polyFeat,gis)
    lib.queryPoints(query1,gis,pnts)
