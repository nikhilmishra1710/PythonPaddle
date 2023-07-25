import pygame

pygame.font.init()

SCORE_TEXT=pygame.font.SysFont('comicsans',30)
MENU_TEXT=pygame.font.SysFont('Consolas',25,True)
HEAD_TEXT=pygame.font.SysFont('garamond',50,True,True)
height,width=500,1000
window=pygame.display.set_mode((width,height))
pygame.display.set_caption="Game"
WHITE=(255,255,255)
BLUE=(0,98,255)
YELLOW=(234,255,0)

VEL=5
BALL_VEL=[3,3]

PLAYER1_MISS=pygame.USEREVENT+1
PLAYER2_MISS=pygame.USEREVENT+2
PLAYER1_NAME=PLAYER2_NAME=''

TOTAL_HITS=HITS=1

def update():
    pygame.display.update()

def draw_environment(player1,player2,ball,score1,score2):
    global PLAYER1_NAME,PLAYER2_NAME
    x=window.get_width()//2-2
    pos=[(x,0),(x,110),(x,220),(x,330),(x,440)]
    height,width=90,4    
   
    window.fill((0,0,0))
    text1=SCORE_TEXT.render(PLAYER1_NAME+": "+str(score1),1,(0,255,0))
    window.blit(text1,(window.get_width()//2-text1.get_width()-10,10))
    text2=SCORE_TEXT.render(PLAYER2_NAME+": "+str(score2),1,(0,255,0))
    window.blit(text2,(window.get_width()//2+10,10))
    for i in pos:
        rectangle=pygame.Rect(i[0],i[1],width,height)
        pygame.draw.rect(window,(0,255,0),rectangle)
    
    pygame.draw.rect(window,(255,255,255),player1,border_radius=5)
    pygame.draw.rect(window,(255,255,255),player2,border_radius=5)
    pygame.draw.rect(window,(255,0,0),ball,border_radius=10)
    
    update()

def handle_movement(player1,player2,keypress):
    if keypress[pygame.K_w] and player1.y>0:
        player1.y-=VEL
    if keypress[pygame.K_s] and player1.y<window.get_height()-player1.height:
        player1.y+=VEL
    if keypress[pygame.K_UP] and player2.y>0:
        player2.y-=VEL
    if keypress[pygame.K_DOWN] and player2.y<window.get_height()-player2.height:
        player2.y+=VEL

def ball_movement(player1,player2,ball):
    global BALL_VEL,TOTAL_HITS,HITS
    if HITS%8==0:
        HITS=1
        print("Speed increment")
        if BALL_VEL[0]>0:
            BALL_VEL[0]+=1
        else:
            BALL_VEL[0]-=1
        if BALL_VEL[1]>0:
            BALL_VEL[1]+=1
        else:
            BALL_VEL[1]-=1
        print(BALL_VEL)
    if ball.y<=0:
        BALL_VEL[1]*=(-1)
    if ball.y>=500 - ball.height:
        BALL_VEL[1]*=(-1)
    if player1.colliderect(ball):
        TOTAL_HITS+=1
        HITS+=1
        BALL_VEL[0]*=-1
    if player2.colliderect(ball):
        TOTAL_HITS+=1
        HITS+=1
        BALL_VEL[0]*=-1
    
    if ball.x<=0:
        pygame.event.post(pygame.event.Event(PLAYER1_MISS))
        pygame.time.delay(1000)
        ball.x=window.get_width()//2-10
        ball.y=window.get_height()//2-10
        HITS=1
        BALL_VEL=[3,3]
        print("miss",HITS)
        
    if ball.x>=window.get_width() - ball.width:
        pygame.event.post(pygame.event.Event(PLAYER2_MISS))
        pygame.time.delay(1000)
        ball.x=window.get_width()//2-10
        ball.y=window.get_height()//2-10
        HITS=1
        BALL_VEL=[3,3]
        
    ball.x+=BALL_VEL[0]
    ball.y+=BALL_VEL[1]    

def game():
    PLAYER1_POINT=PLAYER2_POINT=0
    player1=pygame.Rect(10,0,15,80)
    player2=pygame.Rect(window.get_width()-15-10,0,15,80)
    ball=pygame.Rect(window.get_width()//2-10,window.get_height()//2-10,20,20)
    clk=pygame.time.Clock()
    run=True
    while run:
        clk.tick(60)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                print(event.pos)
            if event.type==PLAYER1_MISS:
                PLAYER2_POINT+=1
            if event.type==PLAYER2_MISS:
                PLAYER1_POINT+=1
                
               
        keypress=pygame.key.get_pressed()
        ball_movement(player1,player2,ball)
        handle_movement(player1,player2,keypress)
        draw_environment(player1,player2,ball,PLAYER1_POINT,PLAYER2_POINT)

inc,i=1,1
flicker=1

def draw_mainmenu(player1,player2,text1,field1,text2,field2,selected):
    menu_bg=(255,0,0)
    window.fill(menu_bg)
    head_render=HEAD_TEXT.render("2 PLAYER PONG",1,WHITE)
    window.blit(head_render,(window.get_width()//2-head_render.get_width()//2,20))
        
    text_render1=MENU_TEXT.render("ENTER PLAYER 1 NAME",1,WHITE)
    pygame.draw.rect(window,menu_bg,text1,border_radius=5)
    window.blit(text_render1,(text1.x+5,text1.y+3))
    
    text_render2=MENU_TEXT.render(player1,1,WHITE)
    pygame.draw.rect(window,(161,159,159),field1,border_radius=5)
    window.blit(text_render2,(window.get_width()//2-text_render2.get_width()//2,field1.y+3))
    
    text_render3=MENU_TEXT.render("ENTER PLAYER 2 NAME",1,WHITE)
    pygame.draw.rect(window,menu_bg,text2,border_radius=5)
    window.blit(text_render3,(text2.x+5,text2.y+3))
    
    text_render4=MENU_TEXT.render(player2,1,WHITE)
    pygame.draw.rect(window,(161,159,159),field2,border_radius=5)
    window.blit(text_render4,(window.get_width()//2-text_render4.get_width()//2,field2.y+3))
    
    global flicker
    if(flicker==180):
        flicker=1
    
    if flicker>=121:
        text_render5=MENU_TEXT.render("PRESS ENTER KEY TO CONTINUE",1,WHITE)
    elif flicker>=61 and flicker<=120:
        text_render5=MENU_TEXT.render("PRESS ENTER KEY TO CONTINUE",1,YELLOW)
    elif flicker>=1 and flicker<=60:
        text_render5=MENU_TEXT.render("PRESS ENTER KEY TO CONTINUE",1,BLUE)
    
    flicker+=1
    window.blit(text_render5,(window.get_width()//2-text_render5.get_width()//2,window.get_height()-text_render5.get_height()-10))
    
    global inc,i
    if i==60:
        inc=-2
    if i==0:
        inc=1
    i+=inc
    if selected=="field1":
        POINTER=pygame.Rect(window.get_width()//2-text_render2.get_width()//2+text_render2.get_width(),field1.y+3,2,25)
        if inc==1:
            pygame.draw.rect(window,WHITE,POINTER)
        else:
            pygame.draw.rect(window,(161,159,159),POINTER)
    elif selected=="field2":
        POINTER=pygame.Rect(window.get_width()//2-text_render4.get_width()//2+text_render4.get_width(),field2.y+3,2,25)
        if inc==1:
            pygame.draw.rect(window,WHITE,POINTER)
        else:
            pygame.draw.rect(window,(161,159,159),POINTER)

    update()
        
def mainmenu():
    max=6
    cursor = pygame.cursors.compile(pygame.cursors.textmarker_strings)
    width,height=270,31
    global PLAYER1_NAME,PLAYER2_NAME
    PLAYER1_NAME=PLAYER2_NAME=selected=''
    clk=pygame.time.Clock()
    text1=pygame.Rect(window.get_width()//2-width//2,150,width,height)
    field1=pygame.Rect(window.get_width()//2-(width-100)//2,200,width-100,height)
    text2=pygame.Rect(window.get_width()//2-width//2,270,width,height)
    field2=pygame.Rect(window.get_width()//2-(width-100)//2,330,width-100,height)
    run=True
    while run:
        clk.tick(60)
        for event in pygame.event.get():
            if event.type==pygame.MOUSEMOTION:
                if ((event.pos[0] >= field1.x and event.pos[0] <=field1.x+field1.width and event.pos[1]>= field1.y and event.pos[1]<=field1.y+field1.height) or 
                (event.pos[0] >= field2.x and event.pos[0] <=field2.x+field2.width and event.pos[1]>= field2.y and event.pos[1]<=field2.y+field2.height)):
                    pygame.mouse.set_cursor((8, 16), (0, 0), *cursor)
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
                    
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
                
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= field1.x and event.pos[0] <=field1.x+field1.width and event.pos[1]>= field1.y and event.pos[1]<=field1.y+field1.height:
                    selected="field1"
                elif event.pos[0] >= field2.x and event.pos[0] <=field2.x+field2.width and event.pos[1]>= field2.y and event.pos[1]<=field2.y+field2.height:
                    selected="field2"
                else:
                    selected=''
                    
            if event.type==pygame.KEYDOWN:
                if selected=="field1" :
                    if (event.key>=97 and event.key<=122) and len(PLAYER1_NAME)<max:
                        PLAYER1_NAME+=chr(event.key-32)
                    if event.key==8:
                        PLAYER1_NAME=PLAYER1_NAME[:len(PLAYER1_NAME)-1]
            
                if selected=="field2" :
                    if (event.key>=97 and event.key<=122) and len(PLAYER2_NAME)<max:
                        PLAYER2_NAME+=chr(event.key-32)
                    if event.key==8:
                        PLAYER2_NAME=PLAYER2_NAME[:len(PLAYER2_NAME)-1]
                if event.key==13:
                    if PLAYER1_NAME=='' or PLAYER2_NAME=='':
                        pass
                    else:
                        game()
                
        draw_mainmenu(PLAYER1_NAME,PLAYER2_NAME,text1,field1,text2,field2,selected)

mainmenu()