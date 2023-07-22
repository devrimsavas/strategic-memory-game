when i wanted to make a memory game, my aim was to create an easy simple demo for beginner. But now it became  a strategical memory game. when you develop a game , take an easy concept and use your imaginary. and write game journal as follows: 

first, i needed some shapes, i decided to use photoshop's builtin custom shapes. At the very first version of this game, i used  these tiles . However, i did not like . Random shapes, no meaning. And suddenly i thought this game might have some strategical elements. Therefore, i needed a theme. I decided for medieval theme. Normally if you want to sell your game, you need to buy graphic set or you need to draw all of them but  I found some graphics for both tiles and other graphics. I prepared them with photoshop for my aim. Anyway, tile set can be easly changed. I found a medieval sound track from free library and added this. 

technic: inorder to keep main code simple, i had to divide game into 3 files. Player_Class creates players, game_items includes game dictionary and other texts used in game. I had to use some trick due to python Tkinter limitation. 

game play: You can play solo or two persons. Player can collect, defense, attack or wellfare cards. Each card has its own value. At intro screen player can start a new game from menu or easly press start game text. Show cards buttons show players card. Rules menu show the value of each card. 

issues: I made a huge mistake when i started to write game. in order to see tiles better, i made them a bit bigger (80x110) but now the problem is about game board size. the height is 1300 pixels , it means game does not fit a regular screen. I did not understand my mistake since i have a big screen. Python is not ideal to create game actually. The perfect solution is to use unity engine. I still did not write game over screen but when there is not any tiles on the board no crash. simply , players can collect their point. Game has not total score calculator. Total score should be based on defense, attack and wellfare scores. But i did not think of it yet. 
Another important problem is click speed. Player should be patient to click on cards. Othercase, it can create problem. card opening time can be changed. 
there was a bug which i detected but i could not solve. but i made a tricky solution which by-pass the code causes problem. 
I did not add another tile set although i added to menu. 

Further ideas: The game table should be smaller size. It means tiles should be smaller. When game starts, defense, attack and wellfare can be assigned by dice rolling. Player names should be dynamic and players can write their name. No need hardcoded. I will make board and tiles smaller soon. 


