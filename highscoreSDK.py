import sqlite3
with sqlite3.connect("Scoreboard.db") as conn:
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS highscores (username TEXT, score FLOAT)')

def user_indb(user:str):
    with sqlite3.connect("Scoreboard.db") as conn:
        c = conn.cursor()
        c.execute('SELECT 1 FROM highscores WHERE username = ?',(user,))
        prescence = bool(c.fetchone())
    
   
    return prescence

def score_indb(score:float):
    with sqlite3.connect("Scoreboard.db") as conn:
        c = conn.cursor()
        c.execute('SELECT 1 FROM highscores WHERE score = ?',(score,))
        prescence = bool(c.fetchone())
    
    return prescence

def all_users():
    all_users = []
    seen = set()
    with sqlite3.connect("Scoreboard.db") as conn:
        c = conn.cursor()
        c.execute('SELECT username FROM highscores')
        all_users = list(set(c.fetchall()))
    all_users = [user[0] for user in all_users]
    return all_users
def all_scores():
    all_scores = []
    with sqlite3.connect("Scoreboard.db") as conn:
        c = conn.cursor()
        c.execute('SELECT DISTINCT score FROM highscores ORDER BY score DESC')
        all_scores = [row[0] for row in c.fetchall()]
    
    return all_scores

def add_scores(user:str,score:float):
    
    try:

        with sqlite3.connect("Scoreboard.db") as conn:
            c = conn.cursor()
            c.execute('INSERT INTO highscores VALUES (?,?)',(user,score))
        
        print("Score added!")
    except Exception as e:
        print(e)


def get_by_user(users:list[str]):
    all_relevant_values:list[tuple[str,float]] = []
    user_dict :dict[str,list[float]] ={}
    for user in users:
        user_dict[user] = []
        with sqlite3.connect("Scoreboard.db") as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM highscores WHERE username = ?',(user,))
            all_relevant_values+=c.fetchall()
    
    
    for user,val in all_relevant_values:
        user_dict[user].append(val)

    return user_dict

def get_by_score(scores:list[float]):
    legends:dict[float,list[str]] = {}
    for score in scores:
        
        with sqlite3.connect("Scoreboard.db") as conn:
            c = conn.cursor()
            c.execute('SELECT username FROM highscores WHERE score = ?',(score,))
            users_with_score = list(dict.fromkeys([user[0] for user in c.fetchall()]))
        legends[score] = users_with_score
        
        
    return legends    

def get_all():
    all_dict:dict[str,list[float]] = {}
    with sqlite3.connect("Scoreboard.db") as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM highscores')
        data = c.fetchall()
        
    
    for user,value in data:
        if user in all_dict:
            all_dict[user].append(value)
        else:
            all_dict[user] = []
            all_dict[user].append(value)

    return all_dict

def del_user_score(user:str):
    with sqlite3.connect("Scoreboard.db") as conn:
        c = conn.cursor()
        c.execute('DELETE FROM highscores WHERE username = ?',(user,))
    
    
def del_all():
    
    with sqlite3.connect("Scoreboard.db") as conn:
        c = conn.cursor()
        c.execute('DELETE FROM highscores')
    


def my_searcher(text:str):
    users = all_users()
    suggestions:list[str]= []
    if text == "":
        return suggestions
    for user in users:
        if (user[:len(text)]).upper() == text.upper():
            suggestions.append(user)
    return suggestions

def top(x:int):
    all_scores_list  = all_scores()[:x] if len(all_scores())>= x else all_scores()
    score_board = get_by_score(all_scores_list)
    min_score = -1
    legends:list[str] = []
    for score in sorted(score_board.keys(),reverse=True):
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

def all_plays()->int:
    with sqlite3.connect("Scoreboard.db") as conn:
        c = conn.cursor()
        c.execute('SELECT username FROM highscores')
        all_players = c.fetchall()
    return len(all_players)
if __name__ == "__main__":
    print(all_plays())