import sys
import matlab.engine
eng = matlab.engine.start_matlab()


#print sys.argv
f=open(sys.argv[1])
lines = f.read()
startOfPlayers = lines.index('{')
startegyStart = lines[startOfPlayers+1:].index('{')
startegyEnd = lines[startOfPlayers+1:][startegyStart+1:].index('}')

x=lines[startOfPlayers+1:][startegyStart+1:][:startegyEnd].split()

stratergies = [int(p) for p in x]
noOfPlayers=len(stratergies)
payoffs = [float(p) for p in lines.splitlines()[-1].split()]
k=0
curr_strat=[1 for i in range(0,len(stratergies))]
possibleStratergies=[]
utils=[{} for i in range(0,len(stratergies))]


while k<len(payoffs):
    possibleStratergies.append(tuple(curr_strat))
    for i in range(0,len(stratergies)):
        utils[i][tuple(curr_strat)]=payoffs[k]
        k=k+1
    for i in range(0,len(stratergies)):
        curr_strat[i]=curr_strat[i]+1
        if curr_strat[i] > stratergies[i]:
            curr_strat[i]=1
        else:
            break

# Generated utilities till now
# print utils
# print possibleStratergies

A_mat=[]
b=[]
lb=[0 for p in possibleStratergies]
ub=[1 for p in possibleStratergies]
Aeq=[1 for p in possibleStratergies]
beq=[1]
f=[0 for p in possibleStratergies]

for s in possibleStratergies:
        s_index=possibleStratergies.index(s)
        for i in range(0,noOfPlayers):
              f[s_index] = f[s_index]+utils[i][s]
        f[s_index]=f[s_index]*-1

for i in range(0,noOfPlayers):
        for s_i in range(0,stratergies[i]):
                curr_strat = s_i+1
                for s_dash_i in range(0,stratergies[i]):
                        A_row=[0 for p in possibleStratergies]
                        curr_dash_strat = s_dash_i+1
                        if s_i != s_dash_i:
                                #Generating s_minus_i

                                for s_minus_i in [p for p in possibleStratergies if p[i]==curr_strat]:
                                        s=s_minus_i[:i]+tuple([curr_strat])+s_minus_i[i+1:]
                                        s_dash=s_minus_i[:i]+tuple([curr_dash_strat])+s_minus_i[i+1:]
                                        A_row[possibleStratergies.index(s)] = (utils[i][s] - utils[i][s_dash])*-1 # reversing the constraint
                                A_mat.append(A_row)
                                b.append(0)
# print A_mat
# print f
# print Aeq
# print beq
# print lb
# print ub
# print b

f=matlab.double(f)
A_mat=matlab.double(A_mat)
Aeq=matlab.double(Aeq)
b=matlab.double(b)
beq=matlab.double(beq)
ub=matlab.double(ub)
lb=matlab.double(lb)
t = eng.linprog(f,A_mat,b,Aeq,beq,lb,ub)
# print t
# print '\n'
for i in range(len(t)):
    print "strategy ",
    print  possibleStratergies[i],
    print '=',
    print t[i]



# use linprog(f,A,b,Aeq,beq,lb,ub) and print the equilibrium
### Convert to eng data types first using eng.double
