This tool was originally developped as a tool for personal use. It is intended to help in the developping process of Sage (http://www.sagemath.org) in conjuction with the Kate editor (http://kate-editor.org/). What it does is basically parse the output of the konsole session in Kate to detect the local variables at each step of the debugging process. It also comunicates with kate through dbus to put the cursor in the line being currently executed, and send the debug control commands to the session.

Installation:

Just unpack the archive.

Dependencies:

* Python 3
* PyQt-5
* Kate
* Sage

Instructions:

1. Start Kate
2. Start a log of the session, to do so, type "script -f logfile" (you can change the name of the log file as you want)
3. Run debugger.py, a window will open
4. In the upper bar, enter the location of the log file.
5. Start sage in the konsole session of kate
6. Do your usual work/development in sage
7. When you want to trace the execution of some command, enter the command in the second text bar of the debugger, hit
return.
8. The debugger app will send the "trace" command, which triggers the pdb process.
9. From now, at each step you will see the file being executed in the kate editor, with the cursor at the line being
executed. The local variables will be shown in the window.
10. The "Next step" button will run the next step of the execution, no matter in which funstion it is.
11. The "Next step in function" will run the next step that stays in the current function. That is, if another function
is called, the execution continues until it returns to the current one.
12. The "Return function" continues the execution until the current function returns.
13. The "Quit debugger" finishes the pdb loop.
14. The buttons "<" and ">" allows you to go back and forth the history of the previously executed steps. Note that this
does not mean that the execution of the command goes back, it just shows the previous states in the window.


For any question or comment, please email me.

mmarco@unizar.es
