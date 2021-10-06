import diary

# Page for users to enter username, password to access the site
# All other pages but signup redirect here if not signed in
# Redirects to home once form submitted
@diary.app.route('/auth/login')
def login():
    # TODO
    return ''

# Page for users to create a new account
# Redirects to home once form submitted
@diary.app.route('/auth/signup')
def signup():
    # TODO
    return ''

# Page for users to log out of account
# Redirects to login once form submitted
@diary.app.route('/auth/logout')
def logout():
    # TODO
    return ''