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
        
    def  advance(self):
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
            return [], Illegalchar("'"+self.current_char+"'")

        # Create a token for the integer value
        return Token('INT', int(num_str), self.line)


    def make_operators(self):
        result =''
        while self.current_char is not None and  self.current_char in OPERATORS :
            result += self.current_char
            if result == '-' and self.peek() in DIGITS:
                self.advance() 
                num_token = self.make_number()  # Treat it as a negative number
                num_token.value = -int(num_token.value)  # Negate the value
                return num_token # Consume the digit
                
        
            self.advance()
           
            if result == "/" or result == "!":
                result+=self.current_char
               
        

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
                return Token('GROUP_SYTMBOL',result,self.line)
            if result in GROUPING_SYMBOLS  :
                return Token('GROUP_SYMBOL', result, self.line)

            

            if result=='#' and self.current_char in LETTERS:
                 while self.current_char is not None and self.current_char in LETTERS:
                    result += self.current_char
                    self.advance()
            if result in KEYWORDS:
                return Token('keyword', result, self.line)
            else:
                print(" SYNTAX ERRO")
                exit()
                

        return Token('GROUP_SYMBOL', result, self.line)

    
    def get_next_token(self):
        self.token_index+=1
        if self.token_index>=len(self.tokens):
            return None
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
        self.current_token =self.lex.get_next_token()
        self.next_token = self.lex.get_next_token()
    
    def advance_tokens(self):
        self.current_token= self.next_token
        self.next_token = self.lexer.get_next_token()
    
    def return_token(self):
        self.lex.return_token()
        return

    #startRule
    def syntax_analyzer(self):
        self.declarations_state()
        #self.main_function_state() to be done
        return

    #to be tested
    def declarations_state(self):
        while(self.current_token != "#def"):
            if(self.current_token == "#int"):
                self.assignments_state()
<<<<<<< HEAD
            elif(declarations_token.value == "def"):
                #functions_declaration_state
                continue
            
=======
            elif(self.current_token == "def"):
                functions_declaration_state()
>>>>>>> e4a9655af6b93f5f8da52bbdec1965b5ade12274
            else:
                print("Error at line ", declarations_token.line,". Expected variable or function declaration before main.")
                exit()
            self.get_next_token() #not yet sure if needed
        return

    #to be tested
    def assignments_state(self):
        #no need to check #int
        self.get_next_token()
        if(self.current_token.value != "ID"):
            print("Error at line ", self.current.line ,". Expected variable name.")
            exit()
        self.get_next_token()
        if(assignments_token.value != '='):
            print("Error at line ", self.current.line ,". Expected '='.")
            exit()
        self.expression()
        return

    #to be done
    def functions_declaration_state(self):
        #no need to check #def
    return 
    

    def parse_id_list(self):
        id_list = []

        # Check if the current token is an ID
        if self.current_token.type == 'ID':
            # Add the first identifier to the list
            id_list.append(self.current_token.value)
            self.advance_tokens()

            # Check for additional identifiers separated by commas
            while self.current_token.type == ',':
                self.advance_tokens()  # Consume the comma
                if self.current_token.type == 'ID':
                    # Add the identifier to the list
                    id_list.append(self.current_token.value)
                    self.advance_tokens()
                else:
                    # If there's a comma but no following identifier, raise an error
                    raise SyntaxError("Expected identifier after ','")
        

        return id_list
    
    def parse_declaration_line(self):
        if self.current_token.type == '#int':
            self.advance_tokens()  # Consume '#int' token
            self.id_list = self.parse_id_list()  # Parse id_list
            
        else:
            raise SyntaxError("Expected '#int' at the beginning of declaration_line")


##############################################################

    def while_state(self):

        #condition

        while_token = self.get_next_token()
        if(while_token.value != ':'):
            print("Error...")
            return #kill prog


        #statments TO DO




    def if_state(self):
        #since you are inside the if_block then you know that the previous token was "if" 

        #check for condition
        self.condition()

        #check for :
        if_token = self.lex.get_next_token()
        if(if_token.value != ':'):
            print("Error") 
            return #kill program

        #check for: if, while, ekxorisi, return,  print, input
        self.decide_flow() 

        #check for elif
        if_token = self.lex.get_next_token()
        if(if_token.value != "elif"):
            return if_token 

        next_token = self.if_block()

        #check for else
        if(next_token.value != 'else'):
            return next_token

        #check for ':'
        if_token = self.lex.get_next_token()
        if(if_token.value != ':'):
            print("Error") #kill program
            return 

        self.decide_flow()
        
        return #if you get a token that you wont use, then you reaturn it


    def statement_state():
        return        
        #simple_statement
        #strctured_statment



    def dicede_flow_state():

        



        return







    def condition_state():

        return


    def print_state(self):

        print_token = self.get_next_token()     
        if(print_token.value != '('):
            print("Error")
            return #kill

        #expression

        print_token = self.get_next_token()
        if(print_token.value != ')'):
            print("Error")
            return #kill

    def assignment_state(self):

        assignment_token = self.get_next_token()
        if(assignment_token.value != '='):
            print("Error...")
            return


    def simple_statement(self):
        simple_token = self.get_next_token()
        #assignment check
        if(simple_token.type == 'ID'):
            self.assignment_state()

        #print check
        if(simple_token.value == "print"):
            self.print_state()

        #return check
        #if(simple_token.value == "return"):
        

    def input_state(self):
        input_token = self.get_next_token()
        if(input_token.value != "return"):
            self.return_state()
    

    def return_state(self):
        get_next_token = self.get_next_token()
        if(get_next_token.value != '('):
            print("Error... ")
        


#main function
def main():
    
        print("mphkame ")
    
    
    
if __name__ == "__main__":
    main()
