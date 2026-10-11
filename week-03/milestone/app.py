# Week 3 Milestone - Project 1: Desk, with a memory
# Author:
#
#   handle(notes, line)   turn one typed line into the reply (a string).
#                         No printing, no saving, no input().
#
#       add milk | two litres   -> add_note(notes, "milk", "two litres")
#       add milk                -> the same with an empty body
#       list                    -> list_titles(notes)
#       find litres             -> find_notes(notes, "litres")
#       delete milk             -> delete_note(notes, "milk")
#       calc 17 * 23            -> calculate_tool("17 * 23")
#       anything else           -> "Commands: add, list, find, delete, calc, quit"
#
#   main()   load from NOTES_FILE (default notes.json); loop on the prompt "> ";
#            print each reply and save; on quit print "Bye." and stop.
#
# Call main() behind the  if __name__ == "__main__":  guard.
