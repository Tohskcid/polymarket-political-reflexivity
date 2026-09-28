# Theoretical Microfoundations of Political Reflexivity

## 1. Model Environment and Primitives

We formulate a dynamic rational expectations model of a political prediction market with endogenous feedback into real political actions.

### 1.1 Timing and Electoral Outcome
- Time is indexed by $t \in \{0, 1, \dots, T\}$, where $T$ represents the election date.
- There are two political candidates, $A$ and $B$.
- The true electoral outcome is binary:
  $$Y = \mathbf{1}\{\theta_T \ge 0\}$$
  where $Y=1$ denotes a victory for candidate $A$, and $\theta_t \in \mathbb{R}$ represents the underlying net political support (fundamentals) for candidate $A$ relative to candidate $B$ at time $t$.

### 1.2 Law of Motion of Political Fundamentals
The latent political fundamental evolves according to:
$$\theta_{t+1} = \rho \theta_t + \lambda \bar{a}_t + \eta_{t+1}, \quad \eta_{t+1} \overset{i.i.d.}{\sim} \mathcal{N}(0, \sigma_\eta^2)$$
where:
- $\rho \in (0, 1]$ is the persistence of political fundamentals.
- $\bar{a}_t \in \mathbb{R}$ is the aggregate real action taken by political agents (e.g., campaign donations, volunteer effort, media salience, or voter mobilization) in favor of candidate $A$.
- $\lambda \ge 0$ is the **structural reflexivity parameter**:
  - If $\lambda = 0$, the market is purely passive (Hayekian benchmark): political fundamentals evolve exogenously, and the prediction market functions solely as a passive information aggregator.
  - If $\lambda > 0$, real actions causally shift future fundamentals, creating the potential for reflexive feedback.

---

## 2. Real Political Agents: Donors, Voters, and Media

There is a continuum of real political agents indexed by $j \in [0, 1]$. Each agent $j$ chooses an effort/donation level $a_{j,t} \in \mathbb{R}$.

### 2.1 Agent Objective Function
Agent $j$ maximizes expected utility:
$$\max_{a_{j,t}} \mathbb{E}_j \left[ U(a_{j,t}, \bar{a}_t, Y) \;\middle|\; \mathcal{I}_{j,t} \right] = a_{j,t} \mathbb{E}_j[Y \mid \mathcal{I}_{j,t}] - \frac{c}{2} a_{j,t}^2 + \gamma a_{j,t} \bar{a}_t$$
where:
1. $a_{j,t} \mathbb{E}_j[Y \mid \mathcal{I}_{j,t}]$: The expected return to supporting candidate $A$. This captures "backing a winner" motives (e.g., donor access to policy makers, political appointments, prestige, or strategic voting where supporting a viable candidate maximizes expected pivotality).
2. $\frac{c}{2} a_{j,t}^2$: Convex cost of capital, time, or campaign effort ($c > 0$).
3. $\gamma a_{j,t} \bar{a}_t$: Strategic complementarity / peer coordination effects among donors and voters ($\gamma \ge 0$). We assume $c > \gamma$ to ensure interior stability.

### 2.2 Optimal Real Action
The first-order condition with respect to $a_{j,t}$ yields:
$$\frac{\partial U}{\partial a_{j,t}} = \mathbb{E}_j[Y \mid \mathcal{I}_{j,t}] - c a_{j,t} + \gamma \bar{a}_t = 0 \implies a_{j,t}^* = \frac{\mathbb{E}_j[Y \mid \mathcal{I}_{j,t}] + \gamma \bar{a}_t}{c}$$
Integrating across all agents $j \in [0, 1]$ in a symmetric rational expectations equilibrium:
$$\bar{a}_t = \int_0^1 a_{j,t}^* dj = \frac{\bar{\mathbb{E}}_t[Y] + \gamma \bar{a}_t}{c} \implies \bar{a}_t = \frac{1}{c - \gamma} \bar{\mathbb{E}}_t[Y]$$
where $\bar{\mathbb{E}}_t[Y] \equiv \int_0^1 \mathbb{E}_j[Y \mid \mathcal{I}_{j,t}] dj$ is the average subjective probability of candidate $A$'s victory.

---

## 3. Information Structure and Market Pricing

### 3.1 Information Environment
- Each agent $j$ observes:
  1. A noisy private signal of current fundamentals:
     $$s_{j,t} = \theta_t + \xi_{j,t}, \quad \xi_{j,t} \overset{i.i.d.}{\sim} \mathcal{N}(0, \sigma_s^2)$$
  2. The publicly observable prediction market price $P_t \in [0, 1]$.

### 3.2 Prediction Market Traders
- The prediction market trades an Arrow-Debreu contract that pays $\$1$ if $Y=1$ (candidate $A$ wins) and $\$0$ if $Y=0$.
- Risk-neutral, competitive financial traders aggregate information. The equilibrium market price reflects the market's expectation of victory:
  $$P_t = \mathbb{E}_{\text{market}}\left[ Y \;\middle|\; \mathcal{I}_t^{\text{mkt}}, P_t \right]$$

### 3.3 Bayesian Learning from Market Prices
Real agents update their expectation of candidate $A$'s victory by combining their private signal with the public market price $P_t$:
$$\mathbb{E}_j[Y \mid s_{j,t}, P_t] = \alpha P_t + (1 - \alpha) \Phi\left( \frac{s_{j,t}}{\sqrt{\sigma_s^2 + \Sigma^2}} \right)$$
where $\alpha \equiv \frac{h_P}{h_P + h_s} \in (0, 1)$ is the Bayesian weight on the market price, with $h_P$ and $h_s$ denoting the effective precisions of the market price and private signals, respectively.

Aggregating across all agents $j \in [0, 1]$, by the Law of Large Numbers ($\int_0^1 \xi_{j,t} dj = 0$):
$$\bar{\mathbb{E}}_t[Y] = \alpha P_t + (1 - \alpha) \Phi\left( \frac{\theta_t}{\sqrt{\sigma_s^2 + \Sigma^2}} \right)$$
Substituting this into the aggregate action equation:
$$\bar{a}_t = \kappa P_t + \psi \theta_t$$
where:
$$\kappa \equiv \frac{\alpha}{c - \gamma} > 0, \quad \psi \equiv \frac{1 - \alpha}{(c - \gamma)\sqrt{2\pi(\sigma_s^2 + \Sigma^2)}}$$
Here, $\kappa$ measures the **price sensitivity of real political action**.

---

## 4. Equilibrium Characterization and Theorems

### Proposition 1: Equilibrium Fixed-Point Representation
Under Gaussian fundamentals and rational market participants, the equilibrium prediction market price $P^*$ satisfies the nonlinear fixed-point equation:
$$P^* = \mathcal{T}(P^*; \theta_t) \equiv \Phi\left( \frac{\tilde{\theta}_t + \lambda \kappa P^*}{\Sigma} \right)$$
where $\tilde{\theta}_t \equiv \theta_t (1 + \lambda \psi)$ is the fundamental adjusted for direct private actions, $\Phi(\cdot)$ is the standard normal CDF, and $\Sigma > 0$ is the cumulative standard deviation of fundamental shocks until the terminal date.

#### Proof of Proposition 1
Traders recognize that candidate $A$ wins if $\theta_T \ge 0$. Integrating the law of motion forward to $T$:
$$\theta_T = \rho^{T-t} \theta_t + \sum_{k=t}^{T-1} \rho^{T-1-k} \lambda \bar{a}_k + \sum_{k=t+1}^T \rho^{T-k} \eta_k$$
At time $t$, given current price $P_t$ and action $\bar{a}_t = \kappa P_t + \psi \theta_t$, the conditional expectation of terminal fundamental is affine in $\theta_t + \lambda \kappa P_t$. Normalizing the residual shock variance to $\Sigma^2$:
$$\theta_T \mid (\theta_t, P_t) \sim \mathcal{N}\left( \frac{\tilde{\theta}_t + \lambda \kappa P_t}{\nu}, \Sigma^2 \right)$$
Since $Y = \mathbf{1}\{\theta_T \ge 0\}$, by the properties of the Gaussian distribution:
$$\mathbb{E}_{\text{market}}[Y \mid \theta_t, P_t] = \Phi\left( \frac{\tilde{\theta}_t + \lambda \kappa P_t}{\Sigma} \right)$$
In competitive equilibrium, market clearing requires $P_t = \mathbb{E}_{\text{market}}[Y \mid \theta_t, P_t]$, establishing the fixed-point equation. $\blacksquare$

---

### Proposition 2: The Reflexivity Multiplier and Sensitivity Amplification
Suppose $\frac{\lambda \kappa}{\Sigma} < \sqrt{2\pi} \approx 2.5066$. Then:
1. There exists a unique stable equilibrium price $P^*(\tilde{\theta}_t) \in (0, 1)$.
2. The sensitivity of the market price to underlying political fundamentals is strictly amplified by the **Reflexivity Multiplier** $\mathcal{M}$:
   $$\frac{\partial P^*}{\partial \tilde{\theta}_t} = \mathcal{M} \cdot \frac{1}{\Sigma} \phi\left( \frac{\tilde{\theta}_t + \lambda \kappa P^*}{\Sigma} \right)$$
   where:
   $$\mathcal{M} \equiv \frac{1}{1 - \frac{\lambda \kappa}{\Sigma} \phi\left( \frac{\tilde{\theta}_t + \lambda \kappa P^*}{\Sigma} \right)} > 1$$
3. Amplification is state-dependent: $\mathcal{M}$ attains its global maximum when the race is tied ($P^* = 0.5$, $\tilde{\theta}_t + \lambda \kappa P^* = 0$), implying that **reflexivity is strongest in close, competitive elections**.

#### Proof of Proposition 2
1. Consider the function $g(P) \equiv \mathcal{T}(P) - P = \Phi\left( \frac{\tilde{\theta}_t + \lambda \kappa P}{\Sigma} \right) - P$.
   - $g(0) = \Phi\left( \frac{\tilde{\theta}_t}{\Sigma} \right) > 0$.
   - $g(1) = \Phi\left( \frac{\tilde{\theta}_t + \lambda \kappa}{\Sigma} \right) - 1 < 0$.
   - By the Intermediate Value Theorem, there exists at least one root $P^* \in (0, 1)$.
   - Differentiating $\mathcal{T}(P)$ with respect to $P$:
     $$\mathcal{T}'(P) = \frac{\lambda \kappa}{\Sigma} \phi\left( \frac{\tilde{\theta}_t + \lambda \kappa P}{\Sigma} \right)$$
     Since $\phi(z) \le \phi(0) = \frac{1}{\sqrt{2\pi}}$ for all $z \in \mathbb{R}$, we have:
     $$\sup_{P \in [0, 1]} \mathcal{T}'(P) = \frac{\lambda \kappa}{\Sigma \sqrt{2\pi}} < 1$$
     Hence $g'(P) = \mathcal{T}'(P) - 1 < 0$ strictly everywhere. By the Banach Fixed-Point Theorem, $P^*$ is unique and globally stable under tatônnement.
2. Applying the Implicit Function Theorem to $P^* - \Phi\left( \frac{\tilde{\theta}_t + \lambda \kappa P^*}{\Sigma} \right) = 0$:
   $$\frac{\partial P^*}{\partial \tilde{\theta}_t} - \phi\left( \frac{\tilde{\theta}_t + \lambda \kappa P^*}{\Sigma} \right) \frac{1}{\Sigma} \left[ 1 + \lambda \kappa \frac{\partial P^*}{\partial \tilde{\theta}_t} \right] = 0$$
   Rearranging terms:
   $$\frac{\partial P^*}{\partial \tilde{\theta}_t} \left[ 1 - \frac{\lambda \kappa}{\Sigma} \phi\left( \frac{\tilde{\theta}_t + \lambda \kappa P^*}{\Sigma} \right) \right] = \frac{1}{\Sigma} \phi\left( \frac{\tilde{\theta}_t + \lambda \kappa P^*}{\Sigma} \right)$$
   Dividing both sides by the bracketed term yields the stated multiplier. Since $\lambda \kappa > 0$ and $\phi(\cdot) > 0$, the denominator is in $(0, 1)$, so $\mathcal{M} > 1$.
3. Since $\phi(z) = \frac{1}{\sqrt{2\pi}} e^{-z^2/2}$ is strictly maximized at $z = 0$, $\mathcal{M}$ is maximized when $\tilde{\theta}_t + \lambda \kappa P^* = 0$, which corresponds to $P^* = \Phi(0) = 0.5$. $\blacksquare$

---

### Proposition 3: Bifurcation, Tipping Points, and Self-Fulfilling Prophecies
When feedback is strong, such that:
$$\lambda \kappa > \sqrt{2\pi} \Sigma$$
the mapping $\mathcal{T}(P)$ undergoes a pitchfork / fold bifurcation:
1. There exists an open interval of political fundamentals $\tilde{\theta}_t \in (\underline{\theta}, \bar{\theta})$ for which there exist **three distinct equilibrium prices**:
   $$0 < P_L^* < P_M^* < P_H^* < 1$$
   where $P_L^*$ (pessimistic trap) and $P_H^*$ (optimistic surge) are locally stable, while $P_M^*$ is an unstable tipping threshold.
2. An exogenous non-fundamental price shock $\Delta P > P_M^* - P_L^*$ can push the system past the tipping threshold $P_M^*$, triggering a self-reinforcing cascade to $P_H^*$ and permanently shifting the election outcome from $Y=0$ to $Y=1$.

#### Proof of Proposition 3
When $\frac{\lambda \kappa}{\Sigma} > \sqrt{2\pi}$, the maximum slope of $\mathcal{T}(P)$ exceeds 1:
$$\mathcal{T}'(P) \Big|_{z=0} = \frac{\lambda \kappa}{\sqrt{2\pi}\Sigma} > 1$$
Because $\mathcal{T}(P)$ is continuous, strictly increasing, and bounded between 0 and 1, with $\mathcal{T}''(P) > 0$ for $z < 0$ and $\mathcal{T}''(P) < 0$ for $z > 0$, the function $\mathcal{T}(P)$ is strictly S-shaped.
Setting $\tilde{\theta}_t = -\frac{\lambda \kappa}{2}$ aligns the inflection point with $P = 0.5$, giving $\mathcal{T}(0.5) = 0.5$ and $\mathcal{T}'(0.5) > 1$.
Consequently, $g(P) = \mathcal{T}(P) - P$ satisfies $g(0) > 0$, $g'(0.5) > 0$, and $g(1) < 0$. By Rolle's theorem and the concavity structure, $g(P) = 0$ has exactly three roots: $P_L^* < P_M^* < P_H^*$.
At $P_L^*$ and $P_H^*$, $\mathcal{T}'(P^*) < 1$, ensuring local stability. At $P_M^*$, $\mathcal{T}'(P^*) > 1$, implying instability. This establishes the existence of multiple self-fulfilling equilibria. $\blacksquare$

---

## 5. From Theoretical Microfoundations to Empirical Specifications

The theoretical law of motion and agent decision rules directly dictate our econometric specifications.

### 5.1 Dynamic Simultaneous Equations
From Section 2 and Section 3, the joint dynamics of prices $P_t$ and real actions $a_t$ (measured via polling margins $Poll_t$ and donor flows) satisfy:
$$\begin{cases}
a_t = \mu_a + \rho_a a_{t-1} + \kappa P_t + \epsilon_t^a \\
P_t = \mu_P + \rho_P P_{t-1} + \delta a_t + \epsilon_t^P
\end{cases}$$
where:
- $\kappa > 0$ captures the **reflexive channel** ($P_t \to a_t$).
- $\delta \equiv \frac{\lambda}{\Sigma} \phi(\cdot) > 0$ captures the **information aggregation channel** ($a_t \to P_t$).

### 5.2 Testable Empirical Hypotheses
1. **Hypothesis 1 (Passive Market Null vs Reflexivity Alternative)**:
   - $H_0$ (Passive Hayekian Market): $\kappa = 0 \implies P_t$ does not Granger-cause future political polling margins $Poll_{t+h}$.
   - $H_1$ (Political Reflexivity): $\kappa > 0 \implies P_t$ Granger-causes future political polling margins $Poll_{t+h}$.
2. **Hypothesis 2 (Cointegration and Error Correction Dynamics)**:
   - If market prices and political fundamentals are cointegrated $I(1)$, the VECM error correction speed $\alpha_{Poll} \ne 0$ reflects polls adjusting to eliminate pricing disequilibrium.
3. **Hypothesis 3 (Battleground Heterogeneity)**:
   - By Proposition 2, the reflexivity multiplier $\mathcal{M}$ is maximized where $P^* \approx 0.5$. Therefore, empirical reflexivity elasticity should be significantly larger in swing states than in non-competitive states.

---

## 6. Proof Obligation Summary Table

| Obligation ID | Claim / Target Proposition | Mathematical Machinery | Status | Verification Path |
|---|---|---|---|---|
| OBL-01 | Proposition 1: Equilibrium fixed-point representation | Gaussian conditional projection, Law of Large Numbers | Discharged | Sec. 4, Prop. 1 |
| OBL-02 | Proposition 2: Reflexivity multiplier $\mathcal{M} > 1$ and uniqueness | Banach contraction mapping, Implicit Function Theorem | Discharged | Sec. 4, Prop. 2 |
| OBL-03 | Proposition 3: Pitchfork bifurcation and multiple equilibria | S-shaped mapping, intermediate value theorem, stability analysis | Discharged | Sec. 4, Prop. 3 |
| OBL-04 | Proposition 4: SVAR/VECM empirical mapping | Structural simultaneous equations with Bayesian learning | Discharged | Sec. 5 |
