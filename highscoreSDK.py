import sqlite3
def cursor():
    conn = sqlite3.Connection("Scoreboard.db")
    return conn.cursor()
    
c = cursor()
c.execute('CREATE TABLE IF NOT EXISTS highscores (username TEXT, score INTEGER)')

def user_indb(user):
    c = cursor()
    with c.connection:
        c.execute('SELECT 1 FROM highscores WHERE username = ?',(user,))
        prescence = bool(c.fetchone())
    c.close()
    return prescence

def score_indb(score):
    c = cursor()
    with c.connection:
        c.execute('SELECT 1 FROM highscores WHERE score = ?',(score,))
        prescence = bool(c.fetchone)
    c.close()
    return prescence

def all_users():
    c = cursor()
    all_users = []
    
    with c.connection:
        c.execute('SELECT username FROM highscores')
        for user in list(set(c.fetchall())):
            all_users.append("".join(user))
    return all_users

def add_scores(user,score):
    try:
        c = cursor()
        with c.connection:
            c.execute('INSERT INTO highscores VALUES (?,?)',(user,score))
        c.close()
    except Exception as e:
        print(e)

def get_by_user(users):
    c = cursor()
    user_dict = {}
    for user in users:
        with c.connection:
            c.execute('SELECT * FROM highscores WHERE username = ?',(user,))
            values = c.fetchall()
        user_dict[user] = [tple[1] for tple in values] if values else "Empty"
    c.close()
    return user_dict

def get_by_score(score):
    c = cursor()
    legends = []
    with c.connection:
        c.execute('SELECT username FROM highscores WHERE score = ?',(score,))
        f_legends  = list(set(c.fetchall()))
        for tple in f_legends:
            legends.append(tple[0])
        c.close()
    return legends
        

def get_all():
    c = cursor()
    all_dict ={}
    
    with c.connection:
        c.execute('SELECT * FROM highscores')
        values = c.fetchall()
        c.close()
    if values:
        for user, score in values:
            if user not in all_dict:
                all_dict[user] = []
            all_dict[user].append(score)
        return all_dict
    else:
        return "No scores yet"
    


def del_user_score(user):
    c =cursor()
    with c.connection:
        c.execute('DELETE FROM highscores WHERE username = ?',(user,))
    c.close()
    
def del_all():
    c =cursor()
    with c.connection:
        c.execute('DELETE FROM highscores')
    c.close()

def my_searcher(text = str):
    users = all_users()
    suggestions=[]
    if text == "":
        return []
    for user in users:
        if (user[:len(text)]).upper() == text.upper():
            suggestions.append(user)
    return suggestions

def top(x,alle = False):
    score_board = get_all()
    top_scorers = []
    allscores = []
    for user in score_board:
        allscores+=score_board[user]
        
    allscores = list(set(allscores))
    allscores.sort(reverse=True)
    if alle: x = len(allscores)
    first_x_scores = allscores[:x]
    
    for score in first_x_scores:
        top_scorers.append((get_by_score(score) ,score))
    return top_scorers
    
if __name__ == "__main__":
    # add_scores("s",49)
    # print(get_by_user("s"))
    print(all_users())
    # print(user_indb("s"))
    # del_all()
    # print(user_indb("Nyokab"))
    
