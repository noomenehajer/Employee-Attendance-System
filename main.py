############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import cv2, os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

############################################# DESIGN CONSTANTS ################################################

BG_MAIN        = "#F0F4F8"
BG_CARD        = "#FFFFFF"
BG_SIDEBAR     = "#1A2535"
BG_HEADER      = "#FFFFFF"
ACCENT_PRIMARY = "#3B82F6"
ACCENT_HOVER   = "#2563EB"
ACCENT_SUCCESS = "#10B981"
ACCENT_DANGER  = "#EF4444"
ACCENT_WARNING = "#F59E0B"

TEXT_DARK      = "#0F172A"
TEXT_MEDIUM    = "#475569"
TEXT_LIGHT     = "#94A3B8"
TEXT_WHITE     = "#FFFFFF"

BORDER_COLOR   = "#E2E8F0"

FONT_TITLE     = ('Segoe UI', 22, 'bold')
FONT_HEADING   = ('Segoe UI', 13, 'bold')
FONT_SUBHEAD   = ('Segoe UI', 11, 'bold')
FONT_BODY      = ('Segoe UI', 10)
FONT_SMALL     = ('Segoe UI', 9)
FONT_BTN       = ('Segoe UI', 10, 'bold')
FONT_BTN_LG    = ('Segoe UI', 11, 'bold')
FONT_CLOCK     = ('Segoe UI', 28, 'bold')
FONT_DATE      = ('Segoe UI', 11)

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock_lbl.config(text=time_string)
    clock_lbl.after(200, tick)

def contact():
    mess._show(title='Contact', message="Veuillez me contacter sur : 'hajer.noomene@gmail.com'")

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if not exists:
        mess._show(title='Fichiers manquants', message='Contactez-moi pour obtenir de l aide')
        window.destroy()

def set_status(msg, color=TEXT_MEDIUM):
    status_lbl.configure(text=msg, fg=color)

def clear():
    txt_id.delete(0, 'end')
    set_status("Pret - Remplissez le formulaire pour inscrire un employe.", TEXT_MEDIUM)

def clear2():
    txt_name.delete(0, 'end')
    set_status("Pret - Remplissez le formulaire pour inscrire un employe.", TEXT_MEDIUM)

def update_total_count():
    res = 0
    exists = os.path.isfile("EmployeeDetails\\EmployeeDetails.csv")
    if exists:
        with open("EmployeeDetails\\EmployeeDetails.csv", 'r') as f:
            reader = csv.reader(f)
            for l in reader:
                res += 1
        res = max(0, (res // 2) - 1)
    count_lbl.configure(text=str(res))

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("EmployeeDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("EmployeeDetails\\EmployeeDetails.csv")
    if exists:
        with open("EmployeeDetails\\EmployeeDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial += 1
        serial = serial // 2
        csvFile1.close()
    else:
        with open("EmployeeDetails\\EmployeeDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = txt_id.get()
    name = txt_name.get()
    if name.isalpha() or (' ' in name):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (59, 130, 246), 2)
                sampleNum += 1
                cv2.imwrite("TrainingImage\\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                cv2.imshow('Capture - Appuyez sur Q pour arreter', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        row = [serial, '', Id, '', name]
        with open('EmployeeDetails\\EmployeeDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        set_status("✔  Images capturees pour l ID : " + Id + "  (" + name + ")", ACCENT_SUCCESS)
        update_total_count()
    else:
        set_status("⚠  Veuillez saisir un nom valide (lettres uniquement).", ACCENT_DANGER)

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='Aucune inscription', message='Veuillez d abord inscrire un employe !')
        return
    recognizer.save("TrainingImageLabel\\Trainner.yml")
    set_status("✔  Profil enregistre avec succes !", ACCENT_SUCCESS)
    update_total_count()

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

def update_treeview(employee_id, employee_name, date, timestamp):
    tag = 'even' if len(tv.get_children()) % 2 == 0 else 'odd'
    tv.insert('', 'end', text=str(employee_id), values=(employee_name, date, timestamp), tags=(tag,))

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("EmployeeDetails/")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel\\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\\Trainner.yml")
    else:
        mess._show(title='Erreur', message='Aucune donnee d entrainement. Enregistrez d abord un profil.')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Image', 'Name', 'Date', 'Time']
    exists1 = os.path.isfile("EmployeeDetails\\EmployeeDetails.csv")
    if not exists1:
        mess._show(title='Erreur', message='Details employes introuvables !')
        cam.release()
        return
    df = pd.read_csv("EmployeeDetails\\EmployeeDetails.csv")
    attended_today = set()
    set_status("Camera active - Pointage en cours...", ACCENT_PRIMARY)
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (59, 130, 246), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if conf < 50:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H-%M-%S')
                employee_id = df.loc[df['SERIAL NO.'] == serial, 'ID'].values[0]
                employee_name = df.loc[df['SERIAL NO.'] == serial, 'NAME'].values[0]
                if employee_id not in attended_today:
                    img_name = "Attendance/" + str(employee_id) + "_" + date + "_" + timeStamp + ".jpg"
                    cv2.imwrite(img_name, im)
                    attendance = [str(employee_id), img_name, str(employee_name), str(date), str(timeStamp)]
                    with open("Attendance/Attendance_" + date + ".csv", 'a+') as csvFile1:
                        writer = csv.writer(csvFile1)
                        if os.stat("Attendance/Attendance_" + date + ".csv").st_size == 0:
                            writer.writerow(col_names)
                        writer.writerow(attendance)
                    attended_today.add(employee_id)
                    update_treeview(employee_id, employee_name, date, timeStamp)
                cv2.putText(im, str(employee_name), (x, y - 10), font, 0.8, (59, 130, 246), 2)
                cv2.rectangle(im, (x, y + h - 25), (x + w, y + h), (59, 130, 246), -1)
                cv2.putText(im, str(round(100 - conf)) + '% conf', (x + 4, y + h - 8), font, 0.5, (255, 255, 255), 1)
            else:
                cv2.putText(im, 'Inconnu', (x, y - 10), font, 0.8, (239, 68, 68), 2)
        cv2.imshow('Pointage - Appuyez sur Q pour arreter', im)
        if cv2.waitKey(1) == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
    set_status("✔  Session de pointage terminee.", ACCENT_SUCCESS)

############################################# DATA HELPERS #############################################

ts = time.time()
date_now = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date_now.split("-")

mont = {
    '01': 'Janvier',  '02': 'Fevrier', '03': 'Mars',
    '04': 'Avril',    '05': 'Mai',     '06': 'Juin',
    '07': 'Juillet',  '08': 'Aout',    '09': 'Septembre',
    '10': 'Octobre',  '11': 'Novembre','12': 'Decembre'
}

############################################# GUI SETUP ##############################################

window = tk.Tk()
window.geometry("1280x760")
window.resizable(True, True)
window.title("Systeme de Pointage")
window.configure(background=BG_MAIN)

# ─── TTK STYLES ──────────────────────────────────────────────────────────────
style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview",
    background=BG_CARD, foreground=TEXT_DARK, fieldbackground=BG_CARD,
    rowheight=32, font=FONT_BODY, borderwidth=0, relief='flat'
)
style.configure("Treeview.Heading",
    background=BG_SIDEBAR, foreground=TEXT_WHITE,
    font=FONT_SUBHEAD, relief='flat', borderwidth=0, padding=(8, 10)
)
style.map("Treeview",
    background=[('selected', ACCENT_PRIMARY)],
    foreground=[('selected', TEXT_WHITE)]
)
style.map("Treeview.Heading",
    background=[('active', ACCENT_PRIMARY)]
)
style.configure("Vertical.TScrollbar",
    background=BORDER_COLOR, troughcolor=BG_CARD,
    borderwidth=0, arrowcolor=TEXT_LIGHT, relief='flat'
)

# ─── HEADER ──────────────────────────────────────────────────────────────────
tk.Frame(window, bg=ACCENT_PRIMARY, height=4).pack(fill='x')

header = tk.Frame(window, bg=BG_HEADER, height=76)
header.pack(fill='x')
header.pack_propagate(False)

logo_frame = tk.Frame(header, bg=BG_HEADER)
logo_frame.pack(side='left', padx=24, pady=10)

tk.Label(logo_frame, text=" ◉ ", bg=ACCENT_PRIMARY, fg=TEXT_WHITE,
         font=('Segoe UI', 13, 'bold'), padx=10, pady=6).pack(side='left', padx=(0, 14))

title_stack = tk.Frame(logo_frame, bg=BG_HEADER)
title_stack.pack(side='left')
tk.Label(title_stack, text="Systeme de Pointage", bg=BG_HEADER,
         fg=TEXT_DARK, font=FONT_TITLE).pack(anchor='w')
tk.Label(title_stack, text="Reconnaissance Faciale Automatisee", bg=BG_HEADER,
         fg=TEXT_LIGHT, font=FONT_SMALL).pack(anchor='w')

clock_area = tk.Frame(header, bg=BG_HEADER)
clock_area.pack(side='right', padx=30)
clock_lbl = tk.Label(clock_area, text="", bg=BG_HEADER, fg=TEXT_DARK, font=FONT_CLOCK)
clock_lbl.pack(anchor='e')
tk.Label(clock_area, text=day + "  " + mont[month] + "  " + year,
         bg=BG_HEADER, fg=TEXT_MEDIUM, font=FONT_DATE).pack(anchor='e')

tk.Frame(window, bg=BORDER_COLOR, height=1).pack(fill='x')

# ─── MAIN CONTENT ────────────────────────────────────────────────────────────
content = tk.Frame(window, bg=BG_MAIN)
content.pack(fill='both', expand=True, padx=20, pady=16)
content.columnconfigure(0, weight=5)
content.columnconfigure(1, weight=4)
content.rowconfigure(0, weight=1)

# ─── LEFT CARD : Registre de Presence ────────────────────────────────────────
left_card = tk.Frame(content, bg=BG_CARD, bd=0, relief='flat',
                     highlightthickness=1, highlightbackground=BORDER_COLOR)
left_card.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

left_header_fr = tk.Frame(left_card, bg=BG_SIDEBAR, height=52)
left_header_fr.pack(fill='x')
left_header_fr.pack_propagate(False)
tk.Label(left_header_fr, text="  Registre de Presence", bg=BG_SIDEBAR,
         fg=TEXT_WHITE, font=FONT_HEADING).pack(side='left', padx=20, pady=14)

# Stats row
stats_row = tk.Frame(left_card, bg=BG_CARD)
stats_row.pack(fill='x', padx=20, pady=(14, 8))

reg_chip = tk.Frame(stats_row, bg="#EFF6FF", padx=14, pady=8,
                    highlightthickness=1, highlightbackground="#BFDBFE")
reg_chip.pack(side='left', padx=(0, 10))
tk.Label(reg_chip, text="Inscrits au total", bg="#EFF6FF",
         fg=ACCENT_PRIMARY, font=FONT_SMALL).pack(anchor='w')
count_lbl = tk.Label(reg_chip, text="0", bg="#EFF6FF",
                     fg=ACCENT_PRIMARY, font=('Segoe UI', 16, 'bold'))
count_lbl.pack(anchor='w')

today_chip = tk.Frame(stats_row, bg="#ECFDF5", padx=14, pady=8,
                      highlightthickness=1, highlightbackground="#A7F3D0")
today_chip.pack(side='left', padx=(0, 10))
tk.Label(today_chip, text="Presents aujourd hui", bg="#ECFDF5",
         fg=ACCENT_SUCCESS, font=FONT_SMALL).pack(anchor='w')
tk.Label(today_chip, text="0", bg="#ECFDF5",
         fg=ACCENT_SUCCESS, font=('Segoe UI', 16, 'bold')).pack(anchor='w')

date_chip = tk.Frame(stats_row, bg="#FFFBEB", padx=14, pady=8,
                     highlightthickness=1, highlightbackground="#FDE68A")
date_chip.pack(side='left')
tk.Label(date_chip, text="Date", bg="#FFFBEB", fg=ACCENT_WARNING, font=FONT_SMALL).pack(anchor='w')
tk.Label(date_chip, text=day + "/" + month + "/" + year, bg="#FFFBEB",
         fg=ACCENT_WARNING, font=('Segoe UI', 14, 'bold')).pack(anchor='w')

# Track button — MUST be packed BEFORE tree_frame (side=bottom needs priority)
btn_track_frame = tk.Frame(left_card, bg=BG_CARD)
btn_track_frame.pack(side='bottom', fill='x', padx=16, pady=14)

track_btn = tk.Button(btn_track_frame, text="◉  Enregistrer Entree / Sortie",
                      command=TrackImages, fg=TEXT_WHITE, bg=ACCENT_PRIMARY,
                      font=FONT_BTN_LG, relief='flat', cursor='hand2',
                      activebackground=ACCENT_HOVER, activeforeground=TEXT_WHITE,
                      padx=20, pady=12, bd=0)
track_btn.pack(fill='x')
track_btn.bind('<Enter>', lambda e: track_btn.config(bg=ACCENT_HOVER))
track_btn.bind('<Leave>', lambda e: track_btn.config(bg=ACCENT_PRIMARY))

# Treeview — packed AFTER button so expand=True doesn't push button out
tree_frame = tk.Frame(left_card, bg=BG_CARD)
tree_frame.pack(fill='both', expand=True, padx=16, pady=(0, 0))

tv = ttk.Treeview(tree_frame, columns=('name', 'date', 'time'), show='headings tree', height=14)
tv.column('#0', width=80, anchor='center', stretch=False)
tv.column('name', width=190, anchor='w')
tv.column('date', width=130, anchor='center')
tv.column('time', width=120, anchor='center')
tv.heading('#0', text='ID')
tv.heading('name', text='NOM')
tv.heading('date', text='DATE')
tv.heading('time', text='HEURE')
tv.tag_configure('even', background='#F8FAFC')
tv.tag_configure('odd', background=BG_CARD)

scroll = ttk.Scrollbar(tree_frame, orient='vertical', command=tv.yview, style='Vertical.TScrollbar')
tv.configure(yscrollcommand=scroll.set)
tv.pack(side='left', fill='both', expand=True)
scroll.pack(side='right', fill='y')

# ─── RIGHT CARD : Nouvelle Inscription ───────────────────────────────────────
right_card = tk.Frame(content, bg=BG_CARD, bd=0, relief='flat',
                      highlightthickness=1, highlightbackground=BORDER_COLOR)
right_card.grid(row=0, column=1, sticky='nsew')

right_header_fr = tk.Frame(right_card, bg=BG_SIDEBAR, height=52)
right_header_fr.pack(fill='x')
right_header_fr.pack_propagate(False)
tk.Label(right_header_fr, text="  Nouvelle Inscription", bg=BG_SIDEBAR,
         fg=TEXT_WHITE, font=FONT_HEADING).pack(side='left', padx=20, pady=14)

form_body = tk.Frame(right_card, bg=BG_CARD, padx=24, pady=20)
form_body.pack(fill='both', expand=True)
form_body.columnconfigure(0, weight=1)

# ID Field
tk.Label(form_body, text="Identifiant Employe", bg=BG_CARD, fg=TEXT_MEDIUM,
         font=FONT_SUBHEAD).grid(row=0, column=0, sticky='w', pady=(10, 3), columnspan=2)

id_frame = tk.Frame(form_body, bg=BG_CARD, highlightthickness=1,
                    highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_PRIMARY)
id_frame.grid(row=1, column=0, sticky='ew', columnspan=2, pady=(0, 4), ipady=2)

txt_id = tk.Entry(id_frame, fg=TEXT_DARK, font=FONT_BODY, relief='flat',
                  bg=BG_CARD, insertbackground=ACCENT_PRIMARY)
txt_id.pack(side='left', fill='x', expand=True, ipady=8, padx=10)
tk.Button(id_frame, text="✕", command=clear, bg=BG_CARD, fg=TEXT_LIGHT,
          relief='flat', font=FONT_SMALL, cursor='hand2',
          activebackground=BG_CARD, activeforeground=ACCENT_DANGER,
          padx=6, bd=0).pack(side='right', padx=4)

# Name Field
tk.Label(form_body, text="Nom Complet", bg=BG_CARD, fg=TEXT_MEDIUM,
         font=FONT_SUBHEAD).grid(row=2, column=0, sticky='w', pady=(12, 3), columnspan=2)

name_frame = tk.Frame(form_body, bg=BG_CARD, highlightthickness=1,
                      highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_PRIMARY)
name_frame.grid(row=3, column=0, sticky='ew', columnspan=2, pady=(0, 4), ipady=2)

txt_name = tk.Entry(name_frame, fg=TEXT_DARK, font=FONT_BODY, relief='flat',
                    bg=BG_CARD, insertbackground=ACCENT_PRIMARY)
txt_name.pack(side='left', fill='x', expand=True, ipady=8, padx=10)
tk.Button(name_frame, text="✕", command=clear2, bg=BG_CARD, fg=TEXT_LIGHT,
          relief='flat', font=FONT_SMALL, cursor='hand2',
          activebackground=BG_CARD, activeforeground=ACCENT_DANGER,
          padx=6, bd=0).pack(side='right', padx=4)

# Focus effects
txt_id.bind('<FocusIn>',    lambda e: id_frame.config(highlightbackground=ACCENT_PRIMARY))
txt_id.bind('<FocusOut>',   lambda e: id_frame.config(highlightbackground=BORDER_COLOR))
txt_name.bind('<FocusIn>',  lambda e: name_frame.config(highlightbackground=ACCENT_PRIMARY))
txt_name.bind('<FocusOut>', lambda e: name_frame.config(highlightbackground=BORDER_COLOR))

# Separator
tk.Frame(form_body, bg=BORDER_COLOR, height=1).grid(row=4, column=0, columnspan=2,
                                                     sticky='ew', pady=16)

# Action Buttons helper
def styled_btn(parent, text, cmd, color, hover_color, row):
    btn = tk.Button(parent, text=text, command=cmd, fg=TEXT_WHITE, bg=color,
                    font=FONT_BTN_LG, relief='flat', cursor='hand2',
                    activebackground=hover_color, activeforeground=TEXT_WHITE,
                    padx=16, pady=10, bd=0)
    btn.grid(row=row, column=0, columnspan=2, sticky='ew', pady=(0, 8))
    btn.bind('<Enter>', lambda e: btn.config(bg=hover_color))
    btn.bind('<Leave>', lambda e: btn.config(bg=color))
    return btn

styled_btn(form_body, "📷  Prendre des Images",    TakeImages,    ACCENT_PRIMARY, ACCENT_HOVER, 5)
styled_btn(form_body, "💾  Enregistrer le Profil", TrainImages,   ACCENT_SUCCESS, "#059669",    6)

tk.Frame(form_body, bg=BORDER_COLOR, height=1).grid(row=7, column=0, columnspan=2,
                                                     sticky='ew', pady=12)
styled_btn(form_body, "Quitter", window.destroy, ACCENT_DANGER, "#DC2626", 8)

# ─── STATUS BAR ──────────────────────────────────────────────────────────────
tk.Frame(window, bg=BORDER_COLOR, height=1).pack(fill='x')
status_bar = tk.Frame(window, bg=BG_HEADER, height=34)
status_bar.pack(fill='x')
status_bar.pack_propagate(False)

status_lbl = tk.Label(status_bar, text="", bg=BG_HEADER, fg=TEXT_MEDIUM, font=FONT_SMALL)
status_lbl.pack(side='left', padx=20, pady=8)
tk.Label(status_bar, text="Systeme de Pointage",
         bg=BG_HEADER, fg=TEXT_LIGHT, font=FONT_SMALL).pack(side='right', padx=20)


# ─── INIT ────────────────────────────────────────────────────────────────────
tick()
update_total_count()
set_status("Bienvenue - Pret a enregistrer les presences.", TEXT_MEDIUM)

window.mainloop()
