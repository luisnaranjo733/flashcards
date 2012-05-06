"""This script is scrictly ui.
External dependency: clui"""

from clui import base_clui

#------------------------------------------------------------------------
import callable # (placeholders)
#------------------------------------------------------------------------


#------------------------------------------------------------------------
#Main loop
main = base_clui()
main.title = 'Flashcards'
main.initial_message = 'Welcome!'
main.exit_message = 'Bye Bye!'
main.buffer = '='*72

main.add(
        callables=[callable.login],
        display_name = 'Login',
        patterns = ['^login$','^l(og|et) +me +in$'],)

main.execute()
#------------------------------------------------------------------------

