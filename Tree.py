from collections import deque
from definitions import objectTypes


class Tree(deque):
    def addToTree(self, ty, val):
        self.append({'type': ty, 'value': val})

    def popLeftObject(self):
        try:
            lObj = Tree([self.popleft()])
        except:
            lObj = None
            raise IndexError
        while self:
            if self[0]['type'] not in objectTypes:
                lObj.append(self.popleft())
            else:
                break
        return lObj

    def popRightObject(self):
        rObj = Tree([])
        while self:
            rObj.appendleft(self.pop())
            if rObj[0]['type'] in objectTypes:
                break
        return rObj
