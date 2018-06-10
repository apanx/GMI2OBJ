import sys
import os
import struct

OBJ_boilerplate = '232020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020200a2320202020202020202020202020202020202020202020202020202020202020202020202020202020205f5f20205f2e2d2d2727606027272d2d2e2e202020202020200a23202020202020202020202020202020202020202020202020202020202020202020202020202020202f20205c2f2020202020202020202020202020602e20202020200a2320202020202020202020202020202020202020202020202020202020202020202020202020202028202f20205c5f5f5f202020202020202020202020205c202020200a232020202020202020202020202020202020202020202020202020202020202020202020202020207c207c20202020202060272d2e202020205f5f202020205c2020200a23202020202020202020202020202020202020202020202020205f5f5f20202020202020202020202820272e202020202020205f5f602e2760205c602e2020205c20200a232020202020202020202020202020202020205f5f5f20202028202020602e2020202020202020202f5c202020202c2e202e275f5f5c20202f20603a5f5c2020205c200a23202020202020202020202020202020202028202020602d2e20602e202020602e2020202020202f20205c5f205f5f2e60202f202e2d7c207c272e7c3d205c2020207c0a23202020202020202020202020202020202020602d2e202020602d2e602e202020602e2020203a20202020725f5f2c272028202857577c205c57296a2020207c20207c0a23202020202020202020202020202020202020202020602e20202020602e5c2020205f5c20207c202020207c202020205c5f5c5f602f20202060602d2e202f20202f200a232020202020202020202020202e2d2d2727276060602d5f602d2c2020206020202820207c207c202020207c2020202020202020202020205c5f5f2f2e60202e6020200a2320202020202020202020202f2020202020202020202820606060202020205f5f205c20205c7c202020205c202020202d2c5f5f5f5f5f5f2e2d272f20202f202020200a23202020202020202020202f2020202020202020202020602d2e5f202020282020602e5c2020272e202020205c2020202020202f272e2020202e27202e2720202020200a232020202020202020202f2020202020202020202c2e2d2d27273e602d2e20602d2e20602020207c2020202020602e2020202820207c20202f20202f2020205f2020200a232020202020202020282020202020202020207c20202020202f20385938605f3a20605f3a2e207c202020202020205c2020205c207c206c202028202c3a27205c20200a2320202020202020207c20202020202020202e27202020207c20202020202820202028202020202820202020202020205c2020207c5c207c2020205c202029202029200a2320202020202020207c202020202020202e2720202020207c203859382020602d2d2d3a2e5f5f2d5c20202020202020205c20207c20602e202020206060202e2720200a2320202020202020207c202020202020207c2020202020207c202020202038593820202020202020205c20202020202020205c206a20202060272d2e2e2d27202020200a2320202020202020207c20202020202020272e202020202f205c20202020202020202f202020202020207c20202020202020207c2020202020202020202020202020200a2320202020202020207c20202020202020207c2e2d2d272020207c2020202020202f2d2c5f5f5f5f5f5f7c20202020202020207c2020202020202020202020202020200a2320202020202020206c20202020202020207c20202020205f2f2020202020202f20202020202e2d2e207c202020202020202f205c20202020202020202020202020200a232020202020202020205c20202020202020272e2020202f202020202020202f202020202028202860202f2020202020202f2020205c202020202020202020202020200a232020202020205f5f20205c202020202020207c2020207c2020202020207c2020202020207c5c206060202020205f2e272020202020292020202020202020202020200a23202020202e27202f2020205c2020202020207c5f5f2f7c2020202020207c2020202020207c20602d2e5f2e2d2728202020202020207c2020202020202020202020200a23202020207c20285f202020207c2020202020207c20207c2020202020207c2020202020207c2020202020207c20205c2020202020207c2020202020202020202020200a23202020202720202060272d60202020202020207c20207c202020202020205c20202020207c202020202020205c2020602e5f5f5f2f202020202020202020202020200a232020202020602d2e2e5f5f5f5f5f5f5f5f5f2f202020205c5f5f5f5f5f5f5f2920202020205c5f5f5f5f5f5f5f2920202020202020202020202020202020202020200a230a230a'

#byte reading code
def readNF(file_object, num):
    data = file_object.read(num)
    file_object.seek(num * -1, 1)
    return data

def getInteger(file_object):
    data = struct.unpack("<i", file_object.read(4))
    return int(data[0])

def getIntegerNF(file_object):
    data = getInteger(file_object)
    file_object.seek(-4, 1)
    return data

def getString(file_object):
    i = 0
    size = getInteger(file_object)

    if (size == 0):
        return ""
    data = file_object.read(size).rstrip('\0')

    return data

def getRGB(file_object, isRA1 = 0):
    data = struct.unpack("BBB", file_object.read(3))
    file_object.read(1)

    if not isRA1:
        data = "0x" + struct.pack("BBB", data[0], data[1],data[2]).encode('hex')
    else:
        data = "0x" + struct.pack("BBB", data[2], data[1],data[0]).encode('hex')
    return data

def getFloat(file_object):
    data = struct.unpack("<f", file_object.read(4))
    return float(data[0])
    
def tab(file, num):
    for i in range(num):
        file.write("\t")

def getObject(file_object):
    object_type = getInteger(file_object)
    object_version = getInteger(file_object)
    object_version2 = getInteger(file_object)
    print object_type, object_version, object_version2
    return object_type, object_version, object_version2

#Loading loops
def readMaterialList(GMI_file, MTL_file, GMA_file, isRA1 = 0):
    matNumber = getInteger(GMI_file)
    print "Reading {} material(s)".format(matNumber)
    
    GMA_file.write("%s\n" % "*MATERIAL_LIST")
    GMA_file.write("%s\n" % "{")
    tab(GMA_file, 1); GMA_file.write("%s\n" % "*MATERIAL_COUNT\t{}".format(matNumber))
    for i in range(matNumber):
        object_type, object_version, object_version2 = getObject(GMI_file)
        if object_type == 8 and object_version == 2:
            matRef = getInteger(GMI_file)
            matName = getString(GMI_file)
            print "Decompiling MATERIAL "+ matName
            matClass = getString(GMI_file)
            matAmbient = getRGB(GMI_file, isRA1)
            matDiffuse = getRGB(GMI_file, isRA1)
            matSpecular = getRGB(GMI_file, isRA1)
            matShine = getFloat(GMI_file)
            matShineStrength = getFloat(GMI_file)
            matTransparency = getFloat(GMI_file)
            matWiresize = getFloat(GMI_file)
        
            matShading = getInteger(GMI_file)
            if matShading == 9:
                matShading = "Constant"
            elif matShading == 10:
                matShading = "Phong"
            elif matShading == 11:
                matShading = "Metal"
            elif matShading == 12:
                matShading = "Blinn"
            else:
                matShading = "Other"
            
            matXPFallof = getFloat(GMI_file)
            matSelfillum = getFloat(GMI_file)

            matProp = getInteger(GMI_file)

            matFallof = "Out"
            if matProp != 32:
                matFallof = "In"

            if matProp == 1:
                matProp = "*MATERIAL_TWOSIDED"
            elif matProp == 2:
                matProp = "*MATERIAL_WIRE"
            elif matProp == 4:
                matProp = "*MATERIAL_WIREUNITS"
            elif matProp == 8:
                matProp = "*MATERIAL_FACEMAP"
            elif matProp == 16:
                matProp = "*MATERIAL_SOFTEN"
            else:
                matProp = ""

            matXPType = getInteger(GMI_file)
            if matXPType == 1:
                matXPType = "Filter"
            elif matXPType == 2:
                matXPType = "Subtractive"
            elif matXPType == 3:
                matXPType = "Additive"
            else:
                matXPType = "Other"
        
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*MATERIAL")
            tab(GMA_file, 1); GMA_file.write("%s\n" % "{")
            tab(GMA_file, 2); GMA_file.write("%s\n" % "*MATERIAL_REF_NO\t{}".format(matRef))
            tab(GMA_file, 2); GMA_file.write("%s\n" % "*MATERIAL_NAME\t{}".format(matName))
            tab(GMA_file, 2); GMA_file.write("%s\n" % "*MATERIAL_CLASS\t{}".format(matClass))
            tab(GMA_file, 2); GMA_file.write("%s\n" % "*MATERIAL_AMBIENT\t{}".format(matAmbient))
            tab(GMA_file, 2); GMA_file.write("%s\n" % "*MATERIAL_DIFFUSE\t{}".format(matDiffuse))
            tab(GMA_file, 2); GMA_file.write("%s\n" % "*MATERIAL_SPECULAR\t{}".format(matSpecular))
            tab(GMA_file, 2); GMA_file.write("%s\n" % "*MATERIAL_SHINE\t{:f}".format(matShine))
            tab(GMA_file, 2); GMA_file.write("%s\n" % "*MATERIAL_SHINESTRENGTH\t{:f}".format(matShineStrength))
            tab(GMA_file, 2); GMA_file.write("%s\n" % "*MATERIAL_TRANSPARENCY\t{:f}".format(matTransparency))
            tab(GMA_file, 2); GMA_file.write("%s\n" % "*MATERIAL_WIRESIZE\t{:f}".format(matWiresize))
            tab(GMA_file, 2); GMA_file.write("%s\n" % "*MATERIAL_SHADING\t{}".format(matShading))
            tab(GMA_file, 2); GMA_file.write("%s\n" % "*MATERIAL_XP_FALLOFF\t{:f}".format(matXPFallof))
            tab(GMA_file, 2); GMA_file.write("%s\n" % "*MATERIAL_SELFILLUM\t{:f}".format(matSelfillum))
            if matProp != "":
                tab(GMA_file, 2); GMA_file.write("%s\n" % matProp)
            tab(GMA_file, 2); GMA_file.write("%s\n" % "*MATERIAL_FALLOFF\t{}".format(matFallof))
            tab(GMA_file, 2); GMA_file.write("%s\n" % "*MATERIAL_XP_TYPE\t{}".format(matXPType))
        
            textNum = getInteger(GMI_file)
            if textNum > 0:
                object_type, object_version, object_version2 = getObject(GMI_file)
                if object_type == 14 and object_version == 2:
                    readTextureList(GMI_file, MTL_file, GMA_file, isRA1)
            matNum = getInteger(GMI_file)
            if matNum > 0:
                object_type, object_version, object_version2 = getObject(GMI_file)
                if object_type == 7 and object_version == 2:
                    readMaterialList(GMI_file, MTL_file, GMA_file, isRA1)
            tab(GMA_file, 1); GMA_file.write("%s\n" % "}")
    GMA_file.write("%s\n" % "}")

def readTextureList(GMI_file, MTL_file, GMA_file, isRA1 = 0):
        totalCount = getInteger(GMI_file)
        print "Decompiling \tTEXTURE_LIST"
            
        tab(GMA_file, 2); GMA_file.write("%s\n" % "*TEXTURE_LIST")
        tab(GMA_file, 2); GMA_file.write("%s\n" % "{")
        tab(GMA_file, 3); GMA_file.write("%s\n" % "*TEXTURE_COUNT\t{}".format(totalCount))
        for i in range(totalCount):
            object_type, object_version, object_version2 = getObject(GMI_file)
            if object_type == 15 and (object_version == 2 or object_version == 4):
                mapName = getString(GMI_file)
                print "Decompiling \tTEXTURE " + mapName
                mapClass = getString(GMI_file)
                mapBitmap = getString(GMI_file)
                mapAmount = getFloat(GMI_file)
                
                mapStyle = getInteger(GMI_file)

                if mapStyle == 0:
                    mapStyle = "*MAP_AMBIENT"
                elif mapStyle == 1:
                    mapStyle = "*MAP_DIFFUSE"
                elif mapStyle == 2:
                    mapStyle = "*MAP_SPECULAR"
                elif mapStyle == 3:
                    mapStyle = "*MAP_SHINE"
                elif mapStyle == 4:
                    mapStyle = "*MAP_SHINESTRENGTH"
                elif mapStyle == 5:
                    mapStyle = "*MAP_SELFILLUM"
                elif mapStyle == 6:
                    mapStyle = "*MAP_OPACITY"
                elif mapStyle == 7:
                    mapStyle = "*MAP_FILTERCOLOR"
                elif mapStyle == 8:
                    mapStyle = "*MAP_BUMP"
                elif mapStyle == 9:
                    mapStyle = "*MAP_REFLECT"
                elif mapStyle == 10:
                    mapStyle = "*MAP_REFRACT"
                elif mapStyle == 11:
                    mapStyle = "*MAP_DISPLACEMENT"
                elif mapStyle == 12:
                    mapStyle = "*MAP_NAME"
                elif mapStyle == 13:
                    mapStyle = "*MAP_GENERIC"
                else:
                    mapStyle = "*MAP_UNKNOWN"
                    print "Unknown Map Style: {}".format(mapStyle)
                
                mapType = getInteger(GMI_file)
                if mapType == 0:
                    mapType = "Explicit"
                elif mapType == 1:
                    mapType = "Spherical"
                elif mapType == 2:
                    mapType = "Cylindrical"
                elif mapType == 3:
                    mapType = "Shrinkwrap"
                elif mapType == 4:
                    mapType = "Screen"
                else:
                    mapType = "UNKNOWN"
                    print "Unknown Map mapType: {}".format(mapType)

                mapUO = getFloat(GMI_file)
                mapVO = getFloat(GMI_file)
                mapUT = getFloat(GMI_file)
                mapVT = getFloat(GMI_file)
                mapUVWAngle = getFloat(GMI_file)
                mapUVWBlur = getFloat(GMI_file)
                mapUVWBlurOffset = getFloat(GMI_file)
                mapUVWNouseAmt = getFloat(GMI_file)
                mapUVWNoiseSize = getFloat(GMI_file)
                mapUVWNoiseLevel = getInteger(GMI_file)
                mapUVWNoisePhase = getFloat(GMI_file)
                mapBitmapInvert = getInteger(GMI_file)
                mapBitmapColorMap = getInteger(GMI_file)
                mapBitmapFilter = getInteger(GMI_file)
                if mapBitmapFilter > 0:
                    if mapBitmapFilter == 1:
                        mapBitmapFilter = "SAT"
                    else:
                        mapBitmapFilter = "None"
                else:
                    mapBitmapFilter = "Pyramidal"
                
                if isRA1 == 0:
                    mapBitmapChannel = getInteger(GMI_file)
                    texNum = getInteger(GMI_file)
                    if texNum > 0:
                        object_type, object_version, object_version2 = getObject(GMI_file)
                        if object_type == 14 and object_version == 2:
                            readTextureList(GMI_file, MTL_file, GMA_file, isRA1)
                
                tab(GMA_file, 3); GMA_file.write("%s\n" % "*TEXTURE")
                tab(GMA_file, 3); GMA_file.write("%s\n" % "{")
                tab(GMA_file, 4); GMA_file.write("%s\n" % "*MAP_NAME\t{}".format(mapName))
                tab(GMA_file, 4); GMA_file.write("%s\n" % "*MAP_CLASS\t{}".format(mapClass))
                tab(GMA_file, 4); GMA_file.write("%s\n" % "*BITMAP\t{}".format(mapBitmap))
                tab(GMA_file, 4); GMA_file.write("%s\n" % "*MAP_AMOUNT\t{:f}".format(mapAmount))
                tab(GMA_file, 4); GMA_file.write("%s\n" % "{}".format(mapStyle))
                tab(GMA_file, 4); GMA_file.write("%s\n" % "*MAP_TYPE\t{}".format(mapType))
                tab(GMA_file, 4); GMA_file.write("%s\n" % "*UVW_U_OFFSET\t{:f}".format(mapUO))
                tab(GMA_file, 4); GMA_file.write("%s\n" % "*UVW_V_OFFSET\t{:f}".format(mapVO))
                tab(GMA_file, 4); GMA_file.write("%s\n" % "*UVW_U_TILING\t{:f}".format(mapUT))
                tab(GMA_file, 4); GMA_file.write("%s\n" % "*UVW_V_TILING\t{:f}".format(mapVT))
                tab(GMA_file, 4); GMA_file.write("%s\n" % "*UVW_ANGLE\t{:f}".format(mapUVWAngle))
                tab(GMA_file, 4); GMA_file.write("%s\n" % "*UVW_BLUR\t{:f}".format(mapUVWBlur))
                tab(GMA_file, 4); GMA_file.write("%s\n" % "*UVW_BLUR_OFFSET\t{:f}".format(mapUVWBlurOffset))
                tab(GMA_file, 4); GMA_file.write("%s\n" % "*UVW_NOUSE_AMT\t{:f}".format(mapUVWNouseAmt))
                tab(GMA_file, 4); GMA_file.write("%s\n" % "*UVW_NOISE_SIZE\t{:f}".format(mapUVWNoiseSize))
                tab(GMA_file, 4); GMA_file.write("%s\n" % "*UVW_NOISE_LEVEL\t{}".format(mapUVWNoiseLevel))
                tab(GMA_file, 4); GMA_file.write("%s\n" % "*UVW_NOISE_PHASE\t{:f}".format(mapUVWNoisePhase))
                
                if mapBitmapInvert == 1:
                    tab(GMA_file, 4); GMA_file.write("%s\n" % "*BITMAP_INVERT")
                if mapBitmapColorMap == 1:
                    tab(GMA_file, 4); GMA_file.write("%s\n" % "*BITMAP_COLORMAP_ENABLE")

                tab(GMA_file, 4); GMA_file.write("%s\n" % "*BITMAP_FILTER\t{}".format(mapBitmapFilter))
                if isRA1 == 0:
                    tab(GMA_file, 4); GMA_file.write("%s\n" % "*BITMAP_MAP_CHANNEL\t{}".format(mapBitmapChannel))
                tab(GMA_file, 3); GMA_file.write("%s\n" % "}")
        tab(GMA_file, 2); GMA_file.write("%s\n" % "}")

def readObjectNodeTM(GMI_file, GMA_file, preTabNum):
    tab(GMA_file, preTabNum); GMA_file.write("%s\n" % "*NODE_TM")
    tab(GMA_file, preTabNum); GMA_file.write("%s\n" % "{")

    #Fix padding
    while (readNF(GMI_file, 1)[0] == '\x00'):
        print "SKIP"
        GMI_file.read(1)

    object_type, object_version, object_version2 = getObject(GMI_file)
    if object_type == 17 and object_version == 2:
        objName = getString(GMI_file)
        if objName != "":
            tab(GMA_file, preTabNum+1); GMA_file.write("%s\n" % ("*NODE_NAME\t" + objName))
            print "Decompiling \tNODE_TM " + objName
        else:
            tab(GMA_file, preTabNum+1); GMA_file.write("%s\n" % "*NODE_NAME\t(null)");
            print "Decompiling \tNODE_TM"

        #Create and fill the Transformation Matrix
        TM = []
        for x in range(0,4):
            TM.append([])
            for y in range(0,3):
                TM[x].append(getFloat(GMI_file))

        for i in range(0,4):
            tab(GMA_file, preTabNum + 1);
            GMA_file.write("%s\n" % ("*TM_ROW{} {:f}\t{:f}\t{:f}".format(i, TM[i][0], TM[i][1], TM[i][2])))
    
        tab(GMA_file, preTabNum); GMA_file.write("%s\n" % "}")
    return TM

def readObjectList(GMI_file, OBJ_file, MTL_file, GMA_file, isRA1 = 0):
    objCount = getInteger(GMI_file)
    print "Reading {} Object(s)".format(objCount)

    GMA_file.write("%s\n" % "*OBJECT_LIST");
    GMA_file.write("%s\n" % "{");
    GMA_file.write("%s\n" % "*OBJECT_COUNT\t{}".format(objCount))

    v_offset = 1
    vt_offset = 1
    vn_offset = 1
    parent_TM = {}

    for i in range(objCount):

        object_type, object_version, object_version2 = getObject(GMI_file)

        #RA2 Geometry or RA1 Geometry or #RA1 Collision Mesh
        if ((object_type == 2 and object_version == 4) or (object_type == 2 and object_version == 2) or (object_type == 24 and object_version == 2)):
            
            GMA_file.write("%s\n" % "*GEOMOBJECT")
            GMA_file.write("%s\n" % "{")
            objName = getString(GMI_file)
            if objName != "":
                if (object_type == 24 and object_version == 2):
                    objName = "RA1Coll_" + objName
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t{}".format(objName))
                print "Decompiling GEOMOBJECT " + objName
            else:
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t(null)")
                objName = "object"+str(i)
                print "Decompiling GEOMOBJECT..."

            if not (object_type == 24 and object_version == 2):
                if not isRA1:
                    objParent = getString(GMI_file)
                    if objParent != "":
                        tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_PARENT\t{}".format(objParent))

                    objShadeVerts = int(GMI_file.read(1).encode('hex'))
                    tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_SHADEVERTS\t{}".format(objShadeVerts))

            TM = readObjectNodeTM(GMI_file, GMA_file, 1)
            if parent_TM.has_key(objName):
                print 'WARNING - Duplicate object name {}'.format(objName)
            parent_TM[objName] = TM

            if not isRA1 and objParent != "":
                for x in range(0,3):
                    for y in range(0,3):
                        TM[x][y] *= parent_TM[objParent][x][y]
                for x in range(3,4):
                    for y in range(0,3):
                        TM[x][y] += parent_TM[objParent][x][y]

            #readObjGeo
            print "Decompiling \tMESH"
            object_type, object_version, object_version2 = getObject(GMI_file)
            if object_type == 16 and (object_version == 2 or object_version == 4):
            
                meshTimeValue = getInteger(GMI_file)
                meshNumVerts = getInteger(GMI_file)
                meshNumFaces = getInteger(GMI_file)
                meshNumTVerts = getInteger(GMI_file)
                meshNumCVerts = getInteger(GMI_file)
                meshMatRef = getInteger(GMI_file)

                GMA_file.write("%s\n" % "*MESH")
                GMA_file.write("%s\n" % "{")

                tab(GMA_file, 1); GMA_file.write("%s\n" % "*TIMEVALUE\t{}".format(meshTimeValue))
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*MESH_NUMVERTEX\t{}".format(meshNumVerts))
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*MESH_NUMFACES\t{}".format(meshNumFaces))

                tab(GMA_file, 1); GMA_file.write("%s\n" % "*MESH_VERTEX_LIST")
                tab(GMA_file, 1); GMA_file.write("%s\n" % "{")

                vertices = []
                normals = []
                tverts = []
                cverts = []
                faces = []
                cfaces = []

                for i in range(meshNumVerts):
                    x = getFloat(GMI_file)
                    y = getFloat(GMI_file)
                    z = getFloat(GMI_file)
                
                    tx = x * TM[0][0] + y * TM[1][0] + z * TM[2][0]
                    ty = x * TM[0][1] + y * TM[1][1] + z * TM[2][1]
                    tz = x * TM[0][2] + y * TM[1][2] + z * TM[2][2]

                    tx += TM[3][0]
                    ty += TM[3][1]
                    tz += TM[3][2]
                    tab(GMA_file, 2); GMA_file.write("%s\n" % "*MESH_VERTEX\t{}\t{:f}\t{:f}\t{:f}".format(i, x, y, z))
                    vertices.append([tx,ty,tz])

                tab(GMA_file, 1); GMA_file.write("%s\n" % "}")
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*MESH_FACE_LIST")
                tab(GMA_file, 1); GMA_file.write("%s\n" % "{")
            
                for i in range(meshNumFaces):
                    mx = getInteger(GMI_file)
                    my = getInteger(GMI_file)
                    mz = getInteger(GMI_file)
                    mm = getInteger(GMI_file)
                
                    tab(GMA_file, 2); GMA_file.write("%s\n" % "*MESH_FACE\t{:>4}\tA:   {}\tB:   {}\tC:   {}\t*MESH_MTLID {}".format(i, mx, my, mz, mm))

                    mx += v_offset
                    my += v_offset
                    mz += v_offset

                    faces.append([[mx,my,mz,mm],[mx,my,mz],[mx,my,mz]])
                
                tab(GMA_file, 1); GMA_file.write("%s\n" % "}")
            
                if (meshNumTVerts > 0):
                    tab(GMA_file, 1); GMA_file.write("%s\n" % "*MESH_NUMTVERTEX\t{}".format(meshNumTVerts))
                    tab(GMA_file, 1); GMA_file.write("%s\n" % "*MESH_TVERTLIST")
                    tab(GMA_file, 1); GMA_file.write("%s\n" % "{")
                    for i in range(meshNumTVerts):
                        x = getFloat(GMI_file)
                        y = getFloat(GMI_file)
                        z = getFloat(GMI_file)
                        tab(GMA_file, 2); GMA_file.write("%s\n" % "*MESH_TVERT\t{}\t{:f}\t{:f}\t{:f}".format(i, x, y, z))
                        tverts.append([x,y,z])
                    
                    tab(GMA_file, 1); GMA_file.write("%s\n" % "}")
                    tab(GMA_file, 1); GMA_file.write("%s\n" % "*MESH_NUMTVFACES\t{}".format(meshNumFaces))
                    tab(GMA_file, 1); GMA_file.write("%s\n" % "*MESH_TFACELIST")
                    tab(GMA_file, 1); GMA_file.write("%s\n" % "{")

                    for i in range(meshNumFaces):
                        mx = getInteger(GMI_file)
                        my = getInteger(GMI_file)
                        mz = getInteger(GMI_file)
                        tab(GMA_file, 2); GMA_file.write("%s\n" % "*MESH_TFACE\t{}\t{}\t{}\t{}".format(i, mx, my, mz))
                        mx += vt_offset
                        my += vt_offset
                        mz += vt_offset

                        faces[i][1] = [mx,my,mz]
                    
                    tab(GMA_file, 1); GMA_file.write("%s\n" % "}")
                
                if not isRA1:
                    meshHasSecondMaterial = getInteger(GMI_file)
                else:
                    meshHasSecondMaterial = 0

                if (meshHasSecondMaterial):
                    print "WARNING: Second material unsupported"
                    meshHasSecondMaterialAmount = getInteger(GMI_file)
                    for i in range(meshHasSecondMaterialAmount):
                        meshChannelNo = getInteger(GMI_file)
                        tab(GMA_file, 2); GMA_file.write("%s\n" % "*MESH_MAPPINGCHANNEL\t{}".format(meshChannelNo))
                        tab(GMA_file, 2); GMA_file.write("%s\n" % "{")
                    
                        meshNumSTVerts = getInteger(GMI_file)
                        print meshNumSTVerts
                        print getInteger(GMI_file)
                        meshNumSTFaces = getInteger(GMI_file)
                        print meshNumSTFaces
                        print getInteger(GMI_file)
                        print getInteger(GMI_file)
                        print getInteger(GMI_file)
                        print getInteger(GMI_file)

                        tab(GMA_file, 3); GMA_file.write("%s\n" % "*MESH_NUMTVERTEX\t{}".format(meshNumSTVerts))
                        tab(GMA_file, 3); GMA_file.write("%s\n" % "*MESH_TVERTLIST")
                        tab(GMA_file, 3); GMA_file.write("%s\n" % "{")
                        for i in range(meshNumSTVerts):
                            x = getFloat(GMI_file)
                            y = getFloat(GMI_file)
                            z = getFloat(GMI_file)
                            tab(GMA_file, 4); GMA_file.write("%s\n" % "*MESH_TVERT\t{}\t{:f}\t{:f}\t{:f}".format(i, x, y, z))
                        tab(GMA_file, 3); GMA_file.write("%s\n" % "}")

                        tab(GMA_file, 3); GMA_file.write("%s\n" % "*MESH_NUMTVFACES\t{}".format(meshNumSTFaces))
                        tab(GMA_file, 3); GMA_file.write("%s\n" % "*MESH_TFACELIST")
                        tab(GMA_file, 3); GMA_file.write("%s\n" % "{")
                        
                        for i in range(meshNumFaces):
                            mx = getInteger(GMI_file)
                            my = getInteger(GMI_file)
                            mz = getInteger(GMI_file)
                            tab(GMA_file, 4); GMA_file.write("%s\n" % "*MESH_TFACE\t\t{}\t\t{}\t\t{}\t{}".format(i, mx, my, mz))
                        tab(GMA_file, 3); GMA_file.write("%s\n" % "}")

                        tab(GMA_file, 2); GMA_file.write("%s\n" % "}")

            
                if (meshNumCVerts > 0):
                    print "WARNING: CVerts unsupported"
                    tab(GMA_file, 2); GMA_file.write("%s\n" % "*MESH_NUMCVERTEX\t{}".format(meshNumCVerts))
                    tab(GMA_file, 2); GMA_file.write("%s\n" % "*MESH_CVERTLIST")
                    tab(GMA_file, 2); GMA_file.write("%s\n" % "{")

                    for i in range(meshNumCVerts):
                        x = getFloat(GMI_file)
                        y = getFloat(GMI_file)
                        z = getFloat(GMI_file)
                        tab(GMA_file, 3); GMA_file.write("%s\n" % "*MESH_VERTCOL\t{}\t{:f}\t{:f}\t{:f}".format(i, x, y, z))

                    tab(GMA_file, 2); GMA_file.write("%s\n" % "}")
                    tab(GMA_file, 2); GMA_file.write("%s\n" % "*MESH_NUMCVFACES\t{}".format(meshNumFaces))
                    tab(GMA_file, 2); GMA_file.write("%s\n" % "*MESH_CFACELIST")
                    tab(GMA_file, 2); GMA_file.write("%s\n" % "{")

                    for i in range(meshNumFaces):
                        mx = getInteger(GMI_file)
                        my = getInteger(GMI_file)
                        mz = getInteger(GMI_file)
                        tab(GMA_file, 3); GMA_file.write("%s\n" % "*MESH_CFACE\t{}\t{}\t{}\t{}".format(i, mx, my, mz))
                    tab(GMA_file, 2); GMA_file.write("%s\n" % "}")
            
                if (meshNumFaces > 0):
                    tab(GMA_file, 1); GMA_file.write("%s\n" % "*MESH_NORMALS")
                    tab(GMA_file, 1); GMA_file.write("%s\n" % "{")
                    for i in range(meshNumFaces):
                        x = getFloat(GMI_file)
                        y = getFloat(GMI_file)
                        z = getFloat(GMI_file)
                    
                        tx = x * TM[0][0] + y * TM[1][0] + z * TM[2][0]
                        ty = x * TM[0][1] + y * TM[1][1] + z * TM[2][1]
                        tz = x * TM[0][2] + y * TM[1][2] + z * TM[2][2]
                    
                        tab(GMA_file, 2); GMA_file.write("%s\n" % "*MESH_FACENORMAL\t{}\t{:f}\t{:f}\t{:f}".format(i, x, y, z))
                        for j in range(3):
                            f = faces[i][2][j] - v_offset
                            x = getFloat(GMI_file)
                            y = getFloat(GMI_file)
                            z = getFloat(GMI_file)

                            tx = x * TM[0][0] + y * TM[1][0] + z * TM[2][0]
                            ty = x * TM[0][1] + y * TM[1][1] + z * TM[2][1]
                            tz = x * TM[0][2] + y * TM[1][2] + z * TM[2][2]
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*MESH_VERTEXNORMAL\t{}\t{:f}\t{:f}\t{:f}".format(f, x, y, z))
                            normals.append([tx,ty,tz])
                            faces[i][2][j] = (i*3)+j + vn_offset
                    tab(GMA_file, 1); GMA_file.write("%s\n" % "}")
                if not isRA1:
                    meshBackFaceCull = getInteger(GMI_file)
                    tab(GMA_file, 1); GMA_file.write("%s\n" % "*BACKFACE_CULL\t{}".format(meshBackFaceCull))
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*MATERIAL_REF\t{}".format(meshMatRef))

                for i in range(meshNumVerts):
                    OBJ_file.write("%s\n" % "v {} {} {}".format(vertices[i][0], vertices[i][1], vertices[i][2]))
                for i in range(meshNumTVerts):
                    OBJ_file.write("%s\n" % "vt {} {} {}".format(tverts[i][0], tverts[i][1], tverts[i][2]))
                for i in range(meshNumFaces * 3):
                    OBJ_file.write("%s\n" % "vn {} {} {}".format(normals[i][0], normals[i][1], normals[i][2]))
                OBJ_file.write("%s\n" % "\no {0}\ng {0}".format(objName))
                if (meshNumTVerts > 0):
                    for i in range(meshNumFaces):
                        OBJ_file.write("%s\n" % "f {}/{}/{} {}/{}/{} {}/{}/{}".format(faces[i][0][2], faces[i][1][2], faces[i][2][2], faces[i][0][1], faces[i][1][1], faces[i][2][1],faces[i][0][0], faces[i][1][0], faces[i][2][0]))
                else:
                    for i in range(meshNumFaces):
                        OBJ_file.write("%s\n" % "f {}//{} {}//{} {}//{}".format(faces[i][0][2], faces[i][2][2], faces[i][0][1], faces[i][2][1], faces[i][0][0], faces[i][2][0]))

                v_offset += meshNumVerts
                vt_offset += meshNumTVerts
                vn_offset += meshNumFaces * 3
                GMA_file.write("%s\n" % "}")
                GMA_file.write("%s\n" % "}")
        #RA2 Light or RA1 Light
        elif ((object_type == 5 and object_version == 3) or (object_type == 5 and object_version == 2)):

            GMA_file.write("%s\n" % "*LIGHT")
            GMA_file.write("%s\n" % "{");
            
            objName = getString(GMI_file)
            if objName != "":
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t{}".format(objName))
                print "Decompiling LIGHT " + objName
            else:
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t(null)");
                print "Decompiling LIGHT"

            readObjectNodeTM(GMI_file, GMA_file, 1)

            hasSecondTM = getInteger(GMI_file)

            if (hasSecondTM):
                readObjectNodeTM(GMI_file, GMA_file, 1)

            lightType = getInteger(GMI_file)

            if (lightType == 0):
                lightType = "Omni"
            elif (lightType == 1):
                lightType = "Target"
            elif (lightType == 2):
                lightType = "Directional"
            elif (lightType == 4):
                lightType = "Free"
            else:
                lightType = ""
                print "UNKNOWN Light Type {}".format(lightType)

            if not lightType == "":
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*LIGHT_TYPE\t{}".format(lightType))

            shadowType = getInteger(GMI_file)

            if (shadowType == 2):
                shadowType = "Raytraced"
            elif (shadowType == 1):
                shadowType = "Mapped"
            else:
                shadowType = "Off"

            tab(GMA_file, 1); GMA_file.write("%s\n" % "*LIGHT_SHADOWS\t{}".format(shadowType))

            useLight = getInteger(GMI_file)

            tab(GMA_file, 1); GMA_file.write("%s\n" % "*LIGHT_USELIGHT\t{}".format(useLight))

            lightSpotShape = 1 #getInteger(GMI_file)
            if lightSpotShape == 1:
                lightSpotShape = "Circle"
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*LIGHT_SPOTSHAPE\t{}".format(lightSpotShape))

            elif lightSpotShape == 0:
                lightSpotShape = "Rect"
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*LIGHT_SPOTSHAPE\t{}".format(lightSpotShape))

            lightColor = getRGB(GMI_file, isRA1)
            lightIntensity = getFloat(GMI_file)
            lightAspect = getFloat(GMI_file)

            if not isRA1:
                lightHotspot = getFloat(GMI_file)
                lightFalloff = getFloat(GMI_file)
                lightAttnStart = getFloat(GMI_file)
                lightAttnEnd = getFloat(GMI_file)
            else:
                lightAttnStart = getFloat(GMI_file)
                lightAttnEnd = getFloat(GMI_file)
                GMI_file.read(8)

            lightTDist = getFloat(GMI_file)

            if not isRA1:
                lightUseFarAttn = getInteger(GMI_file)

            tab(GMA_file, 1); GMA_file.write("%s\n" % "*LIGHT_COLOR\t{}".format(lightColor))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*LIGHT_INTENS\t{:f}".format(lightIntensity))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*LIGHT_ASPECT\t{:f}".format(lightAspect))
            if lightType != "Omni":
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*LIGHT_HOTSPOT\t{:f}".format(lightHotspot))
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*LIGHT_FALLOFF\t{:f}".format(lightFalloff))
            if lightType != "Directional":
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*LIGHT_ATTNSTART\t{:f}".format(lightAttnStart))
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*LIGHT_ATTNEND\t{:f}".format(lightAttnEnd))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*LIGHT_TDIST\t{:f}".format(lightTDist))
            if not isRA1:
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*USE FAR ATTENUATION =\t{}".format(lightUseFarAttn))

            GMA_file.write("%s\n" % "}")
            
        #Attachement
        elif object_type == 21 and object_version == 2:

            GMA_file.write("%s\n" % "*GMID_ATTACHMENTPT")
            GMA_file.write("%s\n" % "{")

            objName = getString(GMI_file)
            if objName != "":
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t{}".format(objName))
                print "Decompiling GMID_ATTACHMENTPT " + objName 
            else:
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t(null)")
                print "Decompiling GMID_ATTACHMENTPT..."

            TM = readObjectNodeTM(GMI_file, GMA_file, 1)

            attData = getString(GMI_file)
            tab(GMA_file, 1); GMA_file.write("%s\n" % "USER DATA\t{}".format(attData))

            GMA_file.write("%s\n" % "}")


        #SimObject
        elif object_type == 30 and object_version == 2:
            
            GMA_file.write("%s\n" % "*GMID_HAVOK_SIMOBJECT")
            GMA_file.write("%s\n" % "{")

            objName = getString(GMI_file)
            if objName != "":
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t{}".format(objName))
                print "Decompiling GMID_HAVOK_SIMOBJECT " + objName
            else:
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t(null)")
                print "Decompiling GMID_HAVOK_SIMOBJECT"

            simGX = getFloat(GMI_file)
            simGY = getFloat(GMI_file)
            simGZ = getFloat(GMI_file)

            simWorldScale = getFloat(GMI_file)
            simTolerance = getFloat(GMI_file)
            simResolver = getInteger(GMI_file)
            simIncludeDrag = int(GMI_file.read(1).encode("hex"))
            simLinearDrag = getFloat(GMI_file)
            simAngularDrag = getFloat(GMI_file)
            simIncludeDeactivator = int(GMI_file.read(1).encode("hex"))
            simShortFreq = getFloat(GMI_file)
            simLongFreq = getFloat(GMI_file)
            simUseFastSubspace = int(GMI_file.read(1).encode("hex"))
            simUpdatesPertimeStep = getFloat(GMI_file)
            simCollisionPairs = getInteger(GMI_file)

            tab(GMA_file, 1); GMA_file.write("%s\n" % "*GRAVITY\t{:f} {:f} {:f}".format(simGX, simGY, simGZ))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*WORLDSCALE\t{:f}".format(simWorldScale))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*SIMTOLERANCE\t{:f}".format(simTolerance))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*RESOLVER\t{}".format(simResolver))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*INCLUDE_DRAG\t{}".format(simIncludeDrag))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*LINEAR_DRAG\t{:f}".format(simLinearDrag))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*ANGULAR_DRAG\t{:f}".format(simAngularDrag))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*INCLUDE_DEACTIVATOR\t{}".format(simIncludeDeactivator))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*SHORTFREQ\t{:f}".format(simShortFreq))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*LONGFREQ\t{:f}".format(simLongFreq))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*USE_FAST_SUBSPACE\t{}".format(simUseFastSubspace))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*UPDATES_PER_TIMESTEP\t{:f}".format(simUpdatesPertimeStep))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*NUM_COLLISION_PAIRS\t{}".format(simCollisionPairs))

            GMA_file.write("%s\n" % "}")
            
        #RBCollection
        elif object_type == 31 and object_version == 4:
            
            GMA_file.write("%s\n" % "*GMID_HAVOK_RBCOLLECTION")
            GMA_file.write("%s\n" % "{")

            objName = getString(GMI_file)
            if objName != "":
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t{}".format(objName))
                print "Decompiling GMID_HAVOK_RBCOLLECTION " + objName
            else:
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t(null)")
                print "Decompiling GMID_HAVOK_RBCOLLECTION"

            rbDisabledPairs = getInteger(GMI_file)
            rbSolverType = getInteger(GMI_file)
            
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*NUM_DISABLED_PAIRS\t{}".format(rbDisabledPairs))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*SOLVER_TYPE\t{}".format(rbSolverType))
            object_type, object_version, object_version2 = getObject(GMI_file)

            if object_type == 33 and object_version == 2:
                rbCount = getInteger(GMI_file)
                print "Decompiling \tGMID_HAVOK_RIGIDBODY_LIST {}".format(rbCount)

                tab(GMA_file, 1); GMA_file.write("%s\n" % "*COUNT\t{}".format(rbCount))
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*GMID_HAVOK_RIGIDBODY_LIST")
                tab(GMA_file, 1); GMA_file.write("%s\n" % "{")
                tab(GMA_file, 2); GMA_file.write("%s\n" % "*COUNT\t{}".format(rbCount)) #Weird

                for i in range(rbCount):
                    object_type, object_version, object_version2 = getObject(GMI_file)

                    if object_type == 32 and object_version == 4:
                        tab(GMA_file, 2); GMA_file.write("%s\n" % "*GMID_HAVOK_RIGIDBODY")
                        tab(GMA_file, 2); GMA_file.write("%s\n" % "{")

                        objName = getString(GMI_file)
                        if objName != "":
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*NODE_NAME\t{}".format(objName))
                            print "Decompiling \t\tGMID_HAVOK_RIGIDBODY " + objName
                        else:
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*NODE_NAME\t(null)")
                            print "Decompiling \t\tGMID_HAVOK_RIGIDBODY..."

                        rbMass = getFloat(GMI_file)
                        rbElast = getFloat(GMI_file)
                        rbFriction = getFloat(GMI_file)
                        rbOptimisation = getFloat(GMI_file)
                        rbUnyielding = getInteger(GMI_file)
                        rbSimulationGeo = getInteger(GMI_file)

                        tab(GMA_file, 3); GMA_file.write("%s\n" % "*MASS\t{:f}".format(rbMass))
                        tab(GMA_file, 3); GMA_file.write("%s\n" % "*ELASTICITY\t{:f}".format(rbElast))
                        tab(GMA_file, 3); GMA_file.write("%s\n" % "*FRICTION\t{:f}".format(rbFriction))
                        tab(GMA_file, 3); GMA_file.write("%s\n" % "*OPTIMIZATION_LEVEL\t{:f}".format(rbOptimisation))
                        tab(GMA_file, 3); GMA_file.write("%s\n" % "*UNYIELDING\t{}".format(rbUnyielding))
                        tab(GMA_file, 3); GMA_file.write("%s\n" % "*SIMULATION_GEOMETRY\t{}".format(rbSimulationGeo))

                        geometryProxyName = getString(GMI_file)
                        if geometryProxyName != "":
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*GEOMETRY_PROXY_NAME\t{}".format(geometryProxyName))
                        else:
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*GEOMETRY_PROXY_NAME\t(null)")

                        rbUseDisplayProxy = int(GMI_file.read(1).encode("hex"))
                        rbDisableCollisions = int(GMI_file.read(1).encode("hex"))
                        rbInactive = int(GMI_file.read(1).encode("hex"))

                        tab(GMA_file, 3); GMA_file.write("%s\n" % "*USE_DISPLAY_PROXY\t{}".format(rbUseDisplayProxy))
                        tab(GMA_file, 3); GMA_file.write("%s\n" % "*DISABLE_COLLISIONS\t{}".format(rbDisableCollisions))
                        tab(GMA_file, 3); GMA_file.write("%s\n" % "*INACTIVE\t{}".format(rbInactive))
                        
                        displayProxyName = getString(GMI_file)
                        if displayProxyName != "":
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*DISPLAY_PROXY_NAME\t{}".format(displayProxyName))
                        else:
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*DISPLAY_PROXY_NAME\t(null)")

                        readObjectNodeTM(GMI_file, GMA_file, 3)

                        rbGeoTypeInt = getInteger(GMI_file)
                        if (rbGeoTypeInt == 1):
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*HAVOK_GEO_TYPE\tPlane")
                        else:
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*HAVOK_GEO_TYPE\tStandard")

                        rbChildrenNumber = getInteger(GMI_file)
                        tab(GMA_file, 3); GMA_file.write("%s\n" % "*NUMBER_OF_CHILDREN\t{}".format(rbChildrenNumber))

                        tab(GMA_file, 2); GMA_file.write("%s\n" % "}")
                        
                tab(GMA_file, 1); GMA_file.write("%s\n" % "}")
                        
            if rbDisabledPairs > 0:
                object_type, object_version, object_version2 = getObject(GMI_file)
                if object_type == 51 and object_version == 2:
                    rbCount = getInteger(GMI_file)
                    print "Decompiling GMID_HAVOK_DIS_COLLISION_PAIRS {}".format(rbCount)

                    tab(GMA_file, 1); GMA_file.write("%s\n" % "*GMID_HAVOK_DIS_COLLISION_PAIRS")
                    tab(GMA_file, 1); GMA_file.write("%s\n" % "{")
                    tab(GMA_file, 2); GMA_file.write("%s\n" % "*COUNT\t{}".format(rbCount))

                    for i in range(rbCount):
                        rbLeft = getString(GMI_file)
                        rbRight = getString(GMI_file)

                        tab(GMA_file, 2); GMA_file.write("%s\n" % "{{ {}\t{} }}".format(rbLeft, rbRight))

                    tab(GMA_file, 1); GMA_file.write("%s\n" % "}")

            GMA_file.write("%s\n" % "}")

        #Constraint Solver
        elif object_type == 42 and object_version == 3:
            GMA_file.write("%s\n" % "*GMID_HAVOK_CONSTRAINTSOLVER\n{")

            objName = getString(GMI_file)
            if objName != "":
                tab(GMA_file, 1); GMA_file.write("%s\n" % ("*NODE_NAME\t" + objName))
                print "Decompiling GMID_HAVOK_CONSTRAINTSOLVER " + objName
            else:
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t(null)")
                print "Decompiling GMID_HAVOK_CONSTRAINTSOLVER"

            cnTreshold = getFloat(GMI_file)
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*THRESHOLD\t{:f}".format(cnTreshold))

            cnRBName = getString(GMI_file)
            if cnRBName != "":
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*RB_COLLECTION_NAME\t{}".format(cnRBName))
            else:
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*RB_COLLECTION_NAME\t(null)\n")

            cnCount = getInteger(GMI_file)

            if cnCount > 0:
                object_type, object_version, object_version2 = getObject(GMI_file)

                if object_type == 44 and object_version == 2:
                    cnlCount = getInteger(GMI_file)
                    tab(GMA_file, 1); GMA_file.write("%s\n" % "*GMID_HAVOK_CONSTRAINT_LIST")
                    tab(GMA_file, 1); GMA_file.write("%s\n" % "{")
                    tab(GMA_file, 2); GMA_file.write("%s\n" % ("*COUNT\t{}".format(cnlCount)))
                    #print "Decompiling %i constraints...\n", cnlCount);

                    for i in range(cnlCount):
                        object_type, object_version, object_version2 = getObject(GMI_file)

                        if object_type == 47 and object_version == 2:
                            #Hinge
                            tab(GMA_file, 2); GMA_file.write("%s\n" % "*GMID_HAVOK_HINGE_CONSTRAINT")
                            tab(GMA_file, 2); GMA_file.write("%s\n" % "{")
                            cnlName = getString(GMI_file)
                            if cnlName != "":
                                tab(GMA_file, 3); GMA_file.write("%s\n" % ("*NODE_NAME\t"+ cnlName))
                                print "Decompiling \tGMID_HAVOK_HINGE_CONSTRAINT "+ cnlName
                            else:
                                tab(GMA_file, 3); GMA_file.write("%s\n" % "*NODE_NAME\t(null)\n")
                                print "Decompiling \tGMID_HAVOK_HINGE_CONSTRAINT..."

                            readObjectNodeTM(GMI_file, GMA_file, 3)

                            cnlBody1 = getString(GMI_file)
                            cnlBody2 = getString(GMI_file)
                            px = getFloat(GMI_file)
                            py = getFloat(GMI_file)
                            pz = getFloat(GMI_file)
                            ax = getFloat(GMI_file)
                            ay = getFloat(GMI_file)
                            az = getFloat(GMI_file)
                            cnlIsLimited = int(GMI_file.read(1).encode("hex"))
                            cnlFriction = getFloat(GMI_file)
                            cnlAngleLimitA = getFloat(GMI_file)
                            cnlAngleLimitB = getFloat(GMI_file)

                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*BODY1\t{}".format(cnlBody1))
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*BODY2\t{}".format(cnlBody2))
                            tab(GMA_file, 3); GMA_file.write("%s\n" %  "*POINT {:f}\t{:f}\t{:f}".format(px, py, pz))
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*SPIN_AXIS {}\t{}\t{}".format(ax, ay, az))
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*IS_LIMITED {}".format(cnlIsLimited))
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*FRICTION {:f}".format(cnlFriction))
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*ANGLE_LIMITS {:f}\t{:f}".format(cnlAngleLimitA, cnlAngleLimitB))
                            
                            #Padding issues when dealing with CSolvers > 1;
                            while (readNF(GMI_file, 1)[0] == '\x00'):
                                print "SKIP"
                                GMI_file.read(1)

                            tab(GMA_file, 2); GMA_file.write("%s\n" % "}");
                        elif object_type == 46 and object_version == 2:
                            #Wheel
                            tab(GMA_file, 2); GMA_file.write("%s\n" % "*GMID_HAVOK_WHEEL_CONSTRAINT")
                            tab(GMA_file, 2); GMA_file.write("%s\n" % "{")

                            cnlName = getString(GMI_file)
                            if cnlName != "":
                                tab(GMA_file, 3); GMA_file.write("%s\n" % "*NODE_NAME\t{}".format(cnlName))
                                print "Decompiling \tGMID_HAVOK_WHEEL_CONSTRAINT %s...\n", cnlName
                            else:
                                tab(GMA_file, 3); GMA_file.write("%s\n" % "*NODE_NAME\t(null)")
                                print "Decompiling \tGMID_HAVOK_WHEEL_CONSTRAINT..."

                            readObjectNodeTM(GMI_file, GMA_file, 3)

                            cnlBody1 = getString(GMI_file)
                            cnlBody2 = getString(GMI_file)
                            px = getFloat(GMI_file)
                            py = getFloat(GMI_file)
                            pz = getFloat(GMI_file)
                            ax = getFloat(GMI_file)
                            ay = getFloat(GMI_file)
                            az = getFloat(GMI_file)
                            
                            unkn = [None] *8
                            for x in range(8):
                                unkn[x] = getFloat(GMI_file)

                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*BODY1\t{}".format(cnlBody1))
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*BODY2\t{}".format(cnlBody2))
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*POINT {:f}\t{:f}\t{:f}".format(px, py, pz))
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*SPIN_AXIS {:f}\t{:f}\t{:f}".format(ax, ay, az))
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*SUSPENSION_AXIS {:f}\t{:f}\t{:f}".format(unkn[0], unkn[1], unkn[2]))
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*SUSPENSION_LIMITS {:f}\t{:f}".format(unkn[3], unkn[4]))
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*SUSPENSION_FRICTION {:f}".format(unkn[5]))
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*ANGULAR_SPEED {:f}".format(unkn[6]))
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*GAIN {:f}".format(unkn[7]))
                            
                            #Padding issues when dealing with CSolvers > 1;
                            while (readNF(GMI_file, 1)[0] == '\x00'):
                                print "SKIP"
                                GMI_file.read(1)

                            tab(GMA_file, 2); GMA_file.write("%s\n" % "}")
                        elif object_type == 53 and object_version == 2:
                            #PointToPoint
                            
                            tab(GMA_file, 2); GMA_file.write("%s\n" % "*GMID_HAVOK_POINTTOPOINT")
                            tab(GMA_file, 2); GMA_file.write("%s\n" % "{")

                            ptpName = getString(GMI_file)
                            if ptpName != "":
                                tab(GMA_file, 3); GMA_file.write("%s\n" % "*NODE_NAME\t{}".format(ptpName))
                                print "Decompiling \tGMID_HAVOK_POINTTOPOINT " + ptpName
                            else:
                                tab(GMA_file, 3); GMA_file.write("%s\n" % "*NODE_NAME\t(null)")
                                print "Decompiling \tGMID_HAVOK_POINTTOPOINT..."

                            readObjectNodeTM(GMI_file, GMA_file, 3)

                            ptpBody1 = getString(GMI_file)
                            ptpBody2 = getString(GMI_file)

                            ptp1 = getFloat(GMI_file)
                            ptp2 = getFloat(GMI_file)
                            ptp3 = getFloat(GMI_file)
                            ptp4 = getFloat(GMI_file)
                            ptp5 = getFloat(GMI_file)
                            ptp6 = getFloat(GMI_file)

                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*BODY1\t{}".format(ptpBody1))
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*BODY2\t{}".format(ptpBody2))

                            tab(GMA_file, 3); GMA_file.write("%s\n" % "*POINT 1")
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "( {:f}\t{:f}\t{:f} )".format(ptp1, ptp2, ptp3))
                            tab(GMA_file, 3); GMA_file.write("%s\n" % "( {:f}\t{:f}\t{:f} )".format(ptp4, ptp5, ptp6))

                            tab(GMA_file, 2); GMA_file.write("%s\n" % "}")

                    tab(GMA_file, 1); GMA_file.write("%s\n" % "}")
            GMA_file.write("%s\n" % "}")

        #Linear Dashpot
        elif object_type == 48 and object_version == 2:
            
            GMA_file.write("%s\n" % "*GMID_HAVOK_LINEAR_DASHPOT")
            GMA_file.write("%s\n" % "{")

            objName = getString(GMI_file)
            if objName != "":
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t{}".format(objName))
                print "Decompiling GMID_HAVOK_LINEAR_DASHPOT " + objName
            else:
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t(null)")
                print "Decompiling GMID_HAVOK_LINEAR_DASHPOT..."

            readObjectNodeTM(GMI_file, GMA_file, 1)

            adBody1 = getString(GMI_file)
            adBody2 = getString(GMI_file)

            adStrength = getFloat(GMI_file)
            adDamping = getFloat(GMI_file)

            adAllowInterpenetrations = int(GMI_file.read(1).encode("hex"))

            point1Quat1 = getFloat(GMI_file)
            point1Quat2 = getFloat(GMI_file)
            point1Quat3 = getFloat(GMI_file)
            point1Quat4 = getFloat(GMI_file)

            point2Quat1 = getFloat(GMI_file)
            point2Quat2 = getFloat(GMI_file)
            point2Quat3 = getFloat(GMI_file)
            point2Quat4 = getFloat(GMI_file)

            tab(GMA_file, 1); GMA_file.write("%s\n" % "*BODY1\t{}".format(adBody1))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*BODY2\t{}".format(adBody2))

            tab(GMA_file, 1); GMA_file.write("%s\n" % "*STRENGTH\t{:f}".format(adStrength))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*DAMPING\t{:f}".format(adDamping))

            tab(GMA_file, 1); GMA_file.write("%s\n" % "*ALLOW_INTERPENETRATIONS\t{}".format(adAllowInterpenetrations))

            tab(GMA_file, 1); GMA_file.write("%s\n" % "*POINT 1")
            tab(GMA_file, 1); GMA_file.write("%s\n" % "( {:f}\t{:f}\t{:f}\t{:f} )".format(point1Quat1, point1Quat2, point1Quat3, point1Quat4))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*POINT 2")
            tab(GMA_file, 1); GMA_file.write("%s\n" % "( {:f}\t{:f}\t{:f}\t{:f} )".format(point2Quat1, point2Quat2, point2Quat3, point2Quat4))

            GMA_file.write("%s\n" % "}")

        #Angular Dashpot
        elif object_type == 49 and object_version == 2:
            
            GMA_file.write("%s\n" % "*GMID_HAVOK_ANGULAR_DASHPOT")
            GMA_file.write("%s\n" % "{")

            objName = getString(GMI_file)
            if objName != "":
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t{}".format(objName))
                print "Decompiling GMID_HAVOK_ANGULAR_DASHPOT " + objName
            else:
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t(null)")
                print "Decompiling GMID_HAVOK_ANGULAR_DASHPOT..."

            readObjectNodeTM(GMI_file, GMA_file, 1)

            adBody1 = getString(GMI_file)
            adBody2 = getString(GMI_file)

            adStrength = getFloat(GMI_file)
            adDamping = getFloat(GMI_file)

            adAllowInterpenetrations = int(GMI_file.read(1).encode("hex"))

            adQuat1 = getFloat(GMI_file)
            adQuat2 = getFloat(GMI_file)
            adQuat3 = getFloat(GMI_file)
            adQuat4 = getFloat(GMI_file)

            tab(GMA_file, 1); GMA_file.write("%s\n" % "*BODY1\t{}".format(adBody1))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*BODY2\t{}".format(adBody2))

            tab(GMA_file, 1); GMA_file.write("%s\n" % "*STRENGTH\t{:f}".format(adStrength))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*DAMPING\t{:f}".format(adDamping))

            tab(GMA_file, 1); GMA_file.write("%s\n" % "*ALLOW_INTERPENETRATIONS\t{}".format(adAllowInterpenetrations))

            tab(GMA_file, 1); GMA_file.write("%s\n" % "*QUATERNION")
            tab(GMA_file, 1); GMA_file.write("%s\n" % "( {:f}\t{:f}\t{:f}\t{:f} )".format(adQuat1, adQuat2, adQuat3, adQuat4))

            GMA_file.write("%s\n" % "}")

        #Camera
        elif object_type == 4 and object_version == 2:

            GMA_file.write("%s\n" % "*CAMERA")
            GMA_file.write("%s\n" % "{")

            objName = getString(GMI_file)
            if objName != "":
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t{}".format(objName))
                print "Decompiling CAMERA " + objName
            else:
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t(null)")
                print "Decompiling CAMERA"

            readObjectNodeTM(GMI_file, GMA_file, 1)

            hasSecondTM = getInteger(GMI_file)

            if (hasSecondTM):
                readObjectNodeTM(GMI_file, GMA_file, 1)

            Type = getInteger(GMI_file)
            Hither = getFloat(GMI_file)
            Yon = getFloat(GMI_file)
            Near = getFloat(GMI_file)
            Far = getFloat(GMI_file)
            FOV = getFloat(GMI_file)
            TDist = getFloat(GMI_file)

            if (Type == 0):
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*CAMERA_TYPE\tTarget")
            else:
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*CAMERA_TYPE\tFree")

            tab(GMA_file, 1); GMA_file.write("%s\n" % "*CAMERA_HITHER\t{:f}".format(Hither))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*CAMERA_YON\t{:f}".format(Yon))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*CAMERA_NEAR\t{:f}".format(Near))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*CAMERA_FAR\t{:f}".format(Far))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*CAMERA_FOV\t{:f}".format(FOV))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*CAMERA_TDIST\t{:f}".format(TDist))

            GMA_file.write("%s\n" % "}")

        #RA1 Collision Box
        elif object_type == 25 and object_version == 2:
            # readCollisionBox(preTabNum+1)

            GMA_file.write("%s\n" % "*GMID_COLLISION_BOX")
            GMA_file.write("%s\n" % "{")

            objName = getString(GMI_file)
            if objName != "":
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t{}".format(objName))
                print "Decompiling GMID_COLLISION_BOX " + objName
            else:
                tab(GMA_file, 1); GMA_file.write("%s\n" % "*NODE_NAME\t(null)")
                print "Decompiling GMID_COLLISION_BOX..."

            readObjectNodeTM(GMI_file, GMA_file, 1)

            L = getFloat(GMI_file)
            W = getFloat(GMI_file)
            H = getFloat(GMI_file)

            tab(GMA_file, 1); GMA_file.write("%s\n" % "*LENGTH\t{:f}".format(L))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*WIDTH\t{:f}".format(W))
            tab(GMA_file, 1); GMA_file.write("%s\n" % "*HEIGHT\t{:f}".format(H))

            GMA_file.write("%s\n" % "}")

        else:
            file_pos = GMI_file.tell()
            print "Unknown object at {}".format(file_pos)

    GMA_file.write("%s\n" % "}")
    GMI_file.seek(8, 1)

def main(argv):
    isRA1 = 0
    if len(argv) > 1:
        filename = argv[1]

    else:
        from Tkinter import Tk
        from tkFileDialog import askopenfilename
        
        Tk().withdraw()
        filename = askopenfilename(filetypes=[('Binary GMF', '*.gmf'), ('All files', '*.*')])
        if filename =='':
            sys.exit(0)

    GMI_file = open(filename, 'rb')

    if GMI_file.read(3) != "GMI": 
        print "Invalid GMF file!\n"
        sys.exit(1)

    OBJ_file = open(os.path.splitext(filename)[0] + ".obj", "wb")
    MTL_file = open(os.path.splitext(filename)[0] + ".mtl", "wb")
    GMA_file = open(os.path.splitext(filename)[0] + ".gma", "wb")

    gmf_version = getInteger(GMI_file)
    #.decode("hex")
    OBJ_file.write("%s\n" % "#Converted by GMI2OBJ")
    OBJ_file.write(OBJ_boilerplate.decode('hex'))

    GMA_file.write("%s\n" % "GMA")
    GMA_file.write("%s\n" % "*GABRIEL_ASCIIEXPORT\t{}".format(gmf_version))

    for object_type in iter(lambda: GMI_file.read(4), ""):
        object_type = int(struct.unpack("<i", object_type)[0])
        object_version = getInteger(GMI_file)
        object_version2 = getInteger(GMI_file)
        print object_type, object_version, object_version2

        if ((object_type == 1 or object_type == 3 or object_type == 2) and object_version == 0):
            if (object_type == 3 or object_type == 2):
                isRA1 = 1
            else:
                isRA1 = 0
            if object_version2 == 15:
                print "Model Valid"
                GMA_file.write("%s\n" % "*MODEL_TYPE\tBasic Model")
            else:
                print "Unknown Model Type: " + str(type)
                sys.exit(1)

        elif object_type == 1 and object_version == 2:
            #readSceneInfo
            sceneName = getString(GMI_file)
            print "Decompiling SCENE " + sceneName
            OBJ_file.write("%s\n" % ("#" + sceneName))
            sceneFirstFrame = getInteger(GMI_file)
            sceneLastFrame = getInteger(GMI_file)
            sceneFrameSpeed = getInteger(GMI_file)
            sceneTicksPerFrame = getInteger(GMI_file)
            sceneBackgroundStatic = getRGB(GMI_file, isRA1)
            sceneAmbientStatic = getRGB(GMI_file, isRA1)
            GMA_file.write("%s\n" % "*SCENE")
            GMA_file.write("%s\n" % "{");
            GMA_file.write("%s\n" % "\t*SCENE_FILENAME\t{}".format(sceneName))
            GMA_file.write("%s\n" % "\t*SCENE_FIRSTFRAME\t{}".format(sceneFirstFrame))
            GMA_file.write("%s\n" % "\t*SCENE_LASTFRAME\t{}".format(sceneLastFrame))
            GMA_file.write("%s\n" % "\t*SCENE_FRAMESPEED\t{}".format(sceneFrameSpeed))
            GMA_file.write("%s\n" % "\t*SCENE_TICKSPERFRAME\t{}".format(sceneTicksPerFrame))
            GMA_file.write("%s\n" % "\t*SCENE_BACKGROUND_STATIC\t{}".format(sceneBackgroundStatic))
            GMA_file.write("%s\n" % "\t*SCENE_AMBIENT_STATIC\t{}".format(sceneAmbientStatic))
            GMA_file.write("%s\n" % "}")

        elif object_type == 7 and object_version == 2:
            readMaterialList(GMI_file, MTL_file, GMA_file, isRA1)
            
        elif object_type == 18 and object_version == 2:
            readObjectList(GMI_file, OBJ_file, MTL_file, GMA_file, isRA1)

        else:
            file_pos = GMI_file.tell()
            print "Error at {}".format(file_pos)
            sys.exit(1)

    GMI_file.close
    MTL_file.close
    GMA_file.close

    print "Conversion complete"
    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)