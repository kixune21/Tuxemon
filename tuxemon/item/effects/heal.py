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
# Contributor(s):
#
# William Edwards <shadowapex@gmail.com>
# Leif Theden <leif.theden@gmail.com>
# Andy Mender <andymenderunix@gmail.com>
# Adam Chevalier <chevalieradam2@gmail.com>
#

from __future__ import annotations
from tuxemon.item.itemeffect import ItemEffect, ItemEffectResult
from typing import NamedTuple, Union
from tuxemon.monster import Monster


class HealEffectResult(ItemEffectResult):
    pass


class HealEffectParameters(NamedTuple):
    amount: Union[int, float]


class HealEffect(ItemEffect[HealEffectParameters]):
    """
    Heals the target by 'amount' hp.

    This is a constant if amount is an integer, a percentage of total hp
    if a float

    Examples:
    >>> potion = Item('potion')
    >>> potion.parameters.amount = 0.5
    >>> potion.apply(bulbatux)
    >>> # bulbatux is healed by 50% of it's total hp
    """

    name = "heal"
    param_class = HealEffectParameters

    def apply(self, target: Monster) -> HealEffectResult:
        healing_amount = self.parameters.amount
        if type(healing_amount) is float:
            healing_amount *= target.hp

        # Heal the target monster by "self.power" number of hitpoints.
        target.current_hp += int(healing_amount)

        # If we've exceeded the monster's maximum HP, set their health to 100%.
        if target.current_hp > target.hp:
            target.current_hp = target.hp

        return {"success": True}
