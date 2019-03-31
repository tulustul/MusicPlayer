from ui.components.listview import ListComponent

from .decorator import command


@command()
def navigate_list_top(list_component: ListComponent):
    list_component.go_top()


@command()
def navigate_list_bottom(list_component: ListComponent):
    list_component.go_bottom()


@command()
def navigate_list_by(list_component: ListComponent, offset: int):
    list_component.go_by(offset)


@command()
def navigate_next_page(list_component: ListComponent):
    list_component.next_page()


@command()
def navigate_previous_page(list_component: ListComponent):
    list_component.previous_page()


@command()
def autocomplete_input(list_component: ListComponent):
    list_component.autocomplete_input()
