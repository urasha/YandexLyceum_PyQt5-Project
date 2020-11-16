import pygame

pygame.init()


def play_song(file):
    pygame.mixer.music.load(f'song/{file}')
    pygame.mixer.music.play()


def stop_timer_music(timer):
    timer.stop()