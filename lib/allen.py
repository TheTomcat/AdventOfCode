from enum import Enum

class Relation(Enum):
    EQUALS = 'eq'
    BEFORE = 'b'
    AFTER = 'bi'
    MEETS = 'm'
    MET_BY = 'mi'
    OVERLAPS = 'o'
    OVERLAPPED_BY = 'oi'
    STARTS = 's'
    STARTED_BY = 'si'
    DURING = 'd'
    CONTAINS = 'di'
    FINISHES = 'f'
    FINISHED_BY = 'fi'

class AllenInterval:
    '''Implements Allen's interval algebra
    https://stackoverflow.com/questions/325933/determine-whether-two-date-ranges-overlap
    
    X equals Y -> X eq Y
    ** Shortcut '=' operator
    |--X--|
    |--Y--|

    X before Y (inv. after) 
    X b Y (inv. X bi Y)
    ** Shortcut '<' or '>' operator
    |--X--|
            |--Y--|
    
    X meets Y (inv. met by)
    X m Y (inv. X mi Y)
    ** Shortcut '<=' or '>=' operator
    |--X--|
          |--Y--|
    
    X finishes Y (inv. finished by)
    X f Y (inv. X fi Y)
      |--X--|
    |---Y---|

    X starts Y (inv. started by)
    X s Y (inv. X si Y)
    |--X--|
    |---Y---|

    X during Y (inv. contains)
    X d Y (inv. X di Y)
      |--X--|
    |----Y----|

    X overlaps with Y (inv. overlapped by)
    X o Y (inv. X oi Y)
    |--X--|
      |--Y--|
    '''

    def __init__(self, start: float, end: float) -> None:
        self.__start = min(start, end)
        self.__end = max(start, end)

    def relation(self, other: 'AllenInterval') -> 'Relation':
        'return the period relation from self to other'
        relations = {Relation.EQUALS : self.equals, 
                     Relation.BEFORE: self.before,
                     Relation.AFTER: self.after,
                     Relation.MEETS: self.meets,
                     Relation.MET_BY: self.met_by,
                     Relation.OVERLAPS: self.overlaps,
                     Relation.OVERLAPPED_BY: self.overlapped_by,
                     Relation.STARTS: self.starts,
                     Relation.STARTED_BY: self.started_by,
                     Relation.DURING: self.during,
                     Relation.CONTAINS: self.contains,
                     Relation.FINISHES: self.finishes,
                     Relation.FINISHED_BY: self.finished_by}
        for relation, operation in relations.items():
            if operation(other):
                return relation

    def equals(self, other: 'AllenInterval') -> bool:
        '''
        |--X--|
        |--Y--|'''
        return (
            other.__start == self.__start and
            other.__end == self.__end
        )

    def __eq__(self, other: 'AllenInterval') -> bool:
        return self.equals(other)
    
    def before(self, other: 'AllenInterval') -> bool:
        '''
        |--X--|
                |--Y--|'''
        return self.__end < other.__start

    def __lt__(self, other: 'AllenInterval') -> bool:
        return self.before(other)

    def after(self, other: 'AllenInterval') -> bool:
        '''
                |--X--|
        |--Y--|'''
        return other.before(self)

    def __gt__(self, other: 'AllenInterval') -> bool:
        return self.after(other)

    def meets(self, other: 'AllenInterval') -> bool:
        '''
        |--X--|
              |--Y--|'''
        return self.__end == other.__start
    
    def __le__(self, other: 'AllenInterval') -> bool:
        return self.meets(other)

    def met_by(self, other: 'AllenInterval') -> bool:
        '''
              |--X--|
        |--Y--|'''
        return other.meets(self)
    
    def __ge__(self, other: 'AllenInterval') -> bool:
        return self.met_by(other)

    def finishes(self, other: 'AllenInterval') -> bool:
        '''
              |--X--|
            |---Y---|'''
        return (
            self.__end == other.__end and
            self.__start > other.__start
        )

    def finished_by(self, other: 'AllenInterval') -> bool:
        '''
            |---X---|
              |--Y--|'''
        return other.finishes(self)

    def starts(self, other: 'AllenInterval') -> bool:
        '''
            |--X--|
            |---Y---|'''
        return (
            self.__start == other.__start and
            self.__end < other.__end
        )

    def started_by(self, other: 'AllenInterval') -> bool:
        '''
            |---X---|
            |--Y--|'''
        return other.starts(self)

    def during(self, other: 'AllenInterval') -> bool:
        '''
              |--X--|
            |----Y----|'''
        return (
            other.__start < self.__start and
            self.__end < other.__end
        )

    def contains(self, other: 'AllenInterval') -> bool:
        '''
            |----X----|
              |--Y--|'''
        return other.during(self)

    def overlaps(self, other: 'AllenInterval') -> bool:
        '''
            |--X--|
                |--Y--|'''
        return (
            self.__start < other.__start and
            self.__end < other.__end and
            self.__end > other.__start
        )

    def overlapped_by(self, other: 'AllenInterval') -> bool:
        '''
                |--X--|
            |--Y--|'''
        return other.overlaps(self)
    
    def has_inside(self, other: 'AllenInterval') -> bool:
        'X is contained entirely within Y'
        return (other.__start <= self.__start) and (other.__end >= self.__end)
    
    def intersects(self, other: 'AllenInterval') -> bool:
        'there is an intersection (even an instantaneous intersection) between X and Y'
        return (self.__start <= other.__end) and (other.__start <= self.__end)

def test():
    x = AllenInterval(3,6)
    a = AllenInterval(0,1) # before
    assert a.before(x)
    assert x.after(a)
    assert a.relation(x) == Relation.BEFORE
    b = AllenInterval(0,3) # meets
    assert b.meets(x)
    assert x.met_by(b)
    assert b.relation(x) == Relation.MEETS
    c = AllenInterval(0,4)
    assert c.overlaps(x)
    assert x.overlapped_by(c)
    assert c.relation(x) == Relation.OVERLAPS
    d = AllenInterval(3,7) 
    assert d.started_by(x)
    assert x.starts(d)
    assert d.relation(x) == Relation.STARTED_BY
    e = AllenInterval(3,5) # 
    assert e.starts(x)
    assert x.started_by(e)
    assert e.relation(x) == Relation.STARTS
    f = AllenInterval(4,5)
    assert f.during(x)
    assert x.contains(f)
    assert f.relation(x) == Relation.DURING
    g = AllenInterval(4,6)
    assert g.finishes(x)
    assert x.finished_by(g)
    assert g.relation(x) == Relation.FINISHES
    h = AllenInterval(3,6)
    assert h.equals(x)
    assert x.equals(h)
    assert h.relation(x) == Relation.EQUALS
    i = AllenInterval(1,9)
    assert i.contains(x)
    assert x.during(i)
    assert i.relation(x) == Relation.CONTAINS
    j = AllenInterval(1,6)
    assert j.finished_by(x)
    assert x.finishes(j)
    assert j.relation(x) == Relation.FINISHED_BY
    k = AllenInterval(4,9)
    assert k.overlapped_by(x)
    assert x.overlaps(k)
    assert k.relation(x) == Relation.OVERLAPPED_BY
    l = AllenInterval(6,9)
    assert l.met_by(x)
    assert x.meets(l)
    assert l.relation(x) == Relation.MET_BY
    m = AllenInterval(7,9)
    assert m.after(x)
    assert x.before(m)
    assert m.relation(x) == Relation.AFTER
   
    n = AllenInterval(6,3)
    assert n.equals(x)