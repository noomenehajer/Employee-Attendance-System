############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

##################################################################################

def tick():
    time_string =time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)

###################################################################################

def contact():
    mess._show(title='Contact', message="Veuillez me contacter sur : 'hajer.noomene@gmail.com' ")

###################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Certains fichiers sont manquants', message='Contactez-moi pour obtenir de l''aide')
        window.destroy()

###################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Ancien mot de passe introuvable', 'Veuillez saisir un nouveau mot de passe ci-dessous', show='*')
        if new_pas == None:
            mess._show(title='Aucun mot de passe saisi', message='Mot de passe non défini !! Veuillez réessayer')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Mot de passe enregistré', message='Le nouveau mot de passe a été enregistré avec succès !!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Erreur', message='Confirmez à nouveau le nouveau mot de passe !!!')
            return
    else:
        mess._show(title='Mot de passe incorrect', message='Veuillez saisir l ancien mot de passe correct')
        return
    mess._show(title='Mot de passe changé', message='Mot de passe changé avec succès !!')
    master.destroy()

###################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("470x200") 
    master.resizable(False, False)
    master.title("Changer le mot de passe")
    master.configure(background="#F5F5F5")  
    
    padding_x = 10
    padding_y = 10
    
    lbl4 = tk.Label(master, text='Saisir l ancien mot de passe', bg="#F5F5F5", font=('comic', 10, 'bold'))
    lbl4.grid(row=0, column=0, padx=padding_x, pady=padding_y, sticky='e')
    global old
    old = tk.Entry(master, width=25, fg="#4A4A4A", relief='solid', font=('comic', 10, 'bold'), show='*')
    old.grid(row=0, column=1, padx=padding_x, pady=padding_y, sticky='w')
    
    lbl5 = tk.Label(master, text='Saisir le nouveau mot de passe', bg="#F5F5F5", font=('comic', 10, 'bold'))
    lbl5.grid(row=1, column=0, padx=padding_x, pady=padding_y, sticky='e')
    global new
    new = tk.Entry(master, width=25, fg="#4A4A4A", relief='solid', font=('comic', 10, 'bold'), show='*')
    new.grid(row=1, column=1, padx=padding_x, pady=padding_y, sticky='w')
    
    lbl6 = tk.Label(master, text='Confirmer le nouveau mot de passe', bg="#F5F5F5", font=('comic', 10, 'bold'))
    lbl6.grid(row=2, column=0, padx=padding_x, pady=padding_y, sticky='e')
    global nnew
    nnew = tk.Entry(master, width=25, fg="#4A4A4A", relief='solid', font=('comic', 10, 'bold'), show='*')
    nnew.grid(row=2, column=1, padx=padding_x, pady=padding_y, sticky='w')
    
    cancel = tk.Button(master, text="Annuler", command=master.destroy, fg="#FFFFFF", bg="#FF6F61", height=1, width=22, activebackground="#F5F5F5", font=('comic', 10, 'bold'))
    cancel.grid(row=3, column=1, padx=padding_x, pady=padding_y, sticky='e')
    
    save1 = tk.Button(master, text="Enregistrer", command=save_pass, fg="#FFFFFF", bg="#008080", height=1, width=22, activebackground="#F5F5F5", font=('comic', 10, 'bold'))
    save1.grid(row=3, column=0, padx=padding_x, pady=padding_y, sticky='w')
    
    master.mainloop()


#####################################################################################

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Ancien mot de passe introuvable', 'Veuillez entrer un nouveau mot de passe ci-dessous', show='*')
        if new_pas == None:
            mess._show(title=' Aucun mot de passe entré', message='Mot de passe non défini !! Veuillez réessayer')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Mot de passe enregistré', message='Le nouveau mot de passe a été enregistré avec succès !!')
            return
    password = tsd.askstring('Mot de passe', 'Saisir le mot de passe', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Mauvais mot de passe', message='Vous avez entré un mauvais mot de passe')

######################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

#######################################################################################

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("EmployeeDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("EmployeeDetails\EmployeeDetails.csv")
    if exists:
        with open("EmployeeDetails\EmployeeDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("EmployeeDetails\EmployeeDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]
        with open('EmployeeDetails\EmployeeDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Veuillez remplir tous les champs du formulaire"
            message.configure(text=res,fg="#FF6F61")

########################################################################################

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
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################

def update_treeview(employee_id, employee_name, date, timestamp):
    # Insert a new row into the Treeview
    tv.insert('', 'end', text=employee_id, values=(employee_name, date, timestamp))

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("EmployeeDetails/")
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        print("Training data not found!")
        return
    
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Image', 'Name', 'Date', 'Time']
    exists1 = os.path.isfile("EmployeeDetails\EmployeeDetails.csv")
    if exists1:
        df = pd.read_csv("EmployeeDetails\EmployeeDetails.csv")
    else:
        print("Détails de l'employé introuvables !")
        cam.release()
        cv2.destroyAllWindows()
        return
    
    attended_today = set()  # Set to keep track of employees who have already attended today
    
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            
            if conf < 50:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H-%M-%S')
                
                employee_id = df.loc[df['SERIAL NO.'] == serial, 'ID'].values[0]
                employee_name = df.loc[df['SERIAL NO.'] == serial, 'NAME'].values[0]
                
                if employee_id not in attended_today:
                    # Save the image with unique identifier (employee ID and timestamp)
                    img_name = f"Attendance/{employee_id}_{date}_{timeStamp}.jpg"
                    cv2.imwrite(img_name, im)
                    
                    # Update attendance record with image reference
                    attendance = [str(employee_id), img_name, str(employee_name), str(date), str(timeStamp)]
                    with open(f"Attendance/Attendance_{date}.csv", 'a+') as csvFile1:
                        writer = csv.writer(csvFile1)
                        if os.stat(f"Attendance/Attendance_{date}.csv").st_size == 0:
                            writer.writerow(col_names)
                        writer.writerow(attendance)
                    
                    # Mark employee as attended today
                    attended_today.add(employee_id)
                    
                    # Update Treeview with new attendance
                    update_treeview(employee_id, employee_name, date, timeStamp)
                
                # Display recognized name on the image
                cv2.putText(im, employee_name, (x, y + h), font, 1, (255, 255, 255), 2)
            else:
                cv2.putText(im, 'Inconnu', (x, y + h), font, 1, (255, 255, 255), 2)
        
        cv2.imshow('Taking Attendance', im)
        if cv2.waitKey(1) == ord('q'):
            break
    
    cam.release()
    cv2.destroyAllWindows()

    
######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'Janvier',
      '02':'Février',
      '03':'Mars',
      '04':'Avril',
      '05':'Mai',
      '06':'Juin',
      '07':'Juillet',
      '08':'Août',
      '09':'Septembre',
      '10':'Octobre',
      '11':'Novembre',
      '12':'Décembre'
      }

######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.geometry("1300x700")
window.resizable(True,False)
window.title("Systeme de pointage pour les employés")
window.configure(background='#FFFFFF')

frame1 = tk.Frame(window, bg="#F5F5F5")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#F5F5F5")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Système de Pointage par Reconnaissance Faciale" ,fg="#1F3B4D",bg="#FFFFFF" ,width=55 ,height=1,font=('comic', 25, ' bold '))
message3.place(x=10, y=10)
message3.pack(anchor=tk.CENTER, padx=10,pady=10)

frame3 = tk.Frame(window, bg="#9E9E9E", borderwidth=0)
frame3.place(relx=0.52, rely=0.09, relwidth=0.10, relheight=0.07)

frame4 = tk.Frame(window, bg="#9E9E9E", borderwidth=0)
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text = "‎ ‎" + day+" "+mont[month]+" "+year+"   -", fg="#454545" ,height=1,font=('comic', 18, ' bold '))
datef.pack(fill='both',expand=1, ipadx=10, ipady=15)

clock = tk.Label(frame3,fg="#454545" ,width=200 ,height=1,font=('comic', 18, ' bold '))
clock.pack(fill='both',expand=1, ipadx=5, ipady=15)
tick()

head2 = tk.Label(frame2, text="                      Nouvelles Inscriptions                       ", fg="white",bg="#1F3B4D" ,font=('comic', 17, ' bold ') )
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="                 Bienvenue à Nos Employés                       ", fg="white",bg="#1F3B4D" ,font=('comic', 17, ' bold ') )
head1.place(x=0,y=0)

lbl = tk.Label(frame2, text="Saisir votre ID",width=20  ,height=1  ,fg="#4A4A4A"  ,bg="#F5F5F5" ,font=('comic', 13, ' bold ') )
lbl.place(x=0, y=55)

txt = tk.Entry(frame2,width=32 ,fg="black",font=('comic', 13))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="Saisir votre nom",width=20  ,fg="#4A4A4A"  ,bg="#F5F5F5" ,font=('comic', 13, ' bold '))
lbl2.place(x=7, y=140)

txt2 = tk.Entry(frame2,width=32 ,fg="black",font=('comic', 13 )  )
txt2.place(x=30, y=173)

message = tk.Label(frame2, text="" ,bg="#F5F5F5" ,fg="#4A4A4A"  ,width=39,height=1, activebackground = "#3ffc00" ,font=('comic', 14, ' bold '))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="Liste des employés",width=20  ,fg="#4A4A4A"  ,bg="#F5F5F5"  ,height=1 ,font=('comic', 15, ' bold '))
lbl3.place(x=124, y=115)

res=0
exists = os.path.isfile("EmployeeDetails\EmployeeDetails.csv")
if exists:
    with open("EmployeeDetails\EmployeeDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Total des inscriptions jusqu à présent  : '+str(res))

##################### MENUBAR #################################

menubar = tk.Menu(window, relief='ridge', bg="#1F3B4D", fg='white', font=('Helvetica', 12))

filemenu = tk.Menu(menubar, tearoff=0, bg="#1F3B4D", fg='white', font=('Helvetica', 12))
filemenu.add_command(label='Changer le mot de passe', command=change_pass)
filemenu.add_command(label='Contact', command=contact)
filemenu.add_command(label='Quitter', command=window.destroy)

menubar.add_command(label='Changer le mot de passe', command=change_pass)
menubar.add_command(label='Contact', command=contact)
menubar.add_command(label='Quitter', command=window.destroy)

################## TREEVIEW ATTENDANCE TABLE ####################

tv= ttk.Treeview(frame1,height =13,columns = ('name','date','time'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('date',width=133)
tv.column('time',width=133)
tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NOM')
tv.heading('date',text ='DATE')
tv.heading('time',text ='HEURE')

###################### SCROLLBAR ################################

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

###################### BUTTONS ##################################

clearButton = tk.Button(frame2, text="Effacer", command=clear  ,fg="#F5F5F5"  ,bg="#FF6F61"  ,width=11 ,activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton.place(x=335, y=86)
clearButton2 = tk.Button(frame2, text="Effacer", command=clear2  ,fg="#F5F5F5"  ,bg="#FF6F61"  ,width=11 , activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton2.place(x=335, y=172)    
takeImg = tk.Button(frame2, text="Prendre des Images", command=TakeImages  ,fg="#4A4A4A"  ,bg="#abc4e7"  ,width=34  ,height=1, activebackground = "white" ,font=('comic', 12, ' bold '))
takeImg.place(relx=0.5, rely=0.5, anchor='center')
trainImg = tk.Button(frame2, text="Enregistrer le Profil", command=psw ,fg="#4A4A4A"  ,bg="#abc4e7"  ,width=34  ,height=1, activebackground = "white" ,font=('comic', 12, ' bold '))
trainImg.place(relx=0.5, rely=0.6, anchor='center')
trackImg = tk.Button(frame1, text="Enregistrer Entrée/Sortie", command=TrackImages  ,fg="#4A4A4A"  ,bg="#abc4e7"  ,width=35  ,height=1, activebackground = "white" ,font=('comic', 13, ' bold '))
trackImg.place(x=60,y=50)
quitWindow = tk.Button(frame1, text="Quitter", command=window.destroy  ,fg="#F5F5F5"  ,bg="#FF6F61"  ,width=35 ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
quitWindow.place(x=30, y=450)

##################### END ######################################

window.configure(menu=menubar)
window.mainloop()

####################################################################################################
