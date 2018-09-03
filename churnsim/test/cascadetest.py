import threading
from threading import Thread
from churnsim.uk.ac.bristol.rechurn.modes.CloudFailures.DistributionBased.DiskFailures import weibullfailures
from churnsim.uk.ac.bristol.rechurn.modes.CloudFailures.DistributionBased.SoftwareFailures.software import SoftwareFailures
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':
    numberofnodes=[]
    t=0
    failurelist=[]
    times = [i for i in range(100, 1000, 50)]
    hardwarefails=[]
    softwarefails=[]
    for time in times:
        wb = weibullfailures(True, time/10)
        soft_failure = SoftwareFailures(time)
        testnodejson = nx.path_graph(300)

        hardwarefails.append(wb.get_new_topology(testnodejson))
        softwarefails.append(soft_failure.get_new_topology(testnodejson))

    print(hardwarefails)
    print(softwarefails)
    numberoffails=[]
    for i in range(len(hardwarefails)):
        numberoffails.append(hardwarefails[i]+softwarefails[i])
    print(numberoffails)
    sumtotal,sumhard,sumsoft=0,0,0

    for i in range(len(hardwarefails)):
        sumtotal+=numberoffails[i]
        sumhard+=hardwarefails[i]
        sumsoft+=softwarefails[i]
    averagetotal,averagehard,averagesoft=sumtotal/len(numberoffails),sumhard/len(hardwarefails),sumsoft/len(softwarefails)
    print(averagetotal,averagehard,averagesoft)
    perchard=(averagehard/averagetotal)*100
    percsoft=(averagesoft/averagetotal)*100
    print(perchard,percsoft)
    #plt.plot(times,hardwarefails)
    #plt.plot(times,softwarefails)
    #plt.plot(times,numberoffails)
    #plt.xlabel('times')
    #plt.ylabel('number of failures')
    #plt.savefig('Cascadehardwaresoftware.png')
    labels = 'Hardware Failures', 'Software Failures'
    sizes = [averagehard,averagesoft]
    colors = ['lightcoral', 'lightskyblue']

    # Plot
    plt.pie(sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.savefig('ratioofhsfails')


