import pandas as pd
import matplotlib.pyplot as plt
import numpy as np





data1 = pd.read_csv('C:\\Users\\bebj2\\Downloads\\Test2.csv')
data2 = pd.read_csv('C:\\Users\\bebj2\\OneDrive\\Skrivebord\\test3.csv')
data3 = pd.read_csv('C:\\Users\\bebj2\\Downloads\\Test2.csv')

def Tester(data):
    plt.rcParams["figure.figsize2"] = [12,8]
    plt.subplot(2,3,1)
    plt.plot(data['timestamp'], data['actual_robot_current'], label='actual_robot_current')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.legend()


    plt.subplot(2,3,2)
    plt.plot(data['timestamp'], data['actual_robot_current'], label='actual_robot_current')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.legend()

    plt.subplot(2,3,3)
    plt.plot(data['timestamp'], data['actual_robot_current'], label='actual_robot_current')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.legend()

    plt.subplot(2,3,4)
    plt.plot(data['timestamp'], data['actual_robot_current'], label='actual_robot_current')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.legend()

    plt.subplot(2,3,5)
    plt.plot(data['timestamp'], data['actual_robot_current'], label='actual_robot_current')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.legend()

    plt.subplot(2,3,6)
    plt.plot(data['timestamp'], data['actual_robot_current'], label='actual_robot_current')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.legend()




    plt.show()

Tester(data2)



Variabler = np.array([["timestamp", "Timestamp_Realtime", 0,0,0,0],
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
["actual_main_voltage", "actual_robot_voltage", "actual_robot_current",0,0,0],
["output_bit_registers0_to_31", "output_bit_registers32_to_63",0,0,0,0]])

print(Variabler[0,0])
