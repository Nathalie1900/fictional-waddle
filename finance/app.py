import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    # Select data (current user cash amount)
    user_id = session["user_id"]
    session_symbols = []
    user_cash = db.execute("SELECT cash FROM users WHERE id=?", user_id)
    user_cash = user_cash[0]
    user_cash = user_cash["cash"]
    total_cash_stocks = 0
    # Select data from database (for user, stocks, number of shares owned, current price and total value)
    symbols = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id=?", user_id)
    for row in symbols:
        quote_data = lookup(row["symbol"])
        price = quote_data["price"]
        symbol = row["symbol"]
        type = "Buy"
        shares_bought = db.execute("SELECT SUM(shares) AS total FROM transactions WHERE user_id=? AND type=?", user_id, type)
        if not shares_bought[0]["total"]:
            shares_bought = 0
        else:
            shares_bought = shares_bought[0]["total"]
        type = "Sell"
        shares_sold = db.execute("SELECT SUM(shares) AS total FROM transactions WHERE user_id=? AND type=?", user_id, type)
        if not shares_sold[0]["total"]:
            shares_sold = 0
        else:
            shares_sold = shares_sold[0]["total"]
        shares = shares_bought-shares_sold
        total_value = price * shares
        dictionary = {"symbol": symbol, "shares": shares, "price": price, "total": total_value}
        session_symbols.append(dictionary)
        total_cash_stocks += total_value
    return render_template("index.html", total_cash_stocks=total_cash_stocks, user_cash=user_cash, session_symbols=session_symbols)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
     # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Access form data
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)
        quote_data = lookup(symbol)
        if not quote_data:
            return apology("symbol does not exist", 400)
        shares = request.form.get("shares")
        if not shares:
            return apology("must provide number of shares", 400)
        try:
            shares = int(shares)
        except ValueError:
            return apology("shares must be numeric", 400)
        if shares < 1:
            return apology("shares must be a positive integer", 400)
        # Check symbol price
        quote_data = lookup(symbol)
        symbol = quote_data["symbol"]
        price = quote_data["price"]
        user_id = session["user_id"]
        # Check how much cash the user has
        user_cash = db.execute("SELECT cash FROM users WHERE id=?", user_id)
        user_cash = user_cash[0]
        user_cash = user_cash["cash"]
        amount = shares * price
        if amount > user_cash:
            return apology("not enough cash", 403)
        else:
            # Add new data to existing database
            datetime_var = datetime.now()
            date = datetime_var.date()
            time = datetime_var.time()
            type = "Buy"
            db.execute("INSERT INTO transactions (user_id, symbol, shares, amount, date, time, type) VALUES(?, ?, ?, ?, ?, ?, ?)", user_id, symbol, shares, amount, date, time, type)
            new_cash = user_cash - amount
            db.execute("UPDATE users SET cash=? WHERE id=?", new_cash, user_id)
            return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    history = db.execute("SELECT * FROM transactions WHERE user_id=?", user_id)
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    # User reached route via POST (as by submitting a form via POST)
    user_id = session["user_id"]
    if request.method == "POST":
        # Ensure symbol was submitted
        new_password = request.form.get("new_password")
        new_strhash = generate_password_hash(new_password, method='scrypt', salt_length=16)
        db.execute("UPDATE users SET hash=? WHERE id=?", new_strhash, user_id)
        return redirect("/")
     # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("settings.html")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was submitted
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must enter a symbol", 400)
        quote_data = lookup(symbol)
        if not quote_data:
            return apology("symbol does not exist", 400)
        print(repr(quote_data["price"]))
        return render_template("quoted.html", quote_data=quote_data)
     # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 400)
        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            return apology("must provide password", 400)
        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("must confirm password", 400)
        if confirmation != password:
            return apology("passwords don't match", 400)
        strhash = generate_password_hash(password, method='scrypt', salt_length=16)
        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, strhash)
        except ValueError:
            return apology("username already exists", 400)
        return redirect("/")
     # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user_id = session["user_id"]
    bought_symbols = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id=?", user_id)
    session_symbols_x = []
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Access form data
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)
        for row in bought_symbols:
            session_symbols_x.append(row["symbol"])
        if symbol not in session_symbols_x:
            return apology("you haven't bought any shares of that!", 400)
        shares = request.form.get("shares")
        if not shares:
            return apology("must provide number of shares", 400)
        try:
            shares = int(shares)
        except ValueError:
            return apology("shares must be numeric", 400)
        type = "Buy"
        shares_bought = db.execute("SELECT SUM(shares) AS total FROM transactions WHERE user_id=? AND type=?", user_id, type)
        if not shares_bought[0]["total"]:
            shares_bought = 0
        else:
            shares_bought = shares_bought[0]["total"]
        type = "Sell"
        shares_sold = db.execute("SELECT SUM(shares) AS total FROM transactions WHERE user_id=? AND type=?", user_id, type)
        if not shares_sold[0]["total"]:
            shares_sold = 0
        else:
            shares_sold = shares_sold[0]["total"]
        shares_owned = shares_bought-shares_sold
        quote_data = lookup(symbol)
        price = quote_data["price"]
        user_cash = db.execute("SELECT cash FROM users WHERE id=?", user_id)
        user_cash = user_cash[0]
        user_cash = user_cash["cash"]
        datetime_var = datetime.now()
        date = datetime_var.date()
        time = datetime_var.time()
        type = "Sell"
        if shares > shares_owned:
            return apology("you don't have enough shares!", 400)
        elif shares == shares_owned:
            amount = price*shares
            new_cash = user_cash + amount
            shares = 0 - shares
            db.execute("INSERT INTO transactions (user_id, symbol, shares, amount, date, time, type) VALUES(?, ?, ?, ?, ?, ?, ?)", user_id, symbol, shares, amount, date, time, type)
            db.execute("UPDATE users SET cash=? WHERE id=?", new_cash, user_id)
            return redirect("/")
        else:
            amount = price*shares
            new_cash = user_cash + amount
            new_shares = shares_owned - shares
            db.execute("INSERT INTO transactions (user_id, symbol, shares, amount, date, time, type) VALUES(?, ?, ?, ?, ?, ?, ?)", user_id, symbol, shares, amount, date, time, type)
            db.execute("UPDATE users SET cash=? WHERE id=?", new_cash, user_id)
            return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html", bought_symbols=bought_symbols)
