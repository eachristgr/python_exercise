import unittest
from unittest.mock import patch
from PopulationData import PopulationData, NoDataForTheGivenYearError

PopulationData_obj = PopulationData()

class Test(unittest.TestCase):

    def test0(self):
        """find_record_in_year: normal case"""

        records = PopulationData_obj.find_record_in_year(2020)
        expected = 3219

        self.assertEqual(expected, len(records))

    def test1(self):
        """find_record_in_year: exception"""

        expected = 'No records for the year 2021!'
        with self.assertRaises(Exception) as context:
            records = PopulationData_obj.find_record_in_year(2021)
        self.assertTrue(expected in str(context.exception))

    def test2(self):
        """closest_to_average: normal case"""
    
        countys, populations = PopulationData_obj.closest_to_average(2020)
        expected =  (['Columbiana County, OH'], [102514])
        self.assertEqual(expected, (countys, populations))

    def test3(self):
        """closest_to_average: exception"""
        
        expected = 'No records for the year 2021!'
        with self.assertRaises(Exception) as context:
            countys, populations = PopulationData_obj.closest_to_average(2021)
        self.assertTrue(expected in str(context.exception))

    # // Maybe test stdout, stderr is possible

if __name__ == '__main__':
    unittest.main()