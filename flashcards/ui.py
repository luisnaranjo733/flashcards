"""This script is scrictly ui.
External dependency: clui"""

from clui import base_clui

#------------------------------------------------------------------------
import authenticate # (placeholders)
import callables
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
    callables=[authenticate.authenticate],
    display_name = 'Login',
    patterns = ['^log( +)?in$','^l(og|et) +me +in$'],
    )

main.add(
    callables=[authenticate.add_user],
    display_name = 'Add a user',
    patterns = ['^[Aa]dd +(a +)?[Uu]ser$']
    )

main.add(
    callables=[authenticate.__show_users],
    display_name='Show all users',
    patterns=['^(list|show) *(all *)?(of +the +)?users?$']
    )
    
main.add(
    callables=[authenticate.delete_user],
    display_name='Delete a user',
    patterns=['^[Dd]el(ete)? +(a +)?[Uu]ser$'],
    )
    
main.execute()
#------------------------------------------------------------------------

