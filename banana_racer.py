from websocket import create_connection

def calculateNextStep ( result ):

    nextstep = '0'
    lines = result.splitlines()

    if len(lines) == 3:

        line1,line2,line3 = result.splitlines()

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
                if ( start - i ) > mx_size:
                    if empty_spaces: empty_spaces.pop()
                    empty_spaces.append((int(i),int(start)))
                    mx_size = start - i
                i = start
            else:
                i += 1

        abs_index =  ( empty_spaces[0][0] + empty_spaces[0][1]) // 2

        # 2. convert current index to index found above

        current_index = line1.find("V")

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
