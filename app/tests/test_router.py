import logging
import unittest

from contextlib import asynccontextmanager
from unittest.mock import patch

from core.config import settings
from app_lib import clogging


class TestFastapiSampleMgr(unittest.TestCase):
    """ Fastapi Sample Mgr API Test """

    def setUp(self):
        """ Set up test function """
        clogging.logConfig(logLevel='DEBUG')
        self.logger = logging.getLogger(__name__)

    def tearDown(self):
        """ Tear down test function """
        pass

    @patch('app_lib.func_utility.setup_system_initialize')
    def test_root(self, mock_setup_system_initialize):
        """ Unit test function for root() """
        self.logger.info('Unit test function for root()...')
        mock_setup_system_initialize.return_value = None
        from fastapi.testclient import TestClient
        from fastapisample_main import get_app
        @asynccontextmanager
        async def lifespan():
            yield
        self.client = TestClient(get_app(settings, lifespan))
        response = self.client.get("/")
        welcome_msg = 'Welcome Fastapi Sample Manager. Running version: v0.0.0. Enjoy!'

        assert response.status_code == 200
        assert response.json() == {'message': welcome_msg}
