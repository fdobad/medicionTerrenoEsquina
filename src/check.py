#!python3
'''
    Preparado por Fernando Badilla Veliz fernando@badilla.cl, bajo la siguiente licencia:

    ANTI-CAPITALIST SOFTWARE LICENSE (v 1.4)

    Copyright © 2021 Fernando Badilla

    This is anti-capitalist software, released for free use by individuals and organizations that do not operate by capitalist principles.

    Permission is hereby granted, free of charge, to any person or organization (the "User") obtaining a copy of this software and associated documentation files (the "Software"), to use, copy, modify, merge, distribute, and/or sell copies of the Software, subject to the following conditions:

        1. The above copyright notice and this permission notice shall be included in all copies or modified versions of the Software.

        2. The User is one of the following:
            a. An individual person, laboring for themselves
            b. A non-profit organization
            c. An educational institution
            d. An organization that seeks shared profit for all of its members, and allows non-members to set the cost of their labor

            3. If the User is an organization with owners, then all owners are workers and all workers are owners with equal equity and/or equal vote.

            4. If the User is an organization, then the User is not law enforcement or military, or working for or under either.

            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT EXPRESS OR IMPLIED WARRANTY OF ANY KIND, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import csv,sys
from numpy import arctan2,sin,cos,array,radians,pi

a= 6378137#equitorial radius in m
b= 6356752#polar radius in m

def Distance(lat1, lons1, lat2, lons2):
    '''
    distance in a oblate spheroid
    https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
    '''
    lat1=radians(lat1)
    lons1=radians(lons1)
    R1=(((((a**2)*cos(lat1))**2)+(((b**2)*sin(lat1))**2))/((a*cos(lat1))**2+(b*sin(lat1))**2))**0.5 #radius of earth at lat1
    x1=R1*cos(lat1)*cos(lons1)
    y1=R1*cos(lat1)*sin(lons1)
    z1=R1*sin(lat1)

    lat2=radians(lat2)
    lons2=radians(lons2)
    R2=(((((a**2)*cos(lat2))**2)+(((b**2)*sin(lat2))**2))/((a*cos(lat2))**2+(b*sin(lat2))**2))**0.5 #radius of earth at lat2
    x2=R2*cos(lat2)*cos(lons2)
    y2=R2*cos(lat2)*sin(lons2)
    z2=R2*sin(lat2)

    return ((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)**0.5

def FourGonArea(x1,y1,x2,y2,x3,y3,x4,y4):
    '''
    https://mathworld.wolfram.com/PolygonArea.html
    Note that the area of a convex polygon is defined to be positive if the points are arranged in a counterclockwise order, and negative if they are in clockwise order (Beyer 1987). 
    
    Se asume que la lista viene en orden antihorario

    '''
    return 0.5*(x1*y2 - x2*y1 + x2*y3 - x3*y2 + x3*y4 - x4*y3)

def Bearing(alat,alon,blat,blon):
    '''
    http://www.movable-type.co.uk/scripts/latlong.html
    '''
    dL = blon-alon
    X = cos(blat)* sin(dL)
    Y = cos(alat)*sin(blat) - sin(alat)*cos(blat)* cos(dL)
    return arctan2(X,Y)

def latlong2planar(alat,alon,blat,blon):
    d = Distance(alat,alon,blat,blon)
    b = Bearing(alat,alon,blat,blon)
    return [d*cos(pi/2-b),d*sin(pi/2-b)]

def latlon4Area0(alat,alon,blat,blon,clat,clon,dlat,dlon):
    x1,y1=0,0
    x2,y2=array([0,0])+array(latlong2planar(alat,alon,blat,blon))
    x3,y3=array([0,0])+array(latlong2planar(alat,alon,clat,clon))
    x4,y4=array([0,0])+array(latlong2planar(alat,alon,dlat,dlon))
    #print('1',x1,y1)
    #print('2',x2,y2)
    #print('3',x3,y3)
    #print('4',x4,y4)
    return FourGonArea(x1,y1,x2,y2,x3,y3,x4,y4)

def latlon4Area1(alat,alon,blat,blon,clat,clon,dlat,dlon):
    x1,y1=1,1
    x2,y2=array([1,1])+array(latlong2planar(alat,alon,blat,blon))
    x3,y3=array([1,1])+array(latlong2planar(alat,alon,clat,clon))
    x4,y4=array([1,1])+array(latlong2planar(alat,alon,dlat,dlon))
    #print('1',x1,y1)
    #print('2',x2,y2)
    #print('3',x3,y3)
    #print('4',x4,y4)
    return FourGonArea(x1,y1,x2,y2,x3,y3,x4,y4)

def main():
    nombre,lat,lon=[],dict(),dict()
    with open('../doc/resumenKML.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ')
        spamreader.__next__()
        print('Nombre, longitud, latitud')
        for row in spamreader:
            nombre.append(row[0])
            lon[nombre[-1]]=float(row[1])
            lat[nombre[-1]]=float(row[2])
            print(', '.join(row))
    
    distancias=dict()
    for n1 in nombre:
        for n2 in nombre:
            if n1!=n2:
                aux=Distance( lat[n1], lon[n1], lat[n2], lon[n2])
                distancias[(n1,n2)]=aux
                #print(n1,n2, Distance( lat[n1], lon[n1], lat[n2], lon[n2]) )
                if (n1=='EsquinaSurPon' and n2=='EsquinaNorPon') or\
                   (n1=='EsquinaNorPon' and n2=='CanalNorOri') or\
                   (n1=='EsquinaSurPon' and n2=='CanalSurOri') or\
                   (n1=='EsquinaNorPon' and n2=='CorreccionNor') or\
                   (n1=='EsquinaSurPon' and n2=='CorreccionSur'):
                       print('distancia entre',n1,'y',n2,':',aux)
    
    for n1 in nombre:
        for n2 in nombre:
            if n1!=n2:
                assert distancias[(n1,n2)] == distancias[(n2,n1)]
    
    atm0 = latlon4Area0( lat['EsquinaSurPon'], lon['EsquinaSurPon'],
                 lat['CanalSurOri'], lon['CanalSurOri'],
                 lat['CanalNorOri'], lon['CanalNorOri'],
                 lat['EsquinaNorPon'], lon['EsquinaNorPon'])
    print('Area terreno medido 0', atm0)
    ac0 = latlon4Area0( lat['EsquinaSurPon'], lon['EsquinaSurPon'],
                 lat['CorreccionSur'], lon['CorreccionSur'],
                 lat['CorreccionNor'], lon['CorreccionNor'],
                 lat['EsquinaNorPon'], lon['EsquinaNorPon'])
    print('Area corregida 0', ac0)

    atm1 = latlon4Area1( lat['EsquinaSurPon'], lon['EsquinaSurPon'],
                 lat['CanalSurOri'], lon['CanalSurOri'],
                 lat['CanalNorOri'], lon['CanalNorOri'],
                 lat['EsquinaNorPon'], lon['EsquinaNorPon'])
    print('Area terreno medido 1', atm1)
    ac1 = latlon4Area1( lat['EsquinaSurPon'], lon['EsquinaSurPon'],
                 lat['CorreccionSur'], lon['CorreccionSur'],
                 lat['CorreccionNor'], lon['CorreccionNor'],
                 lat['EsquinaNorPon'], lon['EsquinaNorPon'])
    print('Area corregida 1', ac1)
    print('delta medido', atm1 - atm0)
    print('delta corregida', ac1 - ac0)

if __name__ == "__main__":
    sys.exit(main())
