from flask import Flask, render_template, redirect
import sqlite3
import utils.driver as d

app = Flask('__name__')
balance_order = True
payment_order = True
days_order = True


@app.route('/')
def home():
    """Returns home page"""
    data = sqlite3.connect('data.db')
    cursor = data.cursor()
    cursor2 = data.cursor()
    balance_total = 0
    minpay_total = 0
    for t in cursor.execute('SELECT balance FROM masterdata'):
        if t[0] is None:
            pass
        else:
            balance_total += t[0]
    for t in cursor.execute('SELECT min_payment FROM masterdata'):
        if t[0] is None:
            pass
        else:
            minpay_total += t[0]
    cursor.execute('UPDATE masterdata SET balance = ?, min_payment = ? WHERE id = ?',
                   (round(balance_total, 2), round(minpay_total, 2), 15))
    total = cursor2.execute('SELECT * FROM masterdata WHERE id = 15')
    exe = cursor.execute('SELECT * FROM masterdata EXCEPT SELECT * FROM masterdata WHERE id = 15 ORDER BY balance')
    return render_template('dash.html', data=exe, total=total)


@app.route('/data')
def grab_all_data():
    """Function to grab all data by calling chrome driver from utils.driver.py"""
    d.express()
    d.wells_fargo()
    d.macys()
    d.best_buy()
    d.fire_stone()
    d.book_store()
    d.clothes_store()
    d.paypal()
    d.my_cc()
    d.american_airlines()
    return redirect('/')


@app.route('/test/<int:num>')
def testing(num):
    """Calls individual functions to pull data"""
    if num == 1:
        d.clothes_store()
    elif num == 2:
        d.best_buy()
    elif num == 3:
        d.my_cc()
    elif num == 4:
        d.american_airlines()
    elif num == 5:
        d.chase()
    elif num == 6:
        d.fire_stone()
    elif num == 7:
        d.book_store()
    elif num == 8:
        d.macys()
    elif num == 10:
        d.paypal()
    elif num == 11:
        d.express()
    elif num == 12:
        d.wells_fargo()
    elif num == 13:
        pass
    elif num == 14:
        d.grocery_store()
    elif num == 15:
        pass
    else:
        pass
    return redirect('/')


@app.route('/orderbalance')
def order_balance():
    """Used to sort balance"""
    global balance_order
    data = sqlite3.connect('data.db')
    cursor = data.cursor()
    cursor2 = data.cursor()
    balance_total = 0
    minpay_total = 0
    for t in cursor.execute('SELECT balance FROM masterdata'):
        if t[0] is None:
            pass
        else:
            balance_total += t[0]
    for t in cursor.execute('SELECT min_payment FROM masterdata'):
        if t[0] is None:
            pass
        else:
            minpay_total += t[0]
    cursor.execute('UPDATE masterdata SET balance = ?, min_payment = ? WHERE id = ?',
                   (round(balance_total, 2), round(minpay_total, 2), 15))

    if balance_order is True:
        exe = cursor.execute('SELECT * FROM masterdata EXCEPT SELECT * FROM masterdata WHERE id = 15 ORDER BY balance '
                             'DESC')
        balance_order = False
    else:
        exe = cursor.execute('SELECT * FROM masterdata EXCEPT SELECT * FROM masterdata WHERE id = 15 ORDER BY balance')
        balance_order = True

    total = cursor2.execute('SELECT * FROM masterdata WHERE id = 15')
    return render_template('dash.html', data=exe, total=total)


@app.route('/orderpayment')
def order_payment():
    """Used to sort min payment"""
    global payment_order
    data = sqlite3.connect('data.db')
    cursor = data.cursor()
    cursor2 = data.cursor()
    balance_total = 0
    minpay_total = 0
    for t in cursor.execute('SELECT balance FROM masterdata'):
        if t[0] is None:
            pass
        else:
            balance_total += t[0]
    for t in cursor.execute('SELECT min_payment FROM masterdata'):
        if t[0] is None:
            pass
        else:
            minpay_total += t[0]
    cursor.execute('UPDATE masterdata SET balance = ?, min_payment = ? WHERE id = ?',
                   (round(balance_total, 2), round(minpay_total, 2), 15))

    if payment_order is True:
        exe = cursor.execute('SELECT * FROM masterdata EXCEPT SELECT * FROM masterdata WHERE id = 15 ORDER BY balance '
                             'DESC')
        payment_order = False
    else:
        exe = cursor.execute('SELECT * FROM masterdata EXCEPT SELECT * FROM masterdata WHERE id = 15 ORDER BY balance')
        payment_order = True
    total = cursor2.execute('SELECT * FROM masterdata WHERE id = 15')
    return render_template('dash.html', data=exe, total=total)


@app.route('/orderdays')
def order_days():
    """Used to sort days"""
    global days_order
    data = sqlite3.connect('data.db')
    cursor = data.cursor()
    cursor2 = data.cursor()
    balance_total = 0
    minpay_total = 0
    for t in cursor.execute('SELECT balance FROM masterdata'):
        if t[0] is None:
            pass
        else:
            balance_total += t[0]
    for t in cursor.execute('SELECT min_payment FROM masterdata'):
        if t[0] is None:
            pass
        else:
            minpay_total += t[0]
    cursor.execute('UPDATE masterdata SET balance = ?, min_payment = ? WHERE id = ?',
                   (round(balance_total, 2), round(minpay_total, 2), 15))

    if days_order is True:
        exe = cursor.execute('SELECT * FROM masterdata EXCEPT SELECT * FROM masterdata WHERE id = 15 ORDER BY days DESC')
        days_order = False
    else:
        exe = cursor.execute('SELECT * FROM masterdata EXCEPT SELECT * FROM masterdata WHERE id = 15 ORDER BY days')
        days_order = True
    total = cursor2.execute('SELECT * FROM masterdata WHERE id = 15')
    return render_template('dash.html', data=exe, total=total)


if __name__ == '__main__':
    app.run()
