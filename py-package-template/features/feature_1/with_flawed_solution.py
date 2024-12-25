```
def quantity(self, price: float) -> float:
    """Return supply quantity for a given price.

    :param price: Price.
    :type price: float
    :return: Quantity.
    :rtype: float
    """
    if price < self._min_price:
        quantity_at_price = 0.
    else:
        quantity_at_price = self._quantity[self._price <= price][-1]
    return quantity_at_price
```