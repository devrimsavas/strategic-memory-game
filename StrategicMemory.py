from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import random
import time
import os
from player_class import Player
from game_items import item_dict
from game_items import game_intro_text
from game_items import how_to_play
from game_items import about_text
import pygame



#card dimensions #need to make smaller to fit normal screen. 
CARD_WIDTH=80
CARD_HEIGHT=110
clicked_cards=[] # to compare 2 clicked cards
pygame.mixer.init()
global click_sound
global card_taken_sound
click_sound=pygame.mixer.Sound("click.wav")
card_taken_sound=pygame.mixer.Sound("card_taken.mp3")
intro_music=pygame.mixer.Sound("intro.mp3")

global graph_path # pictures folder.can be added new dynamically
graph_path="tiles3d" #this must be same with other path.... important 
global new_game 
new_game=False #false 


#this class will prepare user's taken card. 
class UserGraphic:
    def __init__(self, root,canvas, taken_card_name, labx, laby, labtext):
        self.root = root
        self.canvas=canvas
        self.taken_card_name = taken_card_name
        self.labx = labx
        self.laby = laby
        
        self.labtext = labtext
        self.image_name = None
        self.taken_image = None

    def user_cards_picture(self, **kwargs):
        self.image_name = os.path.join("tiles3d", self.taken_card_name) #check!!! graph_path must be same global later
        taken_image = Image.open(self.image_name)
        taken_image = taken_image.resize((80, 110), Image.Resampling.LANCZOS)
        self.taken_image = ImageTk.PhotoImage(taken_image)
        self.canvas.create_image(self.labx,self.laby,anchor=NW,image=self.taken_image)


#card class prepare cards on

class Card:
    def __init__(self, name, image_file_name,back_image_file):
        self.name = name
        self.image_file_name = image_file_name
        self.image_path = os.path.join(graph_path, self.image_file_name)
        self.shape = None  # Initialize shape item
        self.image_item = None  # Initialize image item
        self.hide_cards=True
        self.back_image_file=back_image_file
        self.back_image_path=os.path.join("back_graph_folder", back_image_file) #important

    def card_shape(self, canvas, x, y, **kwargs):
        self.x = x
        self.y = y

        if not self.shape:
            self.shape = canvas.create_rectangle(self.x, self.y, self.x + CARD_WIDTH, self.y + CARD_HEIGHT,
                                             fill="beige", width=0, outline="gray", **kwargs)

        if os.path.exists(self.image_path) and os.path.exists(self.back_image_path):
        # Open front image
            self.image = Image.open(self.image_path)
            self.image = self.image.resize((CARD_WIDTH, CARD_HEIGHT), Image.Resampling.LANCZOS)
            self.image_tk = ImageTk.PhotoImage(self.image)

        # Open back image
            self.back_image = Image.open(self.back_image_path)
            self.back_image = self.back_image.resize((CARD_WIDTH, CARD_HEIGHT), Image.Resampling.LANCZOS)
            self.back_image_tk = ImageTk.PhotoImage(self.back_image)

        # Decide which image to use
            if not self.image_item:
                if self.hide_cards:
                    self.image_item = canvas.create_image(self.x, self.y, image=self.back_image_tk, anchor=NW)
                else:
                    self.image_item = canvas.create_image(self.x, self.y, image=self.image_tk, anchor=NW)
            else:
                if self.hide_cards:
                    canvas.itemconfig(self.image_item, image=self.back_image_tk)
                else:
                    canvas.itemconfig(self.image_item, image=self.image_tk)
        else:
            messagebox.showerror("Error", "No such image")

        canvas.tag_bind(self.image_item, '<Button-1>', self.on_double_click)  # Double-Button-1 can be changed to double click...


    def on_double_click(self, event):
        global player_turn
        click_sound.play()
        turn_label.config(text=f"PLAYER {all_players[player_turn].name} Turn") 

        self.hide_cards = False  # Unhide the clicked card
        self.card_shape(canvas, self.x, self.y)  # Redraw the card to show the image
        canvas.update()  # Update the canvas immediately
        all_players[0].update_score_box() #unfortunately this is stupid solution but works
        all_players[1].update_score_box() 

        compare_label = None
        clicked_cards.append(self)
        print(self.name)

        if len(clicked_cards) == 2:
            print("It is player: " + all_players[player_turn].name)
            if clicked_cards[0] != clicked_cards[1]:
                if clicked_cards[0].name == clicked_cards[1].name:
                    print("The cards are the same")
                    compare_text = "Well Done"
                    card_taken_sound.play()
                    self.add_cards_to_player(clicked_cards)

                else:
                    print("The cards are different")
                    compare_text = ""
                    time.sleep(2)  # Delay to let players see the card before it gets hidden again
                    for card in clicked_cards:  # For both cards
                        card.hide_cards = True  # Hide the card
                        card.card_shape(canvas, card.x, card.y)  # Redraw the card to hide the image

                if compare_label:
                    canvas.itemconfigure(compare_label, text=compare_text)
                else:

                    pass
                canvas.update()

            else:
                print("Press another card")

                show_cards_label.config(text="Choose a different card")

            player_turn = (player_turn + 1) % 2  # player turn mod 2 #add bonus?? but not fair
            
            clicked_cards.clear()
        turn_label.config(text=f"PLAYER {all_players[player_turn].name} Turn")

    def add_cards_to_player(self, card_list):

        global all_players
        
        player = all_players[player_turn]
        player.player_score+=1
        player.apply_item_effect(item_dict,self.name)
        print(f"{player.name} Score {player.player_score}")
        all_players[0].update_score_box()
        all_players[1].update_score_box()

        single_list=list(set(card_list))

        for card in single_list:
            player.taken_cards.append(card)


        pop_up_cards(player,card)
            
        print(f"Player {all_players[player_turn].name} gets cards")
        print(f'Before add_cards_to_player, player_box: {player.player_box}')
        
        
        coord_player_box=canvas.bbox(player.player_box) #get coords of player box

        if coord_player_box is None:
            print("ERROR :NO BOX ")
            #i found temporary solution fixed points for card animation :( it works but not i wanted
            #player.player_box=draw_player_box()
            coord_player_box=canvas.bbox(player.player_box)

        center_x=750
        center_y=1100

        
        for card in card_list:
            dx=center_x-card.x
            dy=center_y-card.y
            card.move_card(canvas, dx, dy)
            #delete card?
            card.delete_card(canvas)
        

    def delete_card(self,canvas):
        #activate here if need to delete cards
        canvas.delete(self.shape)
        canvas.delete(self.image_item)

    def move_card(self, canvas, dx, dy):
        
        num_steps = 10
        delay = 32
        step_x = dx / num_steps
        step_y = dy / num_steps

        canvas.tag_raise(self.shape)
        canvas.tag_raise(self.image_item)

        for _ in range(num_steps):
            canvas.move(self.shape, step_x, step_y)
            canvas.move(self.image_item, step_x, step_y)
            
            self.x += step_x
            self.y += step_y
            canvas.update()
            time.sleep(delay / 1000)
            canvas.tag_unbind(self.image_item, '<Button-1>')
            canvas.tag_unbind(self.shape, '<Button-1>')

# END OF CARD CLASS



#initialize game list
main_list=[] #hold all graphics files name
graphic_name_list=[] #hold all graphics
global player_turn
player_turn=0
global all_players
all_players=[] #we will set player names here. so cards will go to players box 

#allocate directory and create a file list of *.png

def load_cards():
    main_list.clear()
    directory=os.path.join(os.getcwd(),'tiles_theme_blue') # 'tiles_theme_blue') #        'graph_set') #set directory 
    png_files=[file for file in os.listdir(directory) if file.endswith('.png')] #find png files

    #put all png files to main_list
    for file_name in png_files:
        main_list.append(file_name)

x_start,y_start=10,10
total_cards=[]


def generate_match_cards(amount):
    selected_cards_list=[]
    random.shuffle(main_list)
    for _ in range(amount*2): # to ignore we do not care 
        selected_cards_list.append(main_list.pop())
        
    #we need 2 of same card
    selected_cards_list*=2
    random.shuffle(selected_cards_list)

    return selected_cards_list

def show_cards(cards_list):
    global x_start,y_start,total_cards
    #selected_cards_list=[]
    for i in range(len(cards_list)):
        index=cards_list.pop()
        value=index.replace(".png","")

        card=Card(value,index,'backface1.png') #card back here
        total_cards.append(card)
        card.card_shape(canvas,x_start,y_start)
        x_start=(x_start+100)%1460 #x x-50 1460 1410 
        if x_start==1410:
            y_start+=120
            x_start=10

def prepare_cards():
    clicked_cards.clear()
    global x_start,y_start
    x_start,y_start=10,10
    canvas.delete("all")
    load_cards()
    match_cards=generate_match_cards(28)
    show_cards(match_cards)


def create_players():
    global show_cards_label
    print("create player test")

    player_1=Player("DEVRIM","player1x.png")
    player_1.draw_player_box(canvas,10,1035,"red")
    player_2=Player("MALIN ","player2x.png")
    player_2.draw_player_box(canvas,1143,1035,"blue")

    all_players.append(player_1)
    all_players.append(player_2)

    print(all_players[1].name)

    all_players[0].taken_cards.clear()
    all_players[1].taken_cards.clear()

    score_holder=Label(root,width=110,height=11,borderwidth=0,bg=holder_back_color)
    score_holder.place(x=410,y=1063) #410 1063
    player_1.draw_score_box(score_holder,10,10,bg=root_color,fg="white")
    player_2.draw_score_box(score_holder,560,10,bg=root_color,fg="white")
    
    #border for game area and player info
    border=canvas.create_line(0,990,1400,990,fill="#8adcaf",width=4)

new_game=False 

def start_new_game():
    
    global candle_image_id
    button_start.destroy
    global new_game
    new_game=True
    intro_music.stop() #here need another music track
    global turn_label
    
    turn_label=Label(root,width=0,bg=root_color,fg="white",font=("Gothic",16,"bold")) 
    turn_label.place(x=630,y=1030)
 
    global show_cards_label
    
    if new_game:
        #show_cards_label.config(text="GAME STARTED")
        pass
    global player_turn
    player_turn=0
    prepare_cards()
    create_players()

    
    new_game=True 

    print(new_game) #console test
    player_1_cards.config(bg="#170426",fg="red")
    player_2_cards.config(bg="#170426",fg="blue")

def about_game():

    global about_text
    about_window=Toplevel(root)

    about_window.title("About Game")
    about_window.geometry("600x500")
    about_window.config(bg="beige")
    
    info_text = Text(about_window, width=60, height=20,bg="#1704ff", fg="white", wrap=WORD, borderwidth=3, spacing3=2, font=("Arial",12 ))
    info_text.place(x=10, y=10)
    info_text.insert(END, about_text)
    info_text.config(state="disabled", bg="#170fff")
    close_this = Button(about_window, text="CLOSE THIS WINDOW",font=("cooper black",14 ), command=about_window.destroy)
    close_this.place(x=190, y=450)

def exit_game():
    quit_game=messagebox.askyesno("Quit Game","Do you want to quit (y/n) ?")
    if quit_game:
        root.destroy()
    else:
        pass

def tile_set():
    #add later #add different tile set 
    pass


def game_rules():
    global how_to_play
    rules_window=Toplevel(root)
    rules_window.geometry("920x1000")
    rules_window.title("GAME RULES")
    rules_window.config(bg="#170426") #170426 this is root color 
    
    test_text=how_to_play
    
    rules_text=Text(rules_window,width=80,height=40,wrap="word",fg="black",borderwidth=3,bg="#7dc9d9",spacing3=2,font=("Arial",14,"bold"))
    rules_text.place(x=10,y=10)
    rules_text.insert("1.0",test_text)
    rules_text.config(state="disabled")


    rules_window.mainloop()

    
def pop_up_cards(player,card):  #pop_up_cards(player,card)

    root_c=Toplevel(root)
    root_c.geometry("500x400")
    root_c.title("CARD VALUE")
    root_c.config(bg="#ADD8E6") #170426")root color

    im_name="tiles_theme_blue/"+card.name+".png"

    taken_image = Image.open(im_name)
    taken_image = taken_image.resize((80,120),Image.Resampling.LANCZOS)
    take_image = ImageTk.PhotoImage(taken_image)

    text_holder = LabelFrame(root_c, text="CARD INFO", width=490, height=390, bg="#170426")
    text_holder.place(x=5, y=5)

    label = Label(text_holder, text=f"{player.name.upper()} TAKES {card.name}", font=("Gothic",20), fg="white", bg="#170426")
    label.place(x=100, y=15)

    im_label = Label(text_holder, text="pic", borderwidth=5)
    im_label.image = take_image  # set the image as an attribute of the label
    im_label['image'] = im_label.image  # set the image option to be the image we just defined
    im_label.place(x=200, y=50)

    info_label=Label(root_c,text=f"{item_dict[card.name][3]}",width=45,height=5,font=("Gothic",14),fg="white",bg="#170426")
    info_label.place(x=25,y=200)

    #root_c.update()
    root_c.after(5000,root_c.destroy)

def intro_screen():
    intro_music.play()
    
    #root color=#170426
    #global test_picture
    global new_game
    global root,root_color,canvas,game_intro_text
    global test_picture

    if new_game:
        print("-test new game started")
        return
    else:
        
        def scroll_text():
           
            nonlocal text_id, y_threshold
            canvas.move(text_id, 0, -1)
            bbox = canvas.bbox(text_id)
            if bbox and bbox[3] < y_threshold:
                
                canvas.delete(text_id)
                text_id = canvas.create_text(780, 2200, font=("Old English Text MT", 20, "bold"), fill="#170426", text=game_intro_text, anchor="s")
            root.after(40, scroll_text)

        text_intro=game_intro_text
        text_id=canvas.create_text(780,2200,font=("Old English Text MT",20,"bold"), fill="#170426", text=game_intro_text, anchor="s")

        y_threshold=300
        scroll_text()
        test_picture=Image.open("backface1.png")
        test_picture=test_picture.resize((1200,1200),Image.Resampling.LANCZOS)
        test_picture=ImageTk.PhotoImage(test_picture)
        #canvas.create_image(740,300,image=test_picture)

def show_player_cards(player):
    global root

    if player is None:
        print(f"GAME NOT STARTED")
        return

    for card in player.taken_cards:
        print(card.name)

    # Player cards show
    root_show = Toplevel(root)
    root_show.geometry("620x800")
    root_show.title(f"{player.name}")
    root_show.config(bg="#170426")

    canvas = Canvas(root_show, width=590, height=680, bg="#170426", relief="sunken", borderwidth=3)
    canvas.place(x=10, y=10)

    # Store instances of UserGraphic in a list
    user_graphics = []

    player_taken_cards_x = 0
    player_taken_cards_y = 0

    for card_taken in player.taken_cards:
        file_name_png = card_taken.name + ".png"
        file_name = card_taken.name
        p_taken_graphic = UserGraphic(root_show, canvas, file_name_png, player_taken_cards_x, player_taken_cards_y, file_name)
        user_graphics.append(p_taken_graphic)  # Add each instance to the list
        p_taken_graphic.user_cards_picture()

        player_taken_cards_x += 90

        print(file_name_png, file_name)
        print(player_taken_cards_x, player_taken_cards_y)

    rbutton = Button(root_show, text="close", command=root_show.destroy)
    rbutton.place(x=300, y=750)
    root_show.mainloop()

#MAINLOOP
    
#TKINTER
root_color="#170426"
root=Tk()
root.geometry('1600x1300')
root.resizable(False,False)
root.title("VENI VIDI MEMORY V1")
root.config(bg=root_color)
root.iconbitmap("dragonicon.ico")
#set an background image
bg=Image.open("wooden-texture.png") #background.png #root whole screen
bg=bg.resize((1600,1300),Image.Resampling.LANCZOS)
bg_image=ImageTk.PhotoImage(bg)


bg_label=Label(root,image=bg_image)
bg_label.place(x=0,y=0,relwidth=1,relheight=1)

#image for box
intro_image=Image.open("intro8.png") #intro graphic
intro_image=intro_image.resize((1400,1220),Image.Resampling.LANCZOS)
intro_image=ImageTk.PhotoImage(intro_image)

#cards canvas
canvas_color="#c18eff"
canvas=Canvas(root,width=1400,height=1220,bg=root_color,highlightthickness=0,relief="sunken",borderwidth=3) #maybe solid color
canvas.place(x=100,y=30)

canvas.create_image(0,0,anchor=NW, image=intro_image) 


score_image=Image.open("holder_image.png")
score_image=score_image.resize((210,111),Image.Resampling.LANCZOS)
score_image=ImageTk.PhotoImage(score_image)


global turn_label 

#text for compare cards
#score and info label
holder_back_color=root_color  #root_color

if new_game:
    score_holder=Label(root,width=110,height=11,borderwidth=0,bg=holder_back_color)
    score_holder.place(x=410,y=1063)
    show_cards_label=Label(score_holder,text="START A GAME ",font=("Gothic",30),bg="white",anchor="c",borderwidth=0)
    show_cards_label.place(x=170,y=200)
#intro box
#intro check

if new_game==False:
    intro_screen()

#MENU BAR
menubar=Menu(root)
gamemenu=Menu(menubar,tearoff=0,font=("Terminal",16))
menubar.add_cascade(label="Game",menu=gamemenu,font=("Terminal",16))

gamemenu.add_command(label="New Game",command=lambda:start_new_game())
gamemenu.add_command(label="Exit Game",command=lambda:exit_game())

aboutmenu=Menu(menubar,tearoff=0,font=("Terminal",16))

menubar.add_cascade(label="About",menu=aboutmenu,font=("Terminal",16))
aboutmenu.add_command(label="About",command=lambda:about_game())
aboutmenu.add_command(label="Rules",command=lambda:game_rules())

optionsmenu=Menu(menubar,tearoff=0,font=("Terminal",16))
menubar.add_cascade(label="Options",menu=optionsmenu,font=("Terminal",16))
optionsmenu.add_command(label="Tile Set",command=lambda:tile_set())
root.config(menu=menubar)

#show cards button

player_1_cards=Button(root,text="PLAYER CARDS",font=("Gothic",14),borderwidth=0, bg="#170426",fg="#170426",command=lambda:show_player_cards( all_players[0]))
player_1_cards.place(x=170,y=1220)

player_2_cards=Button(root,text="PLAYER CARDS",font=("Gothic",14), borderwidth=0,bg="#170426",fg="#170426",command=lambda:show_player_cards( all_players[1]))
player_2_cards.place(x=1320,y=1220)


def on_enter(event):
    event.widget.config(fg="yellow",font=("Old English Text MT",46))

def on_leave(event):
    event.widget.config(fg="green",bg="#170426",font=("Old English Text MT",36))


button_start=Button(root,text="START GAME",font=("Old English Text MT",36),fg="green",bg="#170426",borderwidth=0,command=lambda:start_new_game())
button_start.place(x=810,y=1100,width=480,height=80,anchor="center")

button_start.bind("<Enter>",lambda event:on_enter(event))
button_start.bind("<Leave>",lambda event:on_leave(event))


#END MENU BAR 
root.mainloop()

#END GAME 
