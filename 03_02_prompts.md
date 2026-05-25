# Timing bug
I suspect that it is possible for there to be a timing related bug when selecting products and then sending an order (a TOCTOU [time of check time of use] race condition). Specifically I suspect that it might be possible to deselect a product and send the order and still have that product included in the order. For example if the order request happened to reach the server first, it might execute before knowing about the last minute deselection.

Write a script that I could run that would show me this bug.

Keep the script minimal and easy to read. When looping over different attempts, exit when you see the bug and print out what you expected to see and when you actually saw. 

The script should try calling deselect and then /orders, but with a tiny delay before the deselect executes to simulate a pause in the deselect getting processed. Make the length of the pause configurable

