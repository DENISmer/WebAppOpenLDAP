
class Pagintion:
    def __init__(self, items, page, items_per_page=20):
        self.items = items
        self.page = page - 1
        self.items_per_page = items_per_page

    def get_items(self):
        length = len(self.items)
        num_page = length//self.items_per_page

        if num_page * self.items_per_page < length:
            num_page += 1

        if self.page > num_page:
            return [], length, num_page

        start = self.page*self.items_per_page
        end = start + self.items_per_page
        out_items = self.items[start:end]

        return out_items, length, num_page
