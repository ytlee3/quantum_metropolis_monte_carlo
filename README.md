# quantum metropolis monte carlo


For the pure Ising model,
$H = \sum_{\langle i,j \rangle} Z_i Z_j - \sum_j h Z_j$,
we can construct the thermal state using the Metropolis (Markov chain) algorithm, where we randomly pick one site, flip the spin, and either reject or accept it based on an energy- and temperature-dependent probability.
The flipping probability is
$p(\Delta E) = 1$ for $\Delta E \le 0$, and
$p(\Delta E) = e^{-\Delta E/T}$ for $\Delta E > 0$.

In general, for the classical Ising model, we use an ancilla qubit to check the energy difference between neighboring spins and use a controlled rotation gate to encode the flipping probability.

For 1D case, we have the circuit as follow
<img width="468" height="364" alt="1D_circuit" src="https://github.com/user-attachments/assets/f94b30d4-ce28-441c-ada9-771cc89ff76e" />
<img width="758" height="457" alt="2D_circuit" src="https://github.com/user-attachments/assets/6785cb79-c251-4ac4-a91e-0288791b75a2" />
