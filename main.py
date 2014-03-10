from google.appengine.ext import db

import webapp2
import os
import jinja2
import requests
import json
import logging

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

token = 'token'
TOKEN = {token:'93397.f87e38a.8028bf462514476db6e5d85d9968d9d8'}

class Instagram(webapp2.RequestHandler): 
 
    def render(self, instagrams = '', data = ''):
        template_values = {'instagrams':instagrams, 'data':data}
        template = jinja_environment.get_template('instagram.html')
        self.response.out.write(template.render(template_values))          
        
    def get(self):
        access_token = TOKEN[token]
        feed = json.loads(requests.get('https://api.instagram.com/v1/tags/looklab/media/recent?access_token=%s' % access_token).text)
        if feed['meta']['code'] == 200:
            pass
        else:    
            #if original call doesn't work or token expires, need backup for new token?
            code = self.request.get('code')
            data = {'client_id':'f87e38a1da374753a175036c6a261e8d', 'client_secret':'4ef53da82871446a909c6e2e90bc8fa6','grant_type':'authorization_code', 'redirect_uri':'http://localhost:17080/instagram', 'code':code}        
            token_url = 'https://api.instagram.com/oauth/access_token'
            auth_profile = json.loads(requests.post(token_url, data = data).text)   
            access_token = auth_profile['access_token']
            TOKEN[token] = access_token    
            feed = json.loads(requests.get('https://api.instagram.com/v1/tags/looklab/media/recent?access_token=%s' % access_token).text)
            
        #loop through data and build a list of lists to pass into HTML
        INSTAGRAMS = []
        USERNAMES = ['surajkap', 'surajtest', 'radhakapoor9']
        n = 0
        
        #raising IndexError if media number less than 20
        while n < 20:             
            try:
                username = feed['data'][n]['user']['username']    
            except IndexError:            
                break
            if username in USERNAMES:                          
                image = feed['data'][n]['images']['standard_resolution']['url']
                try:
                    caption = feed['data'][n]['caption']['text']
                except TypeError:
                    caption = ''
                likes = feed['data'][n]['likes']['count']    
                instagram = list((image, caption, username, likes))
                INSTAGRAMS.append(instagram)
            else:
                pass    
            n += 1  
        self.render(instagrams = INSTAGRAMS)
         
app = webapp2.WSGIApplication([('/instagram', Instagram)], 
                               debug=True) 
                                                                     
