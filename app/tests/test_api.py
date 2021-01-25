from unittest.mock import patch, mock_open

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from app import get_app


class MyAppTestCase(AioHTTPTestCase):

    async def get_application(self):
        return get_app()

    @unittest_run_loop
    async def test_healthz(self):
        resp = await self.client.request('GET', '/healthz')
        assert resp.status == 200

    @unittest_run_loop
    async def test_illegal_payload(self):
        resp = await self.client.request('POST', '/directoru', json={'foo': 'bar'})
        assert resp.status == 400

    @unittest_run_loop
    async def test_list_dir_success(self):
        dir_list = ['file.txt', 'image.jpg']
        with patch('time.sleep'):
            with patch('os.listdir') as mock_listdir:
                mock_listdir.return_value = dir_list
                resp = await self.client.request('POST', '/directory', json={'path': '/'})
        assert resp.status == 200
        return_json = await resp.json()
        assert return_json['directory_contents'] == dir_list

    @unittest_run_loop
    async def test_list_dir_fail_not_allowed(self):
        with patch('time.sleep'):
            with patch('os.listdir') as mock_listdir:
                mock_listdir.side_effect = PermissionError
                resp = await self.client.request('POST', '/directory', json={'path': '/'})
        assert resp.status == 403

    @unittest_run_loop
    async def test_list_dir_fail_not_found(self):
        with patch('time.sleep'):
            with patch('os.listdir') as mock_listdir:
                mock_listdir.side_effect = FileNotFoundError
                resp = await self.client.request('POST', '/directory', json={'path': '/'})
        assert resp.status == 404

    @unittest_run_loop
    async def test_list_dir_fail_not_a_directory(self):
        with patch('time.sleep'):
            with patch('os.listdir') as mock_listdir:
                mock_listdir.side_effect = NotADirectoryError
                resp = await self.client.request('POST', '/directory', json={'path': '/'})
        assert resp.status == 400

    @unittest_run_loop
    async def test_list_file_success(self):
        file_content = 'Test Content'
        with patch('time.sleep'):
            with patch("builtins.open", mock_open(read_data=file_content)):
                resp = await self.client.request('POST', '/file', json={'path': '/'})
        assert resp.status == 200
        return_json = await resp.json()
        assert return_json['file_contents'] == file_content

    @unittest_run_loop
    async def test_list_file_fail_not_allowed(self):
        with patch('time.sleep'):
            with patch('builtins.open') as mocked_file:
                mocked_file.side_effect = PermissionError
                resp = await self.client.request('POST', '/file', json={'path': '/'})
        assert resp.status == 403

    @unittest_run_loop
    async def test_list_file_fail_not_found(self):
        with patch('time.sleep'):
            with patch('builtins.open') as mocked_file:
                mocked_file.side_effect = FileNotFoundError
                resp = await self.client.request('POST', '/file', json={'path': '/'})
        assert resp.status == 404

    @unittest_run_loop
    async def test_list_file_fail_is_a_directory(self):
        with patch('time.sleep'):
            with patch('builtins.open') as mock_file:
                mock_file.side_effect = IsADirectoryError
                resp = await self.client.request('POST', '/file', json={'path': '/'})
        assert resp.status == 400
