import threading
import time
from queue import Queue
from concurrent import futures
import concurrent
from state import State


def collapse_state(state):
    return tuple(state.l1 + state.l2 + [state.h1, state.h2])


def is_valid_action(specific_action, state):
    # print("Is valid action")
    if specific_action == "PICK-UP":
        return (
                (state.h1 == "" and len(state.l1) == 2 and state.l1[1] == "h1" and state.l1[-1] == "h1") or
                (state.h1 == "" and len(state.l2) == 2 and state.l2[1] == "h1" and state.l2[-1] == "h1") or
                (state.h2 == "" and len(state.l1) == 2 and state.l1[1] == "h2" and state.l1[-1] == "h2") or
                (state.h2 == "" and len(state.l2) == 2 and state.l2[1] == "h2" and state.l2[-1] == "h2")
        )
    elif specific_action == "PUT-DOWN":
        return (
                (state.h1 != "" and len(state.l1) == 1 and state.l1[0] == "h1") or
                (state.h1 != "" and len(state.l2) == 1 and state.l2[0] == "h1") or
                (state.h2 != "" and len(state.l1) == 1 and state.l1[0] == "h2") or
                (state.h2 != "" and len(state.l2) == 1 and state.l2[0] == "h2")
        )
    elif specific_action == "STACK":
        return (
                (state.h1 != "" and len(state.l1) >= 2 and state.l1[-1] == "h1") or
                (state.h1 != "" and len(state.l2) >= 2 and state.l2[-1] == "h1") or
                (state.h2 != "" and len(state.l1) >= 2 and state.l1[-1] == "h2") or
                (state.h2 != "" and len(state.l2) >= 2 and state.l2[-1] == "h2")
        )
    elif specific_action == "UNSTACK":
        return (
                (state.h1 == "" and len(state.l1) > 2 and state.l1[-1] == "h1") or
                (state.h1 == "" and len(state.l2) > 2 and state.l2[-1] == "h1") or
                (state.h2 == "" and len(state.l1) > 2 and state.l1[-1] == "h2") or
                (state.h2 == "" and len(state.l2) > 2 and state.l2[-1] == "h2")
        )
    elif specific_action == "MOVE":
        return (state.h1 != "" or state.h2 != "")
    elif specific_action == "NOOP":
        return True
    else:
        return False


def execute_action(specific_action, state):
    # print("execute_action")
    new_state = State(
        L1=state.l1[:],
        L2=state.l2[:],
        H1=state.h1,
        H2=state.h2
    )

    if specific_action == "PICK-UP":
        if state.h1 == "" and len(state.l1) == 2 and state.l1[1] == "h1":
            new_state.l1 = state.l1[1:]
            new_state.h1 = state.l1[0]
        elif state.h1 == "" and len(state.l2) == 2 and state.l2[1] == "h1":
            new_state.l2 = state.l2[1:]
            new_state.h1 = state.l2[0]
        elif state.h2 == "" and len(state.l1) == 2 and state.l1[1] == "h2":
            new_state.l1 = state.l1[1:]
            new_state.h2 = state.l1[0]
        elif state.h2 == "" and len(state.l2) == 2 and state.l2[1] == "h2":
            new_state.l2 = state.l2[1:]
            new_state.h2 = state.l2[0]
    elif specific_action == "PUT-DOWN":
        if state.h1 != "" and len(state.l1) == 1 and state.l1[0] == "h1":
            new_state.l1 = [state.h1] + state.l1
            new_state.h1 = ""
        elif state.h1 != "" and len(state.l2) == 1 and state.l2[0] == "h1":
            new_state.l2 = [state.h1] + state.l2
            new_state.h1 = ""
        elif state.h2 != "" and len(state.l1) == 1 and state.l1[0] == "h2":
            new_state.l1 = [state.h2] + state.l1
            new_state.h2 = ""
        elif state.h2 != "" and len(state.l2) == 1 and state.l2[0] == "h2":
            new_state.l2 = [state.h2] + state.l2
            new_state.h2 = ""
    elif specific_action == "STACK":
        if state.h1 != "" and len(state.l1) >= 2 and state.l1[-1] == "h1":
            new_state.l1 = state.l1[:-1] + [state.h1] + state.l1[-1:]
            new_state.h1 = ""
        elif state.h1 != "" and len(state.l2) >= 2 and state.l2[-1] == "h1":
            new_state.l2 = state.l2[:-1] + [state.h1] + state.l2[-1:]
            new_state.h1 = ""
        elif state.h2 != "" and len(state.l1) >= 2 and state.l1[-1] == "h2":
            new_state.l1 = state.l1[:-1] + [state.h2] + state.l1[-1:]
            new_state.h2 = ""
        elif state.h2 != "" and len(state.l2) >= 2 and state.l2[-1] == "h2":
            new_state.l2 = state.l2[:-1] + [state.h2] + state.l2[-1:]
            new_state.h2 = ""
    elif specific_action == "UNSTACK":
        if state.h1 == "" and len(state.l1) > 2 and state.l1[-1] == "h1":
            new_state.l1 = state.l1[:-2] + state.l1[-1:]
            new_state.h1 = state.l1[-2]
        elif state.h1 == "" and len(state.l2) > 2 and state.l2[-1] == "h1":
            new_state.l2 = state.l2[:-2] + state.l2[-1:]
            new_state.h1 = state.l2[-2]
        elif state.h2 == "" and len(state.l1) > 2 and state.l1[-1] == "h2":
            new_state.l1 = state.l1[:-2] + state.l1[-1:]
            new_state.h2 = state.l1[-2]
        elif state.h2 == "" and len(state.l2) > 2 and state.l2[-1] == "h2":
            new_state.l2 = state.l2[:-2] + state.l2[-1:]
            new_state.h2 = state.l2[-2]
    elif specific_action == "MOVE":
        if (state.h1 != "" or state.h2 != ""):
            new_state.l1[-1] = state.l2[-1]
            new_state.l2[-1] = state.l1[-1]
    # NOOP does not modify the state

    return new_state


def is_goal_state(current_state, end_state):
    if current_state.h1 != "" or current_state.h2 != "" :
        return False

    if ((len(current_state.l1) - 1) == len(end_state.l1)) and ((len(current_state.l2) - 1) == len(end_state.l2)):
        for i in range(len(current_state.l1) - 1):
            if current_state.l1[i] != end_state.l1[i]:
                return False
        for i in range(len(current_state.l2) - 1):
            if current_state.l2[i] != end_state.l2[i]:
                return False
        return True
    return False


# def is_sub_goal_state(current_state,end_state,i) :
#     m = len(current_state.l2)
#     n = len(current_state.l1)
#     p = len(end_state.l1)
#     q = len(end_state.l2)
#     #
#     if q > i > m :
#         return False
#     if i > q and m < q and n < i - q :
#         return False
#
#     for j in range(i) :
#         if j < q :
#             if current_state.l2[j] != end_state.l2[j] :
#                 return False
#         else :
#             if current_state.l1[(j - q)] != end_state.l1[(j - q)] :
#                 return False
#     return True

sub_goal_state_lock = threading.Lock()


def is_sub_goal_state(current_state,end_state,i) :
    m = len(current_state.l2)
    n = len(current_state.l1)
    p = len(end_state.l1)
    q = len(end_state.l2)

    for j in range(1,i + 1) :
        if j <= q :
            if m - 1 < i :
                return False
            if current_state.l2[j - 1] != end_state.l2[j - 1] :
                return False
        elif j > q :
            if n - 1 < j - q :
                return False
            if p == 0 and j - q - 1 == 0 :
                return True
            if current_state.l1[(j - q) - 1] != end_state.l1[(j - q) - 1] :
                return False
    return True



def sub_goal_bfs(start_state, end_state, i):
    # print("bfs")
    queue = Queue()
    queue.put((State(L1=start_state.l1[:],
                     L2=start_state.l2[:],
                     H1=start_state.h1,
                     H2=start_state.h2), []))
    explored_states = set()

    while not queue.empty():
        current_state, actions_in_queue = queue.get()

        current_state_collapsed = collapse_state(current_state)
        if current_state_collapsed in explored_states:
            continue

        if is_sub_goal_state(start_state, end_state, i):
            actions_in_queue.append(start_state)
            return actions_in_queue

        explored_states.add(current_state_collapsed)

        for specific_action in ["PICK-UP", "PUT-DOWN", "STACK", "UNSTACK", "MOVE", "NOOP"]:

            if is_valid_action(specific_action, current_state):
                new_state_after_action = execute_action(specific_action, current_state)
                new_actions = actions_in_queue + [specific_action]

                new_collapsed_state = collapse_state(new_state_after_action)
                if new_collapsed_state not in explored_states:
                    queue.put((new_state_after_action, new_actions))

                if is_sub_goal_state(new_state_after_action, end_state, i):
                    new_actions.append(new_state_after_action)

                    return new_actions
    return None


def sub_goal_dfs(start_state, end_state, i):
    stack = [(State(L1=start_state.l1[:],
                    L2=start_state.l2[:],
              H1=start_state.h1,H2=start_state.h2)
              , [])]
    explored_states = set()

    while stack:
        current_state, actions_in_stack = stack.pop()

        current_collapse_state = collapse_state(current_state)

        if current_collapse_state in explored_states:
            continue

        if is_sub_goal_state(current_state, end_state, i):
            actions_in_stack.append(current_state)
            return actions_in_stack

        explored_states.add(current_collapse_state)

        for specific_action in ["PICK-UP", "PUT-DOWN", "STACK", "UNSTACK", "MOVE", "NOOP"]:
            if is_valid_action(specific_action, current_state):

                new_state_after_action = execute_action(specific_action, current_state)
                new_actions = actions_in_stack + [specific_action]

                if is_sub_goal_state(new_state_after_action, end_state, i):
                    new_actions.append(new_state_after_action)
                    return new_actions

                new_collapse_state = collapse_state(new_state_after_action)
                if new_collapse_state not in explored_states:
                    stack.append((new_state_after_action, new_actions))

    return None


# def sub_goal(start_state,end_state,i):
#     current_collapse_state = collapse_state(start_state)
#     explored_states=set()
#
#     if is_sub_goal_state(start_state,end_state,i) :
#         print("reached")
#         return [start_state]
#
#     if current_collapse_state in explored_states :
#         return None
#
#     explored_states.add(current_collapse_state)
#
#     for specific_action in ["PICK-UP","PUT-DOWN","STACK","UNSTACK","MOVE","NOOP"] :
#         if is_valid_action(specific_action,start_state) :
#             new_state_after_action = execute_action(specific_action,start_state)
#             current_collapse_state = collapse_state(new_state_after_action)
#
#             if current_collapse_state in explored_states :
#                 continue
#             # new_state_after_action.print_state()
#             if is_sub_goal_state(new_state_after_action,end_state,i) :
#                 print("reached")
#                 return [new_state_after_action]
#
#             action = sub_goal(new_state_after_action,end_state,i)
#
#             if action is not None :
#                 return [specific_action] + action
#
#     return None


# def plan(start_state,end_state) :
#     actions = []
#     i = 0
#     while not is_goal_state(start_state,end_state) and start_state is not None and i < 14 :
#         start_state.print_state()
#         print(i)
#         sub_goal_actions = sub_goal(start_state,end_state,i)
#         if sub_goal_actions is None :
#             break
#         start_state = sub_goal_actions[-1]
#         actions += sub_goal_actions[:-1]
#         i += 1
#
#     if is_goal_state(start_state,end_state) :
#         return actions
#     return None


# def plan(start_state, end_state):
#     actions = []
#     i = 0
#
#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         futures = []
#
#         while not is_goal_state(start_state, end_state) and start_state is not None and i < 14:
#             start_state.print_state()
#             print(i)
#
#             # Submit sub_goal_bfs to the thread pool
#             future_bfs = executor.submit(sub_goal_bfs, start_state, end_state, i)
#             futures.append(future_bfs)
#
#             # Submit sub_goal_dfs to the thread pool
#             future_dfs = executor.submit(sub_goal_dfs, start_state, end_state, i)
#             futures.append(future_dfs)
#
#             # Wait for either sub_goal_bfs or sub_goal_dfs to complete
#             done, not_done = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
#
#             both_canceled = False
#
#             # Iterate over completed futures
#             for future in done:
#                 if future.exception() is None:
#                     other_future = future_bfs if future == future_dfs else future_dfs
#                     other_future.cancel()
#                     time.sleep(1)
#                     sub_goal_actions = future.result()
#                     actions += sub_goal_actions[:-1]
#                     start_state = sub_goal_actions[-1]
#                 else:
#                     # Handle exception or log it
#                     print(f"An error occurred: {future.exception()}")
#                     both_canceled=True
#             # Clear the list of futures for the next iteration
#             futures.clear()
#             if both_canceled :
#                 break
#             i += 1
#     if is_goal_state(start_state,end_state) :
#         return actions
#     return None


def plan(start_state, end_state):
    actions = []
    i = 0
    timeout_seconds_dfs = 0.5  # Adjust this value to your desired timeout for DFS
    timeout_seconds_bfs = None  # Adjust this value to your desired timeout for BFS

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = []
        temp = True

        while not is_goal_state(start_state, end_state) and start_state is not None and i < 14:
            start_time = time.time()
            start_state.print_state()

            # Submit sub_goal_dfs to the thread pool
            future_dfs = executor.submit(sub_goal_dfs, start_state, end_state, i)
            futures.append(future_dfs)

            # Wait for sub_goal_dfs or timeout
            completed, not_completed = concurrent.futures.wait([future_dfs], timeout=timeout_seconds_dfs,
                                                               return_when=concurrent.futures.FIRST_COMPLETED)
            completed_future = None
            # Check if sub_goal_dfs has results
            if completed:
                completed_future = completed.pop()
                if completed_future == future_dfs and not future_dfs.exception():
                    sub_goal_actions = future_dfs.result()
                    actions += sub_goal_actions[:-1]
                    start_state = sub_goal_actions[-1]

                else:
                    print(f"An error occurred in sub_goal_dfs: {future_dfs.exception()}")

            if time.time() - start_time > 0.5:
                futures.clear()
                print("in")
                start_state.print_state()
                # Submit sub_goal_bfs to the thread pool
                future_bfs = executor.submit(sub_goal_bfs, start_state, end_state, i)
                futures.append(future_bfs)

                # Wait for sub_goal_bfs to complete
                completed, not_completed = concurrent.futures.wait([future_bfs], timeout=timeout_seconds_bfs,
                                                                   return_when=concurrent.futures.FIRST_COMPLETED)

                # Check if sub_goal_bfs has results
                if completed:
                    completed_future = completed.pop()
                    if completed_future == future_bfs and not future_bfs.exception():
                        sub_goal_actions = future_bfs.result()
                        actions += sub_goal_actions[:-1]
                        start_state = sub_goal_actions[-1]
                    else:
                        print(f"An error occurred in sub_goal_bfs: {future_bfs.exception()}")

                # Clear the list of futures for the next iteration
            futures.clear()
            i += 1

    if is_goal_state(start_state, end_state):
        return actions

    return None


def output_sequence_states(sequence_of_actions, sequence_of_states):
    if sequence_of_actions is not None:
        print("Sequence of actions to reach the goal state:")
        current_state = sequence_of_states[0]
        for action in sequence_of_actions:
            print(action)
            current_state = execute_action(action, current_state)
            sequence_of_states.append(
                State(L1=current_state.l1[:], L2=current_state.l2[:], H1=current_state.h1, H2=current_state.h2))
    else:
        print("No solution found.")
    return sequence_of_states