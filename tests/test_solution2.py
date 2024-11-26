import unittest
import asyncio
from unittest import mock
from unittest.mock import patch, AsyncMock, mock_open, MagicMock
from aiohttp import ClientSession
from task2.solution import fetch_page, parse_animals, extract_next_url, count_animals, write_to_file, main


class AsyncContextManagerMock(MagicMock):
    async def __aenter__(self):
        return self.aenter

    async def __aexit__(self, *args):
        pass


class TestAnimalScraper(unittest.IsolatedAsyncioTestCase):
    @patch("task2.solution.ClientSession.get")
    async def test_fetch_page(self, mock_get):
        mock_response = AsyncMock()
        mock_response.text = AsyncMock(return_value="<html>Test</html>")
        mock_get.return_value.__aenter__.return_value = mock_response

        async with ClientSession() as session:
            html_text = await fetch_page(session, "http://example.com")

        self.assertEqual(html_text, "<html>Test</html>")
        mock_get.assert_called_once_with("http://example.com")

    async def test_parse_animals(self):
        html_text = '''
        <head> ... </head>
        <body>
        <div id="mw-content">
            <div id="body-content">
                <div class="category-text">
                    <div class="category-generated">
                        <div id="mw-pages">
                            <div>...</div>
                            <div>
                                <div>
                                    <div>
                                        <ul>
                                            <li><a href="link1.html">Лиса</a></li>
                                            <li><a href="link2.html">Медведь</a></li>
                                            <li><a href="link3.html">Лев</a></li>
                                            <li><a href="link4.html">Мышь</a></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </body>
        </html>
        '''
        animals = await parse_animals(html_text)
        # print(animals)
        self.assertEqual(animals, ["Лиса", "Медведь", "Лев", "Мышь"])

    async def test_extract_next_url(self):
        html_text = """
        <html>
            <body>
                <div>...</div>
                <div>...</div>
                <div>
                    <div>...</div>
                    <div>...</div>
                    <div>
                        <div>...</div>
                        <div>...</div>
                        <div>...</div>
                        <div>...</div>
                        <div>
                            <div>...</div>
                            <div>
                                <div>...</div>
                                <div>
                                    <a>...</a>
                                    <a href="/next-page" title="Категория:Животные по алфавиту">Следующая страница</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        """
        animals = ["Лиса", "Медведь", "Лев", "Мышь"]
        next_url = await extract_next_url(html_text, animals)
        self.assertEqual(next_url, "/next-page")

    async def test_count_animals(self):
        animals = ["Лиса", "Медведь", "Лев", "Мышь"]
        animals_counts = {}
        result = await count_animals(animals, animals_counts)
        self.assertEqual(result, {"Л": 2, "М": 2})

    async def test_write_to_file(self):
        animals_counts = {"Л": 2, "М": 2}
        with patch('aiofiles.open') as mock_open:
            mock_open.return_value.__aenter__.return_value.write.return_value = None
            await write_to_file('example.csv', animals_counts)
            mock_open.return_value.__aenter__.return_value.write.assert_any_call("['Буква', 'Количество']\n")
            mock_open.return_value.__aenter__.return_value.write.assert_any_call('Л,2\n')
            mock_open.return_value.__aenter__.return_value.write.assert_any_call('М,2\n')


    @patch('task2.solution.fetch_page')
    @patch('task2.solution.parse_animals')
    @patch('task2.solution.extract_next_url')
    @patch('task2.solution.count_animals')
    @patch('task2.solution.write_to_file')
    async def test_main(self,
                        mock_write_to_file,
                        mock_count_animals,
                        mock_extract_next_url,
                        mock_parse_animals,
                        mock_fetch_page):
        mock_fetch_page.return_value = '<html>example</html>'
        mock_parse_animals.side_effect = [["Лиса", "Медведь", "Лев", "Мышь"], None]
        mock_extract_next_url.side_effect = ["/next-page", None]
        mock_count_animals.animal_counts={"Л": 2, "М": 2}
        mock_count_animals.animal_counts
        mock_parse_animals.return_value = []
        await main()
        mock_write_to_file.assert_any_call('beasts.csv', {})


if __name__ == '__main__':
    unittest.main()
