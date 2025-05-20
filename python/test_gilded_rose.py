import pytest

from gilded_rose import Item, GildedRose


def test_foo():
    items = [Item("foo", 0, 0)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].name == "foo"
    assert items[0].sell_in == -1
    assert items[0].quality == 0


def test_names_are_not_altered_terminal_quality():
    items = [
        Item("foo", sell_in=10, quality=20),
        Item("Aged Brie", sell_in=10, quality=5),
        Item("Conjured Aged Brie", sell_in=11, quality=9),
        Item("Sulfuras, Hand of Ragnaros", sell_in=20, quality=80),
        Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=20),
    ]
    gilded_rose = GildedRose(items)

    for _ in range(1000):
        gilded_rose.update_quality()
        assert items[0].name == "foo"
        assert items[1].name == "Aged Brie"
        assert items[2].name == "Conjured Aged Brie"
        assert items[3].name == "Sulfuras, Hand of Ragnaros"
        assert items[4].name == "Backstage passes to a TAFKAL80ETC concert"

    for item in items:
        expected_quality = {80} if item.name == "Sulfuras, Hand of Ragnaros" else {0, 50}
        assert item.quality in expected_quality


def test_quality_is_never_negative():
    items = [Item("foo", 3, 2), Item("bar", 2, 3)]

    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert items[0].sell_in == 2
    assert items[0].quality == 1
    assert items[1].sell_in == 1
    assert items[1].quality == 2

    gilded_rose.update_quality()

    assert items[0].sell_in == 1
    assert items[0].quality == 0
    assert items[1].sell_in == 0
    assert items[1].quality == 1

    gilded_rose.update_quality()

    assert items[0].sell_in == 0
    assert items[0].quality == 0
    assert items[1].sell_in == -1
    assert items[1].quality == 0

    gilded_rose.update_quality()

    assert items[0].sell_in == -1
    assert items[0].quality == 0
    assert items[1].sell_in == -2
    assert items[1].quality == 0


def test_degradation_is_twice_after_expiration():
    items = [Item("skibidi", sell_in=2, quality=10)]
    glided_rose = GildedRose(items)
    glided_rose.update_quality()
    assert items[0].sell_in == 1
    assert items[0].quality == 9

    glided_rose.update_quality()
    assert items[0].sell_in == 0
    assert items[0].quality == 8

    glided_rose.update_quality()
    assert items[0].sell_in == -1
    assert items[0].quality == 6


def test_aged_brie_update():
    items = [Item("Aged Brie", sell_in=2, quality=21)]
    gilded_rose = GildedRose(items)

    assert items[0].sell_in == 2
    assert items[0].quality == 21

    gilded_rose.update_quality()
    assert items[0].sell_in == 1
    assert items[0].quality == 22

    gilded_rose.update_quality()
    assert items[0].sell_in == 0
    assert items[0].quality == 23

    gilded_rose.update_quality()
    assert items[0].sell_in == -1
    assert items[0].quality == 25

    gilded_rose.update_quality()
    assert items[0].sell_in == -2
    assert items[0].quality == 27


def test_backstage_passes():
    items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=12, quality=10)]
    gilded_rose = GildedRose(items)

    gilded_rose.update_quality()
    assert items[0].sell_in == 11
    assert items[0].quality == 11

    gilded_rose.update_quality()
    assert items[0].sell_in == 10
    assert items[0].quality == 12

    gilded_rose.update_quality()
    assert items[0].sell_in == 9
    assert items[0].quality == 14

    gilded_rose.update_quality()
    assert items[0].sell_in == 8
    assert items[0].quality == 16

    gilded_rose.update_quality()
    gilded_rose.update_quality()
    gilded_rose.update_quality()
    assert items[0].sell_in == 5
    assert items[0].quality == 22

    gilded_rose.update_quality()
    assert items[0].sell_in == 4
    assert items[0].quality == 25

    gilded_rose.update_quality()
    gilded_rose.update_quality()
    gilded_rose.update_quality()
    assert items[0].sell_in == 1
    assert items[0].quality == 34

    gilded_rose.update_quality()
    assert items[0].sell_in == 0
    assert items[0].quality == 37

    gilded_rose.update_quality()
    assert items[0].sell_in == -1
    assert items[0].quality == 0


@pytest.mark.parametrize("sell_in, quality", [(10, 20), (1, 1337), (-1, -10)])
def test_sulfuras_doesnt_change(sell_in: int, quality: int) -> None:
    item = Item("Sulfuras, Hand of Ragnaros", sell_in, quality)
    gilded_rose = GildedRose([item])
    for _ in range(10):
        gilded_rose.update_quality()
    assert item.sell_in == sell_in
    assert item.quality == quality


@pytest.mark.skip(reason="not implemented")
@pytest.mark.parametrize(
    "name", ["foo", "Aged Brie", "Backstage passes to a TAFKAL80ETC concert", "Sulfuras, Hand of Ragnaros"]
)
def test_conjured(name: str):
    items = [
        Item(name, sell_in=20, quality=25),
        Item(f"Conjured {name}", sell_in=20, quality=25),
    ]
    gilded_rose = GildedRose(items)

    for _ in range(5):
        regular, conjured = items
        prev_regular_quality, prev_conjured_quality = regular.quality, conjured.quality

        gilded_rose.update_quality()
        assert regular.sell_in == conjured.sell_in

        if conjured.quality not in {50, 80, 0}:
            regular_quality_diff = prev_regular_quality - regular.quality
            conjured_quality_diff = prev_conjured_quality - conjured.quality
            assert conjured_quality_diff == 2 * regular_quality_diff


if __name__ == "__main__":
    pytest.main()
