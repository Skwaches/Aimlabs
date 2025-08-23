import sqlite3
def cursor():
    conn = sqlite3.Connection("Scoreboard.db")
    return conn.cursor()
    
c = cursor()
c.execute('CREATE TABLE IF NOT EXISTS highscores (username TEXT, score INTEGER)')

def user_indb(user:str):
    c = cursor()
    with c.connection:
        c.execute('SELECT 1 FROM highscores WHERE username = ?',(user,))
        prescence = bool(c.fetchone())
    c.close()
    return prescence

def score_indb(score:int):
    c = cursor()
    with c.connection:
        c.execute('SELECT 1 FROM highscores WHERE score = ?',(score,))
        prescence = bool(c.fetchone)
    c.close()
    return prescence

def all_users():
    c = cursor()
    all_users = []
    seen = set[int]()
    with c.connection:
        c.execute('SELECT username FROM highscores')
        all_users = [user[0] for user in c.fetchall() if user not in seen and not seen.add(user)]
    c.close()
    return all_users

def add_scores(user:str,score:int):
    try:
        c = cursor()
        with c.connection:
            c.execute('INSERT INTO highscores VALUES (?,?)',(user,score))
        c.close()
    except Exception as e:
        print(e)

def get_by_user(users:list[str]):
    c = cursor()
    all_relevant_values = list[tuple[str,int]]()
    user_dict = dict[str,list[int]]()
    for user in users:
        user_dict[user] = []
        with c.connection:
            c.execute('SELECT * FROM highscores WHERE username = ?',(user,))
            all_relevant_values+=c.fetchall()
    c.close()
    
    for user,val in all_relevant_values:
        user_dict[user].append(val)

    return user_dict

def get_by_score(scores:list[int]):
    c = cursor()
    legends = dict[int,list[str]]()
    for score in scores:
        
        with c.connection:
            c.execute('SELECT username FROM highscores WHERE score = ?',(score,))
            users_with_score = list(dict.fromkeys([user[0] for user in c.fetchall()]))
        legends[score] = users_with_score
    c.close()    
        
    return legends    

def get_all():
    c = cursor()
    all_dict = dict[str,list[int]]()
    with c.connection:
        c.execute('SELECT * FROM highscores')
        data = c.fetchall()
        c.close()
    
    for user,value in data:
        if user in all_dict:
            all_dict[user].append(value)
        else:
            all_dict[user] = []
            all_dict[user].append(value)

    return all_dict

def del_user_score(user:int):
    c =cursor()
    with c.connection:
        c.execute('DELETE FROM highscores WHERE username = ?',(user,))
    c.close()
    
def del_all():
    c =cursor()
    with c.connection:
        c.execute('DELETE FROM highscores')
    c.close()

def my_searcher(text:str):
    users = all_users()
    suggestions=list[str]()
    if text == str():
        return suggestions
    for user in users:
        if (user[:len(text)]).upper() == text.upper():
            suggestions.append(user)
    return suggestions

def top(x:int):
    score_board = get_all()
    top_scores  = list[int]()
    for user in score_board:
        temp_score = max(score_board[user])
        if len(top_scores)<x:
            top_scores.append(temp_score)
        elif temp_score >= min(top_scores):
            top_scores.append(temp_score)
            top_scores.remove(min(top_scores))
    top_scores.sort(reverse=True)
    return get_by_score(top_scores)
            

if __name__ == "__main__":
    # print(get_by_user(["click sounds","timesup?","kwach"]))
    print(top(5))