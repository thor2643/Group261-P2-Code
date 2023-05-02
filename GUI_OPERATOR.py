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
Dispensor_number=[10,10,10,10,10,10,10,10] #0-2:top covor colors, 3: fuses, 4-6: bottom color fuses, 7: PCB.


main_frame = tk.Frame(root, bg='#F0F0F0')
main_frame.pack(fill=tk.BOTH, expand=True)
#main_frame.pack_propagate(False)

#page 1:
page_1 = tk.Frame(main_frame)
page_1_lb=tk.Label(page_1, text='Control Center', font=('Times New Roman',50,'bold'), background= '#F0F0F0')
page_1_lb.grid(row=0,  column=0, columnspan=4, padx=5,  pady=5)
message_Alert=tk.Label(page_1, text='No refill needed at the moment', font=('Times New Roman',20,'bold'),bg='#F0F0F0')
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
PCB_number=tk.Label(PCB_frame, text= str(Dispensor_number[7]), font=('Times New Roman',25),bg='white')
PCB_number.pack()
PCB_refill=tk.Label(PCB_frame, text='Refill needed!!', font=('Times New Roman',30,'bold'),fg='red', bg= 'white')
PCB_refill.pack()

#Fuses:
fill_fuse=tk.Label(Fuse_frame, text=" ",bg= 'white')
fill_fuse.pack()
Fuse=tk.Label(Fuse_frame, text='Fuses:', font=('Times New Roman',30,'bold'), background= 'white')
Fuse.pack()
Fuse_number=tk.Label(Fuse_frame, text= str(Dispensor_number[3]), font=('Times New Roman',25),bg='white')
Fuse_number.pack()
Fuse_refill=tk.Label(Fuse_frame, text='Refill needed!!', font=('Times New Roman',30,'bold'),fg='red', bg= 'white')
Fuse_refill.pack()

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
                        text= str(Dispensor_number[0]) + "             " + str(Dispensor_number[1]) + "            " + str(Dispensor_number[2]),
                        font=('Times New Roman',25),
                        bg='white')
top_cov_number.pack()
fill_top_cov_3=tk.Label(top_cov_frame, text=" ",bg= 'white')
fill_top_cov_3.pack()
top_cov_refill=tk.Label(top_cov_frame, text='Refill needed!!', font=('Times New Roman',30,'bold'),fg='red', bg= 'white')
top_cov_refill.pack()

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
                        text= str(Dispensor_number[4]) + "             " + str(Dispensor_number[5]) + "            " + str(Dispensor_number[6]),
                        font=('Times New Roman',25),
                        bg='white')
bot_cov_number.pack()
fill_bot_cov_3=tk.Label(bot_cov_frame, text=" ",bg= 'white')
fill_bot_cov_3.pack()
bot_cov_refill=tk.Label(bot_cov_frame, text='Refill needed!!', font=('Times New Roman',30,'bold'),fg='red', bg= 'white')
bot_cov_refill.pack()


#page 2:
page_2 = tk.Frame(main_frame)
page_2_lb=tk.Label(page_2, text='Refill', font=('Times New Roman',30,'bold'), bg='#F0F0F0')
page_2_lb.grid(row=0,  column=0, columnspan=4, padx=5,  pady=5)

#array for pages:
pages = [page_1, page_2]
print(count)
page = pages[count]
page.pack()

#funktions:
def Refill(): #next page
    global count
    for p in pages:
        p.pack_forget()
        
    count += 1
    page = pages[count]
    page.pack()
    return count

#bottons:
refill_btn=tk.Button(page_1,text='Refill', 
                     font=('Bold', 20),
                     bg='white',
                     width=8,
                     relief=GROOVE,
                     #command=Refill()
                     )
refill_btn.grid(row=2,  column=0, columnspan=4,  padx=5,  pady=5)


root.mainloop()