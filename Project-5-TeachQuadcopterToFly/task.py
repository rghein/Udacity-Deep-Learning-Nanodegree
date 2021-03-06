import numpy as np
from physics_sim import PhysicsSim

class Task():
    """Task (environment) that defines the goal and provides feedback to the agent."""
    def __init__(self, init_pose = None, init_velocities = None, 
        init_angle_velocities = None, runtime = 5., target_pos = None):
        """Initialize a Task object.
        Params
        ======
            init_pose: initial position of the quadcopter in (x,y,z) dimensions and the Euler angles
            init_velocities: initial velocity of the quadcopter in (x,y,z) dimensions
            init_angle_velocities: initial radians/second for each of the three Euler angles
            runtime: time limit for each episode
            target_pos: target/goal (x,y,z) position for the agent
        """
        # Simulation
        self.sim = PhysicsSim(init_pose, init_velocities, init_angle_velocities, runtime) 
        self.action_repeat = 3

        self.state_size = self.action_repeat * 6
        self.action_low = 425
        self.action_high = 475
        self.action_size = 4
        
        # number of steps in episode:
        self.steps = 0 
        
        # current distance from target:
        self.distance = np.linalg.norm(self.target_pos - self.sim.pose[:3]) 

        # Goal
        self.target_pos = target_pos if target_pos is not None else np.array([0., 0., 10.]) 
         
    def get_reward(self):
        """Uses current pose of sim to return reward."""
        distance = np.linalg.norm(self.target_pos - self.sim.pose[:3])
        inverse_square_distance = 1 / ((distance + 1)**2)
        
        return inverse_square_distance / self.action_repeat
        
    def step(self, rotor_speeds):
        """Uses action to obtain next state, reward, done."""
        reward = 0.0
        self.steps += 1
        pose_all = []
        for i in range(self.action_repeat):
            
            # update the sim pose and velocities
            done = self.sim.next_timestep(rotor_speeds) 
            reward += self.get_reward()
            pose_all.append(self.sim.pose) 
               
        next_state = np.concatenate(pose_all)
        
        return next_state, reward, done

    def reset(self):
        """Reset the sim to start a new episode."""
        self.sim.reset()
        self.steps = 0
        self.distance = 0.0
        state = np.concatenate([self.sim.pose] * self.action_repeat) 
        return state
