import webapp2
# from moves import fetch


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World3!')

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
