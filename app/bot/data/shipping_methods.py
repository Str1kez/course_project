from aiogram.types import ShippingOption, LabeledPrice

REGULAR_SHIPPING = ShippingOption(
    id='regular',
    title='Обычная доставка',
    prices=[LabeledPrice('Обычная упаковка', 50_00)]
)

FAST_SHIPPING_DEFAULT = ShippingOption(
    id='fast_default',
    title='Быстрая доставка',
    prices=[LabeledPrice('Обычная упаковка', 100_00)]
)

FAST_SHIPPING_BOX = ShippingOption(
    id='fast_box',
    title='Быстрая доставка в коробке',
    prices=[LabeledPrice('Коробка', 200_00)]
)

PICKUP_SHIPPING = ShippingOption(
    id='pickup',
    title='Самовывоз',
    prices=[LabeledPrice('Забирай сам', 0)]
)
