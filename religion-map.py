import osmstataggregator

class ReligionMap(osmstataggregator.OSMStatsAggregator):
    input_data_table = "religion_point"
    input_data_cols = ['religion', 'denomination']
    land = 'land_polygons.the_geom'
    database = "gis2"

    @classmethod
    def _most_common(rows):
        most_common_religion, count = Counter([x[1] for x in rows]).most_common(1)[0]
        most_common_denomination, count = Counter([x[2] for x in rows if x[1] == most_common_religion]).most_common(1)[0]
        return (most_common_religion, most_common_denomination)
    
    def properties(self, rows):
        """
        Given a list of rows (e.g. from the database), return a dict with a set of
        properties about those rows that we want to measure.
        """

        results = {
            'closest_religion': None,
            'closest_denomination': None,
            'most_common_religion': None,
            'most_common_denomination': None,
            'most_common_10_religion': None,
            'most_common_10_denomination': None,
            'most_common_religion_wi_50km': None,
            'most_common_denomination_wi_50km': None,
            'most_common_religion_wi_10km': None,
            'most_common_denomination_wi_10km': None,
            'most_common_religion_wi_5km': None,
            'most_common_denomination_wi_5km': None,
            'weighted_most_common_religion': None,
            'weighted_most_common_denomination': None,
            'christian_score': None,
            'muslim_score': None,
            'hindu_score': None,
            'buddhist_score': None,
            'shinto_score': None,
            'jewish_score': None,
        }
        if len(rows) > 0:
            # Return closest
            results['closest_religion'] = rows[0][1]
            results['closest_denomination'] = rows[0][2]

            results['most_common_religion'], results['most_common_denomination'] = ReligionMap._most_common(rows)
            results['most_common_10_religion'], results['most_common_10_denomination'] = ReligionMap._most_common(rows[:10])

            wi_50km = [x for x in rows if x[0] <= 50000]
            if len(wi_50km) > 0:
                results['most_common_religion_wi_50km'], results['most_common_denomination_wi_50km'] = ReligionMap._most_common(wi_50km)
            wi_10km = [x for x in rows if x[0] <= 10000]
            if len(wi_10km) > 0:
                results['most_common_religion_wi_10km'], results['most_common_denomination_wi_10km'] = ReligionMap._most_common(wi_10km)
            wi_5km = [x for x in rows if x[0] <= 5000]
            if len(wi_5km) > 0:
                results['most_common_religion_wi_5km'], results['most_common_denomination_wi_5km'] = ReligionMap._most_common(wi_5km)

            religions = {x[1]:0 for x in rows}
            for row in rows:
                distance, religion, denomination = row
                religions[religion] += 1/distance

            results['christian_score'] = religions.get('christian')
            results['muslim_score'] = religions.get('muslim')
            results['jewish_score'] = religions.get('jewish')
            results['shinto_score'] = religions.get('shinto')
            results['buddhist_score'] = religions.get('buddhist')
            results['hindu_score'] = religions.get('hindu')

            weighted_religions = sorted(religions, key=religions.get)
            results['weighted_most_common_religion'] = weighted_religions[0]



        for k, v in results.items():
            if v is None:
                results[k] = 'NULL'
            #else:
            #    results[k] = v
        return results



class IrelandReligionMap(ReligionMap, IrelandArea):
    output_table = "religion_irl"

class GlobalReligionMap(ReligionMap):
    output_table = "religion_polygons_world"
    increment = 0.05

class EuropeReligionMap(EuropeArea, ReligionMap):
    output_table = "religion_euro"
    increment = 0.025

if __name__ == '__main__':
    EuropeReligionMap().main()
