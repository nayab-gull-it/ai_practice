"""
Tic Tac Toe - Streamlit App
Author: Nayab
Features:
- 3x3 interactive board with clickable buttons
- Two player mode (X and O) with turn tracking
- Win / Draw detection with highlighted winning line
- Score tracker (persists across rounds using session_state)
- Reset board / Reset scores
- Clean, colorful, responsive UI with custom CSS
"""

import streamlit as st

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Tic Tac Toe",
    page_icon="❌",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# Custom CSS Styling
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #1f1c2c, #928dab);
    }

    h1.title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb, #1dd1a1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        color: #dcdde1;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }

    div.stButton > button {
        height: 100px;
        width: 100%;
        font-size: 2.5rem;
        font-weight: bold;
        border-radius: 16px;
        border: 2px solid #576574;
        background-color: #2f3640;
        color: #f5f6fa;
        transition: all 0.2s ease-in-out;
    }

    div.stButton > button:hover {
        background-color: #40739e;
        border-color: #00a8ff;
        transform: scale(1.03);
        color: white;
    }

    div.stButton > button:disabled {
        color: #ffffff;
        opacity: 1;
    }

    .score-box {
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 14px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.15);
    }

    .score-label {
        font-size: 0.9rem;
        color: #dcdde1;
    }

    .score-value {
        font-size: 1.8rem;
        font-weight: 800;
    }

    .status-banner {
        text-align: center;
        font-size: 1.4rem;
        font-weight: 700;
        padding: 12px;
        border-radius: 12px;
        margin: 15px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
def init_state():
    if "board" not in st.session_state:
        st.session_state.board = [""] * 9
    if "current_player" not in st.session_state:
        st.session_state.current_player = "X"
    if "winner" not in st.session_state:
        st.session_state.winner = None
    if "winning_combo" not in st.session_state:
        st.session_state.winning_combo = []
    if "scores" not in st.session_state:
        st.session_state.scores = {"X": 0, "O": 0, "Draw": 0}
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "vs_computer" not in st.session_state:
        st.session_state.vs_computer = False


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


def make_move(index):
    if st.session_state.board[index] == "" and not st.session_state.game_over:
        st.session_state.board[index] = st.session_state.current_player
        winner, combo = check_winner(st.session_state.board)

        if winner:
            st.session_state.winner = winner
            st.session_state.winning_combo = combo
            st.session_state.game_over = True
            st.session_state.scores[winner] += 1
        else:
            st.session_state.current_player = (
                "O" if st.session_state.current_player == "X" else "X"
            )

            # Simple computer move (random available cell) if vs_computer enabled
            if st.session_state.vs_computer and not st.session_state.game_over:
                computer_move()


def computer_move():
    import random
    empty_cells = [i for i, v in enumerate(st.session_state.board) if v == ""]
    if not empty_cells:
        return
    choice = random.choice(empty_cells)
    st.session_state.board[choice] = st.session_state.current_player
    winner, combo = check_winner(st.session_state.board)
    if winner:
        st.session_state.winner = winner
        st.session_state.winning_combo = combo
        st.session_state.game_over = True
        st.session_state.scores[winner] += 1
    else:
        st.session_state.current_player = (
            "O" if st.session_state.current_player == "X" else "X"
        )


def reset_board():
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.winning_combo = []
    st.session_state.game_over = False


def reset_scores():
    st.session_state.scores = {"X": 0, "O": 0, "Draw": 0}
    reset_board()


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.markdown("<h1 class='title'>Tic Tac Toe</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Made with Python & Streamlit</p>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Sidebar Options
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Game Options")
    vs_computer = st.toggle("Play vs Computer", value=st.session_state.vs_computer)
    if vs_computer != st.session_state.vs_computer:
        st.session_state.vs_computer = vs_computer
        reset_board()

    st.divider()
    if st.button("🔄 Reset Board", use_container_width=True):
        reset_board()
    if st.button("🗑️ Reset Scores", use_container_width=True):
        reset_scores()

    st.divider()
    st.caption("Rules: Get 3 in a row (horizontal, vertical or diagonal) to win.")

# ---------------------------------------------------------
# Scoreboard
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f"""<div class='score-box'>
        <div class='score-label'>Player X</div>
        <div class='score-value' style='color:#ff6b6b;'>{st.session_state.scores['X']}</div>
        </div>""",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"""<div class='score-box'>
        <div class='score-label'>Draws</div>
        <div class='score-value' style='color:#feca57;'>{st.session_state.scores['Draw']}</div>
        </div>""",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f"""<div class='score-box'>
        <div class='score-label'>Player O</div>
        <div class='score-value' style='color:#48dbfb;'>{st.session_state.scores['O']}</div>
        </div>""",
        unsafe_allow_html=True,
    )

st.write("")

# ---------------------------------------------------------
# Status Banner
# ---------------------------------------------------------
if st.session_state.winner == "Draw":
    st.markdown(
        "<div class='status-banner' style='background-color:#feca57; color:#1e272e;'>"
        "🤝 It's a Draw!</div>",
        unsafe_allow_html=True,
    )
elif st.session_state.winner:
    color = "#ff6b6b" if st.session_state.winner == "X" else "#48dbfb"
    st.markdown(
        f"<div class='status-banner' style='background-color:{color}; color:white;'>"
        f"🎉 Player {st.session_state.winner} Wins!</div>",
        unsafe_allow_html=True,
    )
else:
    turn_color = "#ff6b6b" if st.session_state.current_player == "X" else "#48dbfb"
    st.markdown(
        f"<div class='status-banner' style='background-color:rgba(255,255,255,0.08); "
        f"color:{turn_color}; border:2px solid {turn_color};'>"
        f"Turn: Player {st.session_state.current_player}</div>",
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
        is_winning_cell = index in st.session_state.winning_combo

        label = cell_value if cell_value else " "
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

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.write("")
st.markdown(
    "<p style='text-align:center; color:#dcdde1; font-size:0.8rem;'>"
    "Built with ❤️ using Python & Streamlit</p>",
    unsafe_allow_html=True,
)