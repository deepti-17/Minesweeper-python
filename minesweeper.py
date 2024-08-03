#minesweeper game
import random
import re

class Board:
    def __init__(self,dim_size,num_bombs):
        #board parameters
        self.dim_size=dim_size
        self.num_bombs=num_bombs
        #the board
        self.board=self.make_new_board()
        self.assign_values()
        self.dug=set()         #set(row,col) of locations uncovered already

    def make_new_board(self):
        board=[[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
    
        #planting the bombs
        bombs_planted=0
        while(bombs_planted<self.num_bombs):
            loc=random.randint(0,self.dim_size**2-1)
            row=loc // self.dim_size
            col=loc % self.dim_size
            if board[row][col]=='*':    #bomb planted already
                continue
            board[row][col]='*'         #else plant bomb here
            bombs_planted+=1
        return board

    def assign_values(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c]=='*':
                    continue             #if it is itself a bomb we need not calculate the neighboring bombs
                self.board[r][c]=self.neighboring_bombs(r,c)

    def neighboring_bombs(self,row,col):
        num_bombs_nei=0
        for r in range(max(0,row-1),min(self.dim_size-1,row+1)+1):        #checking row above and row below   #gives all the 8
            for c in range(max(0,col-1),min(self.dim_size-1,col+1)+1):    #checking col left and col right    #squares next to current
                if r==row and c==col:           #dont check current location
                    continue
                if self.board[r][c]=='*':
                    num_bombs_nei+=1
        return num_bombs_nei            

    def dig(self,row,col):         #dig this location
        self.dug.add((row,col))    #keeping track of already dug locations
        if self.board[row][col]=='*':
            return False
        elif self.board[row][col]>0:
            return True
        
        for r in range(max(0,row-1),min(self.dim_size-1,row+1)+1):        #checking row above and row below   #gives all the 8
            for c in range(max(0,col-1),min(self.dim_size-1,col+1)+1):    #checking col left and col right    #squares next to current
                if(r,c) in self.dug:
                    continue       #we have already dug here
                self.dig(r,c)      #recursively search for square with a neighboring bomb
        return True

    def __str__(self):
        visible_board=[[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]    #board that will be visible to player after every move
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if(row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])    #show the value at this location to player
                else:
                    visible_board[row][col]=' '        #dont show whats at the place to palyer
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep                

#playing the game
def play(dim_size=10,num_bombs=10):
    board=Board(dim_size,num_bombs)       #initializing board and planting bombs
    safe=True
    while len(board.dug)<board.dim_size**2-num_bombs:
        print(board)
        user_input = re.split(',(\\s)*',input("Where would you like to dig? Input as row,col: "))
        row,col=int(user_input[0]),int(user_input[-1])
        if row<0 or row>=board.dim_size or col<0 or col>=dim_size:    #input is out of bounds
            print("Invalid Input. Try again.")
            continue
        safe=board.dig(row,col)             #else dig
        if not safe:
            break                   #dug a bomb game over!

    if safe:
        print("CONGRATULATIONS!!! YOU HAVE WON!")
    else:
        print("GAME OVER! TRY AGAIN")    
        board.dug=[(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)    


if __name__ == '__main__':
    play()