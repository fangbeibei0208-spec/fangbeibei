import datetime as dt
import unittest
from unittest.mock import patch
import briefs

class Checks(unittest.TestCase):
    def test_reject_old_future_undated_and_nonweb_sources(self):
        now = dt.datetime(2026, 9, 18, 4, tzinfo=dt.timezone.utc)
        def item(stamp, link='https://example.com/news'):
            return f'<item><title>AI 新闻</title><link>{link}</link><pubDate>{stamp}</pubDate></item>'
        raw = ('<rss><channel>' + item('Fri, 18 Sep 2026 01:00:00 GMT') + item('Mon, 01 Sep 2025 01:00:00 GMT') + item('Fri, 18 Sep 2026 05:00:00 GMT') + item('') + item('Fri, 18 Sep 2026 01:00:00 GMT', 'javascript:alert(1)') + '</channel></rss>').encode()
        self.assertEqual(len(briefs.parse_feed(raw, 'test', now)), 1)

    def test_reject_fabricated_citation(self):
        with self.assertRaises(RuntimeError):
            briefs.render('ai', [{'title':'测试', 'body':'事实说明'*15, 'source_ids':[999]}], [])

    def test_reject_injected_link(self):
        with self.assertRaises(RuntimeError):
            briefs.render('ai', [{'title':'测试', 'body':'事实说明'*15 + ' https://bad.example', 'source_ids':[1]}], [{}])

    @patch.dict('os.environ', {'SERVERCHAN_SENDKEY':'SCTexample'})
    @patch('briefs.request', side_effect=TimeoutError('secret URL'))
    def test_ambiguous_send_not_retried_or_leaked(self, mock):
        with self.assertRaises(RuntimeError) as error:
            briefs.send('测试', '测试')
        self.assertNotIn('secret', str(error.exception))
        self.assertEqual(mock.call_count, 1)

    @patch.dict('os.environ', {'SERVERCHAN_SENDKEY':'SCTexample'})
    @patch('briefs.request', return_value=b'{"code":40001}')
    def test_api_error_not_success(self, mock):
        with self.assertRaises(RuntimeError):
            briefs.send('测试', '测试')

if __name__ == '__main__':
    unittest.main()
