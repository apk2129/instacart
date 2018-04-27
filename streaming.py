import requests
import re

class Password:

    def __init__( self ):
        self.password = []

    def set( self, index, letter ):

        if index > ( len( self.password ) - 1 ):

            max = index - len(self.password) + 1
            while max:
                self.password.append('')
                max -= 1

        if self.password[index] != '':
            return True

        self.password[index] = letter

        if len(self.password) > 50:
            return True

        return False


def getLetter(matrix, up , right ):

    m = len(matrix) - 1
    n = len(matrix[0]) - 1
    return matrix[ m - int(up) ][ int(right)]



if __name__ =="__main__":

    chunk_size        = 1024
    bytes_transferred = 0
    response          = requests.get('https://enigmatic-plains-7414.herokuapp.com/', stream=True)
    password          = Password()

    for chunk in response.iter_content(chunk_size):

        lists  = chunk.strip().split("\n")
        index  = int(re.findall(r"[-+]?\d*\.\d+|\d+", lists[0])[0])
        y,x    = re.findall(r"[-+]?\d*\.\d+|\d+", lists[1] )
        matrix = lists[2:]

        letter = getLetter( matrix, x, y )
        if password.set(index, letter):
            response.close()
            break


    print("password is " + ''.join(password.password))
