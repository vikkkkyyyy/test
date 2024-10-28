from pygame import *


#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
   # конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y):
       # Вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)
       # каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
  
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   # метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
   #метод, в котором реализовано управление спрайтом по кнопкам стрелочкам клавиатуры
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
       # Вызываем конструктор класса (Sprite):
       GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)
  
       self.x_speed = player_x_speed
       self.y_speed = player_y_speed
   def update(self):
    
      if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
          self.rect.x += self.x_speed
      platforms_touched = sprite.spritecollide(self, walls, False)
      if self.x_speed > 0:
          for p in platforms_touched:
              self.rect.right = min(self.rect.right, p.rect.left)
      elif self.x_speed < 0: 
          for p in platforms_touched:
              self.rect.left = max(self.rect.left, p.rect.right) 
      if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
          self.rect.y += self.y_speed
      platforms_touched = sprite.spritecollide(self, walls, False)
      if self.y_speed > 0 : 
          for p in platforms_touched:
              self.rect.bottom = min(self.rect.bottom, p.rect.top)
      elif self.y_speed < 0: 
          for p in platforms_touched:
              self.rect.top = max(self.rect.top, p.rect.bottom) 


class Enemy(GameSprite):
   side = 'left'
   def __init__(self, enemy_image, enemy_x, enemy_y, size_x, size_y, speed):
      GameSprite.__init__(self, enemy_image, enemy_x, enemy_y, size_x, size_y)
      self.speed = speed

   def update(self):
      if self.rect.x >= win_width - 85:
         self.side = 'left'
      if self.rect.x <= 420:
         self.side = 'right'
      if self.side == 'left':
         self.rect.x -= self.speed
      else:
         self.rect.x += self.speed

        


      
#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Лабиринт")
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)#задаем цвет согласно цветовой схеме RGB
#создаем стены картинки
walls = sprite.Group()

w1 = GameSprite('platform_h.png',win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('platform_v.png', 370, 100, 50, 400)

walls.add(w1)
walls.add(w2)
#создаем спрайты
packman = Player('dog.png', 5, win_height - 80, 80, 80, 0, 0)
final = GameSprite('hero.png',600, 400, 80, 80)
tom = Enemy('tom.png', 600, 200, 90, 90, 5)

#игровой цикл
run = True
finish = False 

while run:
   #цикл срабатывает каждую 0.05 секунд
   time.delay(50)
   #закрашиваем окно цветом
  
   for e in event.get():
       if e.type == QUIT:
           run = False
       elif e.type == KEYDOWN:
           if e.key == K_LEFT:
               packman.x_speed = -5
           elif e.key == K_RIGHT:
               packman.x_speed = 5
           elif e.key == K_UP:
               packman.y_speed = -5
           elif e.key == K_DOWN:
               packman.y_speed = 5
       elif e.type == KEYUP:
           if e.key == K_LEFT:
               packman.x_speed = 0
           elif e.key == K_RIGHT:
               packman.x_speed = 0
           elif e.key == K_UP:
               packman.y_speed = 0
           elif e.key == K_DOWN:
               packman.y_speed = 0
   if finish != True:
       window.fill(back)
       walls.draw(window)
       packman.reset()
       final.reset()
       tom.reset()
       packman.update()
       tom.update()
       if sprite.collide_rect(packman, final):
           finish = True
           img = image.load('images.jpg')
           window.fill((255, 255, 255))
           window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
       if sprite.collide_rect(packman, tom):
           finish = True
           img = image.load('over.png')
           window.fill((255, 255, 255))
           window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
           

  
   display.update()
