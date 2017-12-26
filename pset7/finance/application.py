from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():

    # get user's portfolio
    portfolio = db.execute("SELECT symbol, quantity FROM portfolio WHERE user_id = :user_id", user_id=session["user_id"])

    # get data on stocks
    stocks = []
    value = 0
    for item in portfolio:
        symbol = item["symbol"]
        stock = lookup(symbol)
        name = stock["name"]
        shares = item["quantity"]
        price = stock["price"]

        stock_info = {}
        stock_info["symbol"] = symbol
        stock_info["name"] = name
        stock_info["shares"] = shares
        stock_info["price"] = usd(price)
        stock_info["total"] = usd(price * shares)
        # add data to stocks
        stocks.append(stock_info)
        # add total to running total
        value += (price * shares)

    # get user's cash
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    cash = float(cash[0]["cash"])

    # get total
    value += cash

    # render portfolio
    return render_template("index.html", total=usd(value), stocks=stocks, cash=usd(cash))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""

    # if user reached route via POST (as by submitting a form via post)
    if request.method == "POST":

        # ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")

        # ensure symbol is valid
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("invalid symbol")

        # ensure proper number of shares
        if not request.form.get("shares"):
            return apology("must provide shares")

        # ensure shares is valid
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("invalid shares")

        # check how much cash user has
        money = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        money = float(money[0]["cash"])

        # check have enough money
        if not money or money < stock["price"] * shares:
            return apology("not enough money")

        # add stock to user's portfolio
        # check if user already owns that stock
        result = db.execute("SELECT quantity FROM portfolio WHERE user_id = :user_id AND symbol = :symbol",
                             user_id=session["user_id"],
                             symbol=stock["symbol"])

        # if result doesn't exist, insert new stock into portfolio
        if not result:
            db.execute("INSERT INTO portfolio (user_id, symbol, quantity) VALUES (:user_id, :symbol, :quantity)",
                        user_id=session["user_id"],
                        symbol=stock["symbol"],
                        quantity=shares)

        # otherwise, update quantity
        else:
            quantity=result[0]["quantity"]
            db.execute("UPDATE portfolio SET quantity = :quantity WHERE user_id = :user_id AND symbol = :symbol",
                        quantity=quantity+shares,
                        user_id=session["user_id"],
                        symbol=stock["symbol"])

        # add transaction to history
        db.execute("INSERT INTO history (user_id, symbol, quantity, price) VALUES (:user_id, :symbol, :quantity, :price)",
                    user_id=session["user_id"],
                    symbol=stock["symbol"],
                    quantity=shares,
                    price=stock["price"])

        # update user's cash
        total = stock["price"] * shares
        db.execute("UPDATE users SET cash = :cash WHERE id = :id",
                    cash=money-total,
                    id=session["user_id"])

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""

    # get user's transaction history
    transactions = db.execute("SELECT * FROM history WHERE user_id = :user_id", user_id=session["user_id"])
    return render_template("history.html", transactions=transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # if user reached route via POST (as by submitting a form via post)
    if request.method == "POST":

        # ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")

        # ensure symbol is valid
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("invalid symbol")

        # display stock quote
        return render_template("quoted.html", stock=stock)

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # if user reached route via POST (as by submitting a form via post)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password")

        # ensure confirm password was submitted
        if not request.form.get("confirmpassword"):
            return apology("must confirm password")

        # ensure passwords match
        if request.form.get("password") != request.form.get("confirmpassword"):
            return apology("passwords must match")

        # add new user to database
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                             username=request.form.get("username"),
                             hash=pwd_context.hash(request.form.get("password")))

        # remember which user has logged in
        session["user_id"] = result

        # ensure added correctly
        if not result:
            return apology("username already exists")

        # remember which user has logged in
        session["user_id"] = result

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""

     # if user reached route via POST (as by submitting a form via post)
    if request.method == "POST":

        # ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")

        # ensure symbol is valid
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("invalid symbol")

        # ensure proper number of shares
        if not request.form.get("shares"):
            return apology("must provide shares")

        # ensure shares is valid
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("invalid shares")

        # ensure number of shares is not more than number available to sell
        result = db.execute("SELECT quantity FROM portfolio WHERE user_id = :user_id AND symbol = :symbol",
                             user_id=session["user_id"],
                             symbol=stock["symbol"])
        quantity=result[0]["quantity"]
        if shares > quantity:
            return apology("not enough shares")

        # update user portfolio
        # delete from portfolio if quantiy is now 0
        if quantity - shares == 0:
            db.execute("DELETE FROM portfolio WHERE user_id = :user_id AND symbol = :symbol",
                        user_id=session["user_id"],
                        symbol=stock["symbol"])

        # otherwise, update quantity
        else:
            db.execute("UPDATE portfolio SET quantity = :quantity WHERE user_id = :user_id AND symbol = :symbol",
                        quantity=quantity-shares,
                        user_id=session["user_id"],
                        symbol=stock["symbol"])

        # add transaction to history
        db.execute("INSERT INTO history (user_id, symbol, quantity, price) VALUES (:user_id, :symbol, :quantity, :price)",
                    user_id=session["user_id"],
                    symbol=stock["symbol"],
                    quantity=-shares,
                    price=stock["price"])

        # update user's cash
        total = stock["price"] * shares
        db.execute("UPDATE users SET cash = cash + :total WHERE id = :id",
                    total=total,
                    id=session["user_id"])

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        # select symbols
        stocks = db.execute("SELECT symbol FROM portfolio WHERE user_id = :user_id", user_id=session["user_id"])
        return render_template("sell.html", stocks=stocks)

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """Change user password."""

    # if user reached route via POST (as by submitting a form via post)
    if request.method == "POST":

        # ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide current password")

        # ensure new password was submitted
        if not request.form.get("newpassword"):
            return apology("must provide new password")

        # ensure confirm password was submitted
        if not request.form.get("confirmpassword"):
            return apology("must confirm new password")

        # ensure passwords match
        if request.form.get("newpassword") != request.form.get("confirmpassword"):
            return apology("passwords must match")

        # ensure current password is correct
        rows = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("old password incorrect")

        # update user's password
        result = db.execute("UPDATE users SET hash = :hash WHERE id = :id",
                             hash=pwd_context.hash(request.form.get("newpassword")),
                             id=session["user_id"])

        # ensure added correctly
        if not result:
            return apology("password could not be changed")

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("account.html")
