# Research State: Political Reflexivity in Prediction Markets

## 1. Research Question and Scope
- **Core Research Question**: Do political prediction markets (specifically Polymarket) exhibit *political reflexivity*—where market prices actively alter real-world political fundamentals (voter preferences, campaign resources, media momentum) rather than merely passively aggregating dispersed information?
- **Mode**: Microeconomic Theory (Rational Expectations Equilibrium with Real Feedback) + Empirical Econometrics (SVAR, Toda-Yamamoto Granger Causality, VECM, Local Projections, and Swing State Panel FE).
- **Target Audience / Outlet**: Top Economics and Political Economy journals (Quarterly Journal of Economics, Journal of Political Economy, American Economic Review, Review of Economic Studies).
- **Deliverables**: 
  - Authoritative LaTeX manuscript: `paper/manuscript/main.tex`
  - Rendered PDF: `output/pdf/main.pdf`
  - Bibliography: `paper/references/references.bib`
  - Pipeline scripts: `scripts/acquire/`, `scripts/clean/`, `scripts/analyze/`
  - Publication-ready artifacts: `output/tables/`, `output/figures/`
  - Traceability manifest and audit logs: `research/`

## 2. Theoretical Primitives & Proof Obligations
- **Primitives**:
  - Binary electoral outcome $Y \in \{0, 1\}$ at election date $T$.
  - Latent political fundamental state $\theta_t \in \mathbb{R}$.
  - Real political agents (donors, strategic voters, media) choose actions $a_t \in \mathbb{R}$ based on expected victory $\mathbb{E}[Y | \mathcal{I}_t]$ and strategic complementarities $\gamma \ge 0$.
  - Reflexive fundamental evolution: $\theta_{t+1} = \rho \theta_t + \lambda a_t + \eta_{t+1}$, where $\lambda \ge 0$ measures the structural reflexivity parameter.
  - Prediction market traders price Arrow-Debreu contract $P_t = \mathbb{E}[Y | \mathcal{I}_t^{\text{mkt}}, P_t]$.
- **Mathematical Obligations**:
  - [x] Obligation 1: Establish existence and uniqueness of the Rational Expectations Equilibrium with feedback for $\lambda \kappa < \text{threshold}$.
  - [x] Obligation 2: Derive the closed-form Reflexivity Multiplier $\mathcal{M} = \frac{1}{1 - \lambda \kappa \phi(\cdot)/\Sigma} > 1$.
  - [x] Obligation 3: Prove the existence of pitchfork / saddle-node bifurcation (tipping points) and multiple self-fulfilling equilibria when $\lambda \kappa > \sqrt{2\pi}\Sigma$.
  - [x] Obligation 4: Derive the dynamic reduced-form SVAR and VECM representation directly from the microfounded law of motion.

## 3. Empirical Design & Identification Strategy
- **Estimands**:
  1. Bidirectional Granger causality parameters between Polymarket price $P_t$ and real political fundamentals (Polling margins $Poll_t$): Testing $H_0: P_t \not\to Poll_t$ (passive market hypothesis) against $H_1: P_t \to Poll_t$ (reflexivity hypothesis).
  2. Cointegration vector and error-correction speeds of adjustment ($\alpha_P$ vs $\alpha_{Poll}$) in a VECM framework.
  3. Local projection impulse response coefficients $\beta^{(h)}$ of cumulative polling response to high-frequency price shocks.
  4. Swing-state panel elasticity $\beta_{state}$ of polling margins with respect to state Polymarket odds.
- **Identification Threats & Defenses**:
  - *Simultaneity / Reverse Causality*: Identified via timing restrictions (daily high-frequency price precedence), Toda-Yamamoto MWALD procedure robust to arbitrary integration/cointegration, and exogenous whale trade shocks (e.g., October 2024 Fredi9999 / Théo order flow).
  - *Omitted Variables (Common News Shocks)*: Controlled for nationwide debate events, campaign milestones, macro indices, and state fixed effects in the panel specification.
  - *Non-stationarity*: Tested via ADF and KPSS tests; addressed via differencing, cointegration VECM, and lag-augmented VAR ($k + d_{max}$).

## 4. Stopping Rules & Autonomy Budget
- The project will run through the complete data acquisition, profiling, econometric modeling, LaTeX writing, PDF compilation, adversarial referee review, and GitHub push.
