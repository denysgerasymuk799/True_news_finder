from prepare_data.transform_date import transform_date


class LinkedListIterator:
    def __init__(self, head):
        """

        :param head: a head Node
        """
        self.current = head

    def __iter__(self):
        """

        :return: make iteration during loop
        """
        return self

    def __next__(self):
        """
        Get next element
        """
        if not self.current:
            raise StopIteration
        else:
            article_dict = {"title": self.current.title,
                            "date": self.current.date,
                            "similarity": self.current.similarity,
                            "url": self.current.url,
                            "resource": self.current.resource,
                            "text": self.current.text}

            self.current = self.current.next
            return article_dict


class Node:
    def __init__(self, title, date, similarity, url, resource, text, next=None):
        """Instantiates a Node with default next of None"""
        self.title, self.date, self.url, self.resource, self.text, self.similarity = \
            title, date, url, resource, text, similarity

        self.next = next

    def __str__(self):
        """

        :return: title str
        """
        return str(self.title)


class TwoWayNode(Node):
    def __init__(self, title, date, similarity, url, resource, text, previous=None, next=None):
        """Instantiates a TwoWayNode."""
        super().__init__(title, date, similarity, url, resource, text, next)
        self.previous = previous


class LinkedList:
    """Create a new Linked List for articles"""

    def __init__(self, title, date, similarity, url, resource, text):
        """
        title, date, url, resource: str
        same_words: a list of same words
        """
        self.int_head = TwoWayNode(title, date, similarity, url, resource, text)
        self.int_tail = self.int_head
        self.length = 1

    def __iter__(self):
        """

        :return: iteration for all structure
        """
        return LinkedListIterator(self.int_head)

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
                          "    \"date\": {},\n".format(article.date) + \
                          "    \"similarity\": {},\n".format(str(article.similarity)) + \
                          "    \"url\": {},\n".format(article.url) + \
                          "    \"resource\": {}\n),\n".format(article.resource)

            article = article.next

        result_str = result_str[:-2] + "\n}"
        return result_str

    def __repr__(self):
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
                          "    \"date\": {},\n".format(article.date) + \
                          "    \"similarity\": {},\n".format(str(article.similarity)) + \
                          "    \"url\": {},\n".format(article.url) + \
                          "    \"resource\": {}\n),\n".format(article.resource)

            article = article.next

        result_str = result_str[:-2] + "\n}"
        return result_str

    def add(self, title, date, similarity, url, resource, text):
        """
        Add a new TwoWayNode to self.int_tail
        title, date, url, resource: str
        """
        self.int_tail.next = TwoWayNode(title, date, similarity, url, resource, text, self.int_tail)
        self.int_tail = self.int_tail.next
        self.length += 1

    def sorted_merge(self, lst_a, lst_b, sort_parameter):
        """
        :return: merge
        """

        # Base cases
        if lst_a is None:
            return lst_b
        if lst_b is None:
            return lst_a

        lst_a_parameter, lst_b_parameter = 0, 0

        if sort_parameter == "similarity":
            lst_a_parameter = lst_a.similarity
            lst_b_parameter = lst_b.similarity

        elif sort_parameter == "date":
            lst_a_date = str(lst_a.date).split("-")
            lst_b_date = str(lst_b.date).split("-")

            if len(lst_a_date) < 3:
                lst_a_date = transform_date(str(lst_a.date)).split("-")

            if len(lst_b_date) < 3:
                lst_b_date = transform_date(str(lst_b.date)).split("-")

            for position in range(len(lst_a_date)):
                # try:
                if int(lst_a_date[position]) > int(lst_b_date[position]):
                    lst_a_parameter = 1
                    break

                elif int(lst_b_date[position]) > int(lst_a_date[position]):
                    lst_b_parameter = 1
                    break
                # except Exception as e:
                #     print("error", str(e))
                #     continue


        # pick either a or b and recur..
        if lst_a_parameter >= lst_b_parameter:
            result = lst_a
            result.next = self.sorted_merge(lst_a.next, lst_b, sort_parameter)
        else:
            result = lst_b
            result.next = self.sorted_merge(lst_a, lst_b.next, sort_parameter)
        return result

    def merge_sort(self, head, sort_parameter):
        """
        :return: sort
        """
        # Base case if head is None
        if head is None or head.next is None:
            return head

        # get the middle of the list
        middle = self.get_middle(head)
        next_to_middle = middle.next

        # set the next of middle node to None
        middle.next = None

        # Apply mergeSort on left list
        left = self.merge_sort(head, sort_parameter)

        # Apply mergeSort on right list
        right = self.merge_sort(next_to_middle, sort_parameter)

        # Merge the left and right lists
        sorted_list = self.sorted_merge(left, right, sort_parameter)
        return sorted_list

    def get_middle(self, head):
        """
        :return: get middle
        """
        if head is None:
            return head

        slow = head
        fast = head

        while (fast.next is not None and
               fast.next.next is not None):
            slow = slow.next
            fast = fast.next.next

        return slow
