from websocket import create_connection

def getCandidates( line2 ):

        # 1. get absolute index of next line
        abs_index     = 0
        empty_spaces  = []
        mx_size       = 0
        i             = 0

        while i < len(line2):
            if line2[i] == " ":
                start = i
                while line2[start] == ' ':
                    start += 1
                empty_spaces.append((int(i),int(start)))
                mx_size = start - i
                i = start
            else:
                i += 1
        return empty_spaces

def candidateSelection ( i , candidates ):

    if len(candidates) == 1:
        return (candidates[0][0] + candidates[0][1])//2

    # multiple options to choose from
    # 1 selection is largest length but "V" must be able to cross, means no obstacle while making the move
    for x,y in candidates:
        if x <= i or i <= y:
            return (x+y)//2


def calculateNextStep ( result ):

    nextstep = '0'
    lines = result.splitlines()

    if len(lines) == 3:

        line1,line2,line3 = result.splitlines()

        current_index = line1.find("V")

        candidates = getCandidates( line2 )
        abs_index  = candidateSelection( current_index, candidates )

        # 2. convert current index to index found above
        if current_index < abs_index:
            nextstep = str(abs_index - current_index)
        else:
            nextstep = "-" + str(current_index - abs_index)

    return nextstep




if __name__ == "__main__":

    # initiate web socket connection
    ws = create_connection("ws://blooming-falls-3553.herokuapp.com")
    password = []

    while True:

        result =  ws.recv()

        if str(result).startswith("password"):
            password.append(result)
            break

        # processing login for next step
        nextstep = calculateNextStep( result )

        ws.send(nextstep)

    # close the connection
    ws.close()
    print("password is ", password)
