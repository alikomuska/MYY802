import sys


################################
###       ALPHABET           ###
################################


KEYWORDS = {
    'main', 'def', '#def', '#int', 'global', 'if', 'elif', 'else',
    'while', 'print', 'return', 'input', 'int', 'and', 'or', 'not'}

LETTERS=('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
DIGITS=('0123456789')
OPERATORS = set({'+', '-', '*', '//', '%', '<', '>', '==', '<=', '>=', '!=', '='})
SEPARATORS = set({',', ':'})
GROUPING_SYMBOLS = set({'(', ')', '#{', '#}'})
COMMENT_SYMBOL = set('##')



###############################
###         TOKENS          ###
###############################

class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value =value
        self.line = line

    def __repr__(self):
        if self.value: 
            return f'{self.type}:{self.value}'
        return f'{self.type}'
    


###################################
###           ERRORS            ###
###################################

class Error:
    def  __init__(self,error_name,details):
        self.error_name=error_name
        self.details=details

    def as_string(self):
        result=f'{self.error_name}:{self.details}'
        return result      

class Illegalchar(Error):
    def __init__(self,details):
        super().__init__('Illegal char',details)




#####################################
###            LEXER              ###
#####################################
    
class Lexer:
    def __init__(self, sourceCode):
        self.pos = -1
        self.line = 1
        self.current_char = None
        self.tokens = [] 
        self.sourceCode = sourceCode
        self.sourceCodeSize = len(sourceCode)
        self.token_index=-1
        self.make_tokens()
        
    def  advance(self):
        self.pos+=1
        if self.pos < self.sourceCodeSize: # < or <=
            self.current_char=self.sourceCode[self.pos] 
        else: 
             self.current_char=None
        return            


    def make_tokens(self):
       
        self.advance()

        while self.current_char!=None:
            if self.current_char == '\t' or self.current_char == ' ':
                self.advance()
                continue
            elif self.current_char in DIGITS :
                current_token = self.make_number()
            elif self.current_char in LETTERS:
                current_token = self.make_word()
            elif self.current_char in OPERATORS:
                current_token = self.make_operators()
            elif self.current_char in GROUPING_SYMBOLS|COMMENT_SYMBOL:
                current_token = self.make_group_symbols()
            elif self.current_char in COMMENT_SYMBOL:
                self.advance()
                continue # todo self.comment 
            elif self.current_char == '\n':
                self.line+=1
                self.advance()
                continue
            else:
                char=self.current_char
                return[] ,Illegalchar("'"+char+"'")

            self.tokens.append(current_token)

        return self.tokens, None       


    def make_word(self):
        result = ''
        while self.current_char is not None and self.current_char in LETTERS:
                result += self.current_char
                self.advance()
        if result in KEYWORDS:
            return Token('keyword', result, self.line)
        else:        
            return Token('WORD', result, self.line)


    def make_number(self):
        num_str = ''
    
        while self.current_char is not None and self.current_char in DIGITS :
            num_str += self.current_char
            self.advance()
    
        # Check if the next character is an illegal character
        if self.current_char is not None and self.current_char in LETTERS:
            return [], Illegalchar("'" + self.current_char + "'")

        # Create a token for the integer value
        return Token('INT', int(num_str), self.line)


    def make_operators(self):
        result=''
        while self.current_char is not None and self.current_char in OPERATORS:
                result += self.current_char
                self.advance()
        return Token('OPERATOR', result, self.line)
       

    def make_group_symbols(self):
        result=''
        while self.current_char is not None and self.current_char in GROUPING_SYMBOLS|COMMENT_SYMBOL:
                result += self.current_char
                self.advance()
                if self.current_char=='{' or self.current_char=='}':
                    result+=self.current_char
                    return Token('GROUP_SYMBOL',result, self.line)
                elif self.current_char=='#':
                    result +=self.current_char
                    return Token('COMMENT_SYMBOL',result, self.line)
        return Token('GROUP_SYMBOL', result, self.line)
    
    def return_token(self):
        self.token_index+=1
        if self.token_index>=len(self.tokens):
            return None
        return self.tokens[self.token_index]


##################################
###          PARSER            ###
##################################

class Parser:

    def __init__(self, sourceCode):
        self.lex = Lexer(sourceCode)
        self.lex.make_tokens()

    def while_state():

        #condition

        while_token = self.return_token()
        if(while_token.value != ':'):
            print("Error...")
            return #kill prog


        #statments TO DO




    def if_state():
        #since you are inside the if_block then you know that the previous token was "if" 

        #check for condition
        self.condition()

        #check for :
        if_token = self.lex.return_token()
        if(if_token.value != ':'):
            print("Error") 
            return #kill program

        #check for: if, while, ekxorisi, return,  print, input
        self.decide_flow() 

        #check for elif
        if_token = self.lex.return_token()
        if(if_token.value != "elif"):
            return if_token 

        next_token = self.if_block()

        #check for else
        if(next_token.value != 'else'):
            return next_token

        #check for ':'
        if_token = self.lex.return_token()
        if(if_token.value != ':'):
            print("Error") #kill program
            return 

        self.decide_flow()
        
        return #if you get a token that you wont use, then you reaturn it


    def statement_state:
        
        #simple_statement
        #strctured_statment



    def dicede_flow_state():

        



        return







    def condition_state:

        return


    def print_state:

        print_token = self.return_token()     
        if(print_token.value != '('):
            print("Error")
            return #kill

        #expression

        print_token = self.return_token()
        if(print_token.value != ')')
            print("Error")
            return #kill

    def assignment_state:

        assignment_token = self.return_token()
        if(assignment_token.value != '='):
            print("Error...")
            return


    def simple_statement:
        simple_token = self.return_token()
        #assignment check
        if(simple_token.type == 'ID'):
            self.assignment_state()

        #print check
        if(simple_token.value == "print"):
            self.print_state()

        #return check
        if(simple_token.value == "return"):


    def input_state:
        input_token = self.return_token()
        if(input_token.value != "return"):
            self.return_state()
    

    def return_state:
        return_token = self.return_token()
        if(return_token != '('):
            print("Error... ")
        

    def syntax_analyzer(self):
        print(self.currentToken)
        self.currentToken = self.lex.return_token()

#main function
def main():
    inputFilePath = sys.argv[-1]
    sourceCode = open(inputFilePath).read()
    par = Parser(sourceCode)
    par.syntax_analyzer()

if __name__ == "__main__":
    main()
