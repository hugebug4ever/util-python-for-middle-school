#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plane

Detailed description here
"""

import pygame
import argparse
import logging

__author__ = "xilei"
__date__ = "2023/06/14 08:27:51"

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

border = 25
chart_width = 1200
chart_height = 600
offset_x = 0
offset_y = 0
meter_per_point = 1.0

plane_start_x = .0
plane_start_y = chart_height * meter_per_point
plane_start_speed = 5.0
plane_horizontal_acceleration = 4.9
plane_drop_bag_gap = 1.

gravity = 9.8

pygame.init()
gameDisplay = pygame.display.set_mode((chart_width + border * 2, 600 + border * 2))
font = pygame.font.SysFont(None, 20)
clock = pygame.time.Clock()
bags = []

class TheBag:
    def __init__(self, x, y,  v0):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.v0 = v0
        self.lifetime = 0

    def update(self, t):
        self.lifetime += t
        
        if self.y / meter_per_point < 10:
            return

        t = self.lifetime
        self.x = self.start_x + self.v0 * t 
        self.y = self.start_y - gravity * t * t * 0.5

    def draw(self):
        screen_x = border + (self.x - offset_x) / meter_per_point
        screen_y = border + chart_height - (self.y - offset_y) / meter_per_point
        pygame.draw.circle(gameDisplay, green, (screen_x, screen_y), 2)

class ThePlane:
    def __init__(self, x, y, v0, a):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.v0 = v0 
        self.a = a
        self.lifetime = 0
        self.drop_cooldown = plane_drop_bag_gap

    def update(self, dt):
        self.lifetime += dt

        t = self.lifetime
        self.x = self.start_x + self.v0 * t + self.a * t * t * 0.5

        self.drop_cooldown -= dt
        if self.drop_cooldown <= 0:
            self.drop_cooldown = plane_drop_bag_gap
            self.drop()

    def drop(self):
        v_now = self.v0 + self.a * self.lifetime
        new_bag = TheBag(self.x, self.y, v_now)
        bags.append(new_bag)

    def draw(self):
        screen_x = border + (self.x - offset_x) / meter_per_point
        screen_y = border + chart_height - (self.y - offset_y) / meter_per_point
        pygame.draw.circle(gameDisplay, white, (screen_x, screen_y), 2)


def main():

    def draw_coordinate_system():

        pygame.draw.line(gameDisplay, white, (border, border), (border, chart_height + border), 1)
        pygame.draw.line(gameDisplay, white, (border, chart_height + border), (chart_width + border, chart_height + border), 1)

        text_x_offset_img = font.render(f"{offset_x}", True, white, black)
        gameDisplay.blit(text_x_offset_img, (border + 5, chart_height + border + 5))

        text_x_offset_img = font.render(f"{offset_x + chart_width * meter_per_point}", True, white, black)
        gameDisplay.blit(text_x_offset_img, (chart_width + border - 20, chart_height + border + 5))

        text_y_offset_img = font.render(f"{offset_y}", True, white, black)
        gameDisplay.blit(text_y_offset_img, (border - 20, chart_height + border - 15))

        text_y_offset_img = font.render(f"{offset_y + chart_height * meter_per_point}", True, white, black)
        gameDisplay.blit(text_y_offset_img, (border - 20, border + 5))

        text_time = font.render(f"{plane.lifetime:2.2f} s", True, white, black)
        gameDisplay.blit(text_time, (chart_width- 20, 5))

    plane = ThePlane(plane_start_x, plane_start_y, plane_start_speed, plane_horizontal_acceleration)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        clock.tick(30)
        gameDisplay.fill(black)

        keys = pygame.key.get_pressed()
        time_step = 1.0/10
        if keys[pygame.K_SPACE]:
            for bag in bags:
                bag.update(time_step)
                bag.draw()
            plane.update(time_step)

        draw_coordinate_system()
        for bag in bags:
            bag.draw()
        plane.draw()

        pygame.display.update()

if __name__ == '__main__':
    main()
