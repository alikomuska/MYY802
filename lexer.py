import sys


################################
###       ALPHABET           ###
################################


KEYWORDS = {
    'main', 'def', '#def', '#int', 'global', 'if', 'elif', 'else',
    'while', 'print', 'return', 'input', 'int', 'and', 'or', 'not'}

LETTERS=('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
DIGITS=('0123456789')
OPERATORS = ('+', '-', '*', '//', '%', '<', '>', '==', '<=', '>=', '=')
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
                print("Unexpected character in token")
                exit()
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
            return []
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

    def __init__(self, lex):
        self.lex = lex
        self.current_token = Token("NULL", "", 0)
        self.next_token = Token("NULL" , "", 0)
        self.token_init()


    def token_init(self):
        #initialyze current token
        self.current_token = self.lex.get_next_token()
        if(self.current_token.value == "##"):
            self.current_token = self.lex.get_next_token()
            while(self.current_token.value != "##"):
                self.current_token = self.lex.get_next_token() 
            self.current_token = self.lex.get_next_token()
        
        #initialyze current token
        self.next_token = self.lex.get_next_token()
        if(self.next_token.value == "##"):
            self.next_token = self.lex.get_next_token()
            while(self.next_token.value != "##"):
                self.next_token = self.lex.get_next_token() 
            self.next_token = self.lex.get_next_token()
        return


    def advance_token(self):
        self.current_token= self.next_token
        self.next_token = self.lex.get_next_token()
        if(self.next_token.value == "##"):
            self.next_token = self.lex.get_next_token()
            while(self.next_token.value != "##"):
                self.next_token = self.lex.get_next_token() 
            self.next_token = self.lex.get_next_token()
        return 
        

    def global_state(self):
        # Check for the 'global' keyword
        self.id_list()
        if(self.next_token.value == "global"):
            self.global_state()
        return 

    #startRule
    def syntax_analyzer(self):
        self.declarations_state()
        if(self.current_token.value != "#def"):
            print("Error at line", self.current_token.line, ". Main function missing")
            exit()
        self.main_function_state()
        return

    #to be tested
    def declarations_state(self):
        if(self.current_token.value == "#int"):
            self.assignments_state()
            self.advance_token()
        if(self.current_token.value == "def"):
            self.functions_declaration_state()
            self.advance_token()
        return

    #to be tested
    def assignments_state(self):
        if(self.current_token.value != "#int"):
            print("Error at line ", self.current_token.line, "Missing keyword")
            exit()


        if(self.next_token.type != "ID"):
            print("Error at line ", self.current_token.line ,". Expected variable name.")
            exit()

        self.id_list()

        if(self.next_token.value == "="):
            self.advance_token()
            self.expression()
    
        if(self.next_token.value == "#int"):
            self.advance_token()
            self.assignments_state()
    
        return

    #to be tested
    def functions_declaration_state(self):

        if(self.current_token.value != "def"):
            print("Error at line ", self.current_token.line, "Missing keyword 'def'")
            exit()

        self.advance_token()
        if(self.current_token.type != "ID"):
            print("Error ", self.current_token.value, "Line", self.current_token.line)
            exit()

        self.advance_token()
        if(self.current_token.value != '('):
            print("Error ", self.current_token.value, "Line", self.current_token.line)
            exit()

        self.id_list()
        self.advance_token()

        if(self.current_token.value != ')'):
            print("Error ", self.current_token.value, "Line", self.current_token.line)
            exit()

        self.advance_token()
        if(self.current_token.value != ":"):
            print("Error ", self.current_token.value, "Line", self.current_token.line)
            exit()

        self.advance_token()
        if(self.current_token.value != "#{"):
            print("Error ", self.current_token.value, "Line", self.current_token.line)
            exit()
            
        #delcarations (assignments)
        if(self.next_token.value == "#int"):
            self.advance_token()
            self.assignments_state()

        #functions
        if(self.next_token.value == "def"):
            self.advance_token()
            self.functions_declaration_state()
        
        #globals 
        if(self.next_token.value == "global"):
            self.advance_token()
            self.global_state()


        #code_block
        self.code_block_state(0, 1) #is_main = 0 multipleLines =  multipleLines = 1

        self.advance_token()
        if(self.current_token.value != "#}"):
            print("Error ", self.current_token.value, "Line", self.current_token.line)
            print("function declaration_Error")
            exit()
           
        if(self.next_token.value == "def"):
            self.advance_token()
            self.functions_declaration_state()

        return 
    
    #to be done
    def main_function_state(self):
        if(self.next_token.value != "main"):
            print("Error no main function")
            print("Error ", self.current_token.value, "Line", self.current_token.line)
            exit()

        self.advance_token()


    	#delcarations (assignments)
        if(self.next_token.value == "#int"):
            self.advance_token()
            self.assignments_state()

        #functions
        if(self.next_token.value == "def"):
            self.advance_token()
            self.functions_declaration_state()
        
        #globals 
        if(self.next_token.value == "global"):
            self.advance_token()
            self.global_state()


        #code_block
        self.code_block_state(0, 1) #is_main = 0 multipleLines =  multipleLines = 1
        print("################")
        print("COMPILATION DONE")
        print("################")
        return 
    
    #to be done
    def id_list(self):
        # Check if the current token is an ID
        if(self.next_token.type != "ID"):
            return

        self.advance_token()

        while(self.next_token.value == ","):
            self.advance_token()
            self.id_list()
            return

        return
    
     


    def code_block_state(self, is_main, multipleLines):

        if(self.next_token.value == "if"):
            self.advance_token()
            self.if_state()
        elif(self.next_token.value == "while"):
            self.advance_token()
            self.while_state()
        elif(self.next_token.value == "return"):
            self.advance_token()
            self.return_state()
        elif(self.next_token.value == "print"):
            self.advance_token()
            self.print_state()
        elif(self.next_token.type == "ID"):
            self.advance_token()
            if(self.next_token.value != "="):
                print("Error ", self.current_token.value, "Line", self.current_token.line)
                print("Error expected '='")
                exit() 
            self.advance_token()
            if(self.next_token.value == "int"): 
                self.input_state()
            else:
                self.expression()
        else:
            return 


        if(multipleLines == 0):
            return
        
        self.code_block_state(0, 1)
        return


########################################
### while, if, print, return , input ###
########################################


    #to be tested
    def while_state(self):
        self.condition()

        self.advance_token()
        if(self.current_token.value != ":"):
            print("Error ", self.current_token.value, "Line", self.current_token.line)
            exit()

        has_bracket = 0
        if(self.next_token.value == "#{"):
            self.advance_token()
            has_bracket = 1

        self.code_block_state(0, has_bracket)

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
            print("Error ", self.current_token.value, "Line", self.current_token.line)
            exit()

        has_brackets = 0
        if(self.next_token.value == "#{"):
            self.advance_token()
            has_brackets = 1

        #check for: if, while, ekxorisi, return,  print, input
        self.code_block_state(0, has_brackets)

        #check for elif
        if(self.next_token.value == "elif"):
            self.elif_state()

        #check for else
        if(self.next_token.value == 'else'):
            self.else_state()
            return

        if(has_brackets == 1):
            if(self.next_token.value != "#}"):
                print("Error ", self.current_token.value, "Line", self.current_token.line)
                exit()
            self.advance_token()
        return


    def print_state(self):
        if self.next_token.value != "(":
            print("Error ", self.current_token.value, "Line", self.current_token.line)
            print("Error missing a '('")
            exit()

        self.advance_token()

        self.expression()

        if (self.next_token.value != ")"):
             print("Error ", self.current_token.value, "Line", self.current_token.line)
             print("Missing a ')' ")
             exit()

        self.advance_token()

        return

    #DONE
    def condition(self):
        while(self.next_token.value != ":"):
            self.advance_token()
        return

    def expression(self):
        if(self.next_token.value == "+" or self.next_token.value == "-"):
            self.advance_token()
        self.un_expression()
        return


    def un_expression(self):
        has_parenthesis = 0

        if(self.next_token.value == "("):
            has_parenthesis = 1
            self.advance_token()
            self.expression()
        else:
            self.term()        

        if(self.next_token.value == ")" and has_parenthesis == 1):
            has_parenthesis = 0
            self.advance_token()

        if(self.next_token.type == "OPERATOR"):
            self.advance_token()
            self.expression()
        else:
            if(has_parenthesis == 1):
                print("Error ", self.current_token.value, "Line", self.current_token.line)
                print("Error missing a ')'")
                exit()
            return

        if(self.next_token.value != ")" and has_parenthesis == 1):
            print("Error ", self.current_token.value, "Line", self.current_token.line)
            print("Error missing a ')'")
            exit()
            
        return

    def term(self):
        #check if term is int, ID, function call

        if(self.next_token.type == "ID"):
            self.advance_token()
            if(self.next_token.value == "("):
                self.function_call()
                return
        elif(self.next_token.type == "INT"):
            self.advance_token()
            return
        else:
            print("Error ", self.current_token.value, "Line", self.current_token.line)
            print("Error expected term")
            exit()

        return


    
    def function_call(self):
        if(self.next_token.value != "("):
            print("Error ", self.current_token.value, "Line", self.current_token.line)
            exit()
        self.advance_token()
        self.expression()

        if(self.next_token.value != ")"):
            print("Error at line", self.current_token.line, ". Missing a ')'.")
            exit()

        self.advance_token()

        return




    #DONE
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
        if(self.current_token.value != ")"):
            print("Error at line", self.current_token.line, ". Missing a ')'")
            exit()

        return

    #to be done
    def return_state(self):
        # make it so you can do return fib(3)
        self.expression()
        return

    #to be tested
    def elif_state(self):
        has_brackets = 0
        self.condition()
        if(self.next_token.value != ":"):
            print("Error ", self.current_token.value, "Line", self.current_token.line)
            exit()

        self.advance_token()

        if(self.next_token.value == "#{"):
            self.advance_token()
            has_brackets = 1
        
        
        self.code_block_state(0, has_brackets)
        
        if(has_brackets == 1 and self.next_token.value != "#}"):
            print("Error ", self.current_token.value, "Line", self.current_token.line)
            exit()

        if(self.next_token.value == "elif"):
            self.elif_state()

        return

    #to be tested
    def else_state(self):
        self.advance_token()
        if(self.next_token.value != ":"):
            print("Error ", self.current_token.value, "Line", self.current_token.line)
            exit()
    
        self.advance_token()

        if(self.next_token.value == "#{"):
            self.code_block_state(0, 1)
            if(self.next_token.value != "#}"):
                print("Error ", self.current_token.value, "Line", self.current_token.line)
                print("Error missing a #}")
                exit()
            self.advance_token()
            return

        self.code_block_state(0, 0)

        return




################################################
####       Intemediate Code Generation      ####
################################################


class Int_Code_Generator:
    
    def __init__(self, sourceCode, tokens, index):
        self.symbol_table = []
        self.tokens = tokens
        self.quads = []
        self.token_index = index
        self.current_label = 0
        self.temp_var = 0
        self.current_token = self.get_next_token()
        self.init_code_maker()


    def init_code_maker(self):
                
        while(self.current_token.value == "#int"):
            self.get_next_token()
            self.symbol_table.append(Symbol(self.current_token.value, "variable", None, None))
            #why does the previous line work?
            #maybe I'll put this line into the compliler
            self.get_next_token()
        

        while (self.current_token.type != "NULL"):

            print("current token", self.current_token.value)
            ## assiment
            if(self.current_token.type == "ID"):
                assiment_var = self.current_token
                self.get_next_token()
                line = self.current_token.line
                expression = []
                self.get_next_token()

                while(self.current_token.line == line):
                    expression.append(self.current_token)    
                    self.get_next_token()
                
                #self.assiment(assiment_var, expression)
                self.return_temp_var()
    
            ## print
            if(self.current_token.type == "ID"):
                #
                return

            ## return
            if(self.current_token.type == "ID"):
                #
                return

            ## if
            if(self.current_token.type == "ID"):
                #
                return

            ## while
            if(self.current_token.type == "ID"):
                #
                return

            self.get_next_token()

        return


    def assiment(self, assiment_var, expression):
        new_expression = []
        parenthesis = []        
        index = 0

        
        #find parenthesis and calculate them
        while(index < len(expression)):
            
            while(expression[index].value != "("):
                new_expression.append(expression[index])
                index+=1
                break    
            
            while(expression[index] != ")"):
                #add 
                parenthesis.append(expression[index])
                index+=1
            
            print(new_expression)
            self.parenthesis(assiment_var, parenthesis)
            temp_var = self.temp_var()
            #make quand 
            #self.make_quand(op, ...
            parenthesis = []
        
        
        #do the mult




        #do the additions



        return

    def parenthesis(self, assiment_var, expression):
        

        return


    def mul_oper(self):
        return


    def add_oper(self):
        return


    def get_next_token(self):
        self.token_index+=1
        if(self.token_index >= len(self.tokens)):
            self.current_token = Token("NULL", "", 0)
            return self.current_token 
        self.current_token = self.tokens[self.token_index]
        return self.current_token

    def genQuad(operator, oper1, oper2, oper3):
        return


    def return_temp_var(self):
        self.temp_var+=1
        return ("T" + str(self.temp_var - 1))


class Symbol:

    def __init__(self, name, symbol_type, func_code, func_par):
        self.name = name
        self.symbol_type = symbol_type
        self.func_code = func_code
        self.func_par = func_par





class Compiler:

    def __init__(self, sourceCode):
    	#Lexer
        self.lex = Lexer(sourceCode)
        
        #Parser
        self.par = Parser(self.lex)
        self.par.syntax_analyzer()

        #Fields
        self.symbol_table = []
        self.tokens = self.lex.tokens
        self.token_index = -1
        self.current_token = Token("NULL", "", 0)
        self.next_token = Token("NULL" , "", 0)
        self.token_init()
        self.make_symbols()
        
        #Int_Code_Genarator
        self.int_generator = Int_Code_Generator(sourceCode, self.lex.tokens, self.token_index)


    def token_init(self):
        #initialyze current token
        self.current_token = self.get_next_token()
        if(self.current_token.value == "##"):
            self.current_token = self.get_next_token()
            while(self.current_token.value != "##"):
                self.current_token = self.get_next_token() 
            self.current_token = self.get_next_token()
        
        #initialyze current token
        self.next_token = self.get_next_token()
        if(self.next_token.value == "##"):
            self.next_token = self.get_next_token()
            while(self.next_token.value != "##"):
                self.next_token = self.get_next_token() 
            self.next_token = self.get_next_token()
        return


    def advance(self):
        self.current_token= self.next_token
        self.next_token = self.get_next_token()
        if(self.next_token.value == "##"):
            self.next_token = self.get_next_token()
            while(self.next_token.value != "##"):
                self.next_token = self.get_next_token() 
            self.next_token = self.get_next_token()
        return 
        
        
    def get_next_token(self):
        self.token_index+=1
        if(self.token_index + 1 >= len(self.tokens)):
            return Token("Null", "", 0)
        return self.tokens[self.token_index] 



    def make_symbols(self):
        if(self.current_token.value == "def" and self.next_token.value == "main"):
            return

        if(self.current_token.value == "#int"):
            self.variables_loader()
            self.advance()

        if(self.current_token.value == "def"):
            self.functions_loader()

        # main function
        return


    def variables_loader(self):
        self.advance()
        self.symbol_table.append(Symbol(self.current_token.value, "variable", None, None))

        if(self.next_token.value == "#int"):
            self.advance()
            self.variables_loader()

        return


    def functions_loader(self):
        function_tokens = []
        function_par = []
        bracket_count = 1

        self.advance()
        function_name = self.current_token.value
        self.advance()
        self.advance()

        while(self.current_token.value != ")"):
            function_par.append(self.current_token.value)
            self.advance()
            if(self.current_token.value == ","):
                self.advance()
    
        self.advance()
        self.advance()

        while (self.current_token.value != "#}" or bracket_count != 0):
            function_tokens.append(self.current_token)
            self.advance()

            if(self.current_token.value == "#{"):
                bracket_count+=1

            if(self.current_token.value == "#}"):
                bracket_count-=1
            

        function_tokens.append(self.current_token)
        self.symbol_table.append(Symbol(function_name, "function", function_tokens, function_par))

        self.advance()
        if(self.current_token.value == "#def"):
            return
        
        if(self.current_token.value == "def"):
            self.functions_loader()

        return



#main function
def main():
    inputFilePath = sys.argv[-1]
    sourceCode = open(inputFilePath).read()
	
    compiler = Compiler(sourceCode)

if __name__ == "__main__":
    main()
