# 🧠 UNIFIED TIME-CHANNEL ARCHITECTURE - TODO LIST

## Priority: CRITICAL (Core Architecture)

### ✅ 1. Regime-dependent encoding (DONE)
- [x] Implement SMALL → event encoding
- [x] Implement MEDIUM → phased time dynamics  
- [x] Implement LARGE → repeated medium chunks
- [ ] **TODO**: Make regimes entropy + overhead dependent (not just size-based)
  - Add entropy calculation for data
  - Factor in CRC overhead per regime
  - Replace fixed thresholds with dynamic calculation

### ✅ 2. Optimal packet size is state-dependent (PARTIAL)
- [x] Basic framework with EfficiencyMetrics
- [ ] **TODO**: Implement S* = argmin(transmission_cost + compute_cost + CRC_cost)
  - Add cost function calculator
  - Track costs over time
  - Learn optimal packet sizes

### ✅ 3. Large data = structured repetition (DONE)
- [x] `encode_large_compositional()` splits into medium chunks
- [x] No new physics, just scaling law
- [ ] **TODO**: Optimize chunk boundaries based on efficiency

---

## Priority: HIGH (Performance Optimization)

### 4. Adaptive packet sizing loop
- [ ] **TODO**: Measure efficiency = useful_bits / total_time
- [ ] **TODO**: Adjust chunk size dynamically during transmission
- [ ] **TODO**: Track efficiency history per regime

### 5. Compute-for-time tradeoff
- [ ] **TODO**: Implement decoding during idle transmission time
- [ ] **TODO**: Amortize compute_cost over transmission delay
- [ ] **TODO**: Add latency budget parameter

### 6. Constraint-based decoding
- [ ] **TODO**: Transmit partial structure + constraints
- [ ] **TODO**: Receiver reconstructs via inference
- [ ] **TODO**: Define constraint language/format

### 7. Virtual channels = constraint partitioning
- [ ] **TODO**: Implement "channels" as structured hypothesis space
- [ ] **NOTE**: Not parallel capacity gain

### 8. Core tradeoff shift
- [ ] **TODO**: Minimize entropy sent vs maximize reconstruction feasibility
- [ ] **TODO**: Add feasibility metric

---

## Priority: MEDIUM (Algorithm Improvements)

### 9. Phase optimisation = global time minimisation
- [ ] **TODO**: Optimize total_time_to_converge (not per-step error)
- [ ] **TODO**: Add global cost function

### 10. Overshoot strategy
- [x] Partially implemented in phase logic
- [ ] **TODO**: Intentionally overshoot early phases
- [ ] **TODO**: Correct via later phases
- [ ] **TODO**: Implement fast divergence → controlled convergence

### 11. Signed decomposition model
- [x] Target = Σ ± S_i implemented
- [x] Cancellation-based correction working
- [ ] **TODO**: Optimize sign search algorithm

### 12. Warm-start M
- [ ] **TODO**: M₀ = previous_state_estimate
- [ ] **TODO**: Remove cold-start inefficiency
- [ ] **TODO**: Cache state between transmissions

### ✅ 13. Phase switching rule (DONE)
- [x] switch phase when d(error)/dt ≥ 0
- [x] Formal "stop improving" rule in `run_phase_with_switch()`

### 14. Time is the cost function
- [x] Objective = minimize total_time (secondary metrics tracked)
- [ ] **TODO**: Make everything else truly secondary (remove redundant optimizations)

---

## Priority: LOW (Advanced Features)

### 15. Temporal interleaving
- [ ] **TODO**: Multiple streams share time structure
- [ ] **TODO**: interleave(chunk_A, chunk_B)
- [ ] **TODO**: Create pseudo-parallelism

### 16. Sweet spot phenomenon
- [ ] **TODO**: Find phase efficiency peak between overhead dominance and refinement collapse
- [ ] **TODO**: Characterize medium regime sweet spot

### 17. Different algebras per regime
- [x] SMALL: event/symbol encoding, no iteration
- [x] MEDIUM: iterative convergence system
- [x] LARGE: compositional medium system
- [ ] **TODO**: Optimize each algebra independently

### 18. Hierarchical CRC design
- [ ] **TODO**: small → embedded validation
- [ ] **TODO**: medium → per-chunk CRC
- [ ] **TODO**: large → structural CRC only
- [ ] **NOTE**: CRC is not uniform across regimes

### 19. Large is pure composition
- [x] large = repetition(medium)
- [x] No new mechanism required

### 20. Machine-learned thresholding
- [x] AdaptiveThresholds class created
- [ ] **TODO**: regime boundaries = learned from efficiency curves
- [ ] **TODO**: Not fixed constants
- [ ] **TODO**: Implement adjust_thresholds() method

---

## Priority: FUTURE (Research/Experimental)

### 21. Small data fix
- [x] Small data does NOT use M×t dynamics
- [x] Direct encoding into temporal events
- [ ] **TODO**: Optional batching into medium frames

### 22. Small → Medium embedding (buffer layer)
- [ ] **TODO**: small messages → buffer → medium frame
- [ ] **TODO**: Eliminate small inefficiency via batching

### 23. Compression with stop condition
- [ ] **TODO**: compress until marginal_gain < compute_cost + decoding_loss
- [ ] **TODO**: True "zip until optimal" rule

### 24. Predictive layer (AI model)
- [ ] **TODO**: Predict incoming small messages
- [ ] **TODO**: Pre-fill buffer
- [ ] **TODO**: Send deltas when wrong
- [ ] **TODO**: prediction → transmission → correction cycle
- [ ] **NOTE**: Reduces latency

---

## Next Steps (Immediate Action Items)

1. **Implement entropy-based regime selection** (replace size-only thresholds)
2. **Add cost function optimization** (transmission + compute + CRC)
3. **Complete hierarchical CRC** (different validation per regime)
4. **Implement learning algorithm** for threshold adjustment
5. **Add warm-start capability** (cache M₀ between runs)
6. **Optimize sign search** (currently brute force)
7. **Create formal simulation** with measurable phase transition points

---

## Testing Requirements

- [ ] Test regime boundaries with varying entropy data
- [ ] Measure efficiency curves for different packet sizes
- [ ] Validate CRC collision rates per regime
- [ ] Benchmark warm-start vs cold-start performance
- [ ] Test overshoot strategy convergence speed
- [ ] Verify large data chunking efficiency

---

## Documentation Needed

- [ ] Mathematical proofs for regime transitions
- [ ] Efficiency curve visualizations
- [ ] Cost function derivations
- [ ] API documentation for new classes
- [ ] Performance benchmarks vs baseline

---

**Last Updated**: Current session
**Status**: Core architecture implemented, optimization phase beginning
- [ ] Predict incoming small messages
- [ ] Pre-fill buffer
- [ ] Send deltas when prediction wrong
- [ ] Reduce latency via prediction → transmission → correction

### 10. Hierarchical CRC design
- [ ] SMALL: embedded validation
- [ ] MEDIUM: per-chunk CRC
- [ ] LARGE: structural CRC only
- [ ] CRC is not uniform across regimes

### 11. Constraint-based decoding
- [ ] Transmit partial structure + constraints
- [ ] Receiver reconstructs via inference
- [ ] Message = constraints + temporal structure

### 12. Temporal interleaving
- [ ] Multiple streams share time structure
- [ ] Interleave(chunk_A, chunk_B)
- [ ] Create pseudo-parallelism

## Priority 4: Measurement & Validation

### 13. Formal simulation
- [ ] Measurable phase transition points between regimes
- [ ] Testable system with measurable outcomes
- [ ] Efficiency curves per regime

### 14. Cost function optimization
- [ ] Objective: minimize total_time
- [ ] Track: transmission_time + compute_time + prediction_error_cost + CRC_overhead
- [ ] Everything secondary to time minimization

---

## Implementation Order

1. ✅ Create this TODO file
2. ✅ Implement regime detection (SMALL/MEDIUM/LARGE)
3. ✅ Fix small data handling (direct encoding + buffer)
4. ✅ Add adaptive packet sizing framework
5. ✅ Implement proper phase switching rule (d(error)/dt >= 0)
6. ⏳ Add warm-start capability (framework in place)
7. ⏳ Implement hierarchical CRC
8. ⏳ Add efficiency tracking and learning
9. ⏳ Build predictive buffer layer
10. ⏳ Create formal benchmarking suite

---

## Current State Analysis

The existing `datachannel.py` has:
- ✅ Basic M×t dynamics
- ✅ Phase-based decomposition
- ✅ CRC validation
- ✅ Sign combination search
- ✅ Offset reconstruction

Missing:
- ❌ Regime-dependent behavior
- ❌ Small data optimization
- ❌ Adaptive sizing
- ❌ Learning/thresholding
- ❌ Predictive capabilities
- ❌ Hierarchical validation
- ❌ Efficiency tracking
