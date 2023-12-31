import pygame

WIDTH,HEIGHT= 900,500
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
WHITE=(255,255,255)
BLACK=(0,0,0)
YELLOW=(255,255,0)
RED=(255,0,0)
pygame.display.set_caption("Moroccan Simle Game")
BORDER=pygame.Rect(WIDTH // 2 - 5,0,10,HEIGHT)
SPACESHIP_WIDTH,SPACESHIP_HEIGHT=100,70
FPS=90
BULLET_VEL = 5
MAX_BULLETS = 200
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 1
YELLOW_SPACESHIP_IMAGE=pygame.image.load('moro.png')
RED_SPACESHIP_IMAGE=pygame.image.load('moroo.png')
YELLOW_SPACESHIP=pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
RED_SPACESHIP=pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT))


def draw_window(red,yellow,red_bullets,yellow_bullets):

    WIN.fill(WHITE)
    pygame.draw.rect(WIN,BLACK,BORDER)

    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:

        pygame.draw.rect(WIN,YELLOW, bullet)


    pygame.display.update()

def yellow_handle_movement(keys_pressed,yellow):
       
    if keys_pressed[pygame.K_LEFT] and yellow.x - 5  > BORDER.x + BORDER.width:
        yellow.x-=5
    if keys_pressed[pygame.K_RIGHT] and yellow.x + 5 + yellow.width < WIDTH:
        yellow.x+=5
    if keys_pressed[pygame.K_UP] and yellow.y - 5 > 0:
        yellow.y-=5
    if keys_pressed[pygame.K_DOWN] and yellow.y - 5 < HEIGHT - 70:
        yellow.y+=5

def red_handle_movement(keys_pressed,red):
    if keys_pressed[pygame.K_a] and red.x - 5 > 0:
        red.x-=5
    if keys_pressed[pygame.K_b] and red.x - 5 + red.width < BORDER.x:
        red.x+=5
    if keys_pressed[pygame.K_s] and red.y - 5 > 0:
        red.y-=5
    if keys_pressed[pygame.K_d] and red.y - 5 < HEIGHT - 70 :
        red.y+=5

def handle_bullets(red_bullets,yellow_bullets,red,yellow):
    for bullet in yellow_bullets:

        bullet.x = bullet.x - BULLET_VEL

        if red.colliderect(bullet):
            # pygame.event.post(pygame.event.Event(YELLOW_HIT))
            yellow_bullets.remove(bullet)
        # elif bullet.x > WIDTH:
        #     yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            # pygame.event.post(pygame.event.Event(RED_HIT))
            red_bullets.remove(bullet)
        # elif bullet.x < 0:
        #     red_bullets.remove(bullet)      



def main():
    red=pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow=pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    
    red_bullets=[]
    yellow_bullets=[]


    clock=pygame.time.Clock()
    run=True
    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet=pygame.Rect(yellow.x + yellow.width , yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)


                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet=pygame.Rect(red.x + red.width, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)



        
        
        keys_pressed=pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)
       
        handle_bullets(red_bullets, yellow_bullets , red, yellow)

        draw_window(red,yellow,red_bullets,yellow_bullets)
        
    pygame.quit()

if __name__=="__main__":    
    main()