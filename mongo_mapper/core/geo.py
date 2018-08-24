class Geo:

    @staticmethod
    def pos_to_field(latitude, longitude):
        return [longitude, latitude]

    @staticmethod
    def field_to_pos(field):
        longitude = field[0]
        latitude = field[1]
        return latitude, longitude

    @staticmethod
    def list_positions_to_polygon(*positions):
        p = list(positions)
        result = {'type': 'Polygon', 'coordinates': [p]}
        return result

    @staticmethod
    def polygon_to_list_positions(polygon):
        return polygon['coordinates'][0]

    @staticmethod
    def polygons_to_multi_polygon(*polygons):
        coordinates = []

        for polygon in polygons:
            coordinates.append(polygon['coordinates'][0])

        result = {
            'type': "MultiPolygon",
            'coordinates': [coordinates]
        }

        return result

    @staticmethod
    def multi_polygon_to_polygons(multi_polygon):
        result = []

        for d in multi_polygon['coordinates'][0]:
            result.append(
                {
                    'type': "Polygon",
                    'coordinates': [d]
                }
            )
        return result
