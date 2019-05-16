from dataclasses import dataclass
from typing import Dict, List, Optional

from ui.colors import colors

from .abstract_component import AbstractComponent
from .component import Component
from .layout import AbstractLayout, Layout
from ..rect import Rect


@dataclass
class Tab:
    component: AbstractComponent
    title: str


class TabsLayout(AbstractLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = Layout(direction=Layout.Direction.vertical)
        self.header = TabsHeaderComponent(self)

        self.tabs: List[Tab] = []
        self.displayed_tab: Optional[Tab] = None
        self.tabs_titles: Dict[str, Tab] = {}

        self.layout.add(self.header)
        self.childs.append(self.layout)

    def mark_for_update(self):
        super().mark_for_update()
        self.layout.mark_for_update()

    def update_layout(self) -> set:
        return self.layout.update_layout()

    def get_tab(self, tab_title: str):
        if tab_title in self.tabs_titles:
            return self.tabs_titles[tab_title]
        return None

    def add_tab(self, tab: Tab):
        self.tabs_titles[tab.title] = tab
        self.tabs.append(tab)

        if self.displayed_tab:
            self.layout.remove(self.displayed_tab.component)

        self.displayed_tab = tab

        self.layout.add(tab.component)

        self.header.mark_for_redraw()

    def remove_tab(self, tab: Tab):
        if tab not in self.tabs:
            return

        self.tabs.remove(tab)
        del self.tabs_titles[tab.title]

        if tab.component in self.layout.childs:
            self.layout.remove(tab.component)

        if self.tabs:
            self.layout.add(self.tabs[0].component)

        self.header.mark_for_redraw()

    def switch_to_tab_index(self, index: int):
        assert index >= 0 and index < len(self.tabs)

        if (
            self.displayed_tab
            and self.displayed_tab.component in self.layout.childs
        ):
            self.layout.remove(self.displayed_tab.component)
            self.displayed_tab = None

        self.displayed_tab = self.tabs[index]
        self.layout.add(self.displayed_tab.component)

    def switch_to_tab(self, tab: Tab):
        index = self.tabs.index(tab)
        self.switch_to_tab_index(index)

    def set_rect(self, rect: Rect):
        super().set_rect(rect)
        self.layout.set_rect(self.rect)


class TabsHeaderComponent(Component):
    def __init__(self, tabs_layout: TabsLayout):
        super().__init__(size=1)
        self.tabs_layout = tabs_layout

    def draw_content(self):
        childs_count = min(len(self.tabs_layout.tabs), 9)
        tab = self.tabs_layout.displayed_tab

        if tab:
            width = self.rect.width - childs_count * 2 - 2
            self.draw_text(tab.title, 0, 0, width)

        if childs_count > 1:
            chars_count = childs_count * 2
            tabs_chars = " ".join(str(i) for i in range(1, childs_count + 1))
            x = self.rect.width - chars_count
            self.draw_text(tabs_chars, 0, x, chars_count)

            current_index = self.tabs_layout.tabs.index(tab)
            color = colors["distinguished-item"]
            self.draw_text(
                str(current_index + 1), 0, x + current_index * 2, 1, color
            )
