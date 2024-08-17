import numpy as np

header = '('
# column_list = ["osmid", "continent", "name", "aerialway", "aeroway", "amenity", "barrier", "boundary", "admin_level",
#                "building", "entrance", "craft", "emergency", "geological", "healthcare", "highway", "footway",
#                "sidewalk",
#                "cycleway", "abutters", "bus_bay", "junction", "lanes", "lit", "motorroad", "oneway", "overtaking",
#                "priority_road", "service", "smoothness", "surface", "turn", "historic", "landuse", "leisure",
#                "man_made",
#                "military", "natural", "office", "place", "population", "is_in", "power", "public_transport", "railway",
#                "usage", "route", "shop", "sport", "telecom", "tourism", "water", "waterway", "area", "bridge",
#                "access",
#                "est_width", "maxwidth", "maxaxleload", "maxheight", "maxlength", "maxstay", "maxweight", "maxspeed",
#                "minspeed"]
column_list = ["osmid", "x", "y", "continent", "name", "aerialway", "aeroway", "amenity", "barrier", "boundary",
               "admin_level", "building", "entrance", "height", "craft", "emergency", "geological", "healthcare",
               "highway",
               "ford", "lit", "historic", "landuse", "leisure", "man_made", "military", "natural", "office", "place",
               "population", "is_in", "power", "public_transport", "railway", "shop", "sport", "telecom", "tourism",
               "water", "waterway", "crossing"]

for i in range(len(column_list)):
    if column_list[i] == 'x' or column_list[i] == 'y':
        header = header + column_list[i] + ' FLOAT,'
    elif column_list[i] == 'osmid':
        header = header + column_list[i] + ' BIGINT,'
    else:
        header = header + column_list[i] + ' VARCHAR(65535),'

print(header)
