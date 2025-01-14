from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import pyodbc
import time

pd.set_option("display.max.rows", None)
pd.set_option("display.max.column", None)
pd.set_option("display.max_colwidth", None)

# Settings

chrome_options = Options()
chrome_options.add_experimental_option("detach", True) 
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--ignore-certificate-errors-spki-list")
chrome_options.add_argument('--log-level=3')  
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


# Start 

# ------------------------------------- Players ------------------------------------- #

def players ():

    player_white = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".player-component.player-bottom .player-details .player-name .player-name-name"))) 
    

    player_black = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".player-component .player-details .player-name .player-name-name")))

    
    return player_white, player_black


# ------------------------------------- ELO ------------------------------------- #


def elo():

    try:
        elo_white = driver.find_element(By.CSS_SELECTOR, "div.board-layout-player.board-layout-bottom > div.player-component > div.player-player > div.player-details > span.player-rating")
        elo_white = elo_white.text
    except:
        elo_white = None

    try:
        elo_black = driver.find_element(By.CSS_SELECTOR, "div.board-layout-player.board-layout-top > div.player-component > div.player-player > div.player-details > span.player-rating")
        elo_black = elo_black.text
    except:
        elo_black = None

    return elo_white, elo_black


# ------------------------------------- Country ------------------------------------- #

def country():

    try:
        country_div_white = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.board-layout-player.board-layout-bottom > div.player-component > div.player-player > div.player-details > div.country-flags-component"))) 
        
        country_attribute_white = country_div_white.get_attribute("class")
        
        class_list = country_attribute_white.split()

        for part in class_list:
            if part.startswith("country-") and part != ("country-flags-component"):
                country_white = part.split("-")[-1]
    except:
        country_white = None

    try:
        country_div_black = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.board-layout-player.board-layout-top > div.player-component > div.player-player > div.player-details > div.country-flags-component"))) 
        
        country_attribute_black = country_div_black.get_attribute("class")
        
        class_list = country_attribute_black.split()

        for part in class_list:
            if part.startswith("country-") and part != ("country-flags-component"):
                country_black = part.split("-")[-1]
    except:
        country_black = None
    
    return country_white, country_black
# ------------------------------------- Title ------------------------------------- #

def title():

    try:
        title_white = driver.find_element(By.CSS_SELECTOR, "div.board-layout-player.board-layout-bottom > div.player-component > div.player-player > div.player-details > span.user-chess-title-component.player-title")
        title_white = title_white.text
    except:
        title_white = None

    try:
        title_black = driver.find_element(By.CSS_SELECTOR, "div.board-layout-player.board-layout-top > div.player-component > div.player-player > div.player-details > span.user-chess-title-component.player-title")
        title_black = title_black.text
    except:
        title_black = None

    return title_white, title_black

# ------------------------------------- Accuracy ------------------------------------- #

def accuracy ():

    accuracy_white = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".accuracy-score-component.accuracy-score-white .accuracy-score-text .accuracy-score-value"))
    )

    accuracy_black = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".accuracy-score-component.accuracy-score-black .accuracy-score-text .accuracy-score-value"))
    )
    return accuracy_white, accuracy_black

# ------------------------------------- Moves ------------------------------------- #

def amount_of_moves():
    
    total_moves = []

    moves_light_row = driver.find_elements(By.CSS_SELECTOR, ".main-line-row.move-list-row.light-row")
    moves_dark_row = driver.find_elements(By.CSS_SELECTOR, ".main-line-row.move-list-row.dark-row")

    for i in range(len(moves_dark_row)): # Solo las piezas negras pueden ser el indice más chico, si usamos las blancas se produce un error por operar fuera del indice
        total_moves.append(moves_light_row[i])
        total_moves.append(moves_dark_row[i])
    
    if len(moves_light_row) > len(moves_dark_row):
        for move in moves_light_row[len(moves_dark_row):]: # Agregamos la última jugada de las blancas, si es que la hicieron, que quedó fuera del indice.
            total_moves.append(move)

    moves = []
    for move in total_moves:
        moves.append(move.text)

    clean_moves = []
    for move in moves:
        clean_moves.append(move.replace("\n", "/"))

    try:
        total_amount = clean_moves[-1].split("/")[0].replace(".", " ")
    except:
        total_amount = 0

    return total_amount, clean_moves


def pieces_move (clean_moves):

    filter_fen = []
    white_moves = []
    black_moves = []

    for move in clean_moves:
        parts = move.split("/")
        for part in parts:
            if len(part) > 0 and not part[0].isdigit() and not part[0] == "-" :
                filter_fen.append(part)

    for index, move in enumerate(filter_fen):
        if index % 2 == 0:
            white_moves.append(move)
        else:
            black_moves.append(move)

    
    return white_moves, black_moves


def specific_moves(white_moves):

    pieces_moves = {
    "N" : 0,    # Knight
    "B" : 0,    # Bishop
    "Q" : 0,    # Queen
    "K" : 0,    # King
    "R" : 0,    # Rook
    "a" : 0,    # A Pawn
    "b" : 0,    # B Pawn
    "c" : 0,    # C Pawn
    "d" : 0,    # D Pawn
    "e" : 0,    # E Pawn
    "f" : 0,    # F Pawn
    "g" : 0,    # G Pawn
    "h" : 0     # H Pawn
    }
    
    for move in white_moves:
        if len(move) > 0 and move[0] in pieces_moves:
                pieces_moves[move[0]] += 1            
     
    w_knight = pieces_moves["N"]
    w_bishop = pieces_moves["B"]
    w_queen = pieces_moves["Q"]
    w_king = pieces_moves["K"]
    w_rook = pieces_moves["R"]
    w_a_pawn = pieces_moves["a"]
    w_b_pawn = pieces_moves["b"]
    w_c_pawn = pieces_moves["c"]
    w_d_pawn = pieces_moves["d"]
    w_e_pawn = pieces_moves["e"]
    w_f_pawn = pieces_moves["f"]
    w_g_pawn = pieces_moves["g"]
    w_h_pawn = pieces_moves["h"]

    return  w_knight, w_bishop, w_queen, w_king, w_rook, w_a_pawn, w_b_pawn, w_c_pawn, w_d_pawn, w_e_pawn, w_f_pawn, w_g_pawn, w_h_pawn

def specific_moves(black_moves):

    pieces_moves_black = {
    "N" : 0,    # Knight
    "B" : 0,    # Bishop
    "Q" : 0,    # Queen
    "K" : 0,    # King
    "R" : 0,    # Rook
    "a" : 0,    # A Pawn
    "b" : 0,    # B Pawn
    "c" : 0,    # C Pawn
    "d" : 0,    # D Pawn
    "e" : 0,    # E Pawn
    "f" : 0,    # F Pawn
    "g" : 0,    # G Pawn
    "h" : 0     # H Pawn
    }
    
    for move in black_moves:
        if len(move) > 0 and move[0] in pieces_moves_black:
                pieces_moves_black[move[0]] += 1            
     
    b_knight = pieces_moves_black["N"]
    b_bishop = pieces_moves_black["B"]
    b_queen = pieces_moves_black["Q"]
    b_king = pieces_moves_black["K"]
    b_rook = pieces_moves_black["R"]
    b_a_pawn = pieces_moves_black["a"]
    b_b_pawn = pieces_moves_black["b"]
    b_c_pawn = pieces_moves_black["c"]
    b_d_pawn = pieces_moves_black["d"]
    b_e_pawn = pieces_moves_black["e"]
    b_f_pawn = pieces_moves_black["f"]
    b_g_pawn = pieces_moves_black["g"]
    b_h_pawn = pieces_moves_black["h"]

    return b_knight, b_bishop, b_queen, b_king, b_rook, b_a_pawn, b_b_pawn, b_c_pawn, b_d_pawn, b_e_pawn, b_f_pawn, b_g_pawn, b_h_pawn


# ------------------------------------- Opening  ------------------------------------- #

def opening_name():
    
    WebDriverWait(driver, 20).until_not(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".eco-opening-name"), "Custom Position"))

    opening = driver.find_element(By.CSS_SELECTOR, ".eco-opening-name")

    return opening


# ------------------------------------- Result  ------------------------------------- #

def result():

    game_result = driver.find_element(By.CSS_SELECTOR, ".game-over-modal-header-component")

    return game_result

# ------------------------------------- Classification  ------------------------------------- #

def brilliant_f(white_moves, black_moves):

    brilliant = driver.find_elements(By.CSS_SELECTOR, '.node-highlight-content.offset-for-annotation-icon[style="color: var(--color-classification-brilliant)"]')

    brilliant_moves_list = []
    white_brilliant_moves = []
    black_brilliant_moves = []

    for move in brilliant:
        brilliant_moves_list.append(move.text.strip())

    for move in white_moves:
        if move in brilliant_moves_list:
            white_brilliant_moves.append(move)

    for move in black_moves:
        if move in brilliant_moves_list:
            black_brilliant_moves.append(move)        

    return white_brilliant_moves, black_brilliant_moves

def mistakes_f(white_moves, black_moves):

    mistakes = driver.find_elements(By.CSS_SELECTOR, '.node-highlight-content.offset-for-annotation-icon[style="color: var(--color-classification-mistake)"]')

    mistakes_moves_list = []
    white_mistakes_moves = []
    black_mistakes_moves = []

    for move in mistakes:
        mistakes_moves_list.append(move.text.strip())

    for move in white_moves:
        if move in mistakes_moves_list:
            white_mistakes_moves.append(move)

    for move in black_moves:
        if move in mistakes_moves_list:
            black_mistakes_moves.append(move)        

    return white_mistakes_moves, black_mistakes_moves

def miss(white_moves, black_moves):

    miss = driver.find_elements(By.CSS_SELECTOR, '.node-highlight-content.offset-for-annotation-icon[style="color: var(--color-classification-miss)"]')

    miss_moves_list = []
    white_miss_moves = []
    black_miss_moves = []

    for move in miss:
        miss_moves_list.append(move.text.strip())

    for move in white_moves:
        if move in miss_moves_list:
            white_miss_moves.append(move)

    for move in black_moves:
        if move in miss_moves_list:
            black_miss_moves.append(move)        

    return white_miss_moves, black_miss_moves

def great_moves_f(white_moves, black_moves):

    great_moves = driver.find_elements(By.CSS_SELECTOR, '.node-highlight-content.offset-for-annotation-icon[style="color: var(--color-classification-great)"]')

    great_moves_list = []
    white_great_moves = []
    black_great_moves = []

    for move in great_moves:
        great_moves_list.append(move.text.strip())

    for move in white_moves:
        if move in great_moves_list:
            white_great_moves.append(move)

    for move in black_moves:
        if move in great_moves_list:
            black_great_moves.append(move)        

    return white_great_moves, black_great_moves

def blunder_count(white_moves, black_moves):
 
    blunders = driver.find_elements(By.CSS_SELECTOR, '.node-highlight-content.offset-for-annotation-icon[style="color: var(--color-classification-blunder)"]')
    
    blunders_list = []
    white_blunders = []
    black_blunders = []

    for blunder in blunders:
        blunders_list.append(blunder.text.strip())

    for move in white_moves:
        if move in blunders_list:
            white_blunders.append(move)

    for move in black_moves:
        if move in blunders_list:
            black_blunders.append(move)        

    return white_blunders, black_blunders



# ------------------------------------- SQL ------------------------------------- #

def connect_db():

    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=PC;'  
        'DATABASE=Olympiads;'  
        'Trusted_Connection=yes;'  
    )
    return conn

def insert_data_on_main(conn, player_white, elo_white, title_white, country_white, player_black, elo_black, title_black, country_black, opening, total_amount, game_result, accuracy_white, white_brilliant_moves, \
                        white_blunders, white_mistakes_moves, white_great_moves, white_miss_moves, accuracy_black, black_brilliant_moves, black_blunders, black_mistakes_moves, \
                        black_great_moves, black_miss_moves):
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO dbo.Round3 (white_pieces, elo_white, title_white, country_white, black_pieces, elo_black, title_black, country_black, opening, amount_of_moves, game_result, accuracy_white, \
                   white_brilliants, white_blunders, white_mistakes, white_greats, white_miss, accuracy_black, black_brilliants, black_blunders, black_mistakes, black_greats, black_miss)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (player_white, elo_white, title_white, country_white, player_black, elo_black, title_black, country_black, opening, total_amount, game_result, accuracy_white, white_brilliant_moves, \
              white_blunders, white_mistakes_moves, white_great_moves, white_miss_moves, accuracy_black, black_brilliant_moves, black_blunders, black_mistakes_moves, \
              black_great_moves, black_miss_moves)
    )
    conn.commit()

def insert_data_white_table2(conn, player_white, w_a_pwn, w_b_pwn, w_c_pwn, w_d_pwn, w_e_pwn, w_f_pwn, w_g_pwn, w_h_pwn, w_knight, w_bishop, w_king, w_queen, w_rook):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dbo.MovesRound3(player_name, a_pawn, b_pawn, c_pawn, d_pawn, e_pawn, f_pawn, g_pawn, h_pawn, knight, bishop, king, queen, rook)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (player_white, w_a_pwn, w_b_pwn, w_c_pwn, w_d_pwn, w_e_pwn, w_f_pwn, w_g_pwn, w_h_pwn, w_knight, w_bishop, w_king, w_queen, w_rook)
    )
    conn.commit()

def insert_data_black_table2(conn, player_black, b_a_pwn, b_b_pwn, b_c_pwn, b_d_pwn, b_e_pwn, b_f_pwn, b_g_pwn, b_h_pwn, b_knight, b_bishop, b_king, b_queen, b_rook):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dbo.MovesRound3 (player_name, a_pawn, b_pawn, c_pawn, d_pawn, e_pawn, f_pawn, g_pawn, h_pawn, knight, bishop, king, queen, rook)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (player_black, b_a_pwn, b_b_pwn, b_c_pwn, b_d_pwn, b_e_pwn, b_f_pwn, b_g_pwn, b_h_pwn, b_knight, b_bishop, b_king, b_queen, b_rook)
    )
    conn.commit()

# ------------------------------------- Main ------------------------------------- #

    
def main():

    df = pd.read_csv(r"round3.csv", header = 1, names = ["Links"])


    for row in df["Links"]: 
        
        driver.get(row)
    
        time.sleep(15)

        player_white_elem, player_black_elem = players()
        accuracy_white_elem, accuracy_black_elem = accuracy()
        opening_elem = opening_name()
        moves, clean_moves = amount_of_moves()
        white_moves, black_moves = pieces_move(clean_moves)
        game_result_elem = result()
        elo_white, elo_black = elo()
        title_white, title_black = title()
        country_white, country_black = country()

        player_white = player_white_elem.text   
        player_black = player_black_elem.text
        accuracy_white = accuracy_white_elem.text
        accuracy_black = accuracy_black_elem.text
        opening = opening_elem.text
        game_result = game_result_elem.text

        buttons = driver.find_elements(By.CLASS_NAME, "v5-tabs-button.underlined-tabs-button")
        analysis_button = buttons[1]
        analysis_button.click()

        white_blunders, black_blunders = blunder_count(white_moves, black_moves)
        white_great_moves, black_great_moves = great_moves_f(white_moves, black_moves)
        white_miss_moves, black_miss_moves = miss(white_moves, black_moves)
        white_mistakes, black_mistakes = mistakes_f(white_moves, black_moves)
        white_brilliant, black_brilliant = brilliant_f(white_moves, black_moves)

        white_brilliant = ", ".join(white_brilliant)
        white_blunders = ", ".join(white_blunders)
        white_great_moves= ", ".join(white_great_moves)
        white_mistakes = ", ".join(white_mistakes)
        white_miss_moves = ", ".join(white_miss_moves)

        black_brilliant = ", ".join(black_brilliant)
        black_blunders = ", ".join(black_blunders)    
        black_great_moves = ", ".join(black_great_moves)
        black_mistakes = ", ".join(black_mistakes) 
        black_miss_moves = ", ".join(black_miss_moves)
        
        w_knight, w_bishop, w_queen, w_king, w_rook, w_a_pwn, w_b_pwn, w_c_pwn, w_d_pwn, w_e_pwn, w_f_pwn, w_g_pwn, w_h_pwn = specific_moves(white_moves)
        b_knight, b_bishop, b_queen, b_king, b_rook, b_a_pwn, b_b_pwn, b_c_pwn, b_d_pwn, b_e_pwn, b_f_pwn, b_g_pwn, b_h_pwn = specific_moves(black_moves)

        print(white_blunders, white_great_moves, white_mistakes)

        conn = connect_db()
        try:
            insert_data_on_main(conn, player_white, elo_white, title_white, country_white, player_black, elo_black, title_black, country_black, opening, moves, game_result, accuracy_white, white_brilliant, \
                                white_blunders, white_mistakes, white_great_moves, white_miss_moves, accuracy_black, black_brilliant, black_blunders, black_mistakes, \
                                black_great_moves, black_miss_moves) 
            insert_data_white_table2(conn, player_white, w_a_pwn, w_b_pwn, w_c_pwn, w_d_pwn, w_e_pwn, w_f_pwn, w_g_pwn, w_h_pwn, w_knight, w_bishop, w_king, w_queen, w_rook)
            insert_data_black_table2(conn, player_black, b_a_pwn, b_b_pwn, b_c_pwn, b_d_pwn, b_e_pwn, b_f_pwn, b_g_pwn, b_h_pwn, b_knight, b_bishop, b_king, b_queen, b_rook)
            print(f"Datos insertados para {player_white} vs {player_black}")

        except:
            print(f"No se han podido insertar los datos para {player_white} vs {player_black}")

    conn.close()
    driver.quit()

main()

