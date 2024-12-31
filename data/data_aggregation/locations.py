'''
Locations Needed:
State Parks
National Parks
National Forests
Wilderness Areas
Cities with population > 10,000
Cities Near Points of Interest
Subareas of points of interest
'''

class LocationScraper:
    def __init__(self):
        pass

    def get_np(self):
        '''
        This method will get a list of all national parks and all relevant information

        args:
        - self

        outputs:
        - dataframe containing np_name, np_state, np_long, np_lat

        Other:
        - url: https://en.wikipedia.org/wiki/List_of_national_parks_of_the_United_States
        - Table Name: List of U.S. national parks
        '''
        pass

    def get_sp(self):
        '''
        This method will get a list of all state parks and all relevant information

        args:
        - self

        outputs:
        - dataframe containing sp_name, sp_state, sp_long, sp_lat

        other:
        - base url: https://en.wikipedia.org/wiki/List_of_Alabama_state_parks
        - table name 1: State parks under direct state management
            - Name
        - table name 2: State parks under shared management
        - url for coordinates: https://en.wikipedia.org/wiki/Cathedral_Caverns_State_Park
        '''
        pass
    
    def get_nf(self):
        '''
        This method will get a list of all national forests and all relevant information

        args:
        - self

        outputs:
        - dataframe containing nf_name, nf_state, nf_long, nf_lat
        '''
        pass

    def get_nw(self):
        '''
        This method will get a list of all national wilderness areas and all relevant information

        args:
        - self

        outputs:
        - dataframe containing nw_name, nw_state, nw_long, nw_lat
        '''
        pass

    def get_cities(self):
        '''
        This method will get a list of all cities with a population over 10,000 and all relevant information

        args:
        - self

        outputs:
        - dataframe containing city_name, city_state, city_zip, city_pop, np_long, np_lat
        '''
        pass

    def get_nearby(self):
        '''
        This method will get a list of all cities near points of interest (np, sp, nw, nf).
        This will include the nearest city to the North, North East, East, South East, South, South West, West, North West.
        Since the points of interest are generally large geographic areas, this will help improve weather/light pollution forecasts 

        args:
        - self

        outputs:
        - dataframe containing city_name, city_state, city_zip, city_pop, np_long, np_lat
        '''
        pass

    def get_subareas(self):
        '''
        This method will get a list of all major subareas within points of interest (np, sp, nw, nf).
        This may include notable tourist attractions, mountains, or areas listed by their associated agency.
        Since the points of interest are generally large geographic areas, this will help improve weather/light pollution forecasts and can allow for more precise location recommendations.

        args:
        - self

        outputs:
        - dataframe containing poi_type, poi_name, subarea_name, subarea_type, subarea_long, subarea_lat
        '''
        pass