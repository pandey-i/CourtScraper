import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper import solve_captcha_direct, save_result_as_pdf, CASE_TYPES

class TestScraper(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_driver = Mock()
        
    def test_solve_captcha_direct_success(self):
        """Test successful CAPTCHA extraction from span"""
        # Mock the driver and span element
        mock_span = Mock()
        mock_span.text = "1234"
        self.mock_driver.find_element.return_value = mock_span
        
        result = solve_captcha_direct(self.mock_driver)
        
        self.assertEqual(result, "1234")
        self.mock_driver.find_element.assert_called_once_with("id", "captcha-code")
    
    def test_solve_captcha_direct_failure(self):
        """Test CAPTCHA extraction failure"""
        self.mock_driver.find_element.side_effect = Exception("Element not found")
        
        result = solve_captcha_direct(self.mock_driver)
        
        self.assertIsNone(result)
    
    def test_save_result_as_pdf(self):
        """Test PDF generation with sample data"""
        test_data = {
            'sno': '1',
            'case_no': 'ARB.P-101/2020',
            'case_no_link': 'http://example.com/case',
            'date': '04-02-2020',
            'date_link': 'http://example.com/date',
            'party': 'R. K. ASSOCIATES AND HOTELIERS PVT.LTD.\nVs\nINDIAN RAILWAY CATERING AND TOURISM CORPORATION LIMITED (IRCTC)',
            'corrigendum': 'NA'
        }
        
        # Test PDF generation (this will create a file)
        filename = save_result_as_pdf(test_data, 'test_output.pdf')
        
        # Check if file was created
        self.assertTrue(os.path.exists('test_output.pdf'))
        
        # Clean up
        if os.path.exists('test_output.pdf'):
            os.remove('test_output.pdf')
    
    def test_case_types_list(self):
        """Test that CASE_TYPES contains expected values"""
        # Check that the list is not empty
        self.assertGreater(len(CASE_TYPES), 0)
        
        # Check that it contains expected case types
        expected_types = ['ARB.P.', 'BAIL APPLN.', 'CA', 'W.P.(C)']
        for case_type in expected_types:
            self.assertIn(case_type, CASE_TYPES)
    
    def test_case_types_format(self):
        """Test that case types are properly formatted"""
        for case_type in CASE_TYPES:
            # Check that case types are strings
            self.assertIsInstance(case_type, str)
            # Check that they're not empty
            self.assertGreater(len(case_type), 0)
            # Check that they don't have leading/trailing whitespace
            self.assertEqual(case_type, case_type.strip())

class TestDatabase(unittest.TestCase):
    
    @patch('database.sqlite3.connect')
    def test_log_query(self, mock_connect):
        """Test query logging functionality"""
        from database import log_query
        
        # Mock the database connection
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.lastrowid = 1
        mock_connect.return_value = mock_conn
        
        # Test logging a query
        query_id = log_query('ARB.P.', '101', '2020')
        
        # Verify the query was logged
        self.assertEqual(query_id, 1)
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()