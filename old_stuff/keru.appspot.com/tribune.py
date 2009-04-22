import cgi
import wsgiref.handlers
import os
import re
import datetime

#from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from django.utils import simplejson


#class AuthorDB(db.Model):
#  author = db.UserProperty()
#  nickname = db.StringProperty()
#  homepage = db.LinkProperty()
#  rate = db.RatingProperty()

class TribuneDB(db.Model):
  #author = db.ReferenceProperty(AuthorDB)
  author = db.UserProperty()
  nickname = db.StringProperty()
  content = db.StringProperty(multiline=False)
  date = db.DateTimeProperty(auto_now_add=True)
  
#class LinkDB(db.Model):
#  id = db.IntegerProperty()
#  lien = db.LinkProperty()
#  type = db.StringListProperty()
#  tribune = db.ReferenceProperty(TribuneDB)
#  rate = db.RatingProperty()
#
#class ImageDB(db.Model):
#  img = db.BlobProperty()
#  link = db.ReferenceProperty(LinkDB)
#  name = db.StringProperty()
#  rate = db.RatingProperty()


class MainPage(webapp.RequestHandler):
  def get(self):
    tribuneList = TribuneDB.all().order('-date').fetch(100)
    template_values = {
      'tribuneList': tribuneList,
      }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))


class TribunePost(webapp.RequestHandler):
  def post(self):
    tDB = TribuneDB()

    NicknameString = self.request.get('nick')
    ContentString = self.request.get('content')

    tDB.nickname = NicknameString
    tDB.content = ContentString
    tDB.put()

    self.redirect('/')


    


def main():
  application = webapp.WSGIApplication(
                                       [('/', MainPage),
                                        ('/post', TribunePost),
                                        ],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
