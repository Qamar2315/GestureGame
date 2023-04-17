import pygame
import cv2
import handTrackingModule
import random
import sqlite3 as sql

pygame.init()
pygame.mixer.init()

width, height= 520,720
window= pygame.display.set_mode((width,height))
pygame.display.set_caption("Whirley Bird")
clock=pygame.time.Clock()
FPS=60

#webcam
cap= cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

#handdectector
detector= handTrackingModule.handDetector()

#colors
red=(255,0,0)
blue=(0,0,255)
green=(0,128,0)
orange=(255,165,0)

#loading backgrounds
gameoverBg= pygame.image.load("assets/backgrounds/back.jpg")
gameoverBg= pygame.transform.scale(gameoverBg,(width,height)).convert_alpha()

welcomeBg= pygame.image.load("assets/backgrounds/frontbg.jpg")
welcomeBg= pygame.transform.scale(welcomeBg,(width,height)).convert_alpha()

gameBg= pygame.image.load("assets/backgrounds/back.png")
gameBg= pygame.transform.scale(gameBg,(width,height)).convert_alpha()

pausedBg= pygame.image.load("assets/backgrounds/pausedbg.jpg")
pausedBg= pygame.transform.scale(pausedBg,(width,height)).convert_alpha()

pauseBtn= pygame.image.load("assets/buttons/pa.png")
pauseBtn= pygame.transform.scale(pauseBtn,(90,90)).convert_alpha()
pauseBtnRect=pauseBtn.get_rect()
pauseBtnRect.x=420
pauseBtnRect.y=8

#loading buttons
start_= pygame.image.load("assets/buttons/start.png")
start_rect=start_.get_rect()
start_rect.x=110
start_rect.y=250

score_= pygame.image.load("assets/buttons/score.png")
score_rect=start_.get_rect()
score_rect.x=110
score_rect.y=360

exit_= pygame.image.load("assets/buttons/exit.png")
exit_rect=start_.get_rect()
exit_rect.x=110
exit_rect.y=450

restart_= pygame.image.load("assets/buttons/resume.png")
restart_rect=start_.get_rect()
restart_rect.x=110
restart_rect.y=250

menu_= pygame.image.load("assets/buttons/restart.png")
menu_rect=start_.get_rect()
menu_rect.x=110
menu_rect.y=320

#loading objects
spriteImg=pygame.image.load("assets/objects/pngegg.png")
spriteImg= pygame.transform.scale(spriteImg,(70,70)).convert_alpha()
spriteImgeRect=spriteImg.get_rect()
spriteImgeRect.x=100
spriteImgeRect.y=600

fruitImg=pygame.image.load("assets/objects/apple.png")
fruitImg= pygame.transform.scale(fruitImg,(50,50)).convert_alpha()

#connecting database and getting highest score
def gethighScore():
    conn= sql.connect("database/gameScores.db")
    c=conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS 
        scores(
            score INTEGER    
        )
    """)
    c.execute("select score FROM scores WHERE rowid=1")
    result=c.fetchall()
    conn.commit()
    conn.close()
    return result[0][0]

highScore=gethighScore()

#this method will return a random block
def getRandomRect(x):
    return pygame.Rect(random.randint(100,500),x,random.randint(50,250),20)

#this will return a random fruit and dimensions of its rectangle
def getRandomFruit(y):
    fruitRect= fruitImg.get_rect()
    fruitRect.x=random.randint(100,500)
    fruitRect.y=y
    return fruitImg,fruitRect

#this will blit given text on screen 
def text_screen(text,color,x,y,z=80):
    font= pygame.font.Font("fonts/BebasNeue-Regular.otf",z)
    screen_text= font.render(text,True,color)
    window.blit(screen_text,(x,y))

#welcome window 
def welcomeWindow():
        pygame.mixer.music.load('sounds/No Love - Karaoke ! instrumental.mp3')
        pygame.mixer.music.play()
        exitGame= False
        window.blit(welcomeBg,(0,0))
        window.blit(start_,start_rect)
        window.blit(score_,score_rect)
        window.blit(exit_,exit_rect)
        text_screen("designed and developed by Qamar Ul Islam",orange,50,670,30)
        while not exitGame :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame=True
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if start_rect.collidepoint(x, y):
                        pygame.mixer.music.pause()
                        pygame.mixer.music.load('sounds/interface-124464.mp3')
                        pygame.mixer.music.play()
                        gameLoop()
                    if score_rect.collidepoint(x, y):
                        window.fill((0,0,0))
                        pygame.mixer.music.pause()
                        pygame.mixer.music.load('sounds/interface-124464.mp3')
                        pygame.mixer.music.play()
                        score()
                    if exit_rect.collidepoint(x, y):
                        pygame.mixer.music.pause()
                        pygame.mixer.music.load('sounds/interface-124464.mp3')
                        pygame.mixer.music.play()
                        pygame.quit()
                    

            pygame.display.update()
            clock.tick(FPS)

#gameover window
def gameOver():
    pygame.mixer.music.load('sounds/mixkit-funny-game-lose-tone-2877.wav')
    pygame.mixer.music.play()
    exitGame= False
    while not exitGame :
        window.blit(gameoverBg,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key== pygame.K_SPACE:
                    gameLoop()
                if event.key == pygame.K_ESCAPE:
                    welcomeWindow()
            
        pygame.display.update()
        clock.tick(FPS)

#pausescreen window
def pauseScreen(scr,velo,gOver):
    pygame.mixer.music.load('sounds/interface-124464.mp3')
    pygame.mixer.music.play()
    exitGame= False
    while not exitGame :
        window.blit(pausedBg,(0,0))
        window.blit(restart_,restart_rect)
        window.blit(menu_,menu_rect)
        window.blit(exit_,exit_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if restart_rect.collidepoint(x, y):
                        pygame.mixer.music.load('sounds/interface-124464.mp3')
                        pygame.mixer.music.play()
                        gameLoop(scr,velo,gOver)
                    if menu_rect.collidepoint(x, y):
                        pygame.mixer.music.load('sounds/interface-124464.mp3')
                        pygame.mixer.music.play()
                        gameLoop()
                    if exit_rect.collidepoint(x, y):
                        pygame.mixer.music.load('sounds/interface-124464.mp3')
                        pygame.mixer.music.play()
                        welcomeWindow()

        pygame.display.update()
        clock.tick(FPS)

#score window
def score():
    exitGame= False
    while not exitGame :
        text_screen("HIGHEST SCORE",red,40,90,100)
        text_screen(str(gethighScore()),red,190,230,200)
        text_screen("PRESS ESCAPE",red,160,500,50)
        text_screen("     OR",red,180,550,50)
        text_screen("SPACEBAR TO EXIT",red,130,600,50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    welcomeWindow()
                if event.key == pygame.K_SPACE:
                    welcomeWindow()
        pygame.display.update()
        clock.tick(FPS)

#this method will update highscore in the database if it is smaller greator than current 
def updateHighscore(score):
    #connecting database
    conn= sql.connect("database/gameScores.db")
    c=conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS 
        scores(
            score INTEGER    
        )
    """)
    c.execute(f"UPDATE scores SET score={score} WHERE rowid=1")
    conn.commit()
    conn.close()

#main gameloop
def gameLoop(scr=0,velo=5,gOver=False):
    block1=getRandomRect(100)
    block2=getRandomRect(300)
    block3=getRandomRect(500)

    fruit1,fruit1Rect=getRandomFruit(150)
    fruit2,fruit2Rect=getRandomFruit(250)
    fruit3,fruit3Rect=getRandomFruit(550)

    score=scr
    exitGame=False
    pauseGame=False
    gameOver_=gOver
    y_velocity=velo
    while not exitGame:
        sprite_x=0
        success,img= cap.read()
        img,hands=detector.findHands(img,True)
        if hands:
            pos=detector.findPosition(img,0,False)
            position=pos[9]
            sprite_x,y= position[1], position[2]
        if gameOver_:
            if score> highScore:
                updateHighscore(score)
            pygame.mixer.music.pause()
            gameOver()
        if pauseGame:
            pygame.mixer.music.pause()
            pauseScreen(score,y_velocity,gameOver_)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key== pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    pauseScreen(score,y_velocity,gameOver_)
            if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if pauseBtnRect.collidepoint(x, y):
                        pygame.mixer.music.pause()
                        pauseScreen(score,y_velocity,gameOver_)

        if (score%10 == 0) and score>0:
            y_velocity+=5
            score+=1
        spriteImgeRect.x= sprite_x
        block1.y += y_velocity
        block2.y += y_velocity
        block3.y += y_velocity
        fruit1Rect.y += y_velocity
        fruit2Rect.y += y_velocity
        fruit3Rect.y += y_velocity
        if block1.y > height:
            block1=getRandomRect(100)
            block1.y = 0

        if block2.y > height:
            block2=getRandomRect(300)
            block2.y = 0
        if block3.y > height:
            block3=getRandomRect(500)
            block3.y = 0

        if fruit1Rect.y > height:
            fruit1,fruit1Rect=getRandomFruit(300)
            fruit1Rect.y = 0
        if fruit2Rect.y > height:
            fruit2,fruit2Rect=getRandomFruit(500)
            fruit2Rect.y = 0
        if fruit3Rect.y > height:
            fruit3,fruit3Rect=getRandomFruit(800)
            fruit3Rect.y = 0


        window.blit(gameBg,(0,0))
        window.blit(spriteImg,spriteImgeRect)
        window.blit(fruit1,fruit1Rect)
        window.blit(fruit2,fruit2Rect)
        window.blit(fruit3,fruit3Rect)
        window.blit(pauseBtn,pauseBtnRect)
        pygame.draw.rect(window,orange,block1)
        pygame.draw.rect(window,orange,block2)
        pygame.draw.rect(window,orange,block3)

        if spriteImgeRect.colliderect(fruit1Rect):
            pygame.mixer.music.load("sounds/message-13716.mp3")
            pygame.mixer.music.play()
            fruit1Rect.width=0
            fruit1Rect.height=0
            fruit1Rect.y=1000
            score+=1

        elif spriteImgeRect.colliderect(fruit2Rect):
            pygame.mixer.music.load("sounds/message-13716.mp3")
            pygame.mixer.music.play()
            fruit2Rect.width=0
            fruit2Rect.height=0
            fruit2Rect.y=1000
            score+=1

        elif spriteImgeRect.colliderect(fruit3Rect):
            pygame.mixer.music.load("sounds/message-13716.mp3")
            pygame.mixer.music.play()
            fruit3Rect.width=0
            fruit3Rect.height=0
            fruit3Rect.y=1000
            score+=1
        
        if spriteImgeRect.colliderect(block1) or spriteImgeRect.colliderect(block2) or spriteImgeRect.colliderect(block3):
            gameOver_=True
        if score>highScore:
            text_screen("Hi score: ",red,0,0)
            text_screen(str(score),red,300,0)
        else:
            text_screen("Score: ",red,0,0)
            text_screen(str(score),red,280,0)

        pygame.display.update()
        clock.tick(FPS)

def main():
    try:
        welcomeWindow()
    except Exception as e:
        print("FAILED TO RUN THE GAME BECAUSE OF ERROR: ")
        print(e)
        
#running main method
if __name__ == "__main__":
    main()