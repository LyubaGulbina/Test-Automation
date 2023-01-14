import pytest
from app.calculator import Calculator

class TestCalc:
    def setup(self):
        self.calc = Calculator
    def test_multiply_calculate_correctly(self):
        assert self.calc.multiply(self, 2, 2) == 4

    def test_division_calculation_correctly(self):
        assert self.calc.division(self, 8, 4) == 2

    def test_subtraction_calculation_correctly(self):
        assert self.calc.subtraction(self, 15, 7) == 8

    def test_division_adding_correctly(self):
        assert self.calc.adding(self, 9, 2) == 11


