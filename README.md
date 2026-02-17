# quantum metropolis monte carlo


For the pure Ising model, $H = \sum_{\langle i,j \rangle} Z_i Z_j - \sum_j h Z_j$, we can construct the thermal state based on metropolis (markov chain), where we randomly pick one site, flip the spin, and either reject or accept it based on the energy and temeparture depedent probability.

The probability of flipping $p(\Delta E) =1, \Delta \leq 0$ and $p(\Delta E) = e^{-\Delta E/T, \Delta \lt 0$

<img width="468" height="364" alt="1D_circuit" src="https://github.com/user-attachments/assets/f94b30d4-ce28-441c-ada9-771cc89ff76e" />
<img width="758" height="457" alt="2D_circuit" src="https://github.com/user-attachments/assets/6785cb79-c251-4ac4-a91e-0288791b75a2" />
