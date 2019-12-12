# A quick guide to the admin panel

### The tables

The tables used on each page are a sortable, searchable and pageable. This means that the tables can be sorted by each attribute. The search on the otherhand will allow you to search for any term/string in the table.


### Question Groups

The question groups tab lets you add new group questions and edit existing ones. At the top of the view you'll find a dropdown form that adds a new group question. The new group requires a key (preferrably an integer but strings work aswell), name , and a question in the three supported languages.

Below this form the list of is the list of all existing groups. Every group attribute can be edited simply by clicking on them.

### Sessions

The sessions tab has a few functionalities:
You can view the selected class of each session, and view the question-answer chain that the user has clicked.
There is a slider-checkbox that allows you to filter out all sessions that do not have a selected class - eg a null value on the foreign key table reference.
There is also a "Hidden" feature, which allows for modifying the sql statement to take into acount the minimum amount of answers required to be visible.
This can be accessed by <url of backend>/801fc3r __?min=15__ (without a space)
Or by navigating to the sessions view by clicking the "Sessions" tab, and then manually typing ?min=<insert minimum value> into the URL bar.

By clicking on any of the fields of a session, you are greeted by a different view, where you can then see what attributes got what answer, and at what timestamp.

