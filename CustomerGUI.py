import tkinter as tk
from tkinter import Tk
from tkinter import *
from PIL import ImageTk, Image

# root window
root = tk.Tk()
root.configure(background="light blue")
root.minsize(200, 200)  # width, height
root.maxsize(1000, 1000)
root.geometry("900x600+300+50") # width, height, placement on screen 
root.title('Design your phone')
root.resizable(0, 0)
phone = [0,0,0,1]  #(0=black, 1=blue, 2=white), 0-2 fuses, color, amount
count=0  #page
color= ['Black','Black', 'Black']


main_frame = tk.Frame(root, bg='light blue')

def color_chosen():
    global color
    n = range(3)
    for i in n:
        if phone[i]==0:
            color[i]='Black'
        if phone[i]==1:
            color[i]= 'Blue'
        if phone[i]==2:
            color[i]= 'White'
    return color

#Each page is defined
page_1 = tk.Frame(main_frame)
page_1_lb=tk.Label(page_1, text='Build your phone', font=('Times New Roman',30,'bold'), bg='light blue')
#image part:
img=Image.open('phone_assemp.png')
resize_img= img.resize((300,300))
page_1_img = ImageTk.PhotoImage(resize_img)
page_1_lb.pack()
page_1.pack()
label_img = tk.Label(page_1, image = page_1_img, fg='light blue', bg='light blue')
label_img.pack()

page_2 = tk.Frame(main_frame)
page_2_lb=tk.Label(page_2, text='Bottom cover color', font=('Times New Roman',30,'bold'), bg='light blue')
page_2_lb.pack()


page_3 = tk.Frame(main_frame)
page_3_lb=tk.Label(page_3, text='Number of fuses', font=('Times New Roman',30,'bold'), bg='light blue')
page_3_lb.pack()


page_4 = tk.Frame(main_frame)
page_4_lb=tk.Label(page_4, text='Top cover color', font=('Times New Roman',30,'bold'), bg='light blue')
page_4_lb.pack()

page_5 = tk.Frame(main_frame, bg='light blue')
page_5_lb=tk.Label(page_5, text='Congratulations with your phone design', font=('Times New Roman',30,'bold'),bg='light blue')
chosen_view=tk.Label(page_5, text='You have chosen the following:', font=('Times New Roman',20,'bold'),bg='light blue' )
chosen_top_cov=tk.Label(page_5, text='Top cover: ' + color[2], font=('Times New Roman',12,'bold'),bg='light blue' )
chosen_fuse_count=tk.Label(page_5, text='Fuses: ' + str(phone[1]), font=('Times New Roman',12,'bold'),bg='light blue' )
chosen_bot_cov=tk.Label(page_5, text='Bottom cover: ' + color[2], font=('Times New Roman',12,'bold'),bg='light blue' )
chosen_amount=tk.Label(page_5, text='Amount: ' + str(phone[3]), font=('Times New Roman',12,'bold'),bg='light blue' )
page_5_lb.pack()

page_6 = tk.Frame(main_frame)
page_6_lb=tk.Label(page_6, text='Your order has been recieved', font=('Times New Roman',30,'bold'), bg='light blue')
page_6_lb.pack()

#array for pages:
pages = [page_1, page_2, page_3, page_4, page_5, page_6]
page = pages[count]
page.pack(pady=100)

main_frame.pack(fill=tk.BOTH, expand=True)
 
#funktions
def hide_button(widget):
    # This will remove the widget from toplevel
    widget.pack_forget()
  
  
# Method to make Button(widget) visible
def show_button(widget):
    widget.pack_forget()
    # This will recover the widget from toplevel
    if widget==black_btn or widget==fuse_0:
        widget.pack(padx=0,pady=10)
    if widget==blue_btn or widget==fuse_1:
        widget.pack(padx=0,pady=10)
    if widget==white_btn or widget==fuse_2:
        widget.pack(padx=0,pady=10)
    
def Page_buttons():
    if count == 1 or count == 3:
        show_button(black_btn)
        show_button(blue_btn)
        show_button(white_btn)
        hide_button(fuse_0)
        hide_button(fuse_1)
        hide_button(fuse_2)
    if count == 2:
        show_button(fuse_0)
        show_button(fuse_1)
        show_button(fuse_2)
        hide_button(black_btn)
        hide_button(blue_btn)
        hide_button(white_btn)
    if count == 0 or count == 4:
        hide_button(black_btn)
        hide_button(blue_btn)
        hide_button(white_btn)
        hide_button(fuse_0)
        hide_button(fuse_1)
        hide_button(fuse_2)
        
#funktions
def move_next_page():
    global count
        
    color_chosen()
    #chosen_amount.configure(text='Amount of phones: ' + str(amount_chosen))
    chosen_view.configure(text='You have chosen the following:')
    chosen_top_cov.configure(text='Top cover: ' + str(color[2]))
    chosen_fuse_count.configure(text='Fuses: ' + str(phone[1]))
    chosen_bot_cov.configure(text='Bottom cover: ' + str(color[2]))
    chosen_view.pack(pady=30)
    chosen_amount.pack(pady=10)
    chosen_top_cov.pack(pady=10)
    chosen_fuse_count.pack(pady=10)
    chosen_bot_cov.pack(pady=10)
    
    if count==3:
        next_btn.configure(text='Done')
        back_btn.pack(side=tk.LEFT)
        
    if not count > len(pages)-2:
        for p in pages:
            p.pack_forget()
        count += 1
        page = pages[count]
        page.pack(pady=100)
        Page_buttons()
        return count
        


def move_back_page():
    global count
    
    if count== 4:
        next_btn.configure(text='Next')
        back_btn.pack(side=tk.LEFT)

    if not count ==  0:

        for p in pages:
            p.pack_forget()

        count -= 1
        page = pages[count]
        page.pack(pady=100)
        Page_buttons()
        return count
        
def set_black():
    global count
    phone[count-1]=0
    move_next_page()

def set_blue():
    global count
    phone[count-1]=1
    move_next_page()

def set_white():
    global count
    phone[count-1]=2
    move_next_page()

def set_fuse0():
    phone[1]=0
    move_next_page()
    
def set_fuse1():
    phone[1]=1
    move_next_page()
    
def set_fuse2():
    phone[1]=2
    move_next_page()
    
def Amount():
    try: 
        int(amount.get())
        phone[3]=amount.get()
        amount_label.configure(text='Amount of phones: '+ str(phone[3]))
        amount_label.place(x=645,y=25)
        chosen_amount.configure(text='Amount of phones: ' + str(phone[3]))
        chosen_amount.place()
        return phone[3]
    except ValueError:
        amount_label.configure(text='Amount of phones: '+ str(phone[3]))
        amount_label.place(x=645,y=25)
        


#frames:
bottom_frame = tk.Frame(root)

#Indput for amount:
amount_label=tk.Label(root, text='Amount of phones:', font=('ariel',16),bg='light blue')
amount = tk.Entry(root)
amount_label.place(x=645,y=25)
amount.place(x=650,y=50)

amount_btn=tk.Button(root,text= 'Chose amount',
                     font=('Bold',8),
                     bg='white',
                     relief=GROOVE,
                     command=Amount)
amount_btn.place(x=800 ,y=50)

#buttons page chance:
back_btn = tk.Button(bottom_frame,text='Back', 
                     font=('Bold', 20),
                     bg='white', 
                     width=8,
                     relief=GROOVE,
                     command=move_back_page)
back_btn.pack(side=tk.LEFT)

next_btn = tk.Button(bottom_frame, text='Next',
                     font=('Bold', 20),
                     bg='white',
                     width=8,
                     relief=GROOVE, 
                     command=move_next_page)
next_btn.pack(side=tk.RIGHT)

#bottoms for color:
black_btn = tk.Button(root,text='Black', 
                    font=('Bold', 20),
                    bg='black', fg='white', width=8,
                    command=set_black,
                    relief=GROOVE)


blue_btn = tk.Button(root,text='Blue', 
                    font=('Bold', 20),
                    bg='blue', fg='white', width=8,
                    command=set_blue,
                    relief=GROOVE)


white_btn = tk.Button(root, text='White', 
                    font=('Bold', 20),
                    bg='white', fg='black', width=8,
                    command=set_white,
                    relief=GROOVE)



#bottoms for fuses:

fuse_0 = tk.Button(main_frame,text='0', 
                    font=('Bold', 20),
                    bg='blue', fg='white', 
                    width=8,
                    command=set_fuse0,
                    relief=GROOVE)


fuse_1 = tk.Button(main_frame,text='1', 
                    font=('Bold', 20),
                    bg='blue', fg='white', 
                    width=8,
                    command=set_fuse1,
                    relief=GROOVE)


fuse_2 = tk.Button(main_frame, text='2', 
                    font=('Bold', 20),
                    bg='blue', fg='white', width=8,
                    command=set_fuse2,
                    relief=GROOVE)


#Images:


#placing frames:
bottom_frame.pack(side=tk.BOTTOM,pady=10)

root.mainloop()