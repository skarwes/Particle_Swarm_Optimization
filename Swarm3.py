from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import math

particle_data = []

#schwefel_function implementation
def schwefel_function(X):
    return 418.9829 * len(X) - np.sum(X * np.sin(np.sqrt(np.abs(X))))
#Banana function implementation
def banana(X):
    a = 1
    b = 100
    x = X[0]
    y = X[1]
    return (a - x)**2 + b * (y - x**2)**2


class Particles:
    def __init__(self,x0):
        self.position_i = [] #particle position
        self.velocity_i = [] #particle velocity
        self.best_pos_i = [] #best individual position
        self.best_err_i = -1 #best error for individual
        self.err_i = -1      #individual error

        #Initialize the particle
        for i in range(0,num_dimensions):
            self.velocity_i.append(random.uniform(-1,1))
            self.position_i.append(x0[i])
        self.best_pos_i = list(self.position_i)

    #Fittnes function for particle
    def curr_fitnes(self, costfunc):
        self.err_i = costfunc(self.position_i)

        if self.err_i < self.best_err_i or self.best_err_i == 1:
            self.best_pos_i = self.position_i
            self.best_err_i = self.err_i

    #Velocity function for the particle
    def velocity_update(self, best_pos_g, iter):
        w_max = 0.9
        w_min = 0.4
        #Dynamic inertia weight early iters has a larger value and promotes exploration globally
        #Later iters has a smaller value and promotes local refinement of the position
        w=w = w_max - (w_max - w_min) * (iter / 200) 
        
        
        #cognative constant at 1.5 strikes a balance between own position and global postion #C1 influences how much the particle cares about its own pos
        c1=1.5      
        #social constant at 2 strikes a balance between own position and global postion #C2 influences how much the particle cares about the global best pos
        c2=2        

        for i in range(0,num_dimensions):
            r1=random.random()
            r2=random.random()

            vel_cognitive=c1*r1*(self.best_pos_i[i]-self.position_i[i])
            vel_social=c2*r2*(best_pos_g[i]-self.position_i[i])
            self.velocity_i[i]=w*self.velocity_i[i]+vel_cognitive+vel_social

    #particle position update based on velocity update
    def update_position(self,bounds):
        for i in range(0,num_dimensions):
            self.position_i[i]=self.position_i[i]+self.velocity_i[i]

            #adjust maximum position if necessary
            if self.position_i[i]>bounds[i][1]:
                self.position_i[i]=bounds[i][1]

            #adjust minimum position if neseccary
            if self.position_i[i] < bounds[i][0]:
                self.position_i[i]=bounds[i][0]
class PSO:
    def __init__(self,costFunc,x0,bounds,num_particles,maxiter):
        global num_dimensions
        num_dimensions=len(x0)
        #bet global err
        err_best_g=-1                   
        #best global pos
        pos_best_g=[]                   

        #make the swarm
        swarm=[]
        for i in range(0,num_particles):
            swarm.append(Particles(x0))

        #List to stores the best error at each iteration
        self.best_err_g_history = []

        #Main optimization loop
        self.positions_history = []  #List to store particle positions at each iteration
        i=0
        while i < maxiter:

            current_positions = [particle.position_i[:] for particle in swarm]
            self.positions_history.append(current_positions) 
            
            #print ("best_error_global ",i,err_best_g)
            #Fitnes evaluation for all particles in the swarm
            for j in range(0,num_particles):
                swarm[j].curr_fitnes(costFunc)
                #Chek if current particle is best globally
                if swarm[j].err_i < err_best_g or err_best_g == -1:
                    pos_best_g=list(swarm[j].position_i)
                    err_best_g=float(swarm[j].err_i)

            #Store the best error each iteration 
            self.best_err_g_history.append(err_best_g)

            #Goes throught the swarm and updates velocities and positions
            for j in range(0,num_particles):
                swarm[j].velocity_update(pos_best_g, i)
                swarm[j].update_position(bounds)
            i+=1
        print ('FINAL:')
        print (pos_best_g)
        print (err_best_g)
        



        #Plotting the best error over iterations
        plt.figure(figsize=(10, 6))
        plt.plot(self.best_err_g_history, marker='o', color='b')
        plt.title('Best Error (Fitness) Over Iterations')
        plt.xlabel('Iteration')
        plt.ylabel('Best Error')
        plt.grid(True)
        plt.show()

        positions_history = self.positions_history
        #Animation setup
        fig, ax = plt.subplots()
        ax.set_xlim(a,b)
        ax.set_ylim(a,b)
        scatter = ax.scatter([], [], s=10, color='blue')
        iteration_text = ax.text(-9, 9, "", fontsize=12, color='black')
        #Function to update the scatter plot at each frame
        def update(frame):
            current_positions = positions_history[frame]
            #Update the scatter positions
            scatter.set_offsets(current_positions) 
            #Update the iteration number
            iteration_text.set_text(f'Iteration: {frame + 1}')  
            return scatter,iteration_text

        #Create the animation
        ani = animation.FuncAnimation(fig, update, frames=len(positions_history), interval=200, blit=True)
        plt.title("Particle Swarm Optimization")

        FFMpegWriter = animation.writers['ffmpeg']
        metadata = dict(title="Particle Swarm optimization")
        writer = FFMpegWriter(fps=10, metadata=metadata)
        #to this you can add a file path to wich it saves the animations "ani.save(r"file path"), writer = writer"
        ani.save 

        plt.show()






func_to_optimize = banana #function to be optimized

#updates the plot windows based on function selected
if(func_to_optimize == banana):
    a = -10
    b = 10
   

if(func_to_optimize == schwefel_function):
    a = -1000
    b =  1000
    

#number of dimensions
d= 50 
#initial starting location
initial=[0,0]             
#input bounds
bounds=[(-500,500)]*d  
PSO(func_to_optimize,initial,bounds,num_particles=30,maxiter=200)


