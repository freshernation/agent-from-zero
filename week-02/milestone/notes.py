# Week 2 Milestone - the notes toolkit
# Author:
#
# A note is {"title": ..., "body": ...}. `notes` is a list of them.
# Every function RETURNS a sentence. None of them print.
#
#   add_note(notes, title, body)
#       "Saved 'milk'."
#       "A note needs a title."                     (empty title - nothing added)
#       "There is already a note called 'milk'."    (same title, any capitals)
#
#   list_titles(notes)
#       "1. milk\n2. call the dentist"   or   "No notes yet."
#
#   find_notes(notes, word)
#       "milk: two litres"  - one line per note whose title or body contains the
#       word, ignoring capitals   or   "No notes mention 'cheese'."
#
#   delete_note(notes, title)
#       "Deleted 'milk'."   or   "No note called 'cheese'."
