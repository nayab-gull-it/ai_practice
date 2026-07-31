"""
Tic Tac Toe - Streamlit App (You vs Computer)
Author: Nayab

Features:
- Asks player's name before the game starts
- Player always plays as X, Computer plays as O
- Score tracked using the player's actual name (not "Player X")
- Win / Draw detection with highlighted winning line
- Celebration effect (balloons + glowing banner) when player wins
- Reset board / Reset scores
- Polished dark theme UI with high-contrast text and custom fonts
"""

import random
import streamlit as st

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Tic Tac Toe | You vs Computer",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# Custom CSS Styling (Dark theme, high contrast, nice fonts)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Fredoka:wght@500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at top, #1a1c2c 0%, #0d0e17 65%, #05060a 100%);
    }

    /* Hide default streamlit chrome for a cleaner look */
    #MainMenu, footer, header {visibility: hidden;}

    h1.title {
        text-align: center;
        font-family: 'Fredoka', sans-serif;
        font-size: 3.1rem;
        font-weight: 700;
        background: linear-gradient(90deg, #ff5e78, #ffb84d, #4de1c1, #4dabf7);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        letter-spacing: 1px;
    }

    .subtitle {
        text-align: center;
        color: #e6e6f0;
        font-size: 1.05rem;
        font-weight: 400;
        margin-bottom: 1.4rem;
        opacity: 0.85;
    }

    /* Board buttons */
    div.stButton > button {
        height: 100px;
        width: 100%;
        font-size: 2.6rem;
        font-weight: 800;
        font-family: 'Fredoka', sans-serif;
        border-radius: 18px;
        border: 2px solid #3d4166;
        background: linear-gradient(145deg, #22243a, #1a1c2e);
        color: #ffffff;
        box-shadow: 0 4px 10px rgba(0,0,0,0.35);
        transition: all 0.18s ease-in-out;
    }

    div.stButton > button:hover {
        background: linear-gradient(145deg, #2d3060, #23264a);
        border-color: #4dabf7;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 16px rgba(77,171,247,0.35);
        color: #ffffff;
    }

    div.stButton > button:disabled {
        color: #ffffff !important;
        opacity: 1 !important;
        background: linear-gradient(145deg, #22243a, #1a1c2e);
    }

    /* Primary buttons (Start Game / Play Again) get a bold accent look */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #ff5e78, #ff8b4d) !important;
        border: none !important;
        color: #ffffff !important;
        height: 56px;
        font-size: 1.15rem !important;
        box-shadow: 0 6px 16px rgba(255,94,120,0.35);
    }

    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(90deg, #ff7590, #ffa066) !important;
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 8px 20px rgba(255,94,120,0.5);
    }

    /* Score cards */
    .score-box {
        background: linear-gradient(145deg, #1c1f34, #14162a);
        border-radius: 16px;
        padding: 16px 10px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    .score-label {
        font-size: 0.92rem;
        color: #c7c9e0;
        font-weight: 600;
        letter-spacing: 0.4px;
    }

    .score-value {
        font-size: 2rem;
        font-weight: 800;
        font-family: 'Fredoka', sans-serif;
        margin-top: 4px;
    }

    /* Status banner */
    .status-banner {
        text-align: center;
        font-size: 1.35rem;
        font-weight: 700;
        font-family: 'Fredoka', sans-serif;
        padding: 14px;
        border-radius: 14px;
        margin: 16px 0;
        letter-spacing: 0.3px;
    }

    .win-banner {
        animation: glow 1.2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from { box-shadow: 0 0 10px rgba(255,215,0,0.5), 0 0 20px rgba(255,215,0,0.3); }
        to   { box-shadow: 0 0 25px rgba(255,215,0,0.9), 0 0 45px rgba(255,215,0,0.6); }
    }

    /* Native bordered container styled as a dark card (used for name entry) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(145deg, #1c1f34, #14162a);
        border-radius: 20px !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        padding: 6px;
    }

    .stTextInput input {
        background-color: #22243a !important;
        color: #ffffff !important;
        border: 2px solid #3d4166 !important;
        border-radius: 10px !important;
        font-size: 1.05rem !important;
        padding: 10px 14px !important;
    }

    .stTextInput input:focus {
        border-color: #4dabf7 !important;
        box-shadow: 0 0 0 2px rgba(77,171,247,0.3) !important;
    }

    label, .stTextInput label {
        color: #e6e6f0 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }

    .stCaption, .css-1629p8f, p, span {
        color: #d5d6e6;
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #14162a, #0d0e17);
    }

    /* Radio buttons (difficulty selector) - make clearly visible */
    div[data-testid="stSidebar"] .stRadio label,
    div[data-testid="stSidebar"] .stRadio p {
        color: #ffffff !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }

    div[data-testid="stSidebar"] .stRadio > div {
        background: #1c1f34;
        padding: 10px 14px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.12);
    }

    div[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
        color: #ffffff !important;
    }

    div[data-testid="stSidebar"] .stCaption, 
    div[data-testid="stSidebar"] p,
    div[data-testid="stSidebar"] span,
    div[data-testid="stSidebar"] .stMarkdown {
        color: #e6e6f0 !important;
    }

    footer-note {
        text-align:center;
        color:#9a9cc0;
        font-size:0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
def init_state():
    defaults = {
        "board": [""] * 9,
        "current_player": "X",
        "winner": None,
        "winning_combo": [],
        "game_over": False,
        "player_name": "",
        "name_confirmed": False,
        "difficulty": "Medium",
        "scores": {"player": 0, "Computer": 0, "Draw": 0},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()

WIN_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
]


# ---------------------------------------------------------
# Game Logic Helpers
# ---------------------------------------------------------
def check_winner(board):
    for combo in WIN_COMBOS:
        a, b, c = combo
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a], combo
    if "" not in board:
        return "Draw", []
    return None, []


def record_result(winner):
    st.session_state.winner = winner
    st.session_state.game_over = True
    if winner == "Draw":
        st.session_state.scores["Draw"] += 1
    elif winner == "X":
        st.session_state.scores["player"] += 1
    else:
        st.session_state.scores["Computer"] += 1


def minimax(board, depth, is_maximizing):
    """Minimax search. Computer (O) maximizes, Player (X) minimizes."""
    winner, _ = check_winner(board)
    if winner == "O":
        return 10 - depth
    if winner == "X":
        return depth - 10
    if winner == "Draw":
        return 0

    empty_cells = [i for i, v in enumerate(board) if v == ""]

    if is_maximizing:
        best_score = -float("inf")
        for i in empty_cells:
            board[i] = "O"
            score = minimax(board, depth + 1, False)
            board[i] = ""
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for i in empty_cells:
            board[i] = "X"
            score = minimax(board, depth + 1, True)
            board[i] = ""
            best_score = min(best_score, score)
        return best_score


def best_move_minimax(board):
    """Find the optimal move for the computer using minimax."""
    best_score = -float("inf")
    move = None
    for i in [i for i, v in enumerate(board) if v == ""]:
        board[i] = "O"
        score = minimax(board, 0, False)
        board[i] = ""
        if score > best_score:
            best_score = score
            move = i
    return move


def pick_computer_cell(empty_cells):
    """Choose a cell index for the computer based on the selected difficulty."""
    board = st.session_state.board
    difficulty = st.session_state.difficulty

    if difficulty == "Easy":
        return random.choice(empty_cells)

    if difficulty == "Medium":
        # 1. Take a winning move if available
        for i in empty_cells:
            board[i] = "O"
            if check_winner(board)[0] == "O":
                board[i] = ""
                return i
            board[i] = ""

        # 2. Block the player's winning move if they have one
        for i in empty_cells:
            board[i] = "X"
            if check_winner(board)[0] == "X":
                board[i] = ""
                return i
            board[i] = ""

        # 3. Otherwise play randomly
        return random.choice(empty_cells)

    # Hard: unbeatable minimax
    return best_move_minimax(board)


def computer_move():
    """Computer (O) plays a move based on the chosen difficulty."""
    empty_cells = [i for i, v in enumerate(st.session_state.board) if v == ""]
    if not empty_cells:
        return
    choice = pick_computer_cell(empty_cells)
    st.session_state.board[choice] = "O"
    winner, combo = check_winner(st.session_state.board)
    if winner:
        st.session_state.winning_combo = combo
        record_result(winner)
    else:
        st.session_state.current_player = "X"


def make_move(index):
    if st.session_state.board[index] != "" or st.session_state.game_over:
        return

    # Player move (always X)
    st.session_state.board[index] = "X"
    winner, combo = check_winner(st.session_state.board)

    if winner:
        st.session_state.winning_combo = combo
        record_result(winner)
        return

    st.session_state.current_player = "O"
    computer_move()


def reset_board():
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.winning_combo = []
    st.session_state.game_over = False


def reset_scores():
    st.session_state.scores = {"player": 0, "Computer": 0, "Draw": 0}
    reset_board()


def change_player():
    st.session_state.name_confirmed = False
    reset_scores()


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.markdown("<h1 class='title'>Tic Tac Toe</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>You vs Computer &nbsp;•&nbsp; Built with Python & Streamlit</p>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Step 1: Ask player's name before game starts
# ---------------------------------------------------------
if not st.session_state.name_confirmed:
    with st.container(border=True):
        st.markdown("### 👋 What should we call you?")
        name_input = st.text_input(
            "Enter your name to start the game",
            value=st.session_state.player_name,
            placeholder="e.g. Nayab",
        )
        start_col1, start_col2 = st.columns([1, 1])
        with start_col1:
            start_clicked = st.button("🚀 Start Game", use_container_width=True, type="primary")
        with start_col2:
            st.caption("You'll play as ❌  •  Computer plays as ⭕")

        if start_clicked:
            cleaned_name = name_input.strip()
            if cleaned_name:
                st.session_state.player_name = cleaned_name
                st.session_state.name_confirmed = True
                reset_board()
                st.rerun()
            else:
                st.warning("Please enter your name to continue.")
    st.stop()

player_name = st.session_state.player_name

# ---------------------------------------------------------
# Sidebar Options
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Game Options")
    st.write(f"Playing as: **{player_name}** (❌)")

    st.divider()
    st.subheader("🎯 Difficulty")
    difficulty_options = ["Easy", "Medium", "Hard"]
    selected_difficulty = st.radio(
        "Choose computer difficulty",
        difficulty_options,
        index=difficulty_options.index(st.session_state.difficulty),
        label_visibility="collapsed",
    )
    if selected_difficulty != st.session_state.difficulty:
        st.session_state.difficulty = selected_difficulty
        reset_board()

    if selected_difficulty == "Easy":
        st.caption("🟢 Computer moves randomly.")
    elif selected_difficulty == "Medium":
        st.caption("🟡 Computer blocks you & takes wins, otherwise random.")
    else:
        st.caption("🔴 Computer plays perfectly — unbeatable!")

    st.divider()
    if st.button("🔄 Reset Board", use_container_width=True):
        reset_board()
    if st.button("🗑️ Reset Scores", use_container_width=True):
        reset_scores()
    if st.button("👤 Change Player", use_container_width=True):
        change_player()
        st.rerun()

    st.divider()
    st.caption("Rules: Get 3 in a row (horizontal, vertical or diagonal) to win.")

difficulty_colors = {"Easy": "#4de1c1", "Medium": "#ffb84d", "Hard": "#ff5e78"}
st.markdown(
    f"<p style='text-align:center; margin-bottom:0.6rem;'>"
    f"<span style='background:rgba(255,255,255,0.06); border:1px solid {difficulty_colors[st.session_state.difficulty]}55; "
    f"color:{difficulty_colors[st.session_state.difficulty]}; padding:5px 14px; border-radius:20px; "
    f"font-size:0.85rem; font-weight:600;'>🎯 Difficulty: {st.session_state.difficulty}</span></p>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Scoreboard
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f"""<div class='score-box'>
        <div class='score-label'>{player_name} ❌</div>
        <div class='score-value' style='color:#ff5e78;'>{st.session_state.scores['player']}</div>
        </div>""",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"""<div class='score-box'>
        <div class='score-label'>Draws 🤝</div>
        <div class='score-value' style='color:#ffb84d;'>{st.session_state.scores['Draw']}</div>
        </div>""",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f"""<div class='score-box'>
        <div class='score-label'>Computer ⭕</div>
        <div class='score-value' style='color:#4dabf7;'>{st.session_state.scores['Computer']}</div>
        </div>""",
        unsafe_allow_html=True,
    )

st.write("")

# ---------------------------------------------------------
# Status Banner
# ---------------------------------------------------------
if st.session_state.winner == "Draw":
    st.markdown(
        "<div class='status-banner' style='background:linear-gradient(90deg,#3d3520,#4a4028); "
        "color:#ffd166; border:1px solid #ffb84d55;'>🤝 It's a Draw! Nobody wins this round.</div>",
        unsafe_allow_html=True,
    )
elif st.session_state.winner == "X":
    st.markdown(
        f"<div class='status-banner win-banner' style='background:linear-gradient(90deg,#3a2e12,#4a3a14); "
        f"color:#ffd700; border:1px solid #ffd70066;'>🏆 Congratulations {player_name}! You Won! 🎉</div>",
        unsafe_allow_html=True,
    )
    st.balloons()
elif st.session_state.winner == "O":
    st.markdown(
        "<div class='status-banner' style='background:linear-gradient(90deg,#2a1f30,#331f3d); "
        "color:#c792ea; border:1px solid #c792ea55;'>🤖 Computer wins this round. Try again!</div>",
        unsafe_allow_html=True,
    )
else:
    if st.session_state.current_player == "X":
        st.markdown(
            f"<div class='status-banner' style='background:rgba(255,94,120,0.08); "
            f"color:#ff8fa3; border:2px solid #ff5e7877;'>Your Turn, {player_name}! ❌</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div class='status-banner' style='background:rgba(77,171,247,0.08); "
            "color:#7cc4ff; border:2px solid #4dabf777;'>🤖 Computer is thinking...</div>",
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------
# Game Board (3x3 grid of buttons)
# ---------------------------------------------------------
for row in range(3):
    cols = st.columns(3, gap="small")
    for col in range(3):
        index = row * 3 + col
        cell_value = st.session_state.board[index]

        if cell_value == "X":
            label = "❌"
        elif cell_value == "O":
            label = "⭕"
        else:
            label = " "

        disabled = cell_value != "" or st.session_state.game_over

        with cols[col]:
            st.button(
                label,
                key=f"cell_{index}",
                on_click=make_move,
                args=(index,),
                disabled=disabled,
                use_container_width=True,
            )

# ---------------------------------------------------------
# Play Again Button (only shows after game ends)
# ---------------------------------------------------------
if st.session_state.game_over:
    st.write("")
    if st.button("▶️ Play Again", use_container_width=True, type="primary"):
        reset_board()
        st.rerun()

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.write("")
st.markdown(
    "<p style='text-align:center; color:#9a9cc0; font-size:0.82rem;'>"
    "Built with ❤️ using Python & Streamlit</p>",
    unsafe_allow_html=True,
)