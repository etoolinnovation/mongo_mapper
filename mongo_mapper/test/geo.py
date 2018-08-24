from mongo_mapper.core.geo import Geo

field = Geo.pos_to_field(14, 15)
print(field)
latitude, longitude = Geo.field_to_pos(field)
print(latitude)
print(longitude)

pol = Geo.list_positions_to_polygon([1, 2], [2, 3], [3, 4], [5, 6])
print(pol)
pos = Geo.polygon_to_list_positions(pol)
print(pos)


pol1 = Geo.list_positions_to_polygon([1, 2], [2, 3], [3, 4], [5, 6])
pol2 = Geo.list_positions_to_polygon([1, 2], [2, 3], [3, 4], [5, 6])
pol3 = Geo.list_positions_to_polygon([1, 2], [2, 3], [3, 4], [5, 6])

multi_pol = Geo.polygons_to_multi_polygon(pol2, pol2, pol3)

print(multi_pol)

pols = Geo.multi_polygon_to_polygons(multi_pol)

for pol in pols:
    print(pol)