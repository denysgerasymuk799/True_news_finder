class Node:
    def __init__(self, title, same_words, date, url, resource, next=None):
        """Instantiates a Node with default next of None"""
        self.title, self.date, self.url, self.resource = title, date, url, resource
        self.same_words = same_words
        self.next = next

    def __str__(self):
        return str(self.title)


class TwoWayNode(Node):
    def __init__(self, title, same_words, date, url, resource, previous=None, next=None):
        """Instantiates a TwoWayNode."""
        super().__init__(title, same_words, date, url, resource, next)  # Node.__init__(self, data, next)
        self.previous = previous


class LinkedList:
    """Create a new Linked List for articles"""
    def __init__(self, title, same_words, date, url, resource):
        """
        title, date, url, resource: str
        same_words: a list of same words
        """
        self.int_head = TwoWayNode(title, same_words, date, url, resource)
        self.int_tail = self.int_head
        self.length = 1

    def __str__(self):
        """
        Prints the data stored in self.
        __str__: Node -> Str
        """
        result_str = "{\n"
        article = self.int_head
        article_id = 0
        while article is not None:
            article_id += 1
            result_str += "{}:(\n".format(str(article_id)) + "    \"title\": {},\n".format(article.title) + \
                         "    \"same words\": {},\n".format(str(article.same_words)) + \
                         "    \"date\": {},\n".format(article.date) + \
                         "    \"url\": {},\n".format(article.url) + \
                         "    \"resource\": {}\n),\n".format(article.resource)

            article = article.next

        result_str = result_str[:-2] + "\n}"
        return result_str

    def add(self, title, date, url, resource):
        """
        Add a new TwoWayNode to self.int_tail
        title, date, url, resource: str
        """
        self.int_tail.next = TwoWayNode(title, date, url, resource, self.int_tail)
        self.int_tail = self.int_tail.next
