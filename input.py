import state


def inputs() :
    return initial_state_input(),goal_state_input()


def initial_state_input() :
    initial_state = state.State()
    print("Describe initial state:")
    print("Block inside hand1:")
    initial_state.h1 = input()
    print("Block inside hand2:")
    initial_state.h2 = input()
    print("Number of blocks in L1:")
    l1 = int(input())
    initial_state.l1 = []
    for i in range(l1) :
        print(f"Block in {i + 1} position in L1 location")
        initial_state.l1.append(input())
    print("Number of blocks in L2:")
    l2 = int(input())
    initial_state.l2 = []
    for i in range(l2) :
        print(f"Block in {i + 1} position in L2 location")
        initial_state.l2.append(input())
    initial_state.l1.append("h1")
    initial_state.l2.append("h2")
    return initial_state


def goal_state_input() :
    goal_state = state.State()
    print("Describe goal state:")
    # print("Block inside hand1:")
    # goal_state.h1 = input()
    # print("Block inside hand2:")
    # goal_state.h2 = input()
    print("Number of blocks in L1:")
    l1 = int(input())
    goal_state.l1 = []
    for i in range(l1) :
        print(f"Block in {i + 1} position in L1 location")
        goal_state.l1.append(input())
    print("Number of blocks in L2:")
    l2 = int(input())
    goal_state.l2 = []
    for i in range(l2) :
        print(f"Block in {i + 1} position in L2 location")
        goal_state.l2.append(input())
    # print("Hand in goal state in position above L1 h1/h2:")
    # hand = input()
    # goal_state.l1.append(hand)
    # if hand == "h1" :
    #     goal_state.l2.append("h2")
    # else :
    #     goal_state.l2.append("h1")

    return goal_state
