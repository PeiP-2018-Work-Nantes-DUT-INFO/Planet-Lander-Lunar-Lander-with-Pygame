"""
This module contains the fundamental Control class.
Also contained here are resource loading functions.
"""

import pygame as pg

import state_machine

TIME_PER_UPDATE = 16.0  # Milliseconds


class Control(object):
    """
    Control class for entire project. Contains the game loop, and contains
    the event_loop which passes events to states as needed.
    """

    def __init__(self, caption):
        self.screen = pg.display.get_surface()
        self.caption = caption
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.fps_visible = True
        self.now = 0.0
        self.keys = pg.key.get_pressed()
        self.state_machine = state_machine.StateMachine()

    def update(self):
        """
        Updates the currently active state.
        """
        self.now = pg.time.get_ticks()
        self.state_machine.update(self.keys, self.now)

    def draw(self, interpolate):
        if not self.state_machine.state.done:
            self.state_machine.draw(self.screen, interpolate)
            pg.display.update()
            self.show_fps()

    def event_loop(self):
        """
        Process all events and pass them down to the state_machine.
        The f5 key globally turns on/off the display of FPS in the caption
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            self.state_machine.get_event(event)

    def toggle_show_fps(self, key):
        """Press f5 to turn on/off displaying the framerate in the caption."""
        if key == pg.K_F5:
            self.fps_visible = not self.fps_visible
            if not self.fps_visible:
                pg.display.set_caption(self.caption)

    def show_fps(self):
        """
        Display the current FPS in the window handle if fps_visible is True.
        """
        if self.fps_visible:
            fps = self.clock.get_fps()
            with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
            pg.display.set_caption(with_fps)

    def main(self):
        """Main loop for entire program. Uses a constant timestep."""
        lag = 0.0
        while not self.done:
            lag += self.clock.tick(self.fps)
            self.event_loop()
            while lag >= TIME_PER_UPDATE:
                self.update()
                lag -= TIME_PER_UPDATE
            self.draw(lag / TIME_PER_UPDATE)


class Timer(object):
    """
    A very simple timer for events that are not directly tied to animation.
    """
    def __init__(self, delay, ticks=-1):
        """
        The delay is given in milliseconds; ticks is the number of ticks the
        timer will make before flipping self.done to True.  Pass a value
        of -1 to bypass this.
        """
        self.delay = delay
        self.ticks = ticks
        self.tick_count = 0
        self.timer = None
        self.done = False
        self.paused = False

    def check_tick(self, now):
        """Returns true if a tick worth of time has passed."""
        if self.paused:
            return False
        if not self.timer:
            self.timer = now
            return True
        elif not self.done and now-self.timer > self.delay:
            self.tick_count += 1
            self.timer = now
            if self.ticks != -1 and self.tick_count >= self.ticks:
                self.done = True
            return True
