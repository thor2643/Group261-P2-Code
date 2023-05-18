import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

Variabler = np.array([["timestamp", "timestamp", "timestamp","timestamp","timestamp","timestamp"],
["target_q_0", "target_q_1", "target_q_2", "target_q_3", "target_q_4", "target_q_5"],
["actual_q_0", "actual_q_1", "actual_q_2", "actual_q_3", "actual_q_4", "actual_q_5"],
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



data1 = pd.read_csv('C:\\Users\\bebj2\\Downloads\\Test2.csv')
data2 = pd.read_csv('C:\\Users\\bebj2\\OneDrive\\Skrivebord\\test3.csv')
data3 = pd.read_csv('C:\\Users\\bebj2\\Downloads\\Test2.csv')

def Tester(data):
    plt.rcParams["figure.figsize"] = [12,8]
    plt.subplot(14,6,1)
    plt.plot(data[Variabler[0,0]], data[Variabler[1,1]], label=Variabler[1,1])
    plt.xlabel('Kælling')
    plt.ylabel('Value')
    plt.legend()



    plt.show()

#Tester(data2)


def Tester2(data, tid, indgang, label, værdi):
    plt.rcParams["figure.figsize"] = [12, 8]

    for i in range(13):
        for j in range(6):
            plt.subplot(14, 6, i * 6 + j + 1)
            plt.plot(data[tid], data[indgang[i, j]], label=indgang[i, j])
            plt.xlabel(label)
            plt.ylabel(værdi)
            plt.legend()

    plt.show()

Tester2(data2, Variabler[0, 0], Variabler[1:], 'Kælling', 'Value')




print(Variabler[0,0])
