from ui.components.listview import ListComponent

from .decorator import command


@command()
def navigate_list_top(list_component: ListComponent):
    if list_component:
        list_component.go_top()


@command()
def navigate_list_bottom(list_component: ListComponent):
    if list_component:
        list_component.go_bottom()


@command()
def navigate_list_by(list_component: ListComponent, offset: int):
    if list_component:
        list_component.go_by(offset)


@command()
def navigate_next_page(list_component: ListComponent):
    if list_component:
        list_component.next_page()


@command()
def navigate_previous_page(list_component: ListComponent):
    if list_component:
        list_component.previous_page()


@command()
def select_list_item(list_component: ListComponent):
    list_component.select()


@command()
def toggle_visual_mode(list_component: ListComponent):
    list_component.toggle_visual_mode()


@command()
def inverse_selection(list_component: ListComponent):
    all_items = set(list_component.filtered_data)
    list_component.marked_items = all_items - list_component.marked_items
    list_component.mark_for_redraw()


@command()
def mark_item(list_component: ListComponent):
    item = list_component.value
    if item in list_component.marked_items:
        list_component.marked_items.remove(item)
    else:
        list_component.marked_items.add(item)
    list_component.mark_for_redraw()


@command()
def unmark_all_items(list_component: ListComponent):
    list_component.marked_items.clear()
    list_component.mark_for_redraw()
