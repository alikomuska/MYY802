import sys


################################
###       ALPHABET           ###
################################


KEYWORDS = {
    'main', 'def', '#def', '#int', 'global', 'if', 'elif', 'else',
    'while', 'print', 'return', 'input', 'int', 'and', 'or', 'not'}

LETTERS=('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
DIGITS=('0123456789')
OPERATORS = ('+', '-', '*', '%', '<', '>', '==', '<=', '>=', '=')
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
        
    def advance(self):
        self.pos+=1
        if self.pos < self.sourceCodeSize: # < or <=
            self.current_char=self.sourceCode[self.pos] 
        else: 
             self.current_char=None
        return            


    def make_tokens(self):
        special_result=''
        self.advance()

        while self.current_char!=None:
            if self.current_char == '\t' or self.current_char == ' ' or self.current_char =='[' or self.current_char == ']':
                self.advance()
                continue
            elif self.current_char in DIGITS :
                current_token = self.make_number()
            elif self.current_char in LETTERS:
                current_token = self.make_word()
            elif self.current_char in OPERATORS :
                
                current_token = self.make_operators()
            elif self.current_char=="!" :
                special_result+=self.current_char
                self.advance()
                if self.current_char=='=':
                    special_result+=self.current_char
                    self.advance()
                    current_token=Token('OPERATOR', special_result, self.line)
            elif self.current_char=='/':
                special_result+=self.current_char
                self.advance()
                if self.current_char=='/':
                    special_result+=self.current_char
                    self.advance()
                    current_token= Token('OPERATOR', special_result, self.line)
                
            elif self.current_char=='#':
                current_token = self.make_group_symbols()
            elif self.current_char in GROUPING_SYMBOLS:
                current_token=self.make_group_symbols()
            elif self.current_char in SEPARATORS:
                current_token=self.make_seperators()
            elif self.current_char == '\n':
                self.line+=1
                self.advance()
                continue
            else:
                char=self.current_char
                print("Error in lexer:" +char)

            self.tokens.append(current_token)

        return self.tokens, None       


    def make_word(self):
        result = ''
        while self.current_char is not None and (self.current_char in LETTERS  or self.current_char in DIGITS):
                result += self.current_char
                self.advance()
        if result in KEYWORDS:
            return Token('keyword', result, self.line)
        else:        
            return Token('ID', result, self.line)


    def make_number(self):
        num_str = ''
    
        while self.current_char is not None and self.current_char in DIGITS :
            num_str += self.current_char
            self.advance()
        
        #check the range of the number
        number_value = int(num_str)
        if number_value < -36758 or number_value > 36758:
            return Token('ILLEGAL', num_str, self.line)
        # Check if the next character is an illegal character
        if self.current_char is not None and self.current_char in LETTERS:
            print("Error")
            exit()

        # Create a token for the integer value
        return Token('INT', int(num_str), self.line)

    def make_seperators(self):
        result=''
        result+=self.current_char
        self.advance()
        return Token('SEPERATOR', result, self.line)




    def make_operators(self):
        result =''
        while self.current_char is not None and  self.current_char in OPERATORS :
            result += self.current_char
            if result == '-' and self.peek() is not None and self.peek() in DIGITS:
                self.advance() 
                num_token = self.make_number()  # Treat it as a negative number
                num_token.value = -int(num_token.value)  # Negate the value
                return num_token # Consume the digit
                
        
            self.advance()
           
            if result == "/" or result == "!":
                result+=self.current_char
                self.advance()
               
        

        return Token('OPERATOR', result, self.line)
         
    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.sourceCode):
            return self.sourceCode[peek_pos]
        else:
            return None
   

    
    def make_group_symbols(self):
        result = ''
        

        while self.current_char is not None:
            result += self.current_char
            self.advance()

            if result == '#' and self.current_char == '#':
             result += self.current_char
             self.advance()
             return Token('COMMENT_SYMBOL', result, self.line)
            if result =='#' and (self.current_char=='{' or self.current_char=='}'):
                result+=self.current_char
                self.advance()
                return Token('GROUP_SYTMBOL',result,self.line)
            if result in GROUPING_SYMBOLS  :
                self.advance()
                return Token('GROUP_SYMBOL', result, self.line)

            

            if result=='#' and self.current_char in LETTERS:
                 while self.current_char is not None and self.current_char in LETTERS:
                    result += self.current_char
                    self.advance()
            if result in KEYWORDS:
                self.advance()
                return Token('keyword', result, self.line)
            else:
                print(" SYNTAX ERRO")
                exit()
                
        
        return Token('GROUP_SYMBOL', result, self.line)

    
    def get_next_token(self):
        self.token_index+=1
        if self.token_index>=len(self.tokens):
            return Token("EOF", "", self.line)
        return self.tokens[self.token_index]

    def return_token(self):
        self.token_index-=1
        return

##################################
###          PARSER            ###
##################################

class Parser:

    def __init__(self,sourceCode):
        self.lex = Lexer(sourceCode)
        self.current_token = Token("NULL", "", 0)
        self.next_token = Token("NULL" , "", 0)
        self.current_token_init()

    def current_token_init(self):
        while(self.current_token.type == "NULL"):
            self.advance_token()
        return

    def advance_token(self):
        if(self.next_token.value == "##"):
            self.current_token= self.next_token
            self.next_token = self.lex.get_next_token()
            while(elf.next_token != "##"):   
                self.current_token= self.next_token
                self.next_token = self.lex.get_next_token()
        
        self.current_token= self.next_token
        self.next_token = self.lex.get_next_token()
        print("Current token: ", self.current_token.value)
        print("Next token: ", self.next_token.value)
        

    def return_token(self):
        self.lex.return_token()
        return


    def global_state(self):
           
        # Check for the 'global' keyword
        self.advance()
        if self.current_token.type != 'keyword' or self.current_token.value != 'global':
                print("Expected 'global' keyword for global statement")

        self.id_list()

         # Grammar check successful (no data structure returned)

        if(self.next_token.value == "global"):
            self.advance_token()
            self.global_state()

        return 

    #startRule
    def syntax_analyzer(self):
        self.declarations_state()
        self.advance_token()
        if(self.current_token.value != "#def"):
            print("Error at line", self.current_token.line, ". Main function missing")
        self.main_function_state()
        return

    #to be tested
    def declarations_state(self):
        self.assignments_state()
        self.functions_declaration_state()
        return

    #to be tested
    def assignments_state(self):
        #no need to check #int
        self.advance_token()
        if(self.current_token.value != "ID"):
            print("Error at line ", self.current_token.line ,". Expected variable name.")
            exit()
        self.get_next_token()
        if(self.current_token.value != '='):
            print("Error at line ", self.current_token.line ,". Expected '='.")
            exit()
        self.expression()

        if(self.next_token.value == "#int"):
            self.advance_token()
            self.assignments_state()

        return

    #to be tested
    def functions_declaration_state(self):
        #no need to check def
        self.advance_token()
        if(self.current_token.type != "ID"):
            print("Error ...")
            exit()
        self.advance_token()
        if(self.current_token.value != '('):
            print("Error ...")
            exit()

        self.id_list()

        self.advance_token()
        if(self.current_token.value != "#{"):
            print("Error...")
            exit()
        self.advance_token()
            
        #delcarations (assignments)
        self.assignments_state()

        #functions
        self.function_declaration_state()
        
        #globals
        self.global_state()

        #code_block
        self.code_block_state(0) #is_main = 0

        self.advance_token()
        if(self.current_token.value != "#}"):
            print("Error ..")
            exit()
           
        if(self.next_token.value == "def"):
            self.advance_token()
            self.functions_declaration_state()

        return 
    
    #to be done
    def main_function_state(self):
        #no need to check #def
        self.advance_token()
        if(self.current_token.value != "main"):
            print("Error ...")
            exit()

        #delcarations (assignments)
        self.assignments_state()

        #functions
        self.function_declaration_state()

        #globals
        self.global_state()

        #code_block
        self.code_block_state(1) #is_main = 1

        return 
    
    #to be done
    def id_list(self):
        self.advance_token()
        # Check if the current token is an ID
        if( self.current_token.type == 'ID'):
            # Add the first identifier to the list
            
            self.advance_token()
            #to be done /checked 
            # Check for additional identifiers separated by commas
            while self.current_token.value == ',':
                self.advance_token()  # Consume the comma
                if self.current_token.type != 'ID':
                    # If there's a comma but no following identifier, raise an error
                    print("Expected identifier after ','")
                    exit()
                self.advance_token()    
        return
    
     


    def code_block_state(self, is_main):
        self.advance_token()

        if(self.current_token.value == "if"):
            self.if_block()
            return
        elif(self.current_token.value == "while"):
            self.while_state()
            return
        elif(self.current_token.value == "return"):
            self.return_state()
            return
        elif(self.current_token.value == "print"):
            self.print_state()
            return
        elif(self.current_token.type == "ID"):
            self.advance_token()
            if(self.next_token.value == "int"):
                self.input_state()
            else:
                self.assignments_state()
        else:
            print("Error at line", self.current.line, ". Code block not ended properly")
            exit()
        
        #if is_main == 0 run until #}
        if(is_main == 0):
            if(self.next_token.value != "#}"):
                self.advance_token()
                self.code_block_state()
            return

        #if is_main == 1 run until end of file
        if(is_main == 1):
            if(self.next_token.value != ""):
                self.advance_token()
                self.code_block_state()
                return
            else:
                print("Compilation done")
                return
        return

### while, if, print, return , input ###

    #to be tested
    def while_state(self):

        self.condition()

        self.advance_token()
        if(self.current.token.value != ":"):
            print("Error ...")
            exit()

        has_bracket = 0
        if(self.next_token.value == "#{"):
            self.advance_token()
            has_bracket = 1

        self.code_block()

        if(has_bracket == 1 and self.next_token.value != "#}"):
            print("Error at line ". self.next_token.line, ". Missing '#}'")
            exit()
        elif(has_bracket == 1):
            self.advance_token()
            return
        return


    def if_state(self):
        #check for condition
        self.condition()

        #check for :
        self.advance_token()
        if(self.current_token.value != ':'):
            print("Error") 
            exit()

        has_brackets = 0
        if(self.next_token.value == "#{"):
            self.advance_token()
            has_brackets = 1

        #check for: if, while, ekxorisi, return,  print, input
        self.code_block()

        #check for elif
        if(self.next_token.value == "elif"):
            self.elif_state()
            return 

        #check for else
        if(self.next_token.value == 'else'):
            self.self_state()
            return

        if(has_brackets == 1):
            if(self.next_token.value != "#}"):
                print("Error ...")
                exit()
            self.advance_token()
        return


    def print_state(self):
        has_brackets=0
        if self.next_token.value == '(':
            self.advance_token()
            self.has_brackets=1

        self.expresion()

        if has_brackets==1:    
            if self.next_token.value==')':
                self.advance_token()
                
            else:
                print("Expected ')'")

    ##########################################    
    def condition(self):
        while(self.next_token.value != ":"):
            self.advance_token()
        return

    def expression(self):
        while(self.current_token.value != ":"):
            self.advance_token()
        return
    ##########################################

    #to be tested
    def input_state(self):
        if(self.current_token.value != "="):
            print("Error at line", self.current_token.line, ". Missing a '='")
            exit()
        self.advance_token() #self.current_token is '=' and it has been checked at the code_block

        self.advance_token() 
        if(self.current_token.value != '('):
            print("Error at line", self.current_token.line, ". Missing a '('")
            exit()

        self.advance_token()
        if(self.current_token.value != 'input'):
            print("Error at line", self.current_token.line, ". Missing a '('")
            exit()

        self.advance_token()
        if(self.current_token.value != '('):
            print("Error at line", self.current_token.line, ". Missing a '('")
            exit()

        self.advance_token()
        if(self.current_token.value != ')'):
            print("Error at line", self.current_token.line, ". Missing a ')'")
            exit()

        self.advance_token()
        if(self.current_token.value != ')'):
            print("Error at line", self.current_token.line, ". Missing a ')'")
            exit()

    #to be tested 
    def return_state(self):
        self.expresion()
        return

    #to be tested
    def elif_state(self):
        self.exprextion()
        self.advance_token()
        if(self.current_token.value != ":"):
            print("Error ...")
            exit
        self.code_block_state()
        
        if(self.next_token.value == "elif"):
            self.elif_state()
        return

    #to be tested
    def else_state(self):
        self.advannce_token()
        if(self.current_token.value != ":"):
            print("Error ...")
            exit()

        self.code_block_state()
        return

#main function
def main():
    inputFilePath = sys.argv[-1]
    sourceCode = open(inputFilePath).read()
    lex = Lexer(sourceCode)
    
    
    #for token in lex.tokens:
    #    print("Type:", token.type)
    #    print("Value:", token.value)
    #    print("")
    

    par = Parser(sourceCode)

    while(par.current_token.type != "EOF"):    
        par.advance_token()

if __name__ == "__main__":
    main()
