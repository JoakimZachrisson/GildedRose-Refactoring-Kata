import abc
import enum

import numpy as np

__all__ = ["GildedRose", "Item"]


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
        self._is_conjured = item.name.lower().startswith("conjured")

    def decrease_quality(self, amount: int) -> None:
        amount = amount * 2 if self._is_conjured else amount
        self.item.quality = np.clip(self.item.quality - amount, 0, 50)

    @property
    def expired(self) -> bool:
        return self.item.sell_in < 0

    def update(self) -> None:
        self.item.sell_in -= 1
        decrease_amount = self.compute_quality_decrease()
        self.decrease_quality(decrease_amount)

    @abc.abstractmethod
    def compute_quality_decrease(self) -> int:
        ...


class _Generic(_ItemWrapper):
    def compute_quality_decrease(self):
        return 2 if self.expired else 1


class _AgedBrie(_ItemWrapper):
    def compute_quality_decrease(self):
        return -2 if self.expired else -1


class _BackstagePasses(_ItemWrapper):
    def compute_quality_decrease(self):
        if self.item.sell_in >= 10:
            amount = -1
        elif 5 <= self.item.sell_in < 10:
            amount = -2
        elif 0 <= self.item.sell_in < 5:
            amount = -3
        else:
            amount = self.item.quality
        return amount


class _Sulfuras(_ItemWrapper):
    def compute_quality_decrease(self) -> int:
        return 0

    def update(self) -> None:
        ...


def wrap(item: Item) -> _ItemWrapper:
    if _Name.AGED_BRIE in item.name:
        factory_method = _AgedBrie
    elif _Name.SULFURAS in item.name:
        factory_method = _Sulfuras
    elif _Name.BACKSTAGE_PASSES in item.name:
        factory_method = _BackstagePasses
    else:
        factory_method = _Generic

    return factory_method(item=item)


class GildedRose:
    def __init__(self, items: list[Item]) -> None:
        self._items = [wrap(item) for item in items]

    def update_quality(self) -> None:
        for item in self._items:
            item.update()
