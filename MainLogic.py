from queue import Queue

from state import State


def collapse_state(state) :
    return tuple(state.l1 + state.l2 + [state.h1,state.h2])


def is_valid_action(specific_action,state) :
    if specific_action == "PICK-UP" :
        return (
                (state.h1 == "" and len(state.l1) == 2 and state.l1[1] == "h1" and state.l1[-1] == "h1") or
                (state.h1 == "" and len(state.l2) == 2 and state.l2[1] == "h1" and state.l2[-1] == "h1") or
                (state.h2 == "" and len(state.l1) == 2 and state.l1[1] == "h2" and state.l1[-1] == "h2") or
                (state.h2 == "" and len(state.l2) == 2 and state.l2[1] == "h2" and state.l2[-1] == "h2")
        )
    elif specific_action == "PUT-DOWN" :
        return (
                (state.h1 != "" and len(state.l1) == 1 and state.l1[0] == "h1") or
                (state.h1 != "" and len(state.l2) == 1 and state.l2[0] == "h1") or
                (state.h2 != "" and len(state.l1) == 1 and state.l1[0] == "h2") or
                (state.h2 != "" and len(state.l2) == 1 and state.l2[0] == "h2")
        )
    elif specific_action == "STACK" :
        return (
                (state.h1 != "" and len(state.l1) >= 2 and state.l1[-1] == "h1") or
                (state.h1 != "" and len(state.l2) >= 2 and state.l2[-1] == "h1") or
                (state.h2 != "" and len(state.l1) >= 2 and state.l1[-1] == "h2") or
                (state.h2 != "" and len(state.l2) >= 2 and state.l2[-1] == "h2")
        )
    elif specific_action == "UNSTACK" :
        return (
                (state.h1 == "" and len(state.l1) > 2 and state.l1[-1] == "h1") or
                (state.h1 == "" and len(state.l2) > 2 and state.l2[-1] == "h1") or
                (state.h2 == "" and len(state.l1) > 2 and state.l1[-1] == "h2") or
                (state.h2 == "" and len(state.l2) > 2 and state.l2[-1] == "h2")
        )
    elif specific_action == "MOVE" :
        return (state.h1 != "" or state.h2 != "")
    elif specific_action == "NOOP" :
        return True
    else :
        return False


def execute_action(specific_action,state) :
    new_state = State(
        L1=state.l1[:],
        L2=state.l2[:],
        H1=state.h1,
        H2=state.h2
    )

    if specific_action == "PICK-UP" :
        if state.h1 == "" and len(state.l1) == 2 and state.l1[1] == "h1" :
            new_state.l1 = state.l1[1 :]
            new_state.h1 = state.l1[0]
        elif state.h1 == "" and len(state.l2) == 2 and state.l2[1] == "h1" :
            new_state.l2 = state.l2[1 :]
            new_state.h1 = state.l2[0]
        elif state.h2 == "" and len(state.l1) == 2 and state.l1[1] == "h2" :
            new_state.l1 = state.l1[1 :]
            new_state.h2 = state.l1[0]
        elif state.h2 == "" and len(state.l2) == 2 and state.l2[1] == "h2" :
            new_state.l2 = state.l2[1 :]
            new_state.h2 = state.l2[0]
    elif specific_action == "PUT-DOWN" :
        if state.h1 != "" and len(state.l1) == 1 and state.l1[0] == "h1" :
            new_state.l1 = [state.h1] + state.l1
            new_state.h1 = ""
        elif state.h1 != "" and len(state.l2) == 1 and state.l2[0] == "h1" :
            new_state.l2 = [state.h1] + state.l2
            new_state.h1 = ""
        elif state.h2 != "" and len(state.l1) == 1 and state.l1[0] == "h2" :
            new_state.l1 = [state.h2] + state.l1
            new_state.h2 = ""
        elif state.h2 != "" and len(state.l2) == 1 and state.l2[0] == "h2" :
            new_state.l2 = [state.h2] + state.l2
            new_state.h2 = ""
    elif specific_action == "STACK" :
        if state.h1 != "" and len(state.l1) >= 2 and state.l1[-1] == "h1" :
            new_state.l1 = state.l1[:-1] + [state.h1] + state.l1[-1 :]
            new_state.h1 = ""
        elif state.h1 != "" and len(state.l2) >= 2 and state.l2[-1] == "h1" :
            new_state.l2 = state.l2[:-1] + [state.h1] + state.l2[-1 :]
            new_state.h1 = ""
        elif state.h2 != "" and len(state.l1) >= 2 and state.l1[-1] == "h2" :
            new_state.l1 = state.l1[:-1] + [state.h2] + state.l1[-1 :]
            new_state.h2 = ""
        elif state.h2 != "" and len(state.l2) >= 2 and state.l2[-1] == "h2" :
            new_state.l2 = state.l2[:-1] + [state.h2] + state.l2[-1 :]
            new_state.h2 = ""
    elif specific_action == "UNSTACK" :
        if state.h1 == "" and len(state.l1) > 2 and state.l1[-1] == "h1" :
            new_state.l1 = state.l1[:-2] + state.l1[-1 :]
            new_state.h1 = state.l1[-2]
        elif state.h1 == "" and len(state.l2) > 2 and state.l2[-1] == "h1" :
            new_state.l2 = state.l2[:-2] + state.l2[-1 :]
            new_state.h1 = state.l2[-2]
        elif state.h2 == "" and len(state.l1) > 2 and state.l1[-1] == "h2" :
            new_state.l1 = state.l1[:-2] + state.l1[-1 :]
            new_state.h2 = state.l1[-2]
        elif state.h2 == "" and len(state.l2) > 2 and state.l2[-1] == "h2" :
            new_state.l2 = state.l2[:-2] + state.l2[-1 :]
            new_state.h2 = state.l2[-2]
    elif specific_action == "MOVE" :
        if state.h1 != "" or state.h2 != "" :
            new_state.l1[-1] = state.l2[-1]
            new_state.l2[-1] = state.l1[-1]
    # NOOP does not modify the state

    return new_state


def is_goal_state(current_state,end_state) :
    if current_state.h1 != "" or current_state.h2 != "" :
        return False

    if ((len(current_state.l1) - 1) == len(end_state.l1)) and ((len(current_state.l2) - 1) == len(end_state.l2)) :
        for i in range(len(current_state.l1) - 1) :
            if current_state.l1[i] != end_state.l1[i] :
                return False
        for i in range(len(current_state.l2) - 1) :
            if current_state.l2[i] != end_state.l2[i] :
                return False
        return True
    return False


def is_sub_goal_state(current_state,end_state,i) :
    m = len(current_state.l2)
    n = len(current_state.l1)
    p = len(end_state.l1)
    q = len(end_state.l2)
    #
    if q > i > m :
        return False
    if i > q and m < q and n < i - q :
        return False
    for j in range(i) :
        if j < q :
            if current_state.l2[j] != end_state.l2[j] :
                return False
        else :
            if current_state.l1[(j - q)] != end_state.l1[(j - q)] :
                return False
    return True


def sub_goal(start_state,end_state,i) :
    queue = Queue()
    queue.put((start_state,[]))
    explored_states = set()

    while not queue.empty() :
        current_state,actions_in_queue = queue.get()

        current_state_collapsed = collapse_state(current_state)
        if current_state_collapsed in explored_states :
            continue

        if is_sub_goal_state(start_state,end_state,i) :
            actions_in_queue.append(start_state)
            return actions_in_queue

        explored_states.add(current_state_collapsed)

        for specific_action in ["PICK-UP","PUT-DOWN","STACK","UNSTACK","MOVE","NOOP"] :

            if is_valid_action(specific_action,current_state) :
                new_state_after_action = execute_action(specific_action,current_state)
                new_actions = actions_in_queue + [specific_action]

                if is_sub_goal_state(new_state_after_action,end_state,i) :
                    new_actions.append(new_state_after_action)
                    return new_actions

                new_state_collapse=collapse_state(new_state_after_action)
                if new_state_collapse not in explored_states:
                    queue.put((new_state_after_action,new_actions))


    return None


def plan(start_state,end_state) :
    actions = []
    i = 0
    while not is_goal_state(start_state,end_state) and start_state is not None and i < 14 :
        start_state.print_state()
        print(i)
        sub_goal_actions = sub_goal(start_state,end_state,i)
        if sub_goal_actions is None :
            break
        start_state = sub_goal_actions[-1]
        actions += sub_goal_actions[:-1]
        i += 1

    if is_goal_state(start_state,end_state) :
        return actions
    return None


def output_sequence_states(sequence_of_actions,sequence_of_states) :
    if sequence_of_actions is not None :
        print("Sequence of actions to reach the goal state:")
        current_state = sequence_of_states[0]
        for action in sequence_of_actions :
            print(action)
            current_state = execute_action(action,current_state)
            sequence_of_states.append(
                State(L1=current_state.l1[:],L2=current_state.l2[:],H1=current_state.h1,H2=current_state.h2))
    else :
        print("No solution found.")
    return sequence_of_states
