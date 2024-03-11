import sys

################################
###         TOKENS           ###
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




class Token:
    def __init__(self, type, value):
        self.type = type
        self.value =value
        

    def __repr__(self):
        if self.value: 
            return f'{self.type}:{self.value}'
        return f'{self.type}'
    

#####################################
###           ERRORS            ###
#####################################
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
###           POSITION            ###
#####################################



#####################################
###            LEXER              ###
#####################################
    
class Lexer:
    def __init__(self,text):
        self.text =text 
        self.pos=-1
        self.current_char =None
        self.advance()


    def  advance(self):
        self.pos+=1
        if self.pos < len(self.text):
            self.current_char=self.text[self.pos] 
        else: 
             self.current_char=None
            

    def make_toneks(self):
        tokens=[]
        
        
        
        while self.current_char!=None:
            if self.current_char == '\t' or self.current_char == ' ':
                self.advance()
            elif self.current_char  in DIGITS :
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_word())

            
            elif self.current_char in OPERATORS:
                tokens.append(self.make_operators())
                self.advance() 
            elif self.current_char in GROUPING_SYMBOLS|COMMENT_SYMBOL:
                tokens.append(self.make_group_symbols())
                self.advance()            
            elif self.current_char in COMMENT_SYMBOL:
                tokens.append(Token('COMMENT_SYMBOL',self.current_char))
                self.advance()
            else:
                char=self.current_char
                self.advance()
                return[] ,Illegalchar("'"+char+"'")
        self.advance()         
        return tokens  ,None       

    def make_word(self):
        result = ''
        while self.current_char is not None and self.current_char in LETTERS:
                result += self.current_char
                self.advance()
        if result in KEYWORDS:
            return Token('keyword',result)
        else:        
            return Token('WORD', result)


    def make_number(self):
        num_str = ''
    
        while self.current_char is not None and self.current_char in DIGITS :
            num_str += self.current_char
            self.advance()
    
    # Check if the next character is an illegal character
        if self.current_char is not None and self.current_char in LETTERS:
            return [], Illegalchar("'" + self.current_char + "'")

    # Create a token for the integer value
        return Token('INT', int(num_str))

    def make_operators(self):
        result=''
        while self.current_char is not None and self.current_char in OPERATORS:
                result += self.current_char
                self.advance()
        return Token('OPERATOR', result)
        
    def make_group_symbols(self):
        result=''
        while self.current_char is not None and self.current_char in GROUPING_SYMBOLS|COMMENT_SYMBOL:
                result += self.current_char
                self.advance()
                if self.current_char=='{' or self.current_char=='}':
                    result+=self.current_char
                    return Token('GROUP_SYMBOL',result)
                elif self.current_char=='#':
                    result +=self.current_char
                    return Token('COMMENT_SYMBOL',result)
        return Token('GROUP_SYMBOL', result)
    
    
    
    def run(text):
        basic=Lexer(text)
        tokens=basic.make_tokens()
        return tokens


#  main function
def main():
    inputFilePath = sys.argv[1]



if __name__ == "__main__":
    main()
