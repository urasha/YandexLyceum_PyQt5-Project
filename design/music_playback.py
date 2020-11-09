import pygame

pygame.init()


def play_song(file):
    pygame.mixer.music.load(f'song/{file}')
    pygame.mixer.music.play()
