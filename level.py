from typing import Iterable
import pygame
from pygame.sprite import AbstractGroup
from Settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *

class Level:
    def __init__(self):
        self.display_surface=pygame.display.get_surface()
        self.visible_sprites=YsortCameraGroup()
        self.obstacle_sprites=pygame.sprite.Group()
        self.create_map()
        
    def create_map(self):
        
        layouts={
            'boundary': import_csv_layout(r'D:\GamePython\PythonGame\map\map_FloorBlocks.csv')  

        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):              
                for col_index,col in enumerate(row):
                    if col !='-1':
                        x=col_index * TILESIZE
                        y=row_index * TILESIZE
                        if style=="boundary":
                            Tile((x,y),[self.obstacle_sprites],'invisible')
        #         if col =='x':
        #             Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
        #         if col=='p':
        #             self.player=Player((x,y),[self.visible_sprites],self.obstacle_sprites)
        self.player=Player((2000,1430),[self.visible_sprites],self.obstacle_sprites)    
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        
        super().__init__()
        self.display_surface=pygame.display.get_surface()
        self.half_width=self.display_surface.get_size()[0]//2
        self.half_height=self.display_surface.get_size()[1]//2
        self.offset=pygame.math.Vector2()
        
        self.floor_surface=pygame.image.load(r"D:\GamePython\PythonGame\graphics\tilemap\ground.png").convert()
        self.floor_rect=self.floor_surface.get_rect(topleft=(4,-64))
        
        
        
    def custom_draw(self,player):
        self.offset.x=player.rect.centerx - self.half_width
        self.offset.y=player.rect.centery - self.half_height
        
        floor_offest_pos=self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface,floor_offest_pos)
        
        for spirte in sorted(self.sprites(),key= lambda sprite:sprite.rect.centery):
            offset_pos=spirte.rect.topleft - self.offset
            self.display_surface.blit(spirte.image,offset_pos)