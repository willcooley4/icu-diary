[1mdiff --cc diary/newentry.py[m
[1mindex 1daa698,7e61ac8..0000000[m
[1m--- a/diary/newentry.py[m
[1m+++ b/diary/newentry.py[m
[36m@@@ -68,11 -52,48 +77,22 @@@[m [mdef entry_page()[m
          '''.format(title, content, media, author, diary_id))[m
          conn.commit()[m
  [m
[31m -        #media upload[m
[31m -        if media:[m
[31m -            files = request.files["media"][m
[31m -            for f in files:[m
[31m -                fh = open(f"uploads/{f.filename}", "wb")[m
[31m -                fh.write(f.body)[m
[31m -                fh.close()[m
[31m -[m
[31m -[m
[31m -[m
[31m -[m
[31m -[m
[31m -        context = {'e': 1, 'message': 'Message submitted!'}[m
[31m -        return render_template('newentry.html', **context)[m
[31m -[m
[31m -    # GET[m
[31m -    context = {'e': 0, 'message': ''}[m
[31m -[m
[31m -    #Check for med staff template[m
[31m -    author = flask.session["username"][m
[31m -    conn = get_db()[m
[31m -    cur = conn.cursor()[m
[31m -    cur.execute('''[m
[31m -        SELECT * FROM users[m
[31m -        WHERE username = '{}'[m
[31m -    '''.format(author))[m
[31m -    conn.commit()[m
[31m -    usertype = cur.fetchone()['user_type'][m
[31m -    if usertype == 'physician':[m
[31m -        context = {'e': 2, 'message' : ''}[m
[32m +        context = {'e': 1, 'message': 'Message submitted!', 'user_type': user_type}[m
          return render_template('newentry.html', **context)[m
  [m
[32m +    [m
[32m +    #GET[m
[32m +    context = {'e': 0, 'message': '', 'user_type': user_type}[m
      return render_template('newentry.html', **context)[m
  [m
[32m+ [m
[32m+ # @message_api.route('/messenger/message/send/picture/individual', methods=['POST'])[m
[32m+ # def send_individual_picture():[m
[32m+ #     picture = request.files['picture'][m
[32m+ [m
[32m+ #     temp = tempfile.NamedTemporaryFile(delete=False)[m
[32m+ #     picture.save(temp.name)[m
[32m+ #     firebase.storage().put(temp.name)[m
[32m+ [m
[32m+ #     # Clean-up temp image[m
[32m+ #     os.remove(temp.name)[m
