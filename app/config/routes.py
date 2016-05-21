from system.core.router import routes

routes['default_controller'] = 'Quotes'
routes['/quotepage'] = 'Quotes#quote_page'
routes['/logout'] = 'Quotes#logout'

routes['/addfavorite/<id1>/<id2>'] = 'Quotes#add_favorite'
routes['/deletefavorite/<id>'] = 'Quotes#delete_favorite'
routes['/userpage/<id>'] = 'Quotes#show_user_page'

routes['POST']['/register'] = 'Quotes#register'
routes['POST']['/login'] = 'Quotes#login'
routes['POST']['/postquote/<id>'] = 'Quotes#add_quote'
