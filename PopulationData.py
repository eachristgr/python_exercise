import json
import logging
from urllib.request import Request, urlopen
import pandas as pd


# Exceptions
class NoDataForTheGivenYearError(Exception):
    """Raise when there are not records for the year specified"""


# Population data handler20
class PopulationData:

    def __init__(self) -> None:

        url = 'https://datausa.io/api/data?drilldowns=County&measures=Population'
        site = Request(url, headers={"User-Agent": "Mozilla/5.0"})

        # Load data
        with urlopen(site) as json_file:
            self.data = json.load(json_file)['data']

    def find_record_in_year(self, year: int) -> list:

        # Select records of the specified year
        records = [x for x in self.data if x['Year'] == str(year)]

        # Check if records exist for the specified year
        if len(records) == 0:
            raise NoDataForTheGivenYearError(f'No records for the year {year}!')

        return records

    def closest_to_average(self, year: int):
            
        # Find the records and create a dataframe
        try:
            records = self.find_record_in_year(year)
        except NoDataForTheGivenYearError as ex:
            logging.exception(ex)
            raise
        
        df = pd.DataFrame.from_dict(records)

        # A better approach would be to check if there are multiple records of the same county in a specific year
        # Here that there are not douplicate records, I can not test this, so this check is skipped
        """
        duplicates = df[df['ID County'].duplicated(keep=False) == True]
        if len(duplicates) != 0:
            # do something | raise exception
        """
        
        # Find the average population for the specified year, find and put in a column the absolute difference between the average and every record
        average_population_in_year = df['Population'].mean()
        df['Absolute Differece from Average'] = abs(df['Population'] - average_population_in_year)
        
        # Find the index of the recond with the minimum difference from the average
        # But what if there are there are multiple minimums
        # Find all the reconds with the minimum difference from the average and keep their indexies
        # min_idx = df['Absolute Differece from Average'].idxmin()
        minimums = df.index[df['Absolute Differece from Average'] == df['Absolute Differece from Average'].min()]
        if len(minimums) > 1:
            print(f'{len(minimums)} Minimums')

        for min_idx in minimums:
            # If the population of the county is within +-100  of the average, print the county's record to the standard output stream
            if df.iloc[min_idx]['Absolute Differece from Average'] <= 100:
                print(f'{records[min_idx]}')  # Unless otherwise instructed, print() will default to writing to standard output.

        # Lists are returned due to the assumption that multiple minimums may exist
        return list(df.iloc[minimums]['County']), list(df.iloc[minimums]['Population'])