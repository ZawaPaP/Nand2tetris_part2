
class  SymbolTable():

    TYPE = [
        'int',
        'char',
        'boolean'
        # or class Name
    ]

    KIND = {
        'FIELD': 'field',
        'STATIC':'static',
        'ARG': 'argument',
        'VAR': 'local'
    }

    def __init__(self):
        self.symbolTable = {}
        self.classTable = []
        self.subroutineTable = []
        self.className = ""


    def Constructor(self):
        self.symbolTable = {
            'class': self.classTable,
            'subroutine': self.subroutineTable
        }
        print (self.symbolTable)

    """
    classTable and subroutineTable ex.
    [
        {'name': 'x', 'type': 'int', 'kind': 'field', 'count': 0},
        ...
    ]
    """

    def startSubroutine(self):
        print("subroutineTable: ")
        print(self.subroutineTable)
        self.subroutineTable.clear()

    def define(self, name, Type, kind, count):
        """
        print("name: ")
        print(name)
        print("type: ")
        print(Type)
        print("kind: ")
        print(kind)
        print("count: ")
        print(count)
        """
        if kind == 'static' or kind == 'field':
            defined_names = [row.get('name') for row in self.classTable]
            if not name in defined_names:
                #count = self.varCount(kind, self.classTable)
                row = {
                    'name': name,
                    'type': Type,
                    'kind': kind,
                    'count': count
                }
                self.classTable.append(row)
        elif kind == 'argument':
            defined_names = [row.get('name') for row in self.subroutineTable]
            if not name in defined_names:
                #count = self.varCount(kind, self.subroutineTable)
                row = {
                    'name': name,
                    'type': Type,
                    'kind': kind,
                    'count': count
                }
                self.subroutineTable.append(row)
        elif kind == 'var':
            defined_names = [row.get('name') for row in self.subroutineTable]
            if not name in defined_names:
                #count = self.varCount(kind, self.subroutineTable)
                row = {
                    'name': name,
                    'type': Type,
                    'kind': "local",
                    'count': count
                }
                self.subroutineTable.append(row)
        else:
            print("define: not defined kind")

    def varCount(self, kind):
        subroutine_kinds = [row.get('kind') for row in self.subroutineTable]
        class_kinds = [row.get('kind') for row in self.classTable]
        subroutine_count = subroutine_kinds.count(kind)
        class_count = class_kinds.count(kind)
        if not subroutine_count == 0:
            #print("varCount_subroutine")
            return subroutine_count
        elif not class_count == 0:
            #print("varCount_class")
            return class_count
        else:
            return 0


    def KindOf(self, name):
        s_name = [row.get('name') for row in self.subroutineTable]
        c_name = [row.get('name') for row in self.classTable]
        if name in s_name:
            return [x for x in self.subroutineTable if x['name'] == name][0].get('kind')
        elif name in c_name:
            return [x for x in self.classTable if x['name'] == name][0].get('kind')
        else:
            print("kind is not defined in the tables")
            print(name)
            print(self.subroutineTable)
            return None


    def TypeOf(self, name):
        s_name = [row.get('name') for row in self.subroutineTable]
        c_name = [row.get('name') for row in self.classTable]
        if name in s_name:
            return [x for x in self.subroutineTable if x['name'] == name][0].get('type')
        elif name in c_name:
            return [x for x in self.classTable if x['name'] == name][0].get('type')
        else:
            print("type is not defined in the tables")
            print(name)
            return None


    def IndexOf(self, name):
        s_name = [row.get('name') for row in self.subroutineTable]
        c_name = [row.get('name') for row in self.classTable]
        if name in s_name:
            return [x for x in self.subroutineTable if x['name'] == name][0].get('count')
        elif name in c_name:
            return [x for x in self.classTable if x['name'] == name][0].get('count')
        else:
            print("name is not defined in the tables")
            print(name)
            return None
