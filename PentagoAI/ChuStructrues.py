'''
DATA STRUCTURES
'''

class ChuPriorityQueue(object):

    def __init__(self):

        self.elements = []
        self.num = 0

	#########################################################################
	##########################################################################

    def dequeue(self):

        self.num -= 1
        return self.elements.pop()

	##########################################################################
	##########################################################################

    def enqueue(self, element):

        if self.num == 0:

            self.elements.append(element)

        else:

            idx = 0

            for el in self.elements:

                if element.priority > el.priority:

                    self.elements.insert(idx, element)
                    break

                idx += 1

                if idx == self.num:

                    self.elements.append(element)
                    break

        self.num += 1

    ##########################################################################
	##########################################################################

    def isEmpty(self):
        return self.elements == []

    ##########################################################################
	##########################################################################

    def size(self):
        return len(self.elements)

##########################################################################
##########################################################################
#------------------------------------------------------------------------#
##########################################################################
##########################################################################

class ChuStack(object):

    def __init__(self):
        self.elements = []
        self.size = 0

    def length(self):
        return len(self.elements)

    def push(self, item):
        self.elements.append(item)
        self.size += 1

    def look(self):
    	return self.elements[len(self.elements) - 1]

    def pop(self):
        self.size -= 1
        return self.elements.pop()

    def isEmpty(self):
    	return self.elements == []

##########################################################################
##########################################################################
#------------------------------------------------------------------------#
##########################################################################
##########################################################################

class ChuQueue(object):

    def __init__(self):

        self.elements = []
        self.num = 0

    def isEmpty(self):

        return self.elements == []

    def enqueue(self, item):

        self.elements.insert(0, item)
        self.num += 1

    def dequeue(self):

        self.num -= 1
        return self.elements.pop()

    def size(self):
        return len(self.elements)
