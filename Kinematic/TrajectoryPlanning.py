import sympy as sp
import math
import matplotlib.pyplot as plt
import numpy as np

class TrajectoryPlanner:
    """
    Contains all the relevant functions regarding trajectory generation
    """
    
    def get2PointMoveLFunction(self, pose1, pose2, vel=100, acc=10, tf=0, functionType = "default", start_vel = 0, end_vel = 0):
        """
        Take two poses (numpy array type) and returns and appropriate function and time interval for decribing the position at time t.
        Depending on what values (vel, acc, or tf) are given the function is created using either
        cubic polynomial (functionType="cb") or parabolic blend (functionType="pb") .
        """

        #Make sure the two poses are numpy arrays
        pose1 =  pose1 if isinstance(pose1, np.ndarray) else (np.array(pose1) if isinstance(pose1, list) else np.array([pose1]))
        pose2 =  pose2 if isinstance(pose2, np.ndarray) else (np.array(pose2) if isinstance(pose2, list) else np.array([pose2]))

        if (vel != 0 and acc != 0 and tf != 0):
            raise Exception("One variable must be kept free")
        
        if (vel != 0 and acc != 0):
            #Use parabolic blend
            pass

        elif (tf != 0):
            if functionType.lower() == "pb" or functionType.lower() == "default":
                #Check if acceleration value is valid or set acceleration
                if acc != 0:
                    assert np.all((acc > abs((4*(pose2-pose1)/tf**2)))), f"Acceleration must be higher than {np.max(abs(4*(pose2-pose1)/tf**2))}"
                else:
                    acc = np.max(abs(4*(pose2-pose1)/tf**2))


                #Calculate necessary velocity to stay within the time limit (if possible) and 
                # thereafter use parbolic blend 
                tb = (tf/2)-(np.sqrt(acc**2*tf**2-4*acc*(abs(pose2-pose1)))/(2*acc))

                #Make sure tb is a numpy array to comply with the for-loop in "moveL"
                tb =  tb if isinstance(tb, np.ndarray) else np.array([tb])
                acc = [(acc if 0 <= (pose2[i]-pose1[i]) else -acc) for i in range(tb.size)]
                #print(acc)
                pos_b = pose1+(1/2)*tb**2*acc 

                def moveL(t):
                    vec_out = []
                    for i in range(tb.size):   
                        if t<=abs(tb[i]):
                            vec_out.append(pose1[i]+(1/2)*acc[i]*t**2)
                        elif t>abs(tb[i]) and t<(tf-abs(tb[i])):
                            vec_out.append(pos_b[i]+acc[i]*tb[i]*(t-tb[i]))
                        elif t>=(tf-abs(tb[i])) and t<=tf:
                            vec_out.append(pose2[i]-(1/2)*acc[i]*(tf-t)**2)
                        else:
                            print("You entered a number outside the scope of this function")
                        
                    return vec_out
            
            elif functionType.lower() == "cb":
                a1 = pose1
                a2 = start_vel
                a3 = (3/pow(tf, 2))*(pose2-pose1)-(2/tf)*start_vel-(1/tf)*end_vel
                a4 = (-2/pow(tf,3))*(pose2-pose1)+(1/(pow(tf,2)))*(end_vel+start_vel)
                def moveL(t):
                    return a1+a2*t+a3*(pow(t,2))+a4*(pow(t,3))
                

        elif (vel != 0):
            if functionType.lower() == "cb" or functionType.lower() == "default":
                #Calculate necessary time to keep get the specified average velocity 
                # thereafter use cubic polynomial 
                tf = (math.sqrt((pose2[0]-pose1[0])**2+(pose2[1]-pose1[1])**2+(pose2[2]-pose1[2])**2))/vel

                def moveL(t):
                    a2 = (3/tf**2)*(pose2-pose1)-(2/tf)*start_vel-(1/tf)*end_vel
                    a3 = (-2/tf**3)*(pose2-pose1)+(1/(tf**2))*(end_vel+start_vel)

                    return pose1+start_vel*t+a2*(t**2)+a3*(t**3)
                
            elif functionType.lower() == "linear":
                d_pose = pose2[0:3]-pose1[0:3]
                d_pose_norm = np.linalg.norm(d_pose)

                tf = d_pose_norm/vel
                vel_vector = (d_pose/d_pose_norm)*vel

                def moveL(t):
                    return pose1[0:3]+vel_vector*t




        
        return [moveL, 0, tf]


    def getViaPointsMoveLFunction(self, points, move_info = []):   #avg_speeds = 0, times = 0, via_speeds = 0, point_info = []):
        """
        Takes a list of points, speeds, and timestep at each point and returns a function describing the trajectory
        """
        functions = []
        time_intervals = [0]
        time_sum = 0

        #Create standard formatted list from point_info
        #info = [avg_vel, acc, tf, funcType, v0, vf]
        info = []
        
        for vals in move_info:
            if vals[0] == "linear":                                 #vals = [func, avg_vel]
                info.append([vals[1], 0, 0, vals[0], 0, 0])
            elif vals[0] == "cb" or vals[0] == "default":           #vals = [func, tf, v0, vf]
                if len(vals) == 4:
                    info.append([0, 0, vals[1], vals[0], vals[2], vals[3]])
                elif
    
        print(info)
        for idx in range(len(points)-1):
            func, _, tf = self.get2PointMoveLFunction(  points[idx], 
                                                        points[idx+1], 
                                                        vel=info[idx][0], 
                                                        acc=info[idx][1], 
                                                        tf=info[idx][2], 
                                                        functionType = info[idx][3], 
                                                        start_vel = info[idx][4], 
                                                        end_vel = info[idx][5])
            functions.append(func)
            time_sum += tf
            time_intervals.append(time_sum)
            

        def MoveLWithVia(t):
            for idx in range(len(time_intervals)):
                if  time_intervals[idx] <= t <= time_intervals[idx+1]: #times[idx] <= t <= times[idx+1]:
                    return functions[idx]((t-time_intervals[idx]))[0:3]
        
        
                
        return [MoveLWithVia, 0, time_sum]


    def plot2DTrajectory(self, function, t0, t1, plotAll = False):
        """
        Takes a trajectory function and visualises each entrance in 2D in the interval [t0,t1].
        Note that it only plots the position (or the first 3 entrances returned by the function).
        This is done to avoid chrashes when plotting the function with viapoints, where orientation
        and position can occur and thereby returning arrays of different sizes. 
        If the return shape is consistent plotAll can be set true to plot graphs for both position and orientation.
        Mu
        """
        x = np.linspace(t0, t1, 200)
        if plotAll:
            y = [function(num) for num in x]
        else:
            y = [function(num)[0:3] for num in x]

        fig, ax = plt.subplots()
        ax.plot(x, y)

        ax.set_xlabel("Time")
        ax.set_ylabel("Position")
        ax.legend()
        plt.show()

    def plot3DTrajectory(self, function, t0, t1):
        """
        Takes a trajectory function and visualises the parametric curve in 3D in the interval [t0,t1]
        """
         
        ax = plt.figure().add_subplot(projection='3d')
        t_steps = np.linspace(t0, t1, 200)

        x, y, z = np.transpose([function(t)[0:3] for t in t_steps])

        ax.plot(x, y, z, label='parametric curve')
        ax.legend()

        plt.show()



