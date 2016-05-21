from system.core.model import Model
import re
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

class Quote(Model):
    def __init__(self):
        super(Quote, self).__init__()

    def show_nonfaves(self, id):
        query = "SELECT quote_author, quote, quotes.id AS q_id, users.name, quotes.poster_id AS p_id FROM quotes LEFT JOIN users ON users.id = quotes.poster_id LEFT JOIN users_favorites ON users_favorites.user_id = users.id WHERE NOT quotes.id IN (SELECT quotes.id FROM quotes LEFT JOIN users ON users.id = quotes.poster_id LEFT JOIN users_favorites ON users_favorites.user_id = users.id WHERE users_favorites.user_id = :id)"
        data = {
            'id' :id
        }
        return self.db.query_db(query, data)

    def show_faves(self, id):
        query = "SELECT quote_author, quote, quotes.poster_id AS p_id, name, quotes.id AS q_id, users_favorites.id AS uf_id FROM users_favorites LEFT JOIN quotes on quotes.id = users_favorites.quote_id LEFT JOIN users on users.id = quotes.poster_id WHERE users_favorites.user_id = :id;"
        data = {
            'id': id
        }
        return self.db.query_db(query, data)

    def user_page_info(self, id):
        query = "SELECT name, COUNT(quotes.poster_id) as count FROM users LEFT JOIN quotes ON quotes.poster_id = users.id WHERE quotes.poster_id = :id"
        data = {
            'id': id
        }
        return self.db.query_db(query, data)

    def user_page_quotes(self, id):
        query = "SELECT quote_author, quote, quotes.id AS q_id FROM quotes WHERE quotes.poster_id = :id"
        data = {
            'id': id
        }
        return self.db.query_db(query, data)

    def new_quote(self, info, id):
        query = "INSERT INTO quotes (quote_author, quote, poster_id) VALUES (:quote_author, :quote, :id)"
        data = {
            'quote_author': info['quote_author'],
            'quote': info['quote'],
            'id': id
        }
        self.db.query_db(query, data)

    def add_favorite(self, id1, id2):
        query = "INSERT INTO users_favorites (user_id, quote_id) VALUES (:user_id, :quote_id)"
        
        data = {
            'user_id': id1,
            'quote_id': id2
        }
        self.db.query_db(query, data)

    def delete_favorite(self, id):
        query = "DELETE FROM users_favorites WHERE users_favorites.user_id = :id"
        data = {
            'id' : id,
            }
        self.db.query_db(query, data)

    def login_user(self, info):
        errors = {}

        if not EMAIL_REGEX.match(info['log_email']):
            errors.update({'log_email': 'Please enter a valid email address'})
        if len(info['log_password']) < 8:
            errors.update({'log_password': 'Password must be at least 8 characters'})
        if len(errors) > 0:
            return errors
        else:
            query = "SELECT * FROM users WHERE email = :email LIMIT 1"
            data = {
                'email': info['log_email']
            }
            user = self.db.query_db(query, data)
            if user == []:
                errors.update({'nouser': 'Email is not registered'})
                return errors
            else:
                if self.bcrypt.check_password_hash(user[0]['password'], info['log_password']):
                    logged_user = {'logged_user':{'id': user[0]['id'], 'name':user[0]['name'], 'alias': user[0]['alias'], 'email': user[0]['email'], 'created_at': user[0]['created_at']}}
                    return logged_user
                else:
                    errors.update({'passmatch': 'Password entered does not match registered email'})
                    return errors

    def register_user(self, info):
        errors = {}

        if len(info['reg_name']) < 2:
            errors.update({'reg_name': 'Name must be at least 2 characters long'})
        if len(info['reg_alias']) < 2:
            errors.update({'reg_alias': 'Alias must be at least 2 characters long'})
        if not EMAIL_REGEX.match(info['reg_email']):
            errors.update({'reg_email': 'Please enter a valid email address'})
        if len(info['reg_password']) < 8:
            errors.update({'reg_password':'Password must be at least 8 characters'})
        if info['reg_confirm'] != info ['reg_password']:
            errors.update({'reg_confirm': 'Passwords must be matching'})
        if len(info['reg_dob']) < 1:
            errors.update({'reg_dob': 'Please enter your Date of birth'})
        if len(errors) > 0:
            return errors
        else:
            pw_hash = self.bcrypt.generate_password_hash(info['reg_password'])
            query = "INSERT INTO users (name, alias, email, password, dob, created_at) VALUES (:name, :alias, :email, :password, :dob, NOW())"
            data = {
                'name': info['reg_name'],
                'alias': info['reg_alias'],
                'email': info['reg_email'],
                'password': pw_hash,
                'dob': info['reg_dob']
            }
            self.db.query_db(query, data)
        return 'registered'

