import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

VariablerGammel = np.array([["timestamp", "timestamp", "timestamp","timestamp","timestamp","timestamp"],
["target_q_0", "target_q_1", "target_q_2", "target_q_3", "target_q_4", "target_q_5"], #target pos
["actual_q_0", "actual_q_1", "actual_q_2", "actual_q_3", "actual_q_4", "actual_q_5"], #Actualo pos
["target_qd_0", "target_qd_1", "target_qd_2", "target_qd_3", "target_qd_4", "target_qd_5"],
["actual_qd_0", "actual_qd_1", "actual_qd_2", "actual_qd_3", "actual_qd_4", "actual_qd_5"],
["target_qdd_0", "target_qdd_1", "target_qdd_2", "target_qdd_3", "target_qdd_4", "target_qdd_5"],
["target_current_0", "target_current_1", "target_current_2", "target_current_3", "target_current_4", "target_current_5"],
["actual_current_0", "actual_current_1", "actual_current_2", "actual_current_3", "actual_current_4", "actual_current_5"],
["actual_current_window_0", "actual_current_window_1", "actual_current_window_2", "actual_current_window_3", "actual_current_window_4", "actual_current_window_5"],
["target_moment_0", "target_moment_1", "target_moment_2", "target_moment_3", "target_moment_4", "target_moment_5"],
["target_TCP_pose_0", "target_TCP_pose_1", "target_TCP_pose_2", "target_TCP_pose_3", "target_TCP_pose_4", "target_TCP_pose_5"],
["actual_TCP_pose_0", "actual_TCP_pose_1", "actual_TCP_pose_2", "actual_TCP_pose_3", "actual_TCP_pose_4", "actual_TCP_pose_5"],
["actual_main_voltage", "actual_robot_voltage", "actual_robot_current","timestamp","timestamp","timestamp"],
["output_bit_registers0_to_31", "output_bit_registers32_to_63","timestamp","timestamp","timestamp","timestamp"]])


Variabler = np.array([["timestamp", "timestamp", "timestamp", "timestamp", "timestamp", "timestamp"],
["target_q_0", "target_q_1", "target_q_2", "target_q_3", "target_q_4", "target_q_5"],
["actual_q_0", "actual_q_1", "actual_q_2", "actual_q_3", "actual_q_4", "actual_q_5"],
["target_qdd_0", "target_qdd_1", "target_qdd_2", "target_qdd_3", "target_qdd_4", "target_qdd_5"],
["actual_robot_current", "tool_output_current", "timestamp", "timestamp", "timestamp", "timestamp"]])









#data2 = pd.read_csv('C:\\Users\\bebj2\\OneDrive\\Skrivebord\\test3.csv')
data2 = pd.read_csv('C:\\Users\\bebj2\\Downloads\\3Runs.csv')

#EkstraVAR=VariablerGammel[12,2]
"""
VariablerTilPlot = np.array([["timestamp", "timestamp", "timestamp"],
["target_q_0", "target_q_1", "target_q_2"],
["target_q_3", "target_q_4", "target_q_5"],
["actual_q_0", "actual_q_1", "actual_q_2"],
["actual_q_3", "actual_q_4", "actual_q_5"]])
"""


#VariablerTilPlotGammel = np.array([["timestamp", "timestamp", "timestamp","timestamp","timestamp","timestamp"],
#["target_q_0", "target_q_1", "target_q_2", "target_q_3", "target_q_4", "target_q_5"], #target pos
#["actual_q_0", "actual_q_1", "actual_q_2", "actual_q_3", "actual_q_4", "actual_q_5"]]) #Actualo pos
#["target_qd_0", "target_qd_1", "target_qd_2", "target_qd_3", "target_qd_4", "target_qd_5"],
#["actual_qd_0", "actual_qd_1", "actual_qd_2", "actual_qd_3", "actual_qd_4", "actual_qd_5"],
#["target_qdd_0", "target_qdd_1", "target_qdd_2", "target_qdd_3", "target_qdd_4", "target_qdd_5"],
#["target_current_0", "target_current_1", "target_current_2", "target_current_3", "target_current_4", "target_current_5"],
#["actual_current_0", "actual_current_1", "actual_current_2", "actual_current_3", "actual_current_4", "actual_current_5"],
#["actual_current_window_0", "actual_current_window_1", "actual_current_window_2", "actual_current_window_3", "actual_current_window_4", "actual_current_window_5"],
#["target_moment_0", "target_moment_1", "target_moment_2", "target_moment_3", "target_moment_4", "target_moment_5"],
#["target_TCP_pose_0", "target_TCP_pose_1", "target_TCP_pose_2", "target_TCP_pose_3", "target_TCP_pose_4", "target_TCP_pose_5"],
#["actual_TCP_pose_0", "actual_TCP_pose_1", "actual_TCP_pose_2", "actual_TCP_pose_3", "actual_TCP_pose_4", "actual_TCP_pose_5"],
#["actual_main_voltage", "actual_robot_voltage", "actual_robot_current","timestamp","timestamp","timestamp"],
#["output_bit_registers0_to_31", "output_bit_registers32_to_63","timestamp","timestamp","timestamp","timestamp"]])

VariablerTilPlot = np.array([["timestamp", "timestamp", "timestamp", "timestamp", "timestamp", "timestamp"],
["actual_q_0", "actual_q_1", "actual_q_2", "actual_q_3", "actual_q_4", "actual_q_5"]])
#["actual_robot_current", "tool_output_current", "timestamp", "timestamp", "timestamp", "timestamp"]])








EkstraVAR = np.array(["actual_robot_current", "tool_output_current"])
EkstraVAR = np.array(["actual_q_0", "actual_q_1", "actual_q_2", "actual_q_3", "actual_q_4", "actual_q_5", "actual_robot_current"])


#18 sekunders målinger
HZ = 10
TidsVar = HZ*HZ
Tid1 = 21447.328
Tid1 = data2["timestamp"]
#print(Tid1[0])
lengthTid = len(Tid1)
Tid2=Tid1[lengthTid-1]
#print(Tid2)
TidTotal = Tid2-Tid1[0]
print(TidTotal)


numrows = len(VariablerTilPlot)    # 3 rows in your example
numcols = len(VariablerTilPlot[0]) # 2 columns in your example
#print(numrows)
#print(numcols)


def Tester22(data, tid, indgang, label, værdi):
    plt.rcParams["figure.figsize"] = [12, 8]

    for i in range(numrows-1):
        for j in range(numcols):
            plt.subplot(numrows, numcols, i * 6 + j + 1)
            plt.plot(data[tid], data[indgang[i, j]], label=indgang[i, j])
            plt.xlabel(label)
            plt.ylabel(værdi)
            plt.legend()

    plt.show()

#Tester2(data2, VariablerTilPlot[0, 0], VariablerTilPlot[1:], 'Kælling', 'Value')



holdeVariabel = 0

def Tester2(data, tid, indgang, indgangStor, label, værdi):
    plt.rcParams["figure.figsize"] = [12, 8]

    for i in range(numrows-1):
        for j in range(numcols):
            plt.subplot(numrows, numcols, i * numcols + j + 1)
            plt.plot(data[tid], data[indgang[i, j]], label=indgang[i, j])
            plt.xlabel(label[i,j])
            plt.ylabel(værdi)
            plt.legend()
            Holdevariabel = i*numcols+j

    print(Holdevariabel)

    plt.subplot(numrows,numcols,holdeVariabel+1)
    plt.plot(data[tid], data[indgangStor], label=indgangStor)
    plt.legend()

    plt.show()

#Tester2(data2, VariablerTilPlot[0, 0], VariablerTilPlot[1:], EkstraVAR, VariablerTilPlot[1:], 'Value')



def Tester3(data, tid, indgang, indgangStor, label, værdi):
    plt.rcParams["figure.figsize"] = [12, 8]

    for i in range(numrows-1):
        for j in range(numcols):
            plt.subplot(numrows+1, numcols, i * numcols + j + 1)
            plt.plot(data[tid], data[indgang[i, j]], label=indgang[i, j])
            plt.xlabel(label[i,j])
            plt.ylabel(værdi)


            plt.subplot(numrows+1,numcols,i * numcols + j + 1)
            plt.plot(data[tid], data[indgangStor], label=indgangStor)



            Holdevariabel = i*numcols+j

    print(Holdevariabel)

    plt.show()
#Tester3(data2, VariablerTilPlot[0, 0], VariablerTilPlot[1:], EkstraVAR, VariablerTilPlot[1:], 'Value')







def Tester4(data, tid, indgang, indgangStor, label, værdi):
    plt.rcParams["figure.figsize"] = [12, 8]

    for i in range(numrows-1):
        for j in range(numcols):
            plt.subplot(numrows+1, numcols, i * numcols + j + 1)
            plt.plot(data[tid]-Tid1[0], data[indgang[i, j]])#, label=indgang[i, j])
            plt.xlabel(indgang[i, j]) #Var label før
            plt.ylabel(værdi)
            #plt.legend()
            Holdevariabel = i*numcols+j

    print(Holdevariabel)

    plt.subplot(numrows+1,numcols,Holdevariabel+2)
    plt.plot(data[tid]-Tid1[0], data[indgangStor[0]])#, label=indgangStor[0])
    plt.xlabel(indgangStor[0])
    #plt.legend()

    plt.subplot(numrows+1,numcols,Holdevariabel+3)
    plt.plot(data[tid]-Tid1[0], data[indgangStor[1]])#, label=indgangStor[1])
    plt.xlabel(indgangStor[1])
    #plt.legend()




    plt.show()

#Tester4(data2, VariablerTilPlot[0, 0], VariablerTilPlot[1:], EkstraVAR, 'Time seconds', 'Value')




colorList = ['#2eac66', '#7ebc57', '#b3cd41', '#dfdd19', '#ffed00', '#ff0000','#7300ff', '#b40000', '#890000', '#540000', '#240000']


def Tester5(data, tid, indgangStor):
    fig, ax1 = plt.subplots(figsize=(16, 10))
    ax2 = ax1.twinx()






    for i in range(len(indgangStor)-1):
        ax1.plot(data[tid]-Tid1[0], data[indgangStor[i]], color=colorList[i], lw=1)
        plt.xlabel('seconds')
        ax1.legend(data[indgangStor[i]])
        print(indgangStor[i])


    ax2.plot(data[tid]-Tid1[0], data[indgangStor[len(indgangStor)-1]], color=colorList[6], lw=1)



    plt.show()

Tester5(data2, VariablerTilPlot[0, 0], EkstraVAR)





df = pd.DataFrame(data2[EkstraVAR])
snit = df.mean(0)
talHolder = df.sum(0)
antalTalHolder = df.count(0)

def TeethExtractor():
    print(talHolder[6], antalTalHolder[6], snit[6], talHolder[6]/antalTalHolder[6] )
    print(snit[6]*TidTotal)


#TeethExtractor()
        













