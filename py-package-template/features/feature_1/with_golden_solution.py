```
class SupplyCurve:
    """Class for representing supply curves.

    The curves are boostrapped from a set of input points and assumed
    to be piecewise constant

    :param data: Price-Quantity input data points - a collection of dicts
        containing `price` and `supply` keys.
    :type data: Sequence[Dict[str, int]]
    :raises ValueError: if zero price data is encountered.
    :raises SupplyMonotonicityError: when supply data is non-decreasing
        in price.
    """

    def __init__(self, data: Sequence[Dict[str, int]]) -> None:
        data_price_ord = sorted(data, key=lambda e: e['price'])

        if data_price_ord[0]['price'] == 0:
            raise ValueError('invalid price of 0 in supply data')

        for n, e in enumerate(data_price_ord[1:]):
            current_point = e['supply']
            previous_point = data_price_ord[n]['supply']
            if current_point < previous_point:
                raise SupplyMonotonicityError

        self._price = np.array([d['price'] for d in data_price_ord])
        self._quantity = np.array([d['supply'] for d in data_price_ord])
        self._min_price = self._price.min()

    def __eq__(self, other) -> bool:
        if (np.all(self._price == other._price)
                and np.all(self._quantity == other._quantity)):
            return True
        else:
            return False

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