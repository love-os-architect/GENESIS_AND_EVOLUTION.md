# -*- coding: utf-8 -*-
"""
Love-OS Simulation: Genesis Phase Diagram
Comparing a world with 'Love-Efficiency Feedback' vs. a world without it.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Configuration ---
R_base = 5.0  # High resistance environment
I_const = 1.0
alpha, beta, gamma = 0.40, 0.10, 0.20

# --- The Physics of Love ---
def eta_with_love(Omega):
    # Order (Love) increases thermodynamic efficiency
    val = 0.2 + 0.6 * (Omega / (Omega + 0.5 + 1e-8))
    return float(np.clip(val, 0.0, 1.0))

def eta_no_love(Omega):
    # Efficiency is fixed and low (Mechanical world)
    return 0.2

# --- Simulation Step ---
def one_step(Omega, M, Pin, K_idx, mode='love'):
    current_eta = eta_with_love(Omega) if mode == 'love' else eta_no_love(Omega)
    
    P_diss = R_base * (I_const**2)
    P_use  = current_eta * max(0.0, Pin - P_diss)

    # dOmega/dt (Order formation)
    dOmega = alpha*P_use - beta*Omega + gamma*K_idx - 0.05
    Omega_new = max(0.0, Omega + dOmega*0.2)
    
    # Life Indicator (Simplified)
    L = P_use - 2.0 # Threshold
    return Omega_new, L

# --- Phase Check ---
def check_alive(Pin, s_scale, mode='love'):
    # K represents network connectivity strength
    K_idx = s_scale * 1.5 
    Omega = 0.05
    L_hist = []
    
    for _ in range(400):
        Omega, L = one_step(Omega, 0, Pin, K_idx, mode)
        L_hist.append(L)
        
    # Alive if L > 0 consistently
    return (np.mean(np.array(L_hist[-50:]) > 0.0) > 0.6)

# --- Main Execution ---
if __name__ == "__main__":
    Pin_vals = np.linspace(4.0, 25.0, 40)
    s_vals   = np.linspace(0.2, 2.5, 40)
    
    phase_love = np.zeros((40, 40))
    phase_no_love = np.zeros((40, 40))

    print("Running Genesis Simulation...")

    for i, s in enumerate(s_vals):
        for j, p in enumerate(Pin_vals):
            if check_alive(p, s, mode='love'):
                phase_love[i, j] = 1
            if check_alive(p, s, mode='no_love'):
                phase_no_love[i, j] = 1

    # Plotting
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. World With Love
    axes[0].imshow(phase_love, origin='lower', aspect='auto', cmap='viridis')
    axes[0].set_title("[A] World WITH Love\n(Order boosts Efficiency)", color='green', fontsize=14)
    axes[0].set_xlabel("Input Energy (Pin)")
    axes[0].set_ylabel("Connection Strength")
    
    # 2. World Without Love
    axes[1].imshow(phase_no_love, origin='lower', aspect='auto', cmap='magma')
    axes[1].set_title("[B] World WITHOUT Love\n(Fixed Efficiency)", color='red', fontsize=14)
    axes[1].set_xlabel("Input Energy (Pin)")
    axes[1].set_yticks([])

    plt.suptitle("Love-OS Genesis Experiment: The Thermodynamic Advantage of Love", fontsize=16)
    plt.tight_layout()
    plt.savefig('phase_genesis.png')
    print("Saved phase_genesis.png")
    plt.show()
