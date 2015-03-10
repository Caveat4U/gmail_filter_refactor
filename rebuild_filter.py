import gdata.apps.emailsettings.client

# client = gdata.apps.emailsettings.client.EmailSettingsClient(domain='gmail.com')
# client.ClientLogin(email='chrissterlin@gmail.com', password='Quadrangle10!', source='your-apps')
# client.CreateFilter(username='liz', from_address='alice@gmail.com', has_the_word='project proposal', mark_as_read=True)

# Authorize server-to-server interactions from Google Compute Engine.
from oauth2client import gce
import httplib2

credentials = gce.AppAssertionCredentials(
  scope='https://www.googleapis.com/auth/devstorage.read_write')
http = credentials.authorize(httplib2.Http())