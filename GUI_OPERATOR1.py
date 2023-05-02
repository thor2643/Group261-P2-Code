import tkinter as tk
from tkinter import *

#variables and arrays:
count=0

# root window
root = tk.Tk()
root.config(bg="white")
root.minsize(200, 200)  # width, height
root.maxsize(1200, 750)
root.geometry("1200x750+200+0") # width, height, placement on screen 
root.title("Control GUI")
Dispensor_number=[0,0,0,0,0,0,0,0] #0 PCB, 1 fuses, 2-4: top cover colors, 5-7: bot cover colors.



main_frame = tk.Frame(root, bg='#F0F0F0')
main_frame.pack(fill=tk.BOTH, expand=True)

#page 1:
page_1 = tk.Frame(main_frame)
page_1_lb=tk.Label(page_1, text='Control Center', font=('Times New Roman',50,'bold'), background= '#F0F0F0')
page_1_lb.grid(row=0,  column=0, columnspan=4, padx=5,  pady=5)
message_Alert=tk.Label(page_1, text='You will be alerted if refill is needed:', font=('Times New Roman',20,'bold'),bg='#F0F0F0')
message_Alert.grid(row=1,  column=0, columnspan=4, padx=20,  pady=20)

#frames:
PCB_frame  =  Frame(page_1,  width=300,  height= 200,  bg='white', highlightbackground="black", highlightthickness=2)
PCB_frame.grid(row=1, rowspan=2,  column=0, sticky='w',  padx=10,  pady=10)
PCB_frame.pack_propagate(False)

Fuse_frame  =  Frame(page_1,  width=300,  height=200,  bg='white', highlightbackground="black", highlightthickness=2)
Fuse_frame.grid(row=1, rowspan=2, column=3, sticky='e',  padx=10,  pady=10)
Fuse_frame.pack_propagate(False)

top_cov_frame  =  Frame(page_1,  width=525,  height=  350,  bg='white', highlightbackground="black", highlightthickness=2)
top_cov_frame.grid(row=3,  column=0, columnspan=2, sticky='w', padx=10,  pady=10)
top_cov_frame.pack_propagate(False)

bot_cov_frame  =  Frame(page_1,  width=525,  height=350,  bg='white', highlightbackground="black", highlightthickness=2)
bot_cov_frame.grid(row=3,  column=2, columnspan=2, sticky='e',  padx=10,  pady=10)
bot_cov_frame.pack_propagate(False)

#PCB:
fill_PCB=tk.Label(PCB_frame, text=" ",bg= 'white')
fill_PCB.pack()
PCB=tk.Label(PCB_frame, text='PCB:', font=('Times New Roman',30,'bold'), background= 'white')
PCB.pack()
PCB_number=tk.Label(PCB_frame, text= str(Dispensor_number[0]), font=('Times New Roman',25),bg='white')
PCB_number.pack()
#PCB_refill=tk.Label(PCB_frame, text='Refill needed!!', font=('Times New Roman',30,'bold'),fg='red', bg= 'white')
#PCB_refill.pack()

#Fuses:
fill_fuse=tk.Label(Fuse_frame, text=" ",bg= 'white')
fill_fuse.pack()
Fuse=tk.Label(Fuse_frame, text='Fuses:', font=('Times New Roman',30,'bold'), background= 'white')
Fuse.pack()
Fuse_number=tk.Label(Fuse_frame, text= str(Dispensor_number[1]), font=('Times New Roman',25),bg='white')
Fuse_number.pack()
#Fuse_refill=tk.Label(Fuse_frame, text='Refill needed!!', font=('Times New Roman',30,'bold'),fg='red', bg= 'white')
#Fuse_refill.pack()

#TOP Cover:
fill_top_cov=tk.Label(top_cov_frame, text=" ",bg= 'white')
fill_top_cov.pack()
fill_top_cov_1=tk.Label(top_cov_frame, text=" ",bg= 'white')
fill_top_cov_1.pack()
fill_top_cov_2=tk.Label(top_cov_frame, text=" ",bg= 'white')
fill_top_cov_2.pack()
top_cov=tk.Label(top_cov_frame, text='Top cover:', font=('Times New Roman',30,'bold'), background= 'white')
top_cov.pack(anchor=CENTER)
top_cov_col=tk.Label(top_cov_frame, 
                     text='Black:         Blue:         White:',
                     font=('Times New Roman',20),
                     background= 'white')
top_cov_col.pack()
top_cov_number=tk.Label(top_cov_frame,
                        text= str(Dispensor_number[2]) + "             " + str(Dispensor_number[3]) + "            " + str(Dispensor_number[4]),
                        font=('Times New Roman',25),
                        bg='white')
top_cov_number.pack()
fill_top_cov_3=tk.Label(top_cov_frame, text=" ",bg= 'white')
fill_top_cov_3.pack()
#top_cov_refill=tk.Label(top_cov_frame, text='Refill needed!!', font=('Times New Roman',30,'bold'),fg='red', bg= 'white')
#top_cov_refill.pack()

#BOT Cover:
fill_bot_cov=tk.Label(bot_cov_frame, text=" ",bg= 'white')
fill_bot_cov.pack()
fill_bot_cov_1=tk.Label(bot_cov_frame, text=" ",bg= 'white')
fill_bot_cov_1.pack()
fill_bot_cov_2=tk.Label(bot_cov_frame, text=" ",bg= 'white')
fill_bot_cov_2.pack()
bot_cov=tk.Label(bot_cov_frame, text='Bottom cover:', font=('Times New Roman',30,'bold'), background= 'white')
bot_cov.pack()
bot_cov_col=tk.Label(bot_cov_frame, 
                     text='Black:         Blue:         White:',
                     font=('Times New Roman',20),
                     background= 'white')
bot_cov_col.pack()
bot_cov_number=tk.Label(bot_cov_frame,
                        text= str(Dispensor_number[5]) + "             " + str(Dispensor_number[6]) + "            " + str(Dispensor_number[7]),
                        font=('Times New Roman',25),
                        bg='white')
bot_cov_number.pack()
fill_bot_cov_3=tk.Label(bot_cov_frame, text=" ",bg= 'white')
fill_bot_cov_3.pack()
#bot_cov_refill=tk.Label(bot_cov_frame, text='Refill needed!!', font=('Times New Roman',30,'bold'),fg='red', bg= 'white')
#bot_cov_refill.pack()


#page 2:
page_2 = tk.Frame(main_frame)
page_2_lb=tk.Label(page_2, text='Refill', font=('Times New Roman',30,'bold'), bg='#F0F0F0')
page_2_lb.grid(row=0,  column=0, columnspan=4, padx=5,  pady=5)
message_Alert2=tk.Label(page_2, text='Type the number of items added or removed', font=('Times New Roman',15,'bold'),bg='#F0F0F0')
message_Alert2.grid(row=1,  column=0, columnspan=4, padx=20,  pady=20)
message_Alert3=tk.Label(page_2, text=' and push the corresponding button:', font=('Times New Roman',15,'bold'),bg='#F0F0F0')
message_Alert3.place(x=390,y=150)


#frames page 2:
PCB_frame2  =  Frame(page_2,  width=300,  height= 200,  bg='white', highlightbackground="black", highlightthickness=2)
PCB_frame2.grid(row=1, rowspan=2,  column=0, sticky='w',  padx=10,  pady=10)
PCB_frame2.pack_propagate(False)

Fuse_frame2  =  Frame(page_2,  width=300,  height=200,  bg='white', highlightbackground="black", highlightthickness=2)
Fuse_frame2.grid(row=1, rowspan=2, column=3, sticky='e',  padx=10,  pady=10)
Fuse_frame2.pack_propagate(False)

top_cov_frame2  =  Frame(page_2,  width=525,  height=  350,  bg='white', highlightbackground="black", highlightthickness=2)
top_cov_frame2.grid(row=3,  column=0, columnspan=2, sticky='w', padx=10,  pady=10)
top_cov_frame2.pack_propagate(False)

bot_cov_frame2  =  Frame(page_2,  width=525,  height=350,  bg='white', highlightbackground="black", highlightthickness=2)
bot_cov_frame2.grid(row=3,  column=2, columnspan=2, sticky='e',  padx=10,  pady=10)
bot_cov_frame2.pack_propagate(False)

#PCB:
fill_PCB=tk.Label(PCB_frame2, text=" ",bg= 'white')
fill_PCB.pack()
PCB=tk.Label(PCB_frame2, text='PCB:', font=('Times New Roman',30,'bold'), background= 'white')
PCB.pack()


#Fuses:
fill_fuse=tk.Label(Fuse_frame2, text=" ",bg= 'white')
fill_fuse.pack()
Fuse=tk.Label(Fuse_frame2, text='Fuses:', font=('Times New Roman',30,'bold'), background= 'white')
Fuse.pack()


#TOP Cover:
fill_top_cov=tk.Label(top_cov_frame2, text=" ",bg= 'white')
fill_top_cov.pack()
fill_top_cov_1=tk.Label(top_cov_frame2, text=" ",bg= 'white')
fill_top_cov_1.pack()
fill_top_cov_2=tk.Label(top_cov_frame2, text=" ",bg= 'white')
fill_top_cov_2.pack()
top_cov=tk.Label(top_cov_frame2, text='Top cover:', font=('Times New Roman',30,'bold'), background= 'white')
top_cov.pack(anchor=CENTER)
top_cov_col=tk.Label(top_cov_frame2, 
                     text='Black:         Blue:         White:',
                     font=('Times New Roman',20),
                     background= 'white')
top_cov_col.pack()


#BOT Cover:
fill_bot_cov=tk.Label(bot_cov_frame2, text=" ",bg= 'white')
fill_bot_cov.pack()
fill_bot_cov_1=tk.Label(bot_cov_frame2, text=" ",bg= 'white')
fill_bot_cov_1.pack()
fill_bot_cov_2=tk.Label(bot_cov_frame2, text=" ",bg= 'white')
fill_bot_cov_2.pack()
bot_cov=tk.Label(bot_cov_frame2, text='Bottom cover:', font=('Times New Roman',30,'bold'), background= 'white')
bot_cov.pack()
bot_cov_col=tk.Label(bot_cov_frame2, 
                     text='Black:         Blue:         White:',
                     font=('Times New Roman',20),
                     background= 'white')
bot_cov_col.pack()

#Refill needed text:
PCB_refill=tk.Label(PCB_frame, text='Refill needed!!', font=('Times New Roman',30,'bold'),fg='red', bg= 'white')
PCB_refill.pack()

Fuse_refill=tk.Label(Fuse_frame, text='Refill needed!!', font=('Times New Roman',30,'bold'),fg='red', bg= 'white')
Fuse_refill.pack()

top_cov_refill=tk.Label(top_cov_frame, text='Refill needed!!', font=('Times New Roman',30,'bold'),fg='red', bg= 'white')
top_cov_refill.pack()

bot_cov_refill=tk.Label(bot_cov_frame, text='Refill needed!!', font=('Times New Roman',30,'bold'),fg='red', bg= 'white')
bot_cov_refill.pack()

#funktion for removal of entry input:
def remove_0(indput):
    indput.delete(0,'0')

#Entry is beeing defined:
PCB_entry = tk.Entry(page_2, width=10,highlightthickness=2, highlightbackground="black", exportselection=1)
PCB_entry.place(x=115,y=170)
PCB_entry.bind('<FocusIn>', remove_0(PCB_entry))

fuse_entry = tk.Entry(page_2, width=10,highlightthickness=2, highlightbackground="black")
fuse_entry.place(x=885,y=170)
fuse_entry.bind('<FocusIn>', remove_0(fuse_entry))

top_cov_black_entry = tk.Entry(page_2, width=10,highlightthickness=2, highlightbackground="black")
top_cov_black_entry.place(x=100,y=475)
top_cov_black_entry.bind('<FocusIn>', remove_0(top_cov_black_entry))

top_cov_blue_entry = tk.Entry(page_2, width=10,highlightthickness=2, highlightbackground="black")
top_cov_blue_entry.place(x=225,y=475)
top_cov_blue_entry.bind('<FocusIn>', remove_0(top_cov_blue_entry))

top_cov_white_entry = tk.Entry(page_2, width=10,highlightthickness=2, highlightbackground="black")
top_cov_white_entry.place(x=355,y=475)
top_cov_white_entry.bind('<FocusIn>', remove_0(top_cov_white_entry))

bot_cov_black_entry = tk.Entry(page_2, width=10,highlightthickness=2, highlightbackground="black")
bot_cov_black_entry.place(x=650,y=475)
bot_cov_black_entry.bind('<FocusIn>', remove_0(bot_cov_black_entry))

bot_cov_blue_entry = tk.Entry(page_2, width=10,highlightthickness=2, highlightbackground="black")
bot_cov_blue_entry.place(x=775,y=475)
bot_cov_blue_entry.bind('<FocusIn>', remove_0(bot_cov_blue_entry))

bot_cov_white_entry = tk.Entry(page_2, width=10,highlightthickness=2, highlightbackground="black")
bot_cov_white_entry.place(x=905,y=475)
bot_cov_white_entry.bind('<FocusIn>', remove_0(bot_cov_white_entry))

#array with entry names:
entry_names=[PCB_entry,fuse_entry,top_cov_black_entry,top_cov_blue_entry,top_cov_white_entry,bot_cov_black_entry,bot_cov_blue_entry,bot_cov_white_entry]


#array for pages:
pages = [page_1, page_2]
page = pages[count]
page.pack()

#funktions:  
def entry_eq_0():
    PCB_entry.insert(0,'0')
    PCB_entry.bind('<FocusIn>', remove_0(PCB_entry))

    fuse_entry.insert(0,'0')
    fuse_entry.bind('<FocusIn>', remove_0(fuse_entry))

    top_cov_black_entry.insert(0,'0')
    top_cov_black_entry.bind('<FocusIn>', remove_0(top_cov_black_entry))

    top_cov_blue_entry.insert(0,'0')
    top_cov_blue_entry.bind('<FocusIn>', remove_0(top_cov_blue_entry))

    top_cov_white_entry.insert(0,'0')
    top_cov_white_entry.bind('<FocusIn>', remove_0(top_cov_white_entry))

    bot_cov_black_entry.insert(0,'0')
    bot_cov_black_entry.bind('<FocusIn>', remove_0(bot_cov_black_entry))

    bot_cov_blue_entry.insert(0,'0')
    bot_cov_blue_entry.bind('<FocusIn>', remove_0(bot_cov_blue_entry))

    bot_cov_white_entry.insert(0,'0')
    bot_cov_white_entry.bind('<FocusIn>', remove_0(bot_cov_white_entry))
  
def Update_Numbers():
    PCB_number.configure(text= str(Dispensor_number[0]))
    PCB_number.pack()
    Fuse_number.configure(text= str(Dispensor_number[1]))
    Fuse_number.pack()
    top_cov_number.configure(text= str(Dispensor_number[2]) + "             " + str(Dispensor_number[3]) + "            " + str(Dispensor_number[4]),)
    top_cov_number.pack()
    bot_cov_number.configure(text= str(Dispensor_number[5]) + "             " + str(Dispensor_number[6]) + "            " + str(Dispensor_number[7]),)
    bot_cov_number.pack()
    
def Clear_Entry():
    for i in entry_names:
        i.delete(0, END)
    
def Refill(): #Moves to next page
    global count
    for p in pages:
        p.pack_forget()
        
    count += 1
    page = pages[count]
    page.pack()
    entry_eq_0()
    
def Move_back_page():
    global count
    for p in pages:
            p.pack_forget()

    count -= 1
    page = pages[count]
    page.pack()
    Update_Numbers()
    print(Dispensor_number)
    
#entry variables
entry_values=[0,0,0,0,0,0,0,0] 

def get_entry_values():
    global entry_values
    global fuse_entry
    entry_values[0]= int(PCB_entry.get())
    entry_values[1]= int(fuse_entry.get())
    entry_values[2]= int(top_cov_black_entry.get())
    entry_values[3]= int(top_cov_blue_entry.get())
    entry_values[4]= int(top_cov_white_entry.get())
    entry_values[5]= int(bot_cov_black_entry.get())
    entry_values[6]= int(bot_cov_blue_entry.get())
    entry_values[7]= int(bot_cov_white_entry.get())

def Calculate(indput):
    global entry_values
    global Dispensor_number
    get_entry_values()
    if indput==1:
        for i in range(0,8):
            Dispensor_number[i]=Dispensor_number[i] + entry_values[i]
        return Dispensor_number
 
    if indput==2:
        for i in range(0,8):
            Dispensor_number[i]=Dispensor_number[i] - entry_values[i]
        return Dispensor_number
                              
def Add():
    Calculate(1)
    Move_back_page()
    Clear_Entry()
    Check_If_Refill_Needed()
    
def Rem():
    Calculate(2)
    Move_back_page()
    Clear_Entry()
    Check_If_Refill_Needed()
    
def Check_If_Refill_Needed():
    if Dispensor_number[0] < 5:
        PCB_refill.configure(fg='red')
        PCB_refill.pack()
    else:
        PCB_refill.configure(fg='white')
    
    if Dispensor_number[1] < 41:
        Fuse_refill.configure(fg='red')
        Fuse_refill.pack()
    else:
        Fuse_refill.configure(fg='white')
    
    if (Dispensor_number[2] < 5) or (Dispensor_number[3] < 5) or (Dispensor_number[4] < 5):
        top_cov_refill.configure(fg='red')
        top_cov_refill.pack()
    else:
        top_cov_refill.configure(fg='white')

    if (Dispensor_number[5] < 5) or (Dispensor_number[6] < 5) or (Dispensor_number[7] < 5):
        bot_cov_refill.configure(fg='red')
        bot_cov_refill.pack()
    else:
        bot_cov_refill.configure(fg='white')
        

#bottons:
refill_btn=tk.Button(page_1,text='Refill now',
                     font=('Times New Roman', 30, 'bold'),
                     bg='white',
                     fg='red',
                     width=8,
                     height=2,
                     relief=GROOVE,
                     command=Refill
                     )
refill_btn.grid(row=2,  column=0, columnspan=4,  padx=5,  pady=5)

#buttons page chance:
add_btn = tk.Button(page_2,text='Add', 
                     font=('Bold', 20),
                     bg='green', 
                     width=8,
                     relief=GROOVE,
                     command=Add
                     )
add_btn.place(x=400,y=200)

remove_btn = tk.Button(page_2, text='Remove',
                     font=('Bold', 20),
                     bg='red',
                     width=8,
                     relief=GROOVE, 
                     command=Rem
                     )
remove_btn.place(x=555,y=200)

root.mainloop()