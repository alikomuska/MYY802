

import lexer

while True:

    text = input("cpy>>>")
    lexer_instance = lexer.Lexer(text)  # Create an instance of the Lexer class
    result ,error = lexer_instance.make_toneks()  # Call the make_toneks method
    if error:print(error.as_string())
    else:
        print(result)

