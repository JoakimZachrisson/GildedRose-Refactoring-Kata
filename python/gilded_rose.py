import abc
import dataclasses
import enum

import numpy as np


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class _Name(str, enum.Enum):
    AGED_BRIE = "Aged Brie"
    SULFURAS = "Sulfuras, Hand of Ragnaros"
    BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"



class _ItemWrapper:
    def __init__(self, item: Item) -> None:
        self.item = item

    @property
    def expired(self) -> bool:
        return self.item.sell_in < 0

    @abc.abstractmethod
    def update(self) -> None:
        ...


class _Generic(_ItemWrapper):
    def update(self):
        self.item.sell_in -= 1
        new_quality = self.item.quality - (2 if self.expired else 1)
        self.item.quality = np.clip(new_quality, 0, 50)


class _AgedBrie(_ItemWrapper):
    def update(self):
        self.item.sell_in -= 1
        new_quality = self.item.quality + (2 if self.expired else 1)
        self.item.quality = np.clip(new_quality, 0, 50)


class _BackstagePasses(_ItemWrapper):
    def update(self):
        self.item.sell_in -= 1
        if self.item.sell_in >= 10:
            quality_increase = 1
        elif 5 <= self.item.sell_in < 10:
            quality_increase = 2
        elif 0 <= self.item.sell_in < 5:
            quality_increase = 3
        else:
            quality_increase = -self.item.quality
        new_quality = self.item.quality + quality_increase
        self.item.quality = np.clip(new_quality, 0, 50)


class _Sulfuras(_ItemWrapper):
    def update(self) -> None:
        ...


def wrap(item: Item) -> _ItemWrapper:
    factory_map = {
        _Name.AGED_BRIE: _AgedBrie,
        _Name.SULFURAS: _Sulfuras,
        _Name.BACKSTAGE_PASSES: _BackstagePasses,
    }
    factory_method = factory_map.get(item.name, _Generic)
    return factory_method(item=item)


class GildedRose:
    def __init__(self, items: list[Item]) -> None:
        self._items = [wrap(item) for item in items]

    def update_quality(self) -> None:
        for item in self._items:
            item.update()


# class GildedRose(object):
#     def __init__(self, items):
#         self.items = items
#
#     def update_quality(self):
#         for item in self.items:
#             self._update_quality(item)
#
#     @staticmethod
#     def _update_quality(item: Item) -> None:
#         if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
#             if item.quality > 0:
#                 if item.name != "Sulfuras, Hand of Ragnaros":
#                     item.quality = item.quality - 1
#         else:
#             if item.quality < 50:
#                 item.quality = item.quality + 1
#                 if item.name == "Backstage passes to a TAFKAL80ETC concert":
#                     if item.sell_in < 11:
#                         if item.quality < 50:
#                             item.quality = item.quality + 1
#                     if item.sell_in < 6:
#                         if item.quality < 50:
#                             item.quality = item.quality + 1
#         if item.name != "Sulfuras, Hand of Ragnaros":
#             item.sell_in = item.sell_in - 1
#         if item.sell_in < 0:
#             if item.name != "Aged Brie":
#                 if item.name != "Backstage passes to a TAFKAL80ETC concert":
#                     if item.quality > 0:
#                         if item.name != "Sulfuras, Hand of Ragnaros":
#                             item.quality = item.quality - 1
#                 else:
#                     item.quality = item.quality - item.quality
#             else:
#                 if item.quality < 50:
#                     item.quality = item.quality + 1
