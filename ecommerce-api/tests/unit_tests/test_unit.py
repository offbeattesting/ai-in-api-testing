from main import filter_selected_products


class TestFilterSelectedProducts:
    def test_returns_only_selected_product_ids(self):
        products = [
            {"id": 1, "selected": True},
            {"id": 2, "selected": False},
            {"id": 3, "selected": True},
        ]
        result = filter_selected_products([1, 2, 3], products)
        assert result == [1, 3]

    def test_empty_when_none_selected(self):
        products = [
            {"id": 1, "selected": False},
            {"id": 2, "selected": False},
        ]
        result = filter_selected_products([1, 2], products)
        assert result == []

    def test_empty_when_empty_input(self):
        result = filter_selected_products([], [{"id": 1, "selected": True}])
        assert result == []

    def test_ignores_ids_not_in_products(self):
        products = [{"id": 1, "selected": True}]
        result = filter_selected_products([1, 999], products)
        assert result == [1]

    def test_does_not_mutate_products(self):
        products = [{"id": 1, "selected": True}]
        original = products.copy()
        filter_selected_products([1], products)
        assert products == original
