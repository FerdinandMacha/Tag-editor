
class TagViewModel:
    def __init__(self, tag_name):
        self.name: str = tag_name
        self.included: bool = False
        self.check_showing: bool = True
