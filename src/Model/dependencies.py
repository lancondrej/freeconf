#!/usr/bin/python
#
# dependencies.py
# begin: 16.10.2010 by Jan Ehrenberger
#
# PyFC: Dependecies 
#

import re
from src.Model.lists import boolList, FuzzyList
from src.Model.exception_logging.log import log
from src.Model.constants import Types


# Exceptions
class FcDependencyException(Exception):
    def __init__(self, msg=None):
        Exception.__init__(self, msg)
        if msg is not None:
            log.error("Dependency: " + msg)


class SymbolValue:
    """Class representing actual value of the symbol. Use this as a retrun value for function SymbolBase.value"""

    def __init__(self, data, fuzzy_list=None):
        assert fuzzy_list is None or isinstance(fuzzy_list, FuzzyList)
        if type(data) == bool:
            # Bool value -> Set bool list
            self.list = boolList
            self.data = boolList.getMaxGrade(float(data)).value
        else:
            self.data = data
            self.list = fuzzy_list

    def grade(self):
        if self.list is None:
            raise FcDependencyException("Value '%s' does not have fuzzy list defined!" % (str(self.data),))
        e = self.list.getEntry(self.data)
        return e.grade

    def repr(self):
        """Return representation of the value."""
        return self.data


# Token classes
class SymbolBase:
    """Base class for all other tokens."""
    id = None  # Token identifier
    first = second = None  # used by tree nodes
    priority = None  # Left binding power

    def nud(self):
        """Null denotation. Used for values and prefix operators. For example literals or operator 'not'."""
        raise FcDependencyException("Syntax error (%r)!" % (self.id, ))

    def led(self, left):
        """Left denotation. Used for operators with two operands (infix operators). For example operator 'and'."""
        raise FcDependencyException("Unknown operator (%r)!" % (self.id, ))

    def unlink(self, dep):
        """Recursively remove references to given dependency from dependent objects."""
        if self.first is not None:
            self.first.unlink(dep)
        if self.second is not None:
            self.second.unlink(dep)

    def value(self):
        """Return token's value. It must be of type SymbolValue."""
        raise NotImplementedError("Not implemented abstract method!")

    def __repr__(self):
        out = [self.id, self.first, self.second]
        out = map(str, filter(None, out))
        return "(" + " ".join(out) + ")"


class TokEnd(SymbolBase):
    """Dummy symbol marking end of expression."""
    id = "(end)"
    priority = 0  # Because of zero priority, parser will stop on this token


class TokName(SymbolBase):
    id = "(name)"
    priority = 0

    def __init__(self, name, dep, config_tree):
        self.name = name
        # Find config entry for this name
        self.centry = config_tree.recursiveFindCEntry(self.name)
        if self.centry == None:
            raise FcDependencyException("Failed to find entry %s in dependency '%s' !" % (self.name, dep.conditionText))
        # Add reference to dependency to centry so that the dependency updates whenever centry changes.
        self.centry.addDependent(dep)

    def nud(self):
        return self

    def value(self):
        if self.centry.type in (FcTypes.FUZZY, FcTypes.BOOL):
            return SymbolValue(self.centry.value, self.centry.list)
        else:
            return SymbolValue(self.centry.value)

    def unlink(self, dep):
        """Remove referece to given dependency from dependent obejct."""
        if self.centry != None:
            self.centry.removeDependent(dep)

    def __repr__(self):
        return "(%s %s)" % (self.id[1:-1], str(self.name))


class TokLiteral(SymbolBase):
    """Base class for literal tokens."""
    priority = 0

    def __init__(self, value):
        self.__value = value

    def nud(self):
        return self

    def value(self):
        return self.__value

    def __repr__(self):
        return "(%s %s)" % (self.id[1:-1], str(self.__value.repr()))


class TokLiteralString(TokLiteral):
    id = "(string)"

    def __init__(self, value):
        TokLiteral.__init__(self, SymbolValue(value))


class TokLiteralNumber(TokLiteral):
    id = "(number)"

    def __init__(self, value):
        # Convert value to appropriate number from string
        if type(value) in (str, unicode):
            if "." in value:
                value = float(value)
            else:
                value = int(value)
        TokLiteral.__init__(self, SymbolValue(value))


class TokLiteralBool(TokLiteral):
    id = "(bool)"

    def __init__(self, value):
        if value in ("YES", "TRUE", "1"):
            value = True
        else:
            value = False
        TokLiteral.__init__(self, SymbolValue(value, boolList))


class TokOperator(SymbolBase):
    """Base class for operators."""
    __parser = None

    @property
    def parser(self):
        """This is write only property."""
        raise AttributeError

    @parser.setter
    def parser(self, val):
        self.__parser = parser


class TokOperatorInfix(TokOperator):
    """Base class for infix operators."""

    def led(self, left):
        self.first = left
        self.second = self.parser.expression(self.priority)
        return self


class TokOperatorPrefix(TokOperator):
    """Base class for prefix operators."""

    def nud(self):
        self.first = self.parser.expression(self.priority)
        self.second = None
        return self


class TokOperatorAnd(TokOperatorInfix):
    """Token for fuzzy AND operator."""
    id = "AND"
    priority = 10

    def value(self):
        """Return value with minimum grade."""
        v1 = self.first.value()
        v2 = self.second.value()
        # Find value with min fuzzy grade
        mv = min(v1, v2, key=lambda x: x.grade())
        l = v1.list.joinList(v2.list)  # Join value lists
        return SymbolValue(mv.data, l)


class TokOperatorOr(TokOperatorInfix):
    """Token for OR operator."""
    id = "OR"
    priority = 10

    def value(self):
        """Return value with maximum grade."""
        v1 = self.first.value()
        v2 = self.second.value()
        # Find value with max fuzzy grade
        mv = max(v1, v2, key=lambda x: x.grade())
        l = v1.list.joinList(v2.list)  # Join value lists
        return SymbolValue(mv.data, l)


class TokOperatorNot(TokOperatorPrefix):
    """Token for Not operator."""
    id = "NOT"
    priority = 20

    def value(self):
        # Get value with negated grade
        val = self.first.value()
        grade = 1.0 - val.grade()
        entry = val.list.getMaxGrade(
            grade)  # Get value with maximum allowed grade. If there is no value with such a grade, it will return nearest lower value.
        if entry.grade != grade:
            # COMBAK: Je tato chyba nutna?
            raise FcDependencyException("TokOperatorNot: Failed to find fuzzy value with grade %f in list!" % (grade,))
        return SymbolValue(entry.value, val.list)


class TokOperatorEqual(TokOperatorInfix):
    """Token for = operator."""
    id = "="
    priority = 30

    def value(self):
        a = self.first.value()
        b = self.second.value()
        return SymbolValue(a.repr() == b.repr())


class TokOperatorNEqual(TokOperatorInfix):
    """Token for != operator."""
    id = "!="
    priority = 30

    def value(self):
        a = self.first.value()
        b = self.second.value()
        return SymbolValue(a.repr() != b.repr())


class TokOperatorGT(TokOperatorInfix):
    """Token for GT operator."""
    id = "GT"
    priority = 30

    def value(self):
        a = self.first.value()
        b = self.second.value()
        return SymbolValue(a.repr() > b.repr())


class TokOperatorLT(TokOperatorInfix):
    """Token for LT operator."""
    id = "LT"
    priority = 30

    def value(self):
        a = self.first.value()
        b = self.second.value()
        return SymbolValue(a.repr() < b.repr())


class TokOperatorGE(TokOperatorInfix):
    """Token for GE operator."""
    id = "GE"
    priority = 30

    def value(self):
        a = self.first.value()
        b = self.second.value()
        return SymbolValue(a.repr() >= b.repr())


class TokOperatorLE(TokOperatorInfix):
    """Token for LE operator."""
    id = "LE"
    priority = 30

    def value(self):
        a = self.first.value()
        b = self.second.value()
        return SymbolValue(a.repr() <= b.repr())


class TokOperatorIn(TokOperatorInfix):
    """Token for IN operator."""
    id = "IN"
    priority = 30

    def value(self):
        # First argument is string value, second argument is name of list
        val = str(self.first.value().repr())
        list_name = str(self.second.value().repr())
        # Find the value list
        value_list = None
        if self.parser != None and self.parser.lists != None:
            if list_name in self.parser.lists:
                value_list = self.parser.lists[list_name]
            else:
                raise FcDependencyException("List %s was not found!" % (list_name,))
        else:
            raise FcDependencyException("No lists available!")
        # Test if value is in the list
        entry = value_list.getEntry(val)
        return SymbolValue(entry != None)


class TokOperatorLeftParenthesis(TokOperator):
    """Token for left parenthesis. Process simple parenthesis and function calls."""
    id = "("
    priority = 200  # Parenthesis should have highest priority, so that it can override all other operators.

    def nud(self):
        expr = self.parser.expression()
        self.parser.advance(")")
        return expr


class TokOperatorRightParenthesis(TokOperator):
    """Token for right parenthesis."""
    id = ")"
    priority = 0  # Right parenthesis ends the subexpression, so it should have lowest priority


class TokOperatorComma(TokOperator):
    """Token for comma as a separator in list of function arguments."""
    id = ","
    priority = 0  # Comma is basically delimiter of expressions, so it should have lowest priority


class TokFunction(TokOperator):
    """Base class for functions."""

    def nud(self):
        """Treat function as prefix operator. This function parses list of it's arguments."""
        self.parser.advance("(")  # Skip parenthesis
        self.first = []  # List of arguments
        if self.parser.token.id != ")":
            while True:
                self.first.append(self.parser.expression())
                if self.parser.token.id != ",":
                    break
                self.parser.advance(",")  # Skip next argument delimiter
        self.parser.advance(")")  # Skip end of function
        return self

    def checkArgsNum(self, expect):
        if (len(self.first) != expect):
            raise FcDependencyException(
                "Wrong number of arguments to function %s! Expected %d, got %d."
                % (self.id, expect, len(self.first))
            )


class TokFunctionMin(TokFunction):
    id = "MIN"

    def value(self):
        """Return argument with least value."""
        return min([a.value() for a in self.first], key=lambda x: x.repr())


class TokFunctionMax(TokFunction):
    id = "MAX"

    def value(self):
        """Return argument with greatest value."""
        return max([a.value() for a in self.first], key=lambda x: x.repr())


## String Functions
class TokFunctionStrLen(TokFunction):
    id = "STRLEN"

    def value(self):
        self.checkArgsNum(1)
        return SymbolValue(len(self.first[0].value().repr()))


class TokFunctionSubStr(TokFunction):
    id = "SUBSTR"

    def value(self):
        self.checkArgsNum(3)
        s = self.first[0].value().repr()
        f = int(self.first[1].value().repr())
        l = int(self.first[2].value().repr())
        return SymbolValue(s[f:f + l])


class TokFunctionStrPos(TokFunction):
    id = "STRPOS"

    def value(self):
        self.checkArgsNum(2)
        a = self.first[0].value().repr()
        b = self.first[1].value().repr()
        return SymbolValue(a.find(b))


## Conversion Functions

class TokFunctionString(TokFunction):
    """Function converting any object into it's string representation."""
    id = "STRING"

    def value(self):
        self.checkArgsNum(1)
        return SymbolValue(str(self.first[0].value().repr()))


class TokFunctionNumber(TokFunction):
    """Function converting string object into number."""
    id = "NUMBER"

    def value(self):
        self.checkArgsNum(1)
        arg = self.first[0].value().repr()
        val = 0
        try:
            val = float(arg)
        except ValueError:
            log.warning("Failed to convert '%s' to number!" % (arg,))
        return SymbolValue(val)


class TokFunctionFuzzy(TokFunction):
    """Function creating fuzzy entry."""
    id = "FUZZY"

    def value(self):
        # First argument is string value, second argument is name of the fuzzy list
        self.checkArgsNum(2)
        list_name = str(self.first[1].value().repr())
        # Find the fuzzy list
        fuzzy_list = None
        if self.parser != None and self.parser.lists != None:
            if list_name in self.parser.lists:
                fuzzy_list = self.parser.lists[list_name]
            else:
                raise FcDependencyException("Fuzzy list %s was not found!" % (list_name,))
        else:
            raise FcDependencyException("No fuzzy lists available!")
        # Return value with fuzzy list
        return SymbolValue(str(self.first[0].value().repr()), fuzzy_list)


#### Input ####

class TopDownParser:
    """Abstract class defining Top Down parser"""

    symbol_table = {}
    token = None

    def registerSymbol(self, sym_class):
        """Register given symbol class to symbol table. The class has to inherited from SymbolBase class."""
        self.symbol_table[sym_class.id] = sym_class


    def tokenize(self, text):
        """Generator that will divide text into tokens and return their objects."""
        raise TypeError("Abstract method tokenize called!")

    def expression(self, prio=0):
        t = self.token
        self.token = self.next()  # Returns next token
        left = t.nud()
        # Continue with processing higher priority tokens
        while prio < self.token.priority:
            t = self.token
            self.token = self.next()
            left = t.led(left)
        return left

    def parse(self, text):
        log.debug("Parsing expression: " + text)
        try:
            # Set next to next token function (tokenize is a generator)
            self.next = self.tokenize(text).next
            self.token = self.next()
            return self.expression()
        except StopIteration:
            # Parsing of empty string should result in None
            return None

    def advance(self, id):
        """Set expectation to next token and go to next token if it occured in the code."""
        if id and self.token.id != id:
            raise FcDependencyException("Expected (%r) got %r instead!" % (id, self.token))
        self.token = self.next()

    def __init__(self):
        # Register dummy symbol marking end of expression.
        self.registerSymbol(TokEnd)


class DependencyParser(TopDownParser):
    # Regular expression dividing text into tokens.
    # Should return tuple of (word, literal, operator) for each token of input text.
    r_token = re.compile("\s*(?:([_/A-Za-z]+[-_/A-Za-z0-9]*)|('[^']*'|\"[^\"]*\")|([.0-9]+)|(!=|=|\(|\)|,))")

    def __init__(self):
        TopDownParser.__init__(self)

        ## Register symbols for our dependency language
        self.registerSymbol(TokOperatorAnd)
        self.registerSymbol(TokOperatorOr)
        self.registerSymbol(TokOperatorEqual)
        self.registerSymbol(TokOperatorNEqual)
        self.registerSymbol(TokOperatorGT)
        self.registerSymbol(TokOperatorLT)
        self.registerSymbol(TokOperatorLE)
        self.registerSymbol(TokOperatorGE)
        self.registerSymbol(TokOperatorIn)
        self.registerSymbol(TokOperatorNot)
        self.registerSymbol(TokOperatorLeftParenthesis)
        self.registerSymbol(TokOperatorRightParenthesis)
        self.registerSymbol(TokOperatorComma)
        self.registerSymbol(TokFunctionMin)
        self.registerSymbol(TokFunctionMax)
        self.registerSymbol(TokFunctionStrLen)
        self.registerSymbol(TokFunctionSubStr)
        self.registerSymbol(TokFunctionStrPos)
        self.registerSymbol(TokFunctionString)
        self.registerSymbol(TokFunctionNumber)
        self.registerSymbol(TokFunctionFuzzy)

        self.value_table = {
            "YES": TokLiteralBool,
            "NO": TokLiteralBool,
            "TRUE": TokLiteralBool,
            "FALSE": TokLiteralBool,
        }

    def strip_quotes(self, text):
        return text.strip("'\"")

    def tokenize(self, text):
        """Generator that will tokenize text and return symbol objects"""
        for name, literal, number, operator in self.r_token.findall(text):
            if literal:
                # Process litelral token. par.ex.: "hello"
                literal = self.strip_quotes(literal)
                yield TokLiteralString(literal)
                continue
            elif number:
                # Process number token
                yield TokLiteralNumber(number)
                continue

            # Get name in upper case
            name_u = None
            if name:
                name_u = name.upper()

            if name_u and name_u in self.value_table:
                # Process other values par.ex. yes/no
                value_type = self.value_table[name_u]
                yield value_type(name_u)

            elif name and name_u not in self.symbol_table:
                # Process name token. par.ex.: config
                yield TokName(name, self.dependency, self.config_tree)

            else:
                if name_u:
                    # if name is set here, it has to be in symbol table and therefore is operator
                    # Operators are case insensitive -> convert them to upper case
                    operator = name_u
                # Process operator token. par.ex.: =, and, ...
                symbol_type = self.symbol_table.get(operator)
                if not symbol_type:
                    raise FcDependencyException("Unknown operator (%s)!" % (operator, ))
                # Create object for this operator
                symbol_object = symbol_type()
                symbol_object.parser = self
                yield symbol_object

        symbol = self.symbol_table["(end)"]
        yield symbol()

    def parse(self, text, dep=None, config_tree=None, lists=None):
        self.dependency = dep
        self.config_tree = config_tree
        self.lists = lists
        return TopDownParser.parse(self, text)


#### Dependencies ####


class FcActionSet:
    """Class holding data for one set action. It also stores data in text format as loaded from XML file."""

    def __init__(self, prop=None):
        self.elements = []
        self.elementsText = []
        self.valueType = None
        self.value = None
        self.property = prop

    def resolve(self, root_centry):
        """Resolve action."""
        self.elements = []
        # Find elements in config tree
        for et in self.elementsText:
            e = root_centry.recursiveFindCEntry(et)
            if e == None:
                raise FcDependencyException("Failed to find entry (%s)!" % (et,))
            self.elements.append(e)

    def _elementsDependencyEvent(self, prop, val):
        for e in self.elements:
            log.debug("Setting " + prop + " to " + str(val) + " on " + str(e))
            e.handleDependencyEvent(prop, val)

    def execute(self):
        """Execute action."""
        if self.property == "enable" or self.property == "mandatory" or self.property == "active":
            if self.valueType == "constant":
                if self.value == "yes":
                    self._elementsDependencyEvent(self.property, True)
                elif self.value == "no":
                    self._elementsDependencyEvent(self.property, False)
                else:
                    log.error("Unknown value \"" + self.value + "\" in the dependency, expecting yes or no")
        elif self.property == "value":
            if self.valueType == "constant":
                self._elementsDependencyEvent(self.property, self.value)
            # self.element.setValue(self.value, informGui = True)
            # TODO: valueType reference
        elif self.property == "min" or self.property == "max":
            if self.valueType == "constant":
                try:
                    value = float(self.value)
                    self._elementsDependencyEvent(self.property, value)
                except (ValueError):
                    log.error("Cannot convert " + self.property + " value " + self.value + "to float")
        else:
            log.error("Unknown dependency property " + self.property)
        # raise NotImplementedError


class FcDependency:
    """Class representing dependency."""
    parser = DependencyParser()

    def __init__(self):
        self.conditionText = None  # Original text of condition
        self.condition = None
        self.thenActions = []
        self.elseActions = []

    def resolve(self, root_centry, lists):
        """Parse the condition and store resulting object tree."""
        try:
            self.condition = self.parser.parse(self.conditionText, self, root_centry, lists)
            # Resolve actions:
            for a in self.thenActions:
                a.resolve(root_centry)
            for a in self.elseActions:
                a.resolve(root_centry)
            return True
        except FcDependencyException:
            return False

    def unlink(self):
        """Remove references to this dependency."""
        if self.condition != None:
            self.condition.unlink(self)

    def execute(self):
        """Evaluate condition value and execute then actions or else actions."""
        v = bool(self.condition.value().grade())
        log.debug("Condition '%s' is %s." % (self.conditionText, v))
        if v:
            for a in self.thenActions:
                a.execute()
        else:
            for a in self.elseActions:
                a.execute()
