"""This script is scrictly ui.
External dependency: clui"""

from clui import base_clui

#------------------------------------------------------------------------
import callables # (placeholders)
import models
#------------------------------------------------------------------------


#------------------------------------------------------------------------
#Main loop
main = base_clui()
main.title = 'Flashcards'
main.initial_message = 'Welcome!'
main.exit_message = 'Bye Bye!'
main.buffer = '='*72

main.add(
    callables=[callables.login],
    display_name = 'Login',
    patterns = ['^log( +)?in$','^l(og|et) +me +in$'],
    )

main.add(
    callables=[callables.add_user],
    display_name = 'Add user',
    patterns = ['^[Aa]dd +(a +) [Uu]ser$']
    )

main.add(
    callables=[models.show_users],
    display_name='List users',
    patterns=['^(list|show) *(all *)?users?$']
    )
main.execute()
#------------------------------------------------------------------------

