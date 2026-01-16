# -*- coding: utf-8 -*-
"""
Love-OS Simulation: Evolution of Love
Simulating how 'Love' (Integration) naturally evolves to minimize Resistance (R).
"""

import numpy as np
import matplotlib.pyplot as plt

def simulate_evolution(generations=300, pop_size=200):
    # Population trait A (Love) initialized randomly [0, 1]
    A = np.random.rand(pop_size)
    
    hist_A = []
    hist_R = []
    hist_Fit = []
    
    print("Running Evolution Simulation...")
    
    for gen in range(generations):
        # 1. Physics: Love reduces Resistance (R)
        # Individuals with high Love have low Resistance.
        R = 10.0 + 10.0 * (1.0 - A) 
        
        # 2. Fitness Calculation
        # Efficiency = How much energy they can process (Pin - R)
        Efficiency = np.maximum(0, 20.0 - R)
        
        # Synergy = Benefit from interacting with the group average
        Synergy = 2.0 * A * np.mean(A)
        
        # Cost = Energy cost to maintain complex 'Love' circuitry
        Cost = 0.5 * A
        
        Fitness = 1.0 + Efficiency + Synergy - Cost
        Fitness = np.maximum(Fitness, 0.001) # Avoid negative fitness
        
        # 3. Selection (Survival of the fittest)
        probs = Fitness / np.sum(Fitness)
        next_indices = np.random.choice(pop_size, size=pop_size, p=probs)
        
        # 4. Mutation
        A_next = A[next_indices] + np.random.normal(0, 0.02, pop_size)
        A = np.clip(A_next, 0.0, 1.0)
        
        # Record stats
        hist_A.append(np.mean(A))
        hist_R.append(np.mean(R))
        hist_Fit.append(np.mean(Fitness))

    # Plotting
    fig, ax = plt.subplots(3, 1, figsize=(8, 10), sharex=True)
    
    ax[0].plot(hist_A, color='blue', linewidth=2)
    ax[0].set_ylabel('Mean Love (A)')
    ax[0].set_title('Evolutionary Trajectory over 300 Generations')
    ax[0].grid(True, alpha=0.3)
    
    ax[1].plot(hist_R, color='green', linewidth=2)
    ax[1].set_ylabel('Mean Resistance (R)')
    ax[1].grid(True, alpha=0.3)
    
    ax[2].plot(hist_Fit, color='red', linewidth=2)
    ax[2].set_ylabel('Mean Fitness')
    ax[2].set_xlabel('Generations')
    ax[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plot_evolution.png')
    print("Saved plot_evolution.png")
    plt.show()

if __name__ == "__main__":
    simulate_evolution()
