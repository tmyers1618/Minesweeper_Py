import random, sys, math

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
m, n = 0, 0

def generateFields(diff):
    global hiddenField
    global openField
    hiddenField, openField = {}, {}
    diffs = [0.125, 0.25, 0.5]
    diffrange = math.ceil((m*n)*diffs[diff])

    fillerList=[]
    for k in range(m*n):
        if k < diffrange:
            fillerList.append('B')
        else:
            fillerList.append('*')
    random.shuffle(fillerList)

    for i in range(m):
        for j in range(n):
            name=alphabet[i]+str(j+1)
            hiddenField[name] = fillerList[(i+1)*(j+1)-1]
            openField[name]= '?'

def printField(field):
    currentLine=""
    print('|    ', end='')
    for i in range(n):
        if i<8:
            print(str(i+1), end=' ')
        else:
            print(str(i+1), end='')
    if n>8:
        print(' |')
    else:
        print('|')

    for i in range(m):
        print("| "+alphabet[i]+":", end=" ")
        for j in range(n):
            print(field[alphabet[i]+str(j+1)], end=' ')
        print('|')

def checkBomb(x, y):
    #x is index of new letter, y is new row num 
    if x<0 or x>=m:
        return 0
    elif 0>=y or y>n:
        return 0
    elif hiddenField[alphabet[x]+str(y)]=='B':
        return 1
    else:
        return 0

def sweep(a, b):
    if hiddenField[a+str(b)]=='B':
        openField[a+str(b)]='B'
        return False
    else:
        bombs=countBombs(a, b)
        openField[a+str(b)]=str(bombs)
        hiddenField[a+str(b)]=str(bombs)
        return True

def countBombs(a, b):
    bombs=0
    x=alphabet.index(a)
    bombs+=checkBomb(x+1,b)
    bombs+=checkBomb(x+1,b+1)
    bombs+=checkBomb(x+1,b-1)
    bombs+=checkBomb(x,b+1)
    bombs+=checkBomb(x,b-1)
    bombs+=checkBomb(x-1,b)
    bombs+=checkBomb(x-1,b+1)
    bombs+=checkBomb(x-1,b-1)
    return bombs
    
def newGame():
    global m
    global n
    while True:
        print("New game started. How many rows should the field have? ", end='')
        m = int(input())
        if m>26:
            print('That\'s too many rows - choose something less.')
        else:
            break
    print("And how many columns? ", end='')
    n = int(input())

    print("\nDifficulties:")
    print("1: Private Ryan")
    print('2: Technician Upham')
    print('3: Captain Miller')
    print('Select your difficulty: ', end='')
    choice=int(input())-1
    print("\nGenerating your field...")
    generateFields(choice)

    while True:
        turnBool = newTurn()
        if turnBool == True and '*' not in list(hiddenField.values()):
            print('Congratulations, you cleared the field!  You win!!!')
            numbombs=str(list(hiddenField.values()).count('B'))
            print('From a field of '+str(m*n)+' tiles you found '+numbombs+' mines.')
            print('Here\'s what your minefield looked like:')
            printField(hiddenField)
            print('Your stats - Height: '+str(m)+', Width: '+str(n)+', Bombs: '+numbombs)
            name=''
            while True:
                print('Please enter a username to save your score with (up to 12 characters): ', end='')
                name=input()
                if len(name)>12:
                    print('That\'s too long - try again.')
                elif len(name)<12:
                    name+=' '*(12-len(name))
                    break
                else:
                    break

            height=str(m)
            width=str(n)
            if len(height)<2:
                height=' '*(2-len(height)) + height
            if len(width)<3:
                width=' '*(3-len(width))+width
            if len(numbombs)<3:
                numbombs=' '*(3-len(numbombs))+numbombs
            hsarr=inputHS()
            hsarr.append([name, height, width, numbombs])
            outputHS(hsarr)
            return
        elif turnBool == False:
            print('\nOops...')
            printField(openField)
            print("\nHere's what your minefield looked like: ")
            printField(hiddenField)
            return
        else:
            continue
            
    return

def newTurn():
    printField(openField)

    while True:
        print('\nSelect letter coordinate: ', end='')
        a = input()
        if alphabet.index(a)>=m:
            print('That selection is out of bounds.  Please try again')
        else:
            break
    while True:
        print('Select number coordinate: ', end='')
        b = int(input())
        if b>n:
            print('That selection is out of bounds.  Please try again')
        else:
            break
        
    # a is actual row-letter, b is actual column-number
    print('Would you like to sweep (S) or flag a mine (F)? ', end='')
    choice=input()
    
    if choice=='S':
        sweep(a, b)
        # Portion for automatically cleaning the board
        x=alphabet.index(a)
        for i in range(x-1, x+2):
            for j in range(b-1, b+2):
                if 0<=i<m and 0<j<=n:
                    if checkBomb(i, j)==0 and countBombs(alphabet[i], j)==0:
                        sweep(alphabet[i], j)
        escape=1
        while escape!=0:
            escape=0
            for i in range(m):
                for j in range(n):
                    if openField[alphabet[i]+str(j+1)] == '0':
                        for k in range(i-1, i+2):
                            for l in range(j-1, j+2):
                                if 0<=k<m and 0<=l<n:
                                    if openField[alphabet[k]+str(l+1)]=='?':
                                        escape=1
                                        sweep(alphabet[k], l+1)
        return sweep(a,b)
    
    elif choice=='F':
        openField[a+str(b)]='F'
                  
    else:
        print('Invalid choice.  Make another selection')

def inputHS():
    inputHS = open("highscores.txt")
    hsarray=inputHS.readlines()
    inputHS.close()

    for i in range(len(hsarray)):
        hsarray[i]=hsarray[i].replace('\n', '')
        hsarray[i]=hsarray[i].split(',')

    return hsarray


def printHS(hsarray):
    print('    Name    | Height | Width | Bombs ')
    print()
    for i in range(len(hsarray)):
        print(hsarray[i][0]+'|   '+str(hsarray[i][1])+'   |  '+str(hsarray[i][2])+'  |  '+str(hsarray[i][3]))
    return

def outputHS(hsarray):
    outHS = open("highscores.txt", 'w')
    for i in range(len(hsarray)):
        outHS.write(','.join(hsarray[i])+'\n')
    outHS.close()
    return


#-----------------------------------------------------------------------
print('Welcome to Minesweeper!')
while True:
    print('\nMain Menu:')
    print('1: New Game')
    print('2: High Scores')
    print('3: Exit')
    print('Please make your selection: ', end='')
    pick = int(input())

    if pick==1:
        newGame()
        
    elif pick==2:
        hsarr=inputHS()
        printHS(hsarr)
        
    elif pick==3:
        print('Goodbye!')
        sys.exit()
    else:
        print('Invalid response.  Make another selection')






    

