from todo_app.ToDoCard import ToDoCard

from todo_app.ViewModel import ViewModel

import pytest

@pytest.fixture
def simple_test_items():
    return [ToDoCard(1, "A"), ToDoCard(2, "B"), ToDoCard(3, "C")]

def test_simple_ViewModel_items(simple_test_items):
    simple_ViewModel_items = ViewModel(simple_test_items).items
    assert simple_ViewModel_items == simple_test_items
