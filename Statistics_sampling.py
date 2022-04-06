import numpy as np, matplotlib.pyplot as plt
from scipy import stats
from scipy import special

show = True
#95% interval
alpha = .95

# #  24hpf 0.7mm
HPF = '24hpf'; DIA = '0.7'
#S = [0,3,1]; Eggs = [43,45,45]; speed = ['2.12 m/s','2.12 m/s','2.12 m/s']  #ex 2.1
#S = [11,7]; Eggs = [46,44]; speed = ['1.06 m/s','1.06 m/s']  #ex 2.2
#S = [3,3,7]; Eggs = [45,43,47]; speed = ['0.529 m/s','0.529 m/s','0.529 m/s']  #ex 2.3
#S = [4,18,13]; Eggs = [133,90,135]; speed = ['2.12 m/s','1.06 m/s','0.529 m/s']  #ex 2.sum

#  24hpf 0.8mm
HPF = '24hpf'; DIA = '0.8'
#S = [19,26]; Eggs = [39,48]; speed = ['2.12 m/s','2.12 m/s']  #ex 1.1
#S = [38,28,37]; Eggs = [47,42,37]; speed = ['1.06 m/s','1.06 m/s','1.06 m/s']   #ex 1.2
#S = [36,37,40]; Eggs = [44,47,44]; speed = ['0.529 m/s','0.529 m/s','0.529 m/s']  #ex 1.3
#S = [45,103,113]; Eggs = [87,126,135]; speed = ['2.12 m/s','1.06 m/s','0.529 m/s'] #ex 1.sum
# #  48hpf 0.8mm
#HPF = '48hpf'; DIA = '0.8'
#S = [29,31,29]; Eggs = [43,44,43]; speed = ['2.12 m/s','2.12 m/s','2.12 m/s']   #ex 3.1
#S = [36,41,43]; Eggs = [45,44,45]; speed = ['1.06 m/s','1.06 m/s','1.06 m/s']    #ex 3.2
#S = [39,40,42]; Eggs = [44,43,45]; speed = ['0.529 m/s','0.529 m/s','0.529 m/s']  #ex 3.3
S = [89,120,121]; Eggs = [130,134,132]; speed = ['2.12 m/s','1.06 m/s','0.529 m/s']  #ex 3.sum



N = 10001 #data sampling depth
points = len(S)
# we determine the likelihood distributions for all observations under assumption of binomial distr. 


paths = np.zeros((N,points))
x = np.linspace(0, 1, num=N, endpoint=True)
for i in range(points):
    paths[:,i] = stats.binom.pmf(S[i], Eggs[i], x) * (Eggs[i]+1)
    #paths[:,i] = (stats.binom.cdf(S[i], Eggs[i], x-1/N) - stats.binom.cdf(S[i], Eggs[i], x))*N
    
    
    
    if show:
        plt.plot(x, paths[:,i], label = speed[i])

Means = np.dot(x,paths)/(N - 1)

int_paths = np.cumsum( paths,0)/N

int_index_list = []

for i in range(points):
    int_index_list.append([])

for i in range(points):
    # for every distr., 
    a = 0; b = 0;
    while a < N-1 and b < N-1:
        while int_paths[a,i] - int_paths[b,i] < alpha and a < N-1:
            a+=1
        int_index_list[i].append([b,a,(int_paths[a,i] - int_paths[b,i])/(a-b)])
        
        while int_paths[a,i] - int_paths[b,i] > alpha and b < N-1: 
            b+=1
        int_index_list[i].append([b,a,(int_paths[a,i] - int_paths[b,i])/(a-b)])
    
    
    
    #print(int_paths[b+a,i] - int_paths[b,i])
Certaincy_interval = []
for i in range(points):
    temp = np.array(int_index_list[i])
    
    Certaincy_interval.append(temp[np.argmax(temp[:,2]),0:2]/(N - 1)) 
    

if show:
    plt.xlabel('Estimator success rate')
    plt.ylabel('Chance of estimator being correct')
    plt.title('Likelihood distribution of estimated success rate of eggs ' + HPF + ' with diameter of ' + DIA + ' mm')
    plt.legend()
    plt.show()

            



    
    