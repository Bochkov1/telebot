import unittest
import time

import botfunctions

from unittest.mock import patch, Mock

class TestBotFunctions(unittest.TestCase):
    def test_compound_interest(self):
        # некорректный ввод
        with self.assertRaises(Exception):
            botfunctions.get_compound_interest(2,'ff',3,4)
        # корректный ввод
        actual_value = botfunctions.get_compound_interest(1,1,1,1)
        self.assertEqual(2.0, actual_value)



    def test_tick(self):
        with patch('botfunctions.requests.get') as mocked_request:
            # некорректный ввод
            with self.assertRaises (Exception):
                 botfunctions.get_tick("ANY")

            # корректный ввод
            mocked_request.return_value = Mock(
                status_code=200,
                ok=True,
                json=lambda: {
                    "Time Series (5min)": {
                        "2022-10-21 19:50:00": {
                            "1. open": "19.5300",
                            "2. high": "19.5300",
                            "3. low": "19.5300",
                            "4. close": "19.5300",
                            "5. volume": "529"
                        }
                    }}
            )
            actual_value = botfunctions.get_tick('M')
            mocked_request.assert_called()
            self.assertIn('19.5300', actual_value)

    def test_weather(self):
        with patch('botfunctions.requests.get') as mocked_request:
            # некорректный ввод
            mocked_request.return_value = Mock(
                status_code=200,
                ok=True,
                json=lambda: {
                    "success": 'False',
                    "message": "Error"

                }
            )
        with self.assertRaises(Exception):
            botfunctions.get_wether("ANY")

            mocked_request.return_value = Mock(
                status_code=200,
                ok=True,
                json=lambda: {
                        "success": 'true',
                        "city": "Boston",
                        "result": [
                            {
                                "date": "23.10.2022",
                                "day": "Pazar",
                                "status": "Rain",
                                "degree": "15.82",
                                "min": "11.48",
                                "max": "15.82",
                                "night": "11.82",
                                "humidity": "62"
                            }
                        ]
                }
            )

            actual_degree, actual_status = botfunctions.get_wether('Boston')
            mocked_request.assert_called()
            self.assertEqual('15.82', actual_degree)
            self.assertEqual('Rain', actual_status)

    def test_corona(self):
        with patch('botfunctions.requests.get') as mocked_request:
            # некорректный ввод
            expected_value = 0
            actual_value = botfunctions.get_corona("ANY")
            mocked_request.assert_called()
            self.assertEqual(0, actual_value)


            # корректный ввод
            mocked_request.return_value = Mock(
                status_code=200,
                ok=True,
                json=lambda: {
                        "success": 'true',
                        "result": [
                            {
                                "country": "USA",
                                "totalCases": "99,064,007",
                                "newCases": "+1,128",
                                "totalDeaths": "1,092,793",
                                "newDeaths": "",
                                "totalRecovered": "96,498,807",
                                "activeCases": ""
                            }
                        ]
                }
            )

            actual_value = botfunctions.get_corona('USA')
            self.assertEqual('99,064,007',actual_value)


    def test_phone(self):
        # некорректный ввод
        actual_value = botfunctions.get_phone_code("ANY")
        self.assertEqual(0, len(actual_value))
        # корректный ввод
        actual_value = botfunctions.get_phone_code("Russia")
        self.assertEqual('+7', actual_value)



if __name__ == '__main__':
    unittest.main()
