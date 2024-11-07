##auther amir creating my own programming language

DIGITS = '0123456789'

#################################
# ERROR
#################################

class Error:
    def __init__(self, error_name, details, pos_start, pos_end) -> None:
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f' file: {self.pos_start.file_name}, line: {self.pos_start.ln}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__("Illegal Char", details, pos_start, pos_end)

class Position:
    def __init__(self, index, col, ln, file_name, file_text) -> None:
        self.index = index
        self.col = col
        self.ln = ln
        self.file_name = file_name
        self.file_text = file_text
    
    def advance(self, current_char):
        self.index += 1
        self.col += 1
        if current_char == "\n":
            self.ln += 1
            self.col = 0
        return self
    
    def copy(self):
        return Position(self.index, self.col, self.ln, self.file_name, self.file_text)

#################################
# TOKEN
#################################

TT_INT = "TT_INT"
TT_FLOAT = "TT_FLOAT"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"

class Token:
    def __init__(self, type_, value=None) -> None:
        self.type = type_
        self.value = value

    def __repr__(self) -> str:
        if self.value: return f"{self.type}:{self.value}"
        return f"{self.type}"

# LEXER: A lexer (short for lexical analyzer) is a component 
# of the compiler or interpreter responsible for breaking down
# raw source code into a series of tokens.

class Lexer:
    def __init__(self, file_name, text) -> None:
        self.text = text
        self.file_name = file_name
        self.position = Position(-1, 0, 0, file_name, text)
        self.current_char = None
        self.advance()

    def advance(self):
        """
        Advances the current position in the text by one character
        and updates the current character.
        """
        self.position.advance(self.current_char)
        self.current_char = self.text[self.position.index] if self.position.index < len(self.text) else None

    def make_tokens(self):
        """
        Processes the input text and generates a list of tokens.

        Returns:
            tuple: A list of tokens and an error, if any. If an illegal character
                is encountered, returns an error with the offending character.
        """
        
        tokens = []
        while self.current_char is not None:
            if self.current_char in " \t":
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                pos_start = self.position.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.position, "'" + char + "'")
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))

#################################
# NODES
#################################
class NumberNode:
    def __init__(self, tok) -> None:
        self.tok = tok
    def __repr__(self) -> str:
        return f"{self.tok}"

class BinaryOperationNode:
    def __init__(self, right_node, left_node, op_tok) -> None:
        self.right_node = right_node
        self.left_node = left_node
        self.op_tok = op_tok
    def __repr__(self) -> str:
        return f"{self.right_node}, {self.op_tok}, {self.left_node}"

#################################
# Parser : A parser is a component that processes input data 
# (like code, text, or commands) and converts it into a structured 
# format that a program can work with.
#################################

class Parser:
    def __init__(self, tokens:list) -> None:
        self.tokens = tokens
        self.tok_index = -1
        self.current_token = ""
        self.advance()
    def advance(self):
        self.tok_index +=1
        if self.tok_index < len(self.tokens):
            self.current_token = self.tokens[self.tok_index]
        return self.current_token
    def term():
        pass
    def exprasion():
        pass
    def factor():
        pass

#################################
# RUN
#################################

def run(file_name, text):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()
    return tokens, error
