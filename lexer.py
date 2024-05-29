#Aliko Muska 4427
#Ramo Zanaj 2697
import sys


################################
###       ALPHABET           ###
################################


KEYWORDS = {
    'main', 'def', '#def', '#int', 'global', 'if', 'elif', 'else',
    'while', 'print', 'return', 'input', 'int', 'and', 'or', 'not'}

LETTERS=('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
DIGITS=('0123456789')
OPERATORS = ('+', '-', '*', '%','/','//','!=', '<', '>', '==', '<=', '>=', '!','=')
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
        reps=0
        result=''
        while (self.current_char!=None and self.current_char in OPERATORS) and reps<2 : 
            result+=self.current_char           
            self.advance()

            if result not in OPERATORS:
                print("SYNTAX ERROR ")
                exit()
        return  Token('OPERATOR',result,self.line)
         
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

        has_bracket = 0
        if(self.next_token.value == "#{"):
            self.advance_token()
            has_bracket = 1

        if(self.next_token.value == "#}"):
            print("Error at line", self.current_token.line, ", no statement inside while")
            exit()

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

        has_brackets = 0
        if(self.next_token.value == "#{"):
            self.advance_token()
            has_brackets = 1

        if(self.next_token.value == "#}"):
            print("Error at line", self.current_token.line, ", no statement inside if")
            exit()

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

    #TO BE DONE
    def condition(self):
        if(self.next_token.value == "elif"):
            self.advance_token()
            
        self.bool_term()
        if(self.current_token.value == "or"):
            self.bool_factor()

        if(self.current_token.value != ":"):
            print("Error missing a ':' at line", self.current_token.line)
        return


    def bool_term(self):
        self.bool_factor()
        if(self.current_token.value == "and"):
            self.bool_factor()
    
        return

    def bool_factor(self):
        rel_op = [">", "<", ">=", "<=", "==", "!="]

        if(self.next_token.value == "not"):
            self.advance_token()

        self.expression()
        self.advance_token()
        if(self.current_token.value not in rel_op):
            print("Error at line", self.current_token.line, "rel operator missing")
            exit()
        
        self.expression()
        self.advance_token()

        return


    def expression(self):
        if(self.next_token.value == "+" or self.next_token.value == "-"):
            self.advance_token()
        self.un_expression()
        return


    # has to be changed to recognize also function calls
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

        if(self.next_token.value in ["+", "-", "*", "//", "%"]):
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

        if(self.next_token.value == ")"):
            self.advance_token()
            return

        self.expression()


        while(self.next_token.value == ","):
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
    
    def __init__(self, sourceCode, tokens, index, symbol_table):
        self.symbol_tables = []
        self.symbol_table = symbol_table
        self.symbol_tables.append(symbol_table)
        self.tokens = tokens
        self.int_var = []
        self.quads = []
        self.token_index = 0
        self.label = 0
        self.temp_var = 0
        self.current_token = Token("NULL", "NULL", 0)
        self.next_token = Token("NULL" , "NULL", 0)
        self.token_init()
        self.init_code_maker("NULL")
        self.print_Quads_file(self.quads)
        print("QUADS")
        self.print_quads()
        self.print_symbol_table()

   
    def return_int_var(self):
        return self.int_var

    def return_quads(self):
       return self.quads

    def print_symbol_table(self):
        file_name="symbol_table.sym"
        with open(file_name,"w") as file: 
            file.write("SYMBOL TABLE\n")
            for sym in self.symbol_table:
                file.write("Symbol:" +  sym.name + " Type:" + sym.symbol_type + "\n")

        print("SYMBOL TABLE WRITTEN TO", file_name)
        return


    def print_Quads_file(self, quads):
        file_name="quads.int"
        with open(file_name,"w") as file: 
            file.write("THE QUADS OF THE PROGRAMM\n")
            for quad in quads:
                     file.write( str(quad.label) + ": " + ", ".join([quad.operator , str(quad.operand1), str(quad.operand2), str(quad.operand3)]) + "\n")
        print("TABLE WITH PROGRAMM QUADS  IS WRITTEN TO ", file_name)
        return
    
    
    def init_code_maker(self, end_char):

        self.variables_loader()

        while(self.current_token.value == "global"):
            self.advance_token()
            self.advance_token()


        if(self.current_token.value == "def"):
            self.functions_loader()

        #fuc declaration missing
        self.code_block(end_char, 1)
        self.genQuad("halt", "", "", "")


        return


    def assiment(self, assiment_var, expression):

        #calculate functions
        expression = self.calc_functions(expression)

        #remove parenthesis
        if("(" in expression):
            expression = self.parenthesis(expression)        

        #do the mult
        expression = self.mult_oper(expression)
        
        #do the additions
        self.add_oper(assiment_var, expression)
    
        return


    def calc_functions(self, expression):
        new_expression = []
        op = ["+", "-", "*", "//", "%"]
        index = 0

            
        while index < len(expression):
            if(expression[index] in op or expression[index] == "(" or expression[index] == ")"):
                new_expression.append(expression[index])
                index+=1
    
            elif(index+1 < len(expression) and  expression[index+1] == "("):
                if(self.inSymbolTable(expression[index]) == False):
                    print("Error", expression[index], "not declarted")
                    exit()

                function_name = expression[index]
                temp = self.return_temp_var()
                new_expression.append(temp)
                parameters = []
                index+=2

                if(expression[index] == ")"):
                    index+=1
                    continue

                parenthesis_count = 1
                while(expression[index] != ")" or parenthesis_count !=0):
                    parameters.append(expression[index])
                    index+=1
                    if(expression[index] == ")"):
                        parenthesis_count -=1
                    elif(expression[index] == "("):
                        parenthesis_count +=1
                index+=1
                self.genQuad("begin_block", function_name, "", "")
                self.function_call(function_name, parameters)
                self.genQuad("halt", "", "", "")
                self.genQuad("end_block", function_name, "", "")

            else:
                new_expression.append(expression[index])
                index+=1

        return new_expression


    def function_call(self, function_name, parameters):
        new_parameters = [] 
        int_var_buff = self.int_var
        index_buf = self.token_index
        tokens_buf = self.tokens
        current_token_buf = self.current_token
        next_token_buf = self.next_token
        self.token_index = 1

        for sym in self.symbol_table:
            if(sym.name == function_name):
                self.tokens = sym.func_code
                self.current_token = self.tokens[1]
                self.next_token = self.tokens[2]


    
        self.init_code_maker("#}")

        self.int_var = int_var_buff
        self.token_index = index_buf
        self.tokens = tokens_buf
        self.current_token = current_token_buf
        self.next_token = next_token_buf
        return


    def inSymbolTable(self, token):
        for symbToken in self.symbol_table:
            if(token == symbToken.name and symbToken.symbol_type == "function"):
                return True
        return False


    def parenthesis(self, expression):
        new_expression = []
        parenthesis_counter = 0
        parenthesis = []
        index = 0
        in_parenthesis = False
    
        #find parenthesis and calculate them
        for token in expression:
            
            if(token == "(" and in_parenthesis == False):
                in_parenthesis = True
                parenthesis_counter+=1
                continue 

            if(token == ")"):
                parenthesis_counter-=1
                if(parenthesis_counter == 0):
                    #add the temp var from assiment call to the new expression
                    #new_expression.append(assiment(parenthesis))
                    in_parenthesis = False
                    temp = self.return_temp_var()
                    new_expression.append(temp)
                    self.assiment(temp, parenthesis)
                    parenthesis = []
                if(parenthesis_counter != 0):
                    in_parenthesis = True
                    parenthesis.append(token)
                continue 


            if(in_parenthesis):
                parenthesis.append(token)
                if(token == "("):
                    parenthesis_counter+=1
                continue

            if(in_parenthesis == False):
                new_expression.append(token)
                continue
        return new_expression



    def mult_oper(self, expression):
        index = 0
        new_expression = []
        if(len(expression) < 3):
            return expression

        while(index < len(expression)):
            if(expression[index] == "*" or expression[index] == "//"):
                temp = self.return_temp_var() 
                self.genQuad(expression[index], expression[index-1], expression[index+1], temp)
                new_expression.pop()
                new_expression.append(temp)
                index+=2
                continue
            else:
                new_expression.append(expression[index])
                index+=1
        return new_expression


    def add_oper(self, assiment_var, expression):

        if(len(expression) < 3):
            self.genQuad(":=", expression[0], "",  assiment_var)
            return

        self.genQuad(expression[1], expression[0], expression[2], assiment_var)
        index = 3

        while(index < len(expression)):
            self.genQuad(expression[index], assiment_var, expression[index+1] ,assiment_var)
            index+=2

        return


    def if_block(self):
        exit_jump_quads = []
        self.advance_token()
        backpatch_quad = self.condition()
        self.advance_token() 
        if(self.current_token.value == "#{"):
            self.advance_token() 
            self.code_block("#}", 1)
            self.advance_token() 
        else:
            self.code_block("", 0)

        exit_jump_quads.append(self.genQuad("jump", "", "", ""))

        for quad in backpatch_quad:
            self.backpatch(quad, self.nextQuad())


        while(self.current_token.value == "elif"):
            self.advance_token() 
            backpatch_quad = self.condition()
            self.advance_token() 
            if(self.current_token.value == "#{"):
                self.advance_token()
                self.code_block("#}", 1)
                self.advance_token()
            else:
                self.code_block("", 0)
            exit_jump_quads.append(self.genQuad("jump", "", "", ""))

            for quad in backpatch_quad:
                self.backpatch(quad, self.nextQuad())


        if(self.current_token.value == "else"):
            self.advance_token()
            self.advance_token()
            if(self.current_token.value == "#{"):
                self.advance_token()
                self.code_block("#}", 1)
                self.advance_token()
            else:
                self.code_block("", 0)


        for quad in exit_jump_quads:
            self.backpatch(quad, self.nextQuad())

        return


    def while_block(self):
        self.advance_token() 
        return_label = self.nextQuad()
        backpatch_quad = self.condition()
        self.advance_token() 
        if(self.current_token.value == "#{"):
            self.advance_token() 
            self.code_block("#}", 1)
            self.advance_token()
        else:
            self.code_block("", 0)
    
        self.genQuad("jump", "", "", return_label)
        for quad in backpatch_quad:
            self.backpatch(quad, self.nextQuad())
        return


    def code_block(self, end_token, multiple_lines):

        while(self.current_token.value != end_token):
            
            ## assiment
            if(self.next_token.value == "="):
                assiment_var = self.current_token.value
                self.advance_token()
                self.advance_token()

                #input
                if(self.current_token.value == "int"):
                    #to be checked
                    while(self.current_token.line == self.next_token.line):
                        self.advance_token()

                    self.advance_token()
                    self.genQuad("in", "", "", "")

                #a = 1 (constant)
                elif(self.current_token.line != self.next_token.line):
                    self.genQuad(":=", self.current_token.value, "", assiment_var)
                    self.advance_token()

                ## assiment
                else:
                    line = self.current_token.line
                    expression = []          
                    while(self.current_token.line == line):
                        expression.append(self.current_token.value)    
                        self.advance_token()
                    self.assiment(assiment_var, expression)
            
                if(multiple_lines == 0):
                    return

            ## print
            if(self.current_token.value == "print"):
                while(self.current_token.line == self.next_token.line):
                    self.advance_token()
                self.advance_token()
                self.genQuad("out", "", "", "")
                if(multiple_lines == 0):
                    return


            ## return
            if(self.current_token.value == "return"):
                while(self.current_token.line == self.next_token.line):
                    self.advance_token()
                self.genQuad("ret", "", "", "")
                self.advance_token()
                if(multiple_lines == 0):
                    return


            ##while
            if(self.current_token.value == "while"):
                self.while_block()
                if(multiple_lines == 0):
                    return

            ##if
            if(self.current_token.value == "if"):
                self.if_block()
                if(multiple_lines == 0):
                    return   

        return


    def condition(self):
        new_condition = []
        term = []
        op = ["<", ">", ">=", "<=", "==", "!="]
        rel_op = ""
        parenthesis_counter = 0

        while(self.current_token.value != ":"):
            if(self.current_token.value == "or" or self.current_token.value == "and"):
                if(len(term) == 1):
                    new_condition.append(term[0])
                    term = []
                    new_condition.append(self.current_token.value)
                    self.advance_token()
                    continue

                temp = self.return_temp_var()
                self.assiment(temp, term)
                new_condition.append(temp)
                new_condition.append(self.current_token.value)
                self.advance_token()
                term = []
                continue

            if(self.current_token.value in op):
                if(len(term) == 1):
                    new_condition.append(term[0])
                    new_condition.append(self.current_token.value)
                    self.advance_token()
                    term = []
                    continue
                temp = self.return_temp_var()
                self.assiment(temp, term)
                new_condition.append(temp)
                new_condition.append(self.current_token.value)
                self.advance_token()
                term = []
                continue
            term.append(self.current_token.value)
            self.advance_token()


        if(len(term) == 1):
            new_condition.append(term[0])
            return self.bool_quad(new_condition)

        temp = self.return_temp_var()
        self.assiment(temp, term)
        new_condition.append(temp)
        return self.bool_quad(new_condition)


    def bool_quad(self, condition):
        index = 0
        true_quad = []
        false_quad = []

        true_quad.append(self.genQuad(condition[1], condition[0], condition[2], ""))
        false_quad.append(self.genQuad("jump", "", "", ""))
        index +=3
            

        #multiple boolean variables (to be done)
        while(index < len(condition)):
            if(condition[index] == "and"):
                #true
                for quad in true_quad:
                    self.backpatch(quad, self.nextQuad())
                true_quad = []
                true_quad.append(self.genQuad(condition[index + 2], condition[index + 1], condition[index + 3], ""))
                false_quad.append(self.genQuad("jump", "", "", ""))
                #false

            elif(condition[index] == "or"):
                for quad in false_quad:
                    self.backpatch(quad, self.nextQuad())
                false_quad = []
                true_quad.append(self.genQuad(condition[index + 2], condition[index + 1], condition[index + 3], ""))
                false_quad.append(self.genQuad("jump", "", "", ""))

            index +=4
            
        for quad in true_quad:
            self.backpatch(quad, self.nextQuad())
    
        return false_quad



    def genQuad(self, operator, oper1, oper2, oper3):
        quad = Quad(self.label, operator, oper1, oper2, oper3)
        self.quads.append(quad)
        self.label+=1
        return quad


    def nextQuad(self):
        return self.label


    def newTemp():
        return

    
    def emptyList():
        return 

    def makeList():
        return


    def mergeList():
        return


    def backpatch(self, quad, label):
        quad.operand3 = label
        return

    def return_temp_var(self):
        self.temp_var+=1
        return ("T_" + str(self.temp_var - 1))
        
        
    def print_quads(self):
        assiment = ['+', '-', '*', '//', '%']
        rel_op = [">", "<", ">=", "<=", "==", "!="]

        for quad in self.quads:
            if(quad.operator in assiment): 
                print(str(quad.label), quad.operand3 + " = " + str(quad.operand1) + " " + quad.operator + " " + str(quad.operand2))
            elif(quad.operator in rel_op):
                print(str(quad.label), str(quad.operand1), str(quad.operator), str(quad.operand2), str(quad.operand3))
            elif(quad.operator == ":="):
                print(str(quad.label), str(quad.operand3) + " := " + str(quad.operand1))
            elif(quad.operator == "out"):
                print(str(quad.label), "print")
            elif(quad.operator == "in"):
                print(str(quad.label), "input")
            elif(quad.operator == "ret"):
                print(str(quad.label), "return")
            elif(quad.operator == "jump"):
                print(str(quad.label), "jump", str(quad.operand3))
            elif(quad.operator == "halt"):
                print(str(quad.label), "halt")
            elif(quad.operator == "begin_block" or quad.operator == "end_block"):
                print(str(quad.label), quad.operator, quad.operand1)

        return

    def variables_loader(self):
        variables = []

        while(self.current_token.value == "#int"):
            self.advance_token()
            variables.append(self.current_token.value)
            self.symbol_table.append(Symbol(self.current_token.value, "variable", None, None, None))
            self.advance_token()

        self.int_var = variables
        return


    def functions_loader(self):
        function_tokens = []
        function_par = []
        bracket_count = 1

        self.advance_token()
        function_name = self.current_token.value
        self.advance_token()
        self.advance_token()

        while(self.current_token.value != ")"):
            function_par.append(self.current_token.value)
            self.advance_token()
            if(self.current_token.value == ","):
                self.advance_token()
    
        self.advance_token()
        self.advance_token()

        while (self.current_token.value != "#}" or bracket_count != 0):
            function_tokens.append(self.current_token)
            self.advance_token()

            if(self.current_token.value == "#{"):
                bracket_count+=1

            if(self.current_token.value == "#}"):
                bracket_count-=1
            

        function_tokens.append(self.current_token)
        self.symbol_table.append(Symbol(function_name, "function", function_tokens, function_par))

        self.advance_token()

        if(self.current_token.value == "def"):
            self.functions_loader()

        if(self.current_token.value == "#def"):
            return
        
        return


    def token_init(self):
        if(len(self.tokens) == 0):
            return

        if(len(self.tokens) > 0):
            self.current_token = self.tokens[self.token_index]

        if(len(self.tokens) > 1):
            self.next_token = self.tokens[self.token_index+1]
       
        while(self.current_token.value != "main"):
            self.advance_token()
        self.advance_token()
        return


    def advance_token(self):
        self.token_index += 1
        
        if(self.token_index + 1 < len(self.tokens)):
            self.current_token = self.next_token
            self.next_token = self.tokens[self.token_index+1]
            return
        elif(self.token_index + 1 == len(self.tokens)):
            self.current_token = self.tokens[self.token_index]
            self.next_token = Token("NULL", "NULL", 0)
            return

        self.current_token = Token("NULL", "NULL", 0)
        self.next_token = Token("NULL", "NULL", 0)

        return 


class Symbol:

    def __init__(self, name, symbol_type, func_code, func_par, par_number):
        self.name = name
        self.symbol_type = symbol_type
        self.func_code = func_code
        self.func_par = func_par
        self.par_number = par_number


class Quad:
    def __init__(self, label, operator, operand1, operand2, operand3):
        self.label = label
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.operand3 = operand3


class SymbolTable:

    def __init__(self, block_name):
        return


class FinalCode:

    def __init__(self, quads, symbolTable,int_var, global_variables):
        self.registers = Registers()
        self.quads = quads
        self.symbolTable = symbolTable
        self.int_var = int_var
        self.global_variables = global_variables
        self.offset_table = []
        self.final_code=[]
        self.temp_var_table = []
        self.offset = 0
        self.final_code_gen()

    
    def final_code_gen(self):


        for var in self.int_var:
            self.offset_table.append([var, self.offset])
            self.offset -=4
            

        for quad in self.quads:


            if(quad.operator == ":="):
                self.assiment(quad)

            if(quad.operator == "jump"):
                reg = self.registers.return_available_reg()
                self.final_code.append("li " + str(reg) + ", " + str(quad.operand3*4))
                self.final_code.append("jr "  + str(reg))
                self.registers.make_available_reg(reg)
            if(quad.operator in ["+","-","*","//","%"]):
                self.assembly_transform_operation(quad)
            if(quad.operator in ["!=", "<", ">","==", "<=", ">="]):
               self.assembly_transform_condition(quad)
            if(quad.operator=="in"):
                self.assembly_transform_input(quad)
            if(quad.operator=="out"):
                self.assembly_tranform_output(quad)
            if(quad.operator=="halt"):
                self.assembly_transform_endOfProgramm(quad)
        self.print_final_code()
        return
    

    
    def assiment(self, quad):
        reg = self.registers.return_available_reg()
        if(type(quad.operand1) == int):
            self.final_code.append("li " + str(reg) + ", " + str(quad.operand1))
            self.final_code.append("sw " + str(reg) + ", " + str(self.return_var_offset(quad.operand3))  +"(fp)")
            self.registers.make_available_reg(reg)
        elif(quad.operand1[0:2] == "T_"):
            self.final_code.append("sw " + str(self.return_temp_register(quad.operand1)) +", "  + str(self.return_var_offset(quad.operand3))  +"(fp)")
        else:
            self.final_code.append("lw " + str(reg) + ", " + str(self.return_address(quad.operand1)))
            self.final_code.append("sw " + str(reg) + ", " + str(self.return_address(quad.operand3)))

        self.registers.make_available_reg(quad.operand1)


    def return_address(self, operand):
        offset = self.return_local_offset(operand)
        if(offset >= 0):
            return str(offset) + "(fp)"
        elif(type(self.isglobal_var(operand)) == str):

            print(self.isglobal_var(operand))
            return self.isglobal_var(operand)
        print(operand)
        print("error")
        exit()
        return


    def return_temp_register(self, temp_var):
        for temp in self.temp_var_table:
            if(temp[0] == temp_var):
                return temp[1]


    def return_local_offset(self, operand):
        for index in range(len(self.int_var)):
            if(str(operand) == str(self.int_var[index])):
                return index*4
        return -1


    def return_var_offset(self, var_name):
        for var in self.offset_table:
            if(var[0] == var_name):
                return var[1]
        return -1


    def isglobal_var(self, operand):
        for var in self.global_variables:
            if operand == var[0]:
                return var[1]
        return 0

    def assembly_transform_input(self,quad):
        register1=self.registers.return_available_reg()
        self.final_code.append("li "+ str(register1)+", "+"5")
        self.final_code.append("ecall")
        self.registers.make_available_reg(register1)
        return 

    def assembly_tranform_output(self,quad):
        
            self.final_code.append("li a0,44")
            self.final_code.append("li a7,1")
            self.final_code.append("ecall")
            return 
    
    def assembly_transform_endOfProgramm(self,quad):


            self.final_code.append("li a0,0")
            self.final_code.append("li a7,93")
            self.final_code.append("ecall")
    
            return 
    
    def operand_to_reg(self, operand):
        register = self.registers.return_available_reg()

        if(type(operand) == int):
            print("int", operand)
            self.final_code.append("li " + str(register) + ", " + str(operand))
        
        elif(self.return_local_offset(operand)>=0):
            print("local", operand)
            self.final_code.append("lw " + str(register) + ", " + str(self.return_local_offset(operand))  +"(fp)")

        elif(operand[0:2] == "T_"):
            print("temp", operand)
            register = self.return_temp_register(operand)

        elif(self.isglobal_var(operand)):
            print("global", operand)
            self.final_code.append("lw " + str(register) + ", " + str(self.isglobal_var(operand)))

        else:
            print("Error variable " + str(operand) + " not declared")
            exit()

        return register

    
    def assembly_transform_condition(self,quad):
        register1=self.registers.return_available_reg()
        register2=self.registers.return_available_reg()

        if register1!=0 and register2!=0:
            if quad.operator=="!=":
                assembly_code="bne "
            if quad.operator=="==":
                assembly_code="beq "
            if quad.operator=="<":
                assembly_code="blt "
            if quad.operator==">":
                assembly_code="bgt "
            if quad.operator=="<=":
                assembly_code="blt "
            if quad.operator== ">=" and isinstance(quad.operand3,int):
                assembly_code="bge "
	
        assembly_code += str(register1) + ", " + str(register2) + ", " + str(4*quad.operand3)
        self.final_code.append(assembly_code)
	
        self.registers.make_available_reg(register1)
        self.registers.make_available_reg(register2)
        return 
      





    def assembly_transform_operation(self,quad):
        register1 = self.operand_to_reg(quad.operand1)
        register2 = self.operand_to_reg(quad.operand2)
        register3 = self.registers.return_available_reg()

        if register1!=0 and register2!=0:
            if quad.operator=="+":
                assembly_code="add "
            if quad.operator=="-":
                assembly_code="sub "
            if quad.operator=="*":
                assembly_code="mul "
            if quad.operator=="//":
                assembly_code="div "
            if quad.operator=="%":
                assembly_code="mod "
            if quad.operator== "=" and isinstance(quad.operand3,int):
                assembly_code="addi "
                
            assembly_code+= register3 + ", " + register2 + ", " + register1
            self.final_code.append(assembly_code)


            if(quad.operand3[0:2] == "T_"):
                self.temp_var_table.append([quad.operand3, register3])
            else:
                self.final_code.append("sw " + str(register3) + ", " + self.return_address(quad.operand3))
                self.registers.make_available_reg(register3)


        self.registers.make_available_reg(register1)
        self.registers.make_available_reg(register2)
        return 



    def print_final_code(self):
        print()
        print("Final code")
        for code in self.final_code:
            print(code)




class Registers:
    
    def __init__(self):
        self.registers = []
        for i in range(0,8):
            self.registers.append(Register("t" + str(i)))
        
        
    def return_available_reg(self):
        for reg in self.registers:
            if reg.avaliable == True:
                reg.avaliable = False
                return reg.name
        
        return -1


    def register_storing(self, var):
        for reg in self.registers:
            if(reg.stores == var):
                return reg.name
        return -1 
    

    def make_available_reg(self, register_name):
        for reg in self.registers:
            if(reg.name == register_name):
                reg.avaliable = True
                return
        return



class Register:

    def __init__(self, name):
        self.name = name
        self.stores = ""
        self.avaliable = True



class Compiler:

    def __init__(self, sourceCode):
    	#Lexer
        self.lex = Lexer(sourceCode)
        print("==========")
        print("LEXER DONE")
        print("==========\n")
        
        #Parser
        self.par = Parser(self.lex)
        self.par.syntax_analyzer()
        print("===========")
        print("PARSER DONE")
        print("===========\n")

        #Fields
        self.symbol_table = []
        self.tokens = self.remove_comments(self.lex.tokens)
        self.token_index = 0
        self.current_token = self.tokens[0]
        self.next_token = self.tokens[1]
        self.make_symbols()

        #Int_Code_Genarator
        self.int_generator = Int_Code_Generator(sourceCode, self.tokens, self.token_index, self.symbol_table)
        self.quads = self.int_generator.return_quads()
        print("=======================")
        print("INTERMIDIATE CODE DONE")
        print("=======================")

        #Final Code Maker
        self.final_code_maker = FinalCode(self.quads, self.tokens, self.int_generator.return_int_var(), self.return_global_var_offset())
        print("===============")
        print("FINAL CODE DONE")
        print("===============\n")

        print("*****COMPILATION DONE*****\n")

    def remove_comments(self, tokens):
        new_tokens = []
        in_comment = 0

        for token in tokens:
            if(token.value == "##"):
                if(in_comment == 0):
                    in_comment = 1
                else:
                    in_comment = 0
                continue

            if(in_comment):
                continue

            new_tokens.append(token)

        return new_tokens


    def return_global_var_offset(self):
        offset = 0
        global_var_offset = []

        for symbol in self.symbol_table:
            if(symbol.symbol_type == "function"):
                return global_var_offset

            global_var_offset.append([symbol.name, str(offset)+"(gp)"])
            offset -=4
        return global_var_offset


    def advance(self):
        self.token_index += 1
        if(self.token_index + 1  <  len(self.tokens)):
            self.current_token = self.next_token
            self.next_token = self.tokens[self.token_index+1]
            return
        
        if(self.token_index + 1 ==  len(self.tokens)):
            self.current_token = self.next_token
            self.next_token = Token("NULL", "NULL", 0)
            return

        self.current_token = Token("NULL", "NULL", 0)
        self.next_token = Token("NULL", "NULL", 0)

        return 
 
        


    def make_symbols(self):
        
        if(self.current_token.value == "def" and self.next_token.value == "main"):
            return

        if(self.current_token.value == "#int"):
            self.variables_loader()

        if(self.current_token.value == "def"):
            self.functions_loader()

        # main function
        return


    def variables_loader(self):
        self.advance()
        self.symbol_table.append(Symbol(self.current_token.value, "variable", None, None, None))

        while(self.next_token.value == "#int"):
            self.advance()
            self.symbol_table.append(Symbol(self.next_token.value, "variable", None, None, None))
            self.advance()

        self.advance()
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
        self.symbol_table.append(Symbol(function_name, "function", function_tokens, function_par, len(function_par)))

        self.advance()

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
