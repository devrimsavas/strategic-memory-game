from tkinter import *
from PIL import Image,ImageTk
import os 

class Player:
    def  __init__(self,name,bg_image_filename):
        self.name=name
        self.taken_cards=[]
        self.player_box=None
        self.box_coords=[]
        self.player_box_x=00
        self.player_box_y=00
        self.center_x=00
        self.center_y=00
        self.player_score=0
        self.attack_score=0
        self.defence_score=0
        self.happiness_score=0
        self.defence_score=0
        self.bg_image_path=os.path.join('heroes',bg_image_filename)
        self.bg_photo=None
        self.load_image()

        self.taken_cards=[]

    def load_image(self):

        bg_image=Image.open(self.bg_image_path)

        #resize for player_box
        new_width=250
        new_height=170
        bg_image=bg_image.resize((new_width,new_height),Image.Resampling.LANCZOS)

        self.bg_photo=ImageTk.PhotoImage(bg_image)
        
    def draw_player_box(self,canvas,xp,yp,color): #start px,py=10,1030
        xp1,yp1=xp+250,yp+170

        #original here
        self.player_box=canvas.create_rectangle(xp,yp,xp1,yp1,outline=color,fill=color,width=0)
        self.player_bg=canvas.create_image(xp,yp,image=self.bg_photo,anchor=NW)

        
        self.player_label=canvas.create_text(xp+120,yp-20,text=self.name.upper(),font=('Corier',25),fill="white")
        self.box_coords=canvas.bbox(self.player_box)
        
        self.player_box_x=self.box_coords[0]
        self.player_box_y=self.box_coords[1]
        #self.player_box=canvas.create_rectangle(xp,yp,xp1,yp1,outline=color,fill=color,width=4)

    def draw_score_box(self,root,xp,yp,**kwargs):
        self.score_label=Label(root,text=f"{self.name}:{self.player_score}",font=("Calibri",18),borderwidth=0,relief="sunken",**kwargs)
        self.score_label.place(x=xp,y=yp)

        self.attack_label=Label(root,text=f"{self.name}:Attack Power:{self.attack_score}",font=("Calibri",12),borderwidth=0,**kwargs)
        self.attack_label.place(x=xp,y=yp+40)

        self.defence_label=Label(root,text=f"{self.name}:Defence Power:{self.defence_score}",font=("Calibri",12),borderwidth=0,**kwargs)
        self.defence_label.place(x=xp,y=yp+80)

        self.happiness_label=Label(root,text=f"{self.name}:Happiness:{self.happiness_score}",font=("Calibri",12),borderwidth=0,**kwargs)
        self.happiness_label.place(x=xp,y=yp+120)

    def update_attack_score(self):
        self.attack_label.config(text=f"{self.name}: Attack Power {self.attack_score}")

    def update_score_box(self):
        self.score_label.config(text=f"{self.name}:{self.player_score}")
        self.attack_label.config(text=f"{self.name}:Attack Power:{self.attack_score}")
        self.defence_label.config(text=f"{self.name}:Defense Power{self.defence_score}")
        self.happiness_label.config(text=f"{self.name}:Happiness:{self.happiness_score}")


    def apply_item_effect(self,item_dict,item_name):
        if item_name in item_dict:
            item_values=item_dict[item_name]
            self.attack_score+=item_values[0]
            self.defence_score+=item_values[1]
            self.happiness_score+=item_values[2]

    def show_taken_cards(self):
        if not self.taken_cards:
            print(f"{self.name} has no card yet")
            return f"{self.name} has no card yet"
        else:
            new_list=list(set(self.taken_cards))
            
            for card in new_list:  #self.taken_cards:
                print(card.name)

