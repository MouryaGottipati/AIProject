from Gui import gui_main
import input
import time
from MainLogic3 import plan, output_sequence_states
import sys
import gc
print(sys.getrecursionlimit())
gc.collect()


initial_state,goal_state = input.initial_state_input(), input.goal_state_input()

# initial_state.print_state()
# goal_state.print_state()

start_time = time.time()
sequence_of_actions = plan(initial_state, goal_state)
sequence_of_states = [initial_state]
sequence_of_states = output_sequence_states(sequence_of_actions,sequence_of_states)
print("Code running time in seconds:", time.time() - start_time)
gui_main(sequence_of_states)
gc.collect()