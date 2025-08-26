import sqlite3
def cursor():
    conn = sqlite3.Connection("Scoreboard.db")
    return conn.cursor()
    
c = cursor()
c.execute('CREATE TABLE IF NOT EXISTS highscores (username TEXT, score FlOAT)')

def user_indb(user:str):
    c = cursor()
    with c.connection:
        c.execute('SELECT 1 FROM highscores WHERE username = ?',(user,))
        prescence = bool(c.fetchone())
    c.close()
    return prescence

def score_indb(score:float):
    c = cursor()
    with c.connection:
        c.execute('SELECT 1 FROM highscores WHERE score = ?',(score,))
        prescence = bool(c.fetchone)
    c.close()
    return prescence

def all_users():
    c = cursor()
    all_users = []
    seen = set[float]()
    with c.connection:
        c.execute('SELECT username FROM highscores')
        all_users = [user[0] for user in c.fetchall() if user not in seen and not seen.add(user)]
    c.close()
    return all_users
def all_scores():
    c = cursor()
    all_scores = []
    with c.connection:
        c.execute('SELECT score FROM highscores')
        all_scores = c.fetchall()
    all_scores = list(set(all_scores))
    all_scores = [all_score[0] for all_score in all_scores]
    all_scores.sort(reverse=True)
    c.close
    
    return all_scores

def add_scores(user:str,score:float):
    
    try:
        c = cursor()
        with c.connection:
            c.execute('INSERT INTO highscores VALUES (?,?)',(user,score))
        c.close()
        print("Score added!")
    except Exception as e:
        print(e)


def get_by_user(users:list[str]):
    c = cursor()
    all_relevant_values = list[tuple[str,float]]()
    user_dict = dict[str,list[float]]()
    for user in users:
        user_dict[user] = []
        with c.connection:
            c.execute('SELECT * FROM highscores WHERE username = ?',(user,))
            all_relevant_values+=c.fetchall()
    c.close()
    
    for user,val in all_relevant_values:
        user_dict[user].append(val)

    return user_dict

def get_by_score(scores:list[float]):
    c = cursor()
    legends = dict[float,list[str]]()
    for score in scores:
        
        with c.connection:
            c.execute('SELECT username FROM highscores WHERE score = ?',(score,))
            users_with_score = list(dict.fromkeys([user[0] for user in c.fetchall()]))
        legends[score] = users_with_score
    c.close()    
        
    return legends    

def get_all():
    c = cursor()
    all_dict = dict[str,list[float]]()
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

def del_user_score(user:float):
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
    all_scores_list  = all_scores()[:x] if len(all_scores())>= x else all_scores()
    score_board = get_by_score(all_scores_list)
    min_score = int()
    legends = []
    for score in score_board:
        if len(legends)< x: 
            legends += score_board[score]
            min_score = score
        else:
            break
    to_del = [score for score in score_board if score<min_score]
    for score in to_del:
        if score in score_board:
            del score_board[score]

    return score_board

if __name__ == "__main__":
    print(top(10))