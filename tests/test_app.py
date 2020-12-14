from todo_app.app import ToDoCard, ViewModel

import pytest

simple_test_items =[ToDoCard(1, "A"), ToDoCard(2, "B"), ToDoCard(3, "C")]

def test_simple_ViewModel_items(simple_test_items):
    simple_ViewModel_items = ViewModel(simple_test_items)
    assert simple_ViewModel_items == simple_test_items
