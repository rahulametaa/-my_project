from tkinter import *
import numpy as np
from random import randint,shuffle

class game(object):

    def __init__(self,master):
        self.frame=Frame(master)
        self.count=0
        self.score=0
        self.frame.pack(fill="both",expand=True)
        self.button=[]
        self.board=np.array([[0,0,0],[0,0,0],[0,0,0]])
        self.create_board()

    def create_board(self):
        for i in range(9):
            self.button.append(Button(self.frame,height=5,width=10,text=i+1))
            self.button[i].bind("<Button-1>",self.onclick)
            self.button[i].grid(row=i//3,column=(i+3)%3)
        self.label=Label(self.frame,text="")
        self.label.grid(row=3,column=3)


    def onclick(self,event):
        self.index=int(event.widget.cget("text"))-1
        self.index_i=self.index//3
        self.count+=1
        self.index_j=(self.index+3)%3
        self.board[self.index_i,self.index_j]=1
        self.button[self.index].configure(text="O")
        self.button[self.index].configure(bg="blue")
        self.button[self.index].unbind('<Button-1>')
        x=self.iswinner(self.calculate_score(self.index_i,self.index_j,1),1)
        if(self.count<5 and (not x )):
            self.computer_turn()
        if(self.count==5):
            self.restart()



    def calculate_score(self,i,j,k):
        score=0
        if ( 0 not in self.board[i] and 2/k not in self.board[i]):
           score = score + 10

        elif (0 not in self.board[:,j] and 2/k not in self.board[:,j]):
            score+=10

        elif (i+j)%2==0:
            if(i==1 and j==1):
                if(self.board[0,0]==k and self.board[2,2]==k):
                    score+=10

                elif(self.board[2,0]==k and self.board[0,2]==k):
                    score+=10


            elif(i-j==0):
                if(self.board[0,0]==k and self.board[1,1]==k and self.board[2,2]==k):
                    score += 10

            else:
                if(self.board[0,2] == k and self.board[1, 1] == k and self.board[2, 0] == k):
                    score += 10


        if(score==10):
            return True
        else:
            return False


    def iswinner(self,result,k):
        if(k==1 and result==True):
            self.label.configure(text="you have won ")
            self.restart()
            return True
        elif(k==1):
            return False
        elif(k==2 and result==True):
            self.label.configure(text="computer has won")
            self.restart()

    def reset(self):
        self.board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        for i in range(9):
            self.button[i].bind("<Button-1>", self.onclick)
            self.button[i].configure(text=i+1)
            self.button[i].configure(bg="white")
            self.label.configure(text="")


            self.count=0

    def restart(self):
        self.r1=Button(self.frame,text="Restart",command=self.reset)
        self.r1.grid(row=3,column=4)





    def computer_turn(self):
        (i,j)=self.minimax(self.possible(),2,1)
        self.board[i,j]=2
        self.button[3*i+j].configure(text="X")
        self.button[3 * i + j].configure(bg="orange")
        self.button[3*i+j].unbind('<Button-1>')
        self.iswinner(self.calculate_score(i, j, 2),2)

    def possible(self):
        possible_case=[]
        for t in range(len(np.where(self.board==0)[0])):
            (i,j)=(np.where(self.board==0)[0][t],np.where(self.board==0)[1][t])
            possible_case.append((i,j))
        return possible_case[:]


    def minimax(self,possible_case,k,t=0):
        ls=[]
        for (i,j) in possible_case:
            self.board[i,j]=k
            if(self.terminal(self.possible(),i,j) and t==0):
                return self.utility(self.possible(),i,j,k)
            if(self.terminal(self.possible(),i,j) and t==1):
                ls.append(self.utility(self.possible(),i,j,k))
            elif(k==2):
                ls.append(self.minimax(self.possible(),1))
            else:
                ls.append(self.minimax(self.possible(),2))
            self.board[i,j]=0
        if (t == 1):
            return possible_case[ls.index(max(ls))]

        if(k==2 or k==1):
            return self.max(ls,k)
        else:
            return min(ls)


    def terminal(self,possible_case,i,j):
        if(len(possible_case)==0):
            return True
        elif(self.calculate_score(i,j,1) or self.calculate_score(i,j,2)):
            return True
        else:
            False

    def utility(self,possible_case,i,j,k):
        n=len(possible_case)
        if(k==2 and self.calculate_score(i,j,k)):
            self.board[i, j] = 0
            if(n==0):
                return (10)
            else:
                return (50*(n+1))
        elif(k==1 and self.calculate_score(i,j,k)):
            self.board[i, j] = 0
            if(n==0):
                return -10
            else:
                return((-50)*(n+1))
            return ((n+1)*(-10))
        else:
            self.board[i, j] = 0
            return (0)



    def max(self,ls,k):
        m=0
        for i in ls:
            m=m+i
            return m


    def min(self, ls):
        m=0
        for i in ls:
            if(i<m):
                m=i
        return m


root=Tk()
root.geometry('500x500')
app=game(root)
root.mainloop()
