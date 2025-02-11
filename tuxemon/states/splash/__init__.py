#
# Tuxemon
# Copyright (C) 2014, William Edwards <shadowapex@gmail.com>,
#                     Benjamin Bean <superman2k5@gmail.com>
#
# This file is part of Tuxemon.
#
# Tuxemon is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tuxemon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tuxemon.  If not, see <http://www.gnu.org/licenses/>.
#
# Contributor(s):
#
# William Edwards <shadowapex@gmail.com>
#
#
# states.start Handles the splash screen and start menu.
#
#
from __future__ import annotations
import logging
from typing import Optional, Any

import pygame

from tuxemon import audio
from tuxemon import prepare
from tuxemon import state
from tuxemon.platform.events import PlayerInput
from tuxemon.states.transition.fade import FadeOutTransition

logger = logging.getLogger(__name__)


class SplashState(state.State):
    """
    The state responsible for the splash screen

    """
    default_duration = 3

    def startup(self, **kwargs: Any) -> None:
        # this task will skip the splash screen after some time
        self.task(self.fade_out, self.default_duration)
        self.triggered = False

        width, height = prepare.SCREEN_SIZE

        # The space between the edge of the screen
        splash_border = prepare.SCREEN_SIZE[0] / 20

        # Set up the splash screen logos
        logo = self.load_sprite("gfx/ui/intro/pygame_logo.png")
        logo.rect.topleft = (
            splash_border,
            height - splash_border - logo.rect.height,
        )

        # Set up the splash screen logos
        cc = self.load_sprite("gfx/ui/intro/creative_commons.png")
        cc.rect.topleft = (
            width - splash_border - cc.rect.width,
            height - splash_border - cc.rect.height,
        )

        audio.load_sound("sound_ding").play()

    def resume(self) -> None:
        if self.triggered:
            self.parent.pop_state()

    def process_event(self, event: PlayerInput) -> Optional[PlayerInput]:
        # Skip the splash screen if a key is pressed.
        if event.pressed and not self.triggered:
            self.fade_out()
        return None

    def draw(self, surface: pygame.surface.Surface) -> None:
        if not self.triggered:
            surface.fill((15, 15, 15))
            self.sprites.draw(surface)

    def fade_out(self) -> None:
        self.triggered = True
        self.parent.push_state(FadeOutTransition)
