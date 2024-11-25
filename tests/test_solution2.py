import unittest
from unittest.mock import patch, AsyncMock, mock_open
import asyncio
from aiohttp import ClientSession
from task2.solution import fetch_page, parse_animals, extract_next_url, count_animals, write_to_file


class TestAnimalScraper(unittest.IsolatedAsyncioTestCase):
    @patch("your_module.ClientSession.get")
    async def test_fetch_page(self, mock_get):
        mock_response = AsyncMock()
        mock_response.text = AsyncMock(return_value="<html>Test</html>")
        mock_get.return_value = mock_response

        async with ClientSession() as session:
            html_text = await fetch_page(session, "http://example.com")
        
        self.assertEqual(html_text, "<html>Test</html>")
        mock_get.assert_called_once_with("http://example.com")

    async def test_parse_animals(self):
        html_text = """
        <html>
            <body>
                <div id="mw-pages">
                    <div>
                        <div>
                            <ul>
                                <li><a>Лиса</a></li>
                                <li><a>Медведь</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        """
        animals = await parse_animals(html_text)
        self.assertEqual(animals, ["Лиса", "Медведь"])

    async def test_extract_next_url(self):
        html_text = """
        <html>
            <body>
                <div>
                    <a href="/next-page">Next</a>
                </div>
            </body>
        </html>
        """
        next_url = await extract_next_url(html_text)
        self.assertEqual(next_url, "/next-page")

    async def test_count_animals(self):
        animals = ["Лиса", "Медведь", "Лев", "Мышь"]
        russian_upper_chars = "ЛМ"
        result = await count_animals(animals)
        self.assertEqual(result, {"Л": 2, "М": 2})

    @patch("your_module.aiofiles.open", new_callable=mock_open)
    async def test_write_to_file(self, mock_file):
        animal_counts = {"Л": 2, "М": 2}
        file_name = "test.csv"
        
        await write_to_file(file_name, animal_counts)

        mock_file.assert_called_once_with(file_name, "w")
        handle = mock_file()
        handle.write.assert_any_call("['Буква', 'Количество']\n")
        handle.write.assert_any_call("Л,2\n")
        handle.write.assert_any_call("М,2\n")
