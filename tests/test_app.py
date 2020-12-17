from todo_app.ToDoCard import ToDoCard

from todo_app.ViewModel import ViewModel

from todo_app.trello_config import TODOID, DONEID

import pytest

@pytest.fixture
def simple_test_items():
    return [ToDoCard(1, "A"), ToDoCard(2, "B"), ToDoCard(3, "C")]

@pytest.fixture
def complex_card_examples():
    return [{"id": 1, "name": "A" , "listId" : TODOID}, {"id": 2, "name": "B" , "listId" : TODOID}, {"id": 3, "name": "C" , "listId" : DONEID}]

def test_simple_ViewModel_items(simple_test_items):
    simple_ViewModel_items = ViewModel(simple_test_items).items
    assert simple_ViewModel_items == simple_test_items

def test_ViewModel_status_to_do(complex_card_examples):
    example_card_list = [ToDoCard.from_trello_card(card) for card in complex_card_examples]
    view_model_example = ViewModel(example_card_list)
    assert len(view_model_example.to_do_items()) == 2

def test_ViewModel_status_done(complex_card_examples):
    example_card_list = [ToDoCard.from_trello_card(card) for card in complex_card_examples]
    view_model_example = ViewModel(example_card_list)
    assert len(view_model_example.done_items()) == 1