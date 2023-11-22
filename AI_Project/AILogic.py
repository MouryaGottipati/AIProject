import copy
import sys
import time
from queue import Queue
from Gui import gui_main
from Gui import Gui


class GuiWithState(Gui):
    def __init__(self, state_type):
        super().__init__(state_type)
    def __hash__(self):
        return hash((tuple(self.l1), tuple(self.l2), self.h1, self.h2))

    def collapse_state(self) :
        return tuple(self.l1),tuple(self.l2),self.h1,self.h2


starttime = time.time()

initial_state = GuiWithState("initial")
goal_state = GuiWithState("goal")
print("Describe goal state:")
print("Block inside hand1:")
initial_state.h1 = input()
print("Block inside hand2:")
initial_state.h2 = input()
print("Number of blocks in L1:")
l1 = int(input())
initial_state.l1 = []
for i in range(l1):
    print(f"Block in {i + 1} position in L1 location")
    initial_state.l1.append(input())
print("Number of blocks in L2:")
l2 = int(input())
initial_state.l2 = []
for i in range(l2):
    print(f"Block in {i + 1} position in L2 location")
    initial_state.l2.append(input())
initial_state.l1.append("h1")
initial_state.l2.append("h2")
print("Describe goal state:")
print("Block inside hand1:")
goal_state.h1 = input()
print("Block inside hand2:")
goal_state.h2 = input()
print("Number of blocks in L1:")
l1 = int(input())
goal_state.l1 = []
for i in range(l1):
    print(f"Block in {i + 1} position in L1 location")
    goal_state.l1.append(input())
print("Number of blocks in L2:")
l2 = int(input())
goal_state.l2 = []
for i in range(l2):
    print(f"Block in {i + 1} position in L2 location")
    goal_state.l2.append(input())
print("Hand in goal state in position above L1 h1/h2:")
hand = input()
goal_state.l1.append(hand)
if hand == "h1":
    goal_state.l2.append("h2")
else:
    goal_state.l2.append("h1")

guis = [initial_state]


def is_valid_action(specific_action, state):
    # print("in is_valid_action")
    # state.print_gui()
    if specific_action == "PICK-UP":
        # print("Inside pickup is_valid action")
        if state.h1 == "" and len(state.l1) == 2 and state.l1[1] == "h1":
            return state.l1[-1] == "h1"
        elif state.h1 == "" and len(state.l2) == 2 and state.l2[1] == "h1":
            return state.l2[-1] == "h1"
        elif state.h2 == "" and len(state.l1) == 2 and state.l1[1] == "h2":
            return state.l1[-1] == "h2"
        elif state.h2 == "" and len(state.l2) == 2 and state.l2[1] == "h2":
            return state.l2[-1] == "h2"
        return False
    elif specific_action == "PUT-DOWN":
        # print("Inside Put-Down is_valid action")
        if state.h1 != "" and len(state.l1) == 1 and state.l1[0] == "h1":
            return True
        elif state.h1 != "" and len(state.l2) == 1 and state.l2[0] == "h1":
            return True
        elif state.h2 != "" and len(state.l1) == 1 and state.l1[0] == "h2":
            return True
        elif state.h2 != "" and len(state.l2) == 1 and state.l2[0] == "h2":
            return True
        return False
    elif specific_action == "STACK":
        # print("Inside stack is_valid action")
        if state.h1 != "" and len(state.l1) >= 2 and state.l1[-1] == "h1":
            return True
        elif state.h1 != "" and len(state.l2) >= 2 and state.l2[-1] == "h1":
            return True
        elif state.h2 != "" and len(state.l1) >= 2 and state.l1[-1] == "h2":
            return True
        elif state.h2 != "" and len(state.l2) >= 2 and state.l2[-1] == "h2":
            return True
        return False
    elif specific_action == "UNSTACK":
        # print("Inside unstack is_valid action")
        if state.h1 == "" and len(state.l1) > 2 and state.l1[-1] == "h1":
            return state.l1[-1] == "h1"
        elif state.h1 == "" and len(state.l2) > 2 and state.l2[-1] == "h1":
            return state.l2[-1] == "h1"
        elif state.h2 == "" and len(state.l1) > 2 and state.l1[-1] == "h2":
            return state.l1[-1] == "h2"
        elif state.h2 == "" and len(state.l2) > 2 and state.l2[-1] == "h2":
            return state.l2[-1] == "h2"
        return False
    elif specific_action == "MOVE":
        # print("Inside Move is_valid action")
        return (state.h1 != "" or state.h2 != "") or (state.h1 == "" and state.h2 == "")
    elif specific_action == "NOOP":
        return True
    else:
        return False


def execute_action(specific_action, state):
    new_state = copy.deepcopy(state)

    if specific_action == "PICK-UP":
        # print("Inside pickup execute action")
        if state.h1 == "" and len(state.l1) == 2 and state.l1[1] == "h1":
            # new_state.l1.pop(len(state.l1)-2)
            new_state.l1=state.l1[1:]
            new_state.h1 = state.l1[0]
        elif state.h1 == "" and len(state.l2) == 2 and state.l2[1] == "h1":
            # new_state.l2.pop(len(state.l2)-2)
            new_state.l2=state.l2[1:]
            new_state.h1 = state.l2[0]
        elif state.h2 == "" and len(state.l1) == 2 and state.l1[1] == "h2":
            # new_state.l1.pop(len(state.l1)-2)
            new_state.l1 = state.l1[1 :]
            new_state.h2 = state.l1[0]
        elif state.h2 == "" and len(state.l2) == 2 and state.l2[1] == "h2":
            # new_state.l2.pop(len(state.l2)-2)
            new_state.l2 = state.l2[1:]
            new_state.h2 = state.l2[0]
    elif specific_action == "PUT-DOWN":
        if state.h1 != "" and len(state.l1) == 1 and state.l1[0] == "h1":
            # new_state.l1.insert(0, state.h1)
            new_state.l1 = [state.h1]+state.l1
            new_state.h1 = ""
        elif state.h1 != "" and len(state.l2) == 1 and state.l2[0] == "h1":
            # new_state.l2.insert(0, state.h1)
            new_state.l2 = [state.h1]+state.l2
            new_state.h1 = ""
        elif state.h2 != "" and len(state.l1) == 1 and state.l1[0] == "h2":
            # new_state.l1.insert(0, state.h2)
            new_state.l1 = [state.h2]+state.l1
            new_state.h2 = ""
        elif state.h2 != "" and len(state.l2) == 1 and state.l2[0] == "h2":
            # new_state.l2.insert(0, state.h2)
            new_state.l2 = [state.h2]+state.l2
            new_state.h2 = ""
    elif specific_action == "STACK":
        if state.h1 != "" and len(state.l1) >= 2 and state.l1[-1] == "h1":
            # new_state.l1.insert(len(state.l1) - 1, state.h1)
            new_state.l1=state.l1[:-1]+[state.h1]+state.l1[-1:]
            new_state.h1 = ""
        elif state.h1 != "" and len(state.l2) >= 2 and state.l2[-1] == "h1":
            # new_state.l2.insert(len(state.l2) - 1, state.h1)
            new_state.l2=state.l2[:-1]+[state.h1]+state.l2[-1:]
            new_state.h1 = ""
        elif state.h2 != "" and len(state.l1) >= 2 and state.l1[-1] == "h2":
            # new_state.l1.insert(len(state.l1) - 1, state.h2)
            new_state.l1 = state.l1[:-1] + [state.h2] + state.l1[-1:]
            new_state.h2 = ""
        elif state.h2 != "" and len(state.l2) >= 2 and state.l2[-1] == "h2":
            # new_state.l2.insert(len(state.l2) - 1, state.h2)
            new_state.l2 = state.l2[:-1] + [state.h2] + state.l2[-1:]
            new_state.h2 = ""
    elif specific_action == "UNSTACK":
        if state.h1 == "" and len(state.l1) > 2 and state.l1[-1] == "h1":
            # new_state.l1.pop(len(state.l1) - 2)
            new_state.l1=state.l1[:-2]+state.l2[-1:]
            new_state.h1 = state.l1[-2]
        elif state.h1 == "" and len(state.l2) > 2 and state.l2[-1] == "h1":
            # new_state.l2.pop(len(state.l2) - 2)
            new_state.l2=state.l2[:-2]+state.l2[-1:]
            new_state.h1 = state.l2[-2]
        elif state.h2 == "" and len(state.l1) > 2 and state.l1[-1] == "h2":
            # new_state.l1.pop(len(state.l1) - 2)
            new_state.l1=state.l1[:-2]+state.l1[-1:]
            new_state.h2 = state.l1[-2]
        elif state.h2 == "" and len(state.l2) > 2 and state.l2[-1] == "h2":
            # new_state.l2.pop(len(state.l2) - 2)
            new_state.l2=state.l2[:-2]+state.l2[-1:]
            new_state.h2 = state.l2[-2]
    elif specific_action == "MOVE":
        if (state.h1 != "" or state.h2 != "") or (state.h1 == "" and state.h2 == ""):
            new_state.l1[-1] = state.l2[-1]
            new_state.l2[-1] = state.l1[-1]
    # NOOP does not modify the state

    return new_state


def is_goal_state(state, end_state):
    if state.h1 == end_state.h1 and state.h2 == end_state.h2 and len(state.l1) == len(end_state.l1) and len(
            state.l2) == len(end_state.l2):
        for j in range(len(end_state.l1)):
            if state.l1[j] != end_state.l1[j]:
                return False
        for j in range(len(end_state.l2)):
            if state.l2[j] != end_state.l2[j]:
                return False
        return True
    else:
        return False


def is_same_state(current_state, state):
    if state.h1 == state.h1 and state.h2 == state.h2 and len(state.l1) == len(state.l1) and len(
            state.l2) == len(state.l2):
        for j in range(len(state.l1)):
            if state.l1[j] != state.l1[j]:
                return False
        for j in range(len(state.l2)):
            if state.l2[j] != state.l2[j]:
                return False
        return True
    else:
        return False


def plan(start_state, end_state):
    explored_collapsed = set()
    queue = Queue()

    queue.put((start_state, []))

    while not queue.empty():
        current_state, actions_in_queue = queue.get()

        current_state_collapsed = current_state.collapse_state()
        if current_state_collapsed in explored_collapsed:
            continue

        if current_state_collapsed == end_state.collapse_state():
            return actions_in_queue

        explored_collapsed.add(current_state_collapsed)

        for specific_action in ["PICK-UP", "PUT-DOWN", "STACK", "UNSTACK", "MOVE", "NOOP"]:
            # print(is_valid_action(specific_action, current_state))
            if is_valid_action(specific_action, current_state):
                new_state_after_action = execute_action(specific_action, current_state)
                new_actions = actions_in_queue + [specific_action]
                queue.put((new_state_after_action, new_actions))
    return None


sequence_of_actions = plan(initial_state, goal_state)

if sequence_of_actions is not None:
    print("Sequence of actions to reach the goal state:")
    for action in sequence_of_actions:
        print(action)
        new_state_sequence_action = execute_action(action, initial_state)
        initial_state = copy.deepcopy(new_state_sequence_action)
        new_state_sequence_action .print_gui()
        guis.append(new_state_sequence_action)

else:
    print("No solution found.")
print("Code runing time:",time.time()-starttime)
gui_main(guis)
