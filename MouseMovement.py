import pyautogui
import time

# Store the initial mouse position
initial_x, initial_y = pyautogui.position()

# Flag to control the mouse movement loop
continue_movement = True

try:
    while continue_movement:
        # Sleep for 0.1 seconds to periodically check mouse position
        time.sleep(0.1)
        
        # Get the current mouse position
        current_x, current_y = pyautogui.position()
        
        # Check if the mouse has moved
        if initial_x == current_x and initial_y == current_y:
            # Mouse is still, time to move it dramatically!
            
            # Move the mouse 100 pixels to the right with slower speed (duration=4 seconds)
            pyautogui.moveTo(initial_x + 100, initial_y, duration=4)
            print("Dramatically moved mouse to the right!")
            
            # Move the mouse 100 pixels to the left with slower speed (duration=4 seconds)
            pyautogui.moveTo(initial_x, initial_y, duration=4)
            print("Dramatically moved mouse to the left!")
            
            # Move the mouse 100 pixels up with slower speed (duration=4 seconds)
            pyautogui.moveTo(initial_x, initial_y - 100, duration=4)
            print("Dramatically moved mouse up!")
            
            # Move the mouse 100 pixels down with slower speed (duration=4 seconds)
            pyautogui.moveTo(initial_x, initial_y, duration=4)
            print("Dramatically moved mouse down!")
        
        # Update the initial mouse position for the next loop
        initial_x, initial_y = pyautogui.position()

except KeyboardInterrupt:
    # Handle Ctrl+C to allow the user to cancel the script gracefully
    print("Script canceled by user.")
