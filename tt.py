import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, Defaults
from telegram.constants import ParseMode

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Board representation
board = [[' ' for _ in range(3)] for _ in range(3)]
current_player = 'X'


def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    global board, current_player
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    update.message.reply_text('Welcome to Tic Tac Toe!\nPlayer X goes first.\n' + render_board(), reply_markup=build_keyboard())


def render_board() -> str:
    return '\n'.join([' | '.join(row) for row in board])


def build_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(InlineKeyboardButton(board[i][j], callback_data=f'{i}-{j}'))
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)


def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global current_player
    query = update.callback_query
    query.answer()
    i, j = map(int, query.data.split('-'))

    if board[i][j] == ' ':
        board[i][j] = current_player
        if check_winner():
            query.edit_message_text(text=f'Player {current_player} wins!\n' + render_board())
            return
        if check_draw():
            query.edit_message_text(text='Draw!\n' + render_board())
            return
        current_player = 'O' if current_player == 'X' else 'X'
    query.edit_message_text(text=render_board(), reply_markup=build_keyboard())


def check_winner() -> bool:
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return True
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return True
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return True
    return False


def check_draw() -> bool:
    for row in board:
        if ' ' in row:
            return False
    return True


def main() -> None:
    """Start the bot."""
    defaults = Defaults(parse_mode=ParseMode.MARKDOWN_V2)
    app = ApplicationBuilder().token("7602939669:AAFFC5CWyV8ODKr1bs2p0XmyoTMRncomPRQ").defaults(defaults).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()


if __name__ == '__main__':
    main()
