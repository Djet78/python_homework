from hypothesis import given
import hypothesis.strategies as st
import homework_2 as hw
import pytest


class TestTask2:

    @given(st.integers())
    def test_not_negative(self, val):
        assert hw.longest_binary_gap(val) >= 0

    def test_type_error_raise(self):
        with pytest.raises(TypeError):
            hw.longest_binary_gap("asd")


class TestTask4:

    def test_1(self):
        assert hw.count_natural_divisors_1(1) == 1

    def test_24(self):
        assert hw.count_natural_divisors_1(24) == 8

    def test_simple_digit(self):
        assert hw.count_natural_divisors_1(7) == 2

    def test_value_error_raise(self):
        with pytest.raises(ValueError):
            hw.count_natural_divisors_1(0)

    def test_type_error_raise(self):
        with pytest.raises(TypeError):
            hw.count_natural_divisors_1("")


class TestTask5:

    def test_type_error_raise(self):
        with pytest.raises(TypeError):
            hw.longest_correct_pass(42)

    @given(st.text())
    def test_returned_val(self, text):
        assert hw.longest_correct_pass(text) >= -1


if __name__ == "__main__":
    pytest.param()
    pytest.main()
