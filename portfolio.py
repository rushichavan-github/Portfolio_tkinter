from tkinter import *
from tkinter import messagebox, Menu
import requests
import json
import sqlite3

pycrypto = Tk()
pycrypto.title("PAA CRYPTO PORTFOLIO")
pycrypto.iconbitmap("favicon.ico")

con = sqlite3.connect('coin.db')
cObj = con.cursor()

cObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, symbol TEXT, amount INTEGER, price REAL)")
con.commit()

# cObj.execute("INSERT INTO coin VALUES(1,'BTC',1,3300)")
# con.commit()
#
# cObj.execute("INSERT INTO coin VALUES(2,'ETH',1,1500)")
# con.commit()
#
# cObj.execute("INSERT INTO coin VALUES(3,'DOT',1,70)")
# con.commit()
#
# cObj.execute("INSERT INTO coin VALUES(4,'ATOM',1,20)")
# con.commit()
#
# cObj.execute("INSERT INTO coin VALUES(5,'XTZ',1,500)")
# con.commit()
#
# cObj.execute("INSERT INTO coin VALUES(6,'ADA',1,300)")
# con.commit()
#
# cObj.execute("INSERT INTO coin VALUES(7,'MATIC',1,1.5)")
# con.commit()
#
# cObj.execute("INSERT INTO coin VALUES(8,'USDT',1,1)")
# con.commit()
#
# cObj.execute("INSERT INTO coin VALUES(9,'XRP',1,0.5)")
# con.commit()
#
# cObj.execute("INSERT INTO coin VALUES(10,'DOGE',1,0.4)")
# con.commit()
#
# cObj.execute("INSERT INTO coin VALUES(11,'TRX',1,0.001)")
# con.commit()
#
# cObj.execute("INSERT INTO coin VALUES(12,'XLM',1,32)")
# con.commit()

def reset():
    for cell in pycrypto.winfo_children():
        cell.destroy()

    app_nav()
    app_header()
    my_portfolio()

def app_nav():
    def clear_all():
        cObj.execute("DELETE FROM coin")
        con.commit()

        reset()
        messagebox.showinfo("Portfolio Notification","All data deleted")

    def close():
        pycrypto.destroy()


    menu = Menu()
    file_item = Menu(menu)
    file_item.add_command(label="Clear Portfolio",command=clear_all)
    file_item.add_command(label="Close app", command=close)
    menu.add_cascade(label="File",menu=file_item)

    file_item = Menu(menu)
    file_item.add_command(label="How to use app")
    file_item.add_command(label="Logics behind app")
    menu.add_cascade(label="Help",menu=file_item)
    menu.add_cascade(label="Close",command=close)

    pycrypto.config(menu=menu)

def my_portfolio():
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY=7c1e9052-f15f-412d-8c6e-ea9fc493edc5")
    api = json.loads(api_request.content)

    # coins = [
    #         {
    #         "symbol":"BTC",
    #         "amount_owned": 1 ,
    #         "price_per_coin": 3200
    #         },
    #         {
    #         "symbol":"ETH",
    #         "amount_owned": 1 ,
    #         "price_per_coin": 1500
    #         },
    #         {
    #         "symbol":"DOT",
    #         "amount_owned": 1 ,
    #         "price_per_coin": 70
    #         },
    #         {
    #         "symbol":"ATOM",
    #         "amount_owned": 1 ,
    #         "price_per_coin": 20
    #         },
    #         {
    #         "symbol":"XTZ",
    #         "amount_owned": 1 ,
    #         "price_per_coin": 500
    #         },
    #         {
    #         "symbol":"ADA",
    #         "amount_owned": 1 ,
    #         "price_per_coin": 60
    #         },
    #         {
    #         "symbol":"MATIC",
    #         "amount_owned": 1 ,
    #         "price_per_coin": 1.5
    #         },
    #         {
    #         "symbol":"USDT",
    #         "amount_owned": 1 ,
    #         "price_per_coin": 99
    #         },
    #         {
    #         "symbol":"XRP",
    #         "amount_owned": 1 ,
    #         "price_per_coin": 1
    #         },
    #         {
    #         "symbol":"DOGE",
    #         "amount_owned": 1 ,
    #         "price_per_coin": 0.3
    #         },
    #         {
    #         "symbol":"TRX",
    #         "amount_owned": 2 ,
    #         "price_per_coin": 0.05
    #         },
    #         {
    #         "symbol":"XLM",
    #         "amount_owned": 1 ,
    #         "price_per_coin": 32
    #         }
    #         ]

    cObj.execute("SELECT * FROM coin")
    coins = cObj.fetchall()

    def font_color(amount):
        if amount >= 0:
            return "green"
        else:
            return "red"

    def insert_coin():
        cObj.execute("INSERT INTO coin(symbol, price, amount) VALUES(?,?,?)",(symbol_txt.get(), price_txt.get(), amount_txt.get()))
        con.commit()
        messagebox.showinfo("Portfolio Notification","Coin added successfully")
        reset()

    def update_coin():
        cObj.execute("UPDATE coin SET symbol=?, price=?, amount=? WHERE id=?", (symbol_update.get(), price_update.get(), amount_update.get(), portid_update.get()))
        con.commit()
        messagebox.showinfo("Portfolio Notification","Coin updated successfully")
        reset()

    def delete_coin():
        cObj.execute("DELETE FROM coin WHERE id=?", (portid_delete.get(),))
        con.commit()
        messagebox.showinfo("Portfolio Notification","Coin deleted successfully")
        reset()

    total_pl = 0
    coin_row = 1
    total_current_value = 0
    total_amount_paid = 0

    for i in range(0,100):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                total_paid = coin[2] *coin[3]
                current_value = coin[2] * api["data"][i]["quote"]["USD"]["price"]
                pl_per_coin = api["data"][i]["quote"]["USD"]["price"] -coin[3]
                total_pl_coin = pl_per_coin * coin[2]

                total_pl = total_pl + total_pl_coin
                total_current_value = total_current_value + current_value
                total_amount_paid += total_paid

                # print(api["data"][i]["name"] + " - " + api["data"][i]["symbol"])
                # print("Price - ${0:.6f}".format(api["data"][i]["quote"]["USD"]["price"]))
                # print("Number of coins :",coin[2])
                # print("Total Amount paid : ${0:.6f}".format(total_paid))
                # print("Current Value : ${0:.6f}".format(current_value))
                # print("P/L per Coin : ${0:.6f}".format(pl_per_coin))
                # print("Total P/L With Coin : ${0:.6f}".format(total_pl_coin))
                # print("----------------------")

                portfolio_id = Label(pycrypto, text=coin[0], bg="grey", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                portfolio_id.grid(row=coin_row, column=0, sticky=N+S+E+W)

                name = Label(pycrypto, text=api["data"][i]["name"] + " - " + api["data"][i]["symbol"], bg="grey", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                name.grid(row=coin_row, column=1, sticky=N+S+E+W)

                price = Label(pycrypto, text="${0:.6f}".format(api["data"][i]["quote"]["USD"]["price"]), bg="white", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                price.grid(row=coin_row, column=2, sticky=N+S+E+W)

                no_coins = Label(pycrypto, text=coin[2], bg="grey", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                no_coins.grid(row=coin_row, column=3, sticky=N+S+E+W)

                amount_paid = Label(pycrypto, text="${0:.6f}".format(total_paid), bg="white", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                amount_paid.grid(row=coin_row, column=4, sticky=N+S+E+W)

                current_val = Label(pycrypto, text="${0:.6f}".format(current_value), bg="grey", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                current_val.grid(row=coin_row, column=5, sticky=N+S+E+W)

                pl_coin = Label(pycrypto, text="${0:.6f}".format(pl_per_coin), bg="white", fg=font_color(float("{0:.6f}".format(pl_per_coin))), font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                pl_coin.grid(row=coin_row, column=6, sticky=N+S+E+W)

                totalpl = Label(pycrypto, text="${0:.6f}".format(total_pl_coin), bg="grey", fg=font_color(float("{0:.6f}".format(total_pl_coin))), font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                totalpl.grid(row=coin_row, column=7, sticky=N+S+E+W)

                coin_row += 1

        #insert_coin
    symbol_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_txt.grid(row=coin_row+1, column=1)

    price_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    price_txt.grid(row=coin_row+1, column=2)

    amount_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_txt.grid(row=coin_row+1, column=3)

    add_coin= Button(pycrypto, text="Add Coin", bg="#142E54", fg="white",command=insert_coin, font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    add_coin.grid(row=coin_row+1, column=4, sticky=N+S+E+W)

        #update_coin
    portid_update = Entry(pycrypto, borderwidth=2, relief="groove")
    portid_update.grid(row=coin_row+2, column=0)

    symbol_update = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_update.grid(row=coin_row+2, column=1)

    price_update = Entry(pycrypto, borderwidth=2, relief="groove")
    price_update.grid(row=coin_row+2, column=2)

    amount_update = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_update.grid(row=coin_row+2, column=3)

    update_coin= Button(pycrypto, text="Update Coin", bg="#142E54", fg="white",command=update_coin, font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    update_coin.grid(row=coin_row+2, column=4, sticky=N+S+E+W)

    #delete_coin
    portid_delete = Entry(pycrypto, borderwidth=2, relief="groove")
    portid_delete.grid(row=coin_row+3, column=0)

    delete_coin_txt = Button(pycrypto, text="Delete Coin", bg="#142E54", fg="white", command=delete_coin ,font="Lato 12 bold", borderwidth=2, relief="groove", padx="2", pady="2")
    delete_coin_txt.grid(row=coin_row+3, column=4, sticky=N+S+E+W)

    totalap= Label(pycrypto, text="${0:.6f}".format(total_amount_paid), bg="grey", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    totalap.grid(row=coin_row, column=4, sticky=N+S+E+W)

    totalcv= Label(pycrypto, text="${0:.6f}".format(total_current_value), bg="grey", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    totalcv.grid(row=coin_row, column=5, sticky=N+S+E+W)

    totalpl= Label(pycrypto, text="${0:.6f}".format(total_pl), bg="grey", fg=font_color(float("{0:.6f}".format(total_pl))), font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    totalpl.grid(row=coin_row, column=7, sticky=N+S+E+W)

    api = ""

    refresh= Button(pycrypto, text="Refresh", bg="#142E54", fg="white",command=reset, font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    refresh.grid(row=coin_row+1, column=7, sticky=N+S+E+W)

def app_header():
    portfolio_id= Label(pycrypto, text="Portfolio ID", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    portfolio_id.grid(row=0, column=0, sticky=N+S+E+W)

    name = Label(pycrypto, text="Coin Name", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    name.grid(row=0, column=1, sticky=N+S+E+W)

    price = Label(pycrypto, text="Price", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    price.grid(row=0, column=2, sticky=N+S+E+W)

    no_coins = Label(pycrypto, text="Coins Owned", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    no_coins.grid(row=0, column=3, sticky=N+S+E+W)

    amount_paid = Label(pycrypto, text="Total Amount Paid", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    amount_paid.grid(row=0, column=4, sticky=N+S+E+W)

    current_val = Label(pycrypto, text="Current Value", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    current_val.grid(row=0, column=5, sticky=N+S+E+W)

    pl_coin = Label(pycrypto, text="P/L per Coin", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    pl_coin.grid(row=0, column=6, sticky=N+S+E+W)

    totalpl = Label(pycrypto, text="Total P/L With Coin", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    totalpl.grid(row=0, column=7, sticky=N+S+E+W)


app_nav()
app_header()
my_portfolio()

pycrypto.mainloop()

cObj.close()
con.close()
