# Time-Channel Architecture Improvements TODO

## Priority 1: Core Architecture Fixes

### 1. Regime-dependent encoding (CRITICAL)
- [ ] Implement three distinct regimes: SMALL, MEDIUM, LARGE
- [ ] SMALL: event/symbol encoding (no iteration)
- [ ] MEDIUM: iterative convergence system
- [ ] LARGE: compositional medium system (repetition of medium chunks)
- [ ] Remove size-based heuristics; use entropy + overhead dependent switching

### 2. Small data fix (CRITICAL)
- [ ] Small data should NOT use M×t dynamics
- [ ] Implement direct encoding into temporal events
- [ ] Add buffer layer to batch small messages into medium frames
- [ ] Eliminate small inefficiency via embedding

### 3. Adaptive packet sizing loop
- [ ] Measure efficiency: `useful_bits / total_time`
- [ ] Adjust chunk size dynamically based on efficiency curve
- [ ] Find optimal packet size: `S* = argmin(transmission_cost + compute_cost + CRC_cost)`

### 4. Machine-learned thresholding
- [ ] Make regime boundaries learned from efficiency curves
- [ ] Not fixed constants - adapt over time
- [ ] Track efficiency metrics per regime

## Priority 2: Optimization Strategies

### 5. Phase switching rule
- [ ] Implement formal switch condition: `switch when d(error)/dt ≥ 0`
- [ ] Replace current "stop improving" heuristic

### 6. Overshoot strategy
- [ ] Intentionally overshoot early phases
- [ ] Correct via later phases
- [ ] Enable fast divergence → controlled convergence

### 7. Warm-start M
- [ ] Initialize M₀ = previous_state_estimate
- [ ] Remove cold-start inefficiency
- [ ] Cache state between transmissions

### 8. Compression with stop condition
- [ ] Compress until: `marginal_gain < compute_cost + decoding_loss`
- [ ] Implement true "zip until optimal" rule

## Priority 3: Advanced Features

### 9. Predictive layer (AI model)
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
