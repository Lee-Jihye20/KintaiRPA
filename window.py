import os
from datetime import datetime
import threading
import tkinter as tk
from tkinter import ttk
import config
import kintai
import security
from ttkbootstrap import Button, Label, Checkbutton, Combobox, DateEntry, Menu, Menubutton, Notebook, Frame, Window, Style, dialogs
import json

# メインウィンドウの設定
window = tk.Tk()
window.title('KingOfTimeRPA')
window.geometry("250x400+600+300")
window.resizable(False, False)

# グローバル変数
selected_list = tk.StringVar()
selected_month = tk.StringVar()
selected_year = tk.StringVar()
current_date = datetime.now()
isSaveId = tk.IntVar()
isSavePw = tk.IntVar()

# ディレクトリの初期化
if not os.path.isdir(os.path.abspath('./SavedData')):
    os.mkdir('./SavedData')
if not os.path.isdir(os.path.abspath('./key')):
    os.mkdir('./key')

def quit_me():
    window.quit()
    window.destroy()

def date_submit(id, password, y, m, name, idcheck, pwcheck):
    dataname = "all"
    
    # ID保存の処理
    if idcheck == 1:
        security.encrypt_data(id.encode('utf-8'), 'id')
    elif os.path.isfile('id_encrypted.txt'):
        security.remove_data('id_encrypted.txt')
    
    # パスワード保存の処理
    if pwcheck:
        security.encrypt_data(password.encode('utf-8'), 'pwd')
    elif os.path.isfile('pwd_encrypted.txt'):
        security.remove_data('pwd_encrypted.txt')
    
    # データ種類の設定
    if name == 1:
        dataname = "timecard"
    elif name == 2:
        dataname = "monthly_xls"
    elif name == 3:
        dataname = "monthly_csv"
    elif name == 4:
        dataname = "schedule"
    
    # RPAの実行
    ktstart = threading.Thread(target=kintai.startrpa, args=(id, password, y+2020, m+1, dataname))
    ktstart.start()
    quit_me()
user_frame = ttk.LabelFrame(window, text="ユーザー情報")
user_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
export_frame = ttk.LabelFrame(window, text="出力設定")
export_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
# UI要素の作成と配置
# ユーザーID関連
userid_field = ttk.Entry(user_frame, width=15)
if security.hasFile(os.path.abspath("./SavedData/id_encrypted.txt")):
    isSaveId.set(1)
    data = security.decrypt_data(os.path.abspath('./SavedData/id_encrypted.txt'))
    userid_field.insert(0, data)

# パスワード関連
password_field = ttk.Entry(user_frame, show="*", width=15)
if security.hasFile(os.path.abspath("./SavedData/pwd_encrypted.txt")):
    isSavePw.set(1)
    data = security.decrypt_data(os.path.abspath('./SavedData/pwd_encrypted.txt'))
    password_field.insert(0, data)

# UI要素の配置




# 日付選択
date_label = ttk.Label(export_frame, text="出力する期間:")
date_label.grid(sticky=tk.W,column=0, row=2)

date_select_year = ttk.Combobox(export_frame, values=config.year_list, state='readonly',
                               textvariable=selected_year, width=7)
date_select_year.set(f"{current_date.year}年")
date_select_year.grid(sticky=tk.W, padx=(10,0), column=1, row=2)

date_select_month = ttk.Combobox(export_frame, values=config.month_list, state='readonly',
                                textvariable=selected_month, width=5)
date_select_month.current(current_date.month - 1)
date_select_month.grid(sticky=tk.W,padx=(80,0), column=1, row=2)

# 送信ボタン
ttk.Button(window, text="完了", width=10,
           command=lambda: date_submit(
               userid_field.get(), password_field.get(),
               date_select_year.current(), date_select_month.current(),
               export_select.current(), isSaveId.get(), isSavePw.get()
           )).grid(padx=(0,0), column=0, row=15, columnspan=2)

# UI要素の追加
def save_new_user():
    """新しいユーザーを保存"""
    alias = alias_field.get().strip()
    if not alias:
        dialogs.messagebox.showerror("エラー", "エイリアスを入力してください")
        return
    
    userid = userid_field.get()
    password = password_field.get()
    security.encrypt_user_data(userid, password, alias)
    update_user_list()
def delete_user():
    """ユーザーを削除"""
    selected = user_select.get()
    if not selected:
        return
    security.delete_user_data(selected)
    update_user_list()
def load_user(event=None):
    """選択されたユーザー情報を読み込む"""
    selected = user_select.get()
    if not selected:
        return
    
    user_data = security.get_user_data(selected)
    if user_data:
        userid_field.delete(0, tk.END)
        userid_field.insert(0, user_data['userid'])
        password_field.delete(0, tk.END)
        password_field.insert(0, user_data['password'])

def update_user_list():
    """ユーザーリストを更新"""
    saved_users = security.get_saved_users()
    user_select['values'] = saved_users
    if saved_users:
        user_select.set(saved_users[0])

# UI要素の配置を修正

# ユーザー選択
ttk.Label(user_frame, text="保存済みユーザー:").grid(row=0, column=0, padx=5, pady=5)
user_select = ttk.Combobox(user_frame, state='readonly', width=15)
user_select.grid(row=0, column=1, padx=5, pady=5)
user_select.bind('<<ComboboxSelected>>', load_user)

# 新規ユーザー追加
ttk.Label(user_frame, text="保存名:").grid(row=1, column=0, padx=5, pady=5)
alias_field = ttk.Entry(user_frame, width=15)
alias_field.grid(row=1, column=1, padx=5, pady=5)

# ID/パスワード入力欄
ttk.Label(user_frame, text="ユーザーID:").grid(row=2, column=0, padx=5, pady=5)
userid_field.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(user_frame, text="パスワード:").grid(row=3, column=0, padx=5, pady=5)
password_field.grid(row=3, column=1, padx=5, pady=5)

# 保存ボタン
ttk.Button(user_frame, text="ユーザーを保存", command=save_new_user).grid(
    row=5, column=0, pady=10)
ttk.Button(user_frame, text="ユーザーを削除", command=delete_user).grid(
    row=5, column=1, pady=10)

# 出力設定フレーム


export_desc = ttk.Label(export_frame, text="出力ファイル:")
export_desc.grid(row=0, column=0, padx=5, pady=5)

export_select = ttk.Combobox(export_frame, values=config.select_list, state='readonly',
                            textvariable=selected_list, width=15)
export_select.current(0)
export_select.grid(row=0, column=1, padx=5, pady=5)

# 初期化時にユーザーリストを更新
update_user_list()

window.mainloop()