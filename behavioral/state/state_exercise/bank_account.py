import abc
from dataclasses import dataclass

class State:
    state_name: str

    def __init__(self, amount=0.0):
        self.amount: float = amount

    @property
    def description(self):
        return self.state_name

    def withdraw(self, amount: float):
        raise NotImplementedError

    def deposit(self, amount: float):
        self.amount += amount


class OverdraftState(State):
    state_name = "Overdraft"

    def withdraw(self, amount):
        raise InsufficientFunds


class NormalState(State):
    state_name = "Normal"

    def withdraw(self, amount: float):
        self.amount -= amount


class InsufficientFunds(Exception):
    pass


class BankAccount: # Context
    def __init__(self, id_, amount=0):
        self.id_ = id_
        if amount >= 0.0:
            self._state = NormalState(amount)
        else:
            self._state = OverdraftState(amount)

    def change_state(self) -> State:
        if self._state.amount >= 0.0:
            return NormalState(self._state.amount)
        elif self._state.amount < 0.0:
            return OverdraftState(self._state.amount)

    def deposit(self, amount):
        self._state.deposit(amount)        
        self._state = self.change_state()

    def withdraw(self, amount):
        self._state.withdraw(amount)
        self._state = self.change_state()


    @property
    def description(self):
        return self._state.description

    @property
    def balance(self):
        return self._state.amount

    @property
    def state_description(self):
        return self._state.description
