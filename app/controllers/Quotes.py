from system.core.controller import *

class Quotes(Controller):
    def __init__(self, action):
        super(Quotes, self).__init__(action)
        self.load_model('Quote')
        self.db = self._app.db
   
    def index(self):
        return self.load_view('main.html')

    def logout(self):
    	session.clear()
    	return redirect('/')

    def show_user_page(self, id):
    	userinfo = self.models['Quote'].user_page_info(id)
    	userquotes = self.models['Quote'].user_page_quotes(id)
    	print userquotes
    	print "*" * 50
    	return self.load_view('userpage.html', userinfo = userinfo[0], userquotes = userquotes)


    def quote_page(self):
    	nonfaves = self.models['Quote'].show_nonfaves(session['logged_user']['id'])
    	faves = self.models['Quote'].show_faves(session['logged_user']['id'])
    	return self.load_view('quotes.html', nonfaves = nonfaves, faves = faves)

    def add_quote(self, id):
    	quote = self.models['Quote'].new_quote(request.form, id)
    	return redirect('/quotepage')

    def add_favorite(self, id1, id2):
    	quote = self.models['Quote'].add_favorite(id1, id2)
    	return redirect('/quotepage')

    def delete_favorite(self, id):
    	delete = self.models['Quote'].delete_favorite(id)
    	return redirect('/quotepage')


    def register(self):
    	newuser = self.models['Quote'].register_user(request.form)
    	if newuser == 'registered':
    		session['success'] = 'You have succesfully registered. Please log in!'
    		return redirect('/')
    	else:
    		session.clear()
    		errors = newuser
    		flash(errors)
    	return redirect('/')

    def login(self):
    	signedin = self.models['Quote'].login_user(request.form)
    	if 'logged_user' in signedin:
    		session['logged_user'] = signedin['logged_user']
    		return redirect('/quotepage')
    	else:
    		session.clear()
    		errors = signedin
    		flash(errors)
    	return redirect('/')

