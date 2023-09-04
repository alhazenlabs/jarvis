import unittest
from unittest.mock import Mock, patch
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from utils.db import (
    get_engine,
    load_db,
    session,
    terminating_sn
)


class TestDatabaseUtils(unittest.TestCase):

    def setUp(self):
        # Set up any necessary configurations or mock objects here
        pass

    def tearDown(self):
        # Clean up any resources used during the tests
        pass

    def test_get_engine(self):
        # Test the get_engine function
        engine = get_engine()
        self.assertIsInstance(engine, Engine)

    @patch('os.path.exists')
    @patch('utils.db.Base.metadata.create_all')
    def test_load_db_exists(self, mock_create_all, mock_exists):
        # Test loading the database when it already exists
        mock_exists.return_value = True
        load_db()
        self.assertTrue(mock_exists.called)
        self.assertFalse(mock_create_all.called)

    @patch('os.path.exists')
    @patch('utils.db.Base.metadata.create_all')
    @patch('utils.db.get_engine')
    def test_load_db_not_exists(self, mock_get_engine, mock_create_all, mock_exists):
        # Test loading the database when it does not exist
        mock_exists.return_value = False
        mock_get_engine.return_value = Mock()
        load_db()
        self.assertTrue(mock_exists.called)
        self.assertTrue(mock_create_all.called)

    def test_session(self):
        # Test creating a database session
        with patch('utils.db.get_engine') as mock_get_engine:
            mock_get_engine.return_value = Mock()
            sess = session()
            self.assertIsInstance(sess, Session)

    def test_terminating_sn(self):
        # Test the terminating_sn context manager
        with terminating_sn() as sn:
            self.assertIsInstance(sn, Session)
        # Ensure that the session is closed and the connection is disposed
        self.assertTrue(sn.close)
        self.assertTrue(sn.bind.dispose)


if __name__ == '__main__':
    unittest.main()
