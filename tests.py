import os
import unittest
from unittest.mock import patch
from flask_testing import TestCase
from app import app

class TestWebhook(TestCase):
  def create_app(self):
    app.config['TESTING'] = True
    return app

  @patch('app.threading.Thread')
  @patch('app.logging.error')
  def test_webhook_no_dst_url(self, mock_log, mock_thread):
    if 'RELAY_DST_URL' in os.environ:
      del os.environ['RELAY_DST_URL']

    response = self.client.post('/webhooks/test')
    self.assertEqual(response.status_code, 500)
    self.assertEqual(response.json, {'success': False})
    mock_thread.assert_not_called()
    mock_log.assert_called_once_with('An error occurred in the main thread: RELAY_DST_URL environment variable is not set')

  @patch('app.threading.Thread')
  def test_webhook_with_dst_url(self, mock_thread):
    os.environ['RELAY_DST_URL'] = 'http://localhost'
    response = self.client.post('/webhooks/test')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json, {'success': True})
    mock_thread.assert_called_once()

  @patch('app.threading.Thread', side_effect=Exception('Test exception'))
  @patch('app.logging.error')
  def test_webhook_exception(self, mock_log, mock_thread):
    os.environ['RELAY_DST_URL'] = 'http://localhost'
    mock_thread.side_effect = Exception('Test exception')
    response = self.client.post('/webhooks/test')
    self.assertEqual(response.status_code, 500)
    self.assertEqual(response.json, {'success': False})
    mock_log.assert_called_once_with('An error occurred in the main thread: Test exception')

  def test_status_endpoint(self):
    response = self.client.get('/status')
    self.assertEqual(response.status_code, 200)

  @patch('app.send_discord_notification')
  @patch('app.requests.post')
  def test_discord_notification_sent(self, mock_post, mock_send_discord_notification):
    os.environ['RELAY_DST_URL'] = 'http://localhost'
    os.environ['DISCORD_WEBHOOK_URL'] = 'http://discordwebhook'

    # Mock a successful response from the relay destination
    mock_post.return_value.status_code = 200

    response = self.client.post('/webhooks/test')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json, {'success': True})

    # Check if the Discord notification was sent
    mock_send_discord_notification.assert_called_once_with("Request successfully relayed to http://localhost/test")

if __name__ == '__main__':
    unittest.main()
