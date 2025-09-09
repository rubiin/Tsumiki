from fabric.widgets.box import Box


class LimitBox(Box):
    """A hack for replicating CSS's `max-*` properties"""

    def __init__(self, max_width: int, max_height: int, **kwargs):
        super().__init__(**kwargs)
        self.max_width: int = max_width
        self.max_height: int = max_height

    def do_size_allocate(self, allocation):
        if self.max_width >= 0:
            allocation.width = min(self.max_width, allocation.width)
        if self.max_height >= 0:
            allocation.height = min(self.max_height, allocation.height)
        return Box.do_size_allocate(self, allocation)
