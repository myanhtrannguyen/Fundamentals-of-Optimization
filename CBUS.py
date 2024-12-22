#FIX  LOI
from ortools.sat.python import cp_model
class SolverCBUS():
    def __init__(self,filepath : str):
        self.filepath=filepath
    def takeInput(self):
        self.n,self.k=list(map(int,input().split()))
        self.travel=[list(map(int, input().split())) for i in range(self.n*2+1)]
        self.best=[sum(list(map(sum,self.travel)))]
        
    def takeInputbyFilepath(self):
        with open(self.filepath,"r") as f:
            lines=f.readlines() 
            self.n,self.k=list(map(int,lines[0].split()))
            self.travel=[list(map(int,lines[i].split())) for i in range(1,self.n*2+2)]
            self.best=[sum(list(map(sum,self.travel)))]
    def prepareBeforeRecusive(self):
        self.takeInputbyFilepath()
        self.choices=[[] for i in range(self.n*2)]
        self.choices[0]=list(range(1,self.n+1))
        self.visited=[False for i in range(self.n*2)]
        self.totalLenght=[0]
        self.solution=[0 for i in range(self.n*2)]
        self.cap=[0]
        new=[list(map(lambda x: x if x>0 else float("inf"),self.travel[i])) for i in range(self.n*2+1)]
        self.min=min(list(map(min,new)))
    def solveBacktracking(self,i):
        for choice in self.choices[i]:
            if self.visited[choice-1]==False:
                if(choice<=self.n and self.cap[0]==self.k):
                    continue
                if(choice<=self.n):
                    self.cap[0]+=1
                else:
                    self.cap[0]-=1
                self.solution[i]=choice
                self.visited[choice-1]=True
                if i==0:
                    self.totalLenght[0]+=self.travel[0][choice]
                else:
                    self.totalLenght[0]+=self.travel[self.solution[i-1]][choice]
                if (self.n*2-i)*self.min+self.totalLenght[0]<self.best[0]:
                    if(i==self.n*2-1):
                        self.totalLenght[0]+=self.travel[choice][0]
                        if self.totalLenght[0]<self.best[0]:
                            self.best[0]=self.totalLenght[0]
                        self.totalLenght[0]-=self.travel[choice][0]
                    else:
                        self.choices[i+1]=self.choices[i][:]
                        if choice<=self.n:
                            self.choices[i+1].append(choice+self.n)
                        self.solveBacktracking(i+1)
                        self.choices[i+1]=[]
                if i==0:
                    self.totalLenght[0]=0
                else:
                    self.totalLenght[0]-=self.travel[self.solution[i-1]][choice]
                if(choice<=self.n):
                    self.cap[0]-=1
                else:
                    self.cap[0]+=1
                self.visited[choice-1]=False
                self.solution[i]=0
        

                    
    def Print(self):
        self.takeInputbyFilepath()
        print(self.n,self.k,self.travel) 
    def Solver(self):
        model=cp_model.CpModel()
        self.takeInputbyFilepath()
        D=sum(list(map(sum,self.travel)))
        x=[model.new_int_var(0,self.n*2,"x["+str(i)+"]") for i in range(self.n*2)]
        y=[model.new_int_var(0,D,"y["+str(i)+"]") for i in range(self.n*2+1)]
        model.AddAllDifferent(x)
        model.Add(y[0]==0)
        for i in range(self.n*2):
            model.add(x[i]!=i)
        c=[model.new_int_var(0,self.k,"c["+str(i)+"]") for i in range(self.n*2+2)]
        model.add(c[0]==0)
        for i in range(self.n*2):
            for j in range(self.n*2+1):
                a=model.new_bool_var("")
                model.add(c[i]==0).only_enforce_if(a)
                model.add(c[i]!=0).only_enforce_if(a.Not())
                model.add(x[i]<=self.n).only_enforce_if(a)
                b=model.new_bool_var("")
                model.add(c[i]==self.k).only_enforce_if(b)
                model.add(c[i]!=self.k).only_enforce_if(b.Not())
                model.add(x[i]>self.n).only_enforce_if(b)
                d=model.new_bool_var("")
                model.add(x[i]==j).only_enforce_if(d)
                model.add(x[i]!=j).only_enforce_if(d.Not())
                model.add(y[j]==y[i]+self.travel[i][j]).only_enforce_if(d)
                if (j>self.n):
                    model.add(c[j]==c[i]-1).only_enforce_if(d)
                else:
                    model.add(c[j]==c[i]+1).only_enforce_if(d)
        model.Minimize(y[self.n*2])

        solver=cp_model.CpSolver()    
        
        status=solver.solve(model)
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print(solver.Value(y[self.n*2]))
            for i in range(self.n*2):
                print(solver.Value(x[i]),end=" ")
            print()
            for i in range(self.n*2+1):
                print(solver.Value(y[i]),end=" ")
        else:
            print("NO SOLUTION") 
cp=SolverCBUS("test.txt")  
cp.prepareBeforeRecusive()
cp.solveBacktracking(0)
print(cp.best[0])