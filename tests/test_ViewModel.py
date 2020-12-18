from todo_app.ToDoCard import ToDoCard

from todo_app.ViewModel import ViewModel

from todo_app.trello_config import TODOID, DONEID

import pytest
from datetime import datetime
from datetime import timezone

'''
Gives current datetime in "Timezone" format
'''

right_now = datetime.now()

@pytest.fixture
def simple_test_items():
    return [ToDoCard(1, "A"), ToDoCard(2, "B"), ToDoCard(3, "C")]

@pytest.fixture
def complex_card_examples():
    return [
        ToDoCard(1, "A","To Do"),
        ToDoCard(2, "B","To Do"),
        ToDoCard(3, "C","Done")
    ]

@pytest.fixture
def timed_card_example_eight():
    return [ToDoCard(1, "A" ,"To Do" , datetime.strptime("2020-11-19T15:56:33.468Z", '%Y-%m-%dT%H:%M:%S.%fZ')),
         ToDoCard(1, "A" ,"To Do" , right_now),
         ToDoCard(1, "A" ,"Done" , datetime.strptime("2020-11-19T15:56:33.468Z", '%Y-%m-%dT%H:%M:%S.%fZ')),
         ToDoCard(2, "B" ,"Done" , datetime.strptime("2020-11-20T15:56:33.468Z", '%Y-%m-%dT%H:%M:%S.%fZ')),
         ToDoCard(3, "C" ,"Done" , datetime.strptime("2020-11-21T15:56:33.468Z", '%Y-%m-%dT%H:%M:%S.%fZ')),
         ToDoCard(4, "D" ,"Done" , datetime.strptime("2020-11-18T15:56:33.468Z", '%Y-%m-%dT%H:%M:%S.%fZ')),
         ToDoCard(100, "Omega" ,"Done", right_now),
         ToDoCard(0, "Alpha" ,"Done", right_now)]


def test_simple_ViewModel_items(simple_test_items):
    simple_ViewModel_items = ViewModel(simple_test_items).items
    assert simple_ViewModel_items == simple_test_items

def test_ViewModel_status_to_do(timed_card_example_eight):
    view_model_example = ViewModel(timed_card_example_eight)
    assert len(view_model_example.to_do_items()) == 2

def test_ViewModel_status_done(timed_card_example_eight):
    view_model_example = ViewModel(timed_card_example_eight)
    len(view_model_example.done_items()) == 6

def test_ViewModel_done_items(timed_card_example_eight):
    view_model_example = ViewModel(timed_card_example_eight)
    view_model_done = view_model_example.done_items()
    assertation = True
    for i in view_model_done:
        if i.status != "Done":
            assertation = False
    assert assertation == True

def test_ViewModel_recent_items(timed_card_example_eight):
    view_model_example = ViewModel(timed_card_example_eight)
    view_model_done_recent = view_model_example.recent_done_items()
    assert len(view_model_done_recent) == 2

def test_ViewModel_older_items(timed_card_example_eight):
    view_model_example = ViewModel(timed_card_example_eight)
    view_model_done_recent = view_model_example.older_done_items()
    assert len(view_model_done_recent) == 4
