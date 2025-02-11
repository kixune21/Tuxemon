#
# Tuxemon
# Copyright (c) 2014-2017 William Edwards <shadowapex@gmail.com>,
#                         Benjamin Bean <superman2k5@gmail.com>
#
# This file is part of Tuxemon
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import annotations
import logging
from functools import partial

from tuxemon.event.eventaction import EventAction
from tuxemon.locale import replace_text
from tuxemon.session import Session
from typing import NamedTuple, final, Tuple, Callable, Sequence
from tuxemon.states.choice import ChoiceState

logger = logging.getLogger(__name__)


class DialogChoiceActionParameters(NamedTuple):
    choices: str
    variable: str


@final
class DialogChoiceAction(EventAction[DialogChoiceActionParameters]):
    """
    Ask the player to make a choice.

    Script usage:
        .. code-block::

            dialog_choice <choices>,<variable>

    Script parameters:
        choices: List of possible choices, separated by a colon ":".
        variable: Variable to store the result of the choice.

    """

    name = "dialog_choice"
    param_class = DialogChoiceActionParameters

    def start(self) -> None:
        def set_variable(var_value: str) -> None:
            player.game_variables[self.parameters.variable] = var_value
            self.session.client.pop_state()

        player = self.session.player

        # perform text substitutions
        choices = replace_text(self.session, self.parameters.choices)

        # make menu options for each string between the colons
        var_list = choices.split(":")
        var_menu = list()
        for val in var_list:
            var_menu.append((val, val, partial(set_variable, val)))

        self.open_choice_dialog(self.session, var_menu)

    def update(self) -> None:
        try:
            self.session.client.get_state_by_name(ChoiceState)
        except ValueError:
            self.stop()

    def open_choice_dialog(
        self,
        session: Session,
        menu: Sequence[Tuple[str, str, Callable[[], None]]],
    ) -> ChoiceState:
        logger.info("Opening choice window")
        return session.client.push_state(ChoiceState, menu=menu)
