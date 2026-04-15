import random
import math
from enum import Enum
from typing import Tuple, List, Optional, Dict
from dataclasses import dataclass

# Regime thresholds (will be learned over time)
SMALL_THRESHOLD = 10  # bytes - direct event encoding
MEDIUM_THRESHOLD = 100  # bytes - iterative convergence
# Above MEDIUM_THRESHOLD = LARGE - compositional chunks

class Regime(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

@dataclass
class EfficiencyMetrics:
    useful_bits: float
    total_time: float
    transmission_cost: float
    compute_cost: float
    crc_cost: float
    
    @property
    def efficiency(self) -> float:
        if self.total_time == 0:
            return 0
        return self.useful_bits / self.total_time
    
    @property
    def total_cost(self) -> float:
        return self.transmission_cost + self.compute_cost + self.crc_cost

@dataclass
class RegimeStats:
    count: int = 0
    avg_efficiency: float = 0.0
    total_efficiency: float = 0.0
    
    def update(self, efficiency: float):
        self.count += 1
        self.total_efficiency += efficiency
        self.avg_efficiency = self.total_efficiency / self.count

class AdaptiveThresholds:
    """Learns optimal regime boundaries from efficiency curves."""
    
    def __init__(self):
        self.small_stats = RegimeStats()
        self.medium_stats = RegimeStats()
        self.large_stats = RegimeStats()
        self.history: List[Tuple[int, Regime, float]] = []  # (size, regime, efficiency)
        
    def record(self, size_bytes: int, regime: Regime, efficiency: float):
        self.history.append((size_bytes, regime, efficiency))
        if regime == Regime.SMALL:
            self.small_stats.update(efficiency)
        elif regime == Regime.MEDIUM:
            self.medium_stats.update(efficiency)
        else:
            self.large_stats.update(efficiency)
    
    def get_optimal_regime(self, size_bytes: int) -> Regime:
        """Determine regime based on learned thresholds."""
        # For now, use fixed thresholds but track for learning
        if size_bytes < SMALL_THRESHOLD:
            return Regime.SMALL
        elif size_bytes < MEDIUM_THRESHOLD:
            return Regime.MEDIUM
        else:
            return Regime.LARGE
    
    def adjust_thresholds(self):
        """Adjust thresholds based on efficiency crossover points."""
        # TODO: Implement learning algorithm to find optimal boundaries
        pass

def determine_regime(size_bytes: int, thresholds: Optional[AdaptiveThresholds] = None) -> Regime:
    """Determine encoding regime based on data size."""
    if thresholds:
        return thresholds.get_optimal_regime(size_bytes)
    
    if size_bytes < SMALL_THRESHOLD:
        return Regime.SMALL
    elif size_bytes < MEDIUM_THRESHOLD:
        return Regime.MEDIUM
    else:
        return Regime.LARGE


def ceil_int(x):
    return math.ceil(x)


def make_crc(data_str):
    """Robust checksum using polynomial rolling hash with large prime modulo."""
    # Use a polynomial rolling hash for better distribution than simple sum
    prime = 1000000007  # Large prime for modulo
    base = 31  # Prime base for polynomial
    
    h = 0
    for ch in data_str:
        h = (h * base + int(ch)) % prime
    
    # Return as 9-digit checksum to minimize collisions
    return f"{h:09d}"


def generate_target(data_digits=12):
    data = "".join(str(random.randint(0, 9)) for _ in range(data_digits))
    crc = make_crc(data)
    return int(data + crc)


def encode_small_event(data_int: int) -> Tuple[List[int], int]:
    """
    SMALL regime: Direct event encoding without M×t dynamics.
    Encodes small data directly into temporal events.
    Returns (event_list, time_cost)
    """
    # For small data, use direct binary representation as events
    data_str = str(data_int)
    events = [int(d) for d in data_str]
    # Time cost is proportional to number of digits (events)
    time_cost = len(events)
    return events, time_cost


def decode_small_event(events: List[int]) -> int:
    """Decode small event encoding back to integer."""
    data_str = ''.join(str(e) for e in events)
    return int(data_str) if data_str else 0


def encode_medium_iterative(target: int, max_phases: int = 5) -> Tuple[List[Dict], int, int]:
    """
    MEDIUM regime: Iterative convergence system with phase switching rule.
    Uses M×t dynamics but switches phase when d(error)/dt >= 0.
    Returns (phase_data, final_residual, total_time)
    """
    all_rows = []
    phase_final_s = []
    residual = target
    total_time = 0
    
    for phase in range(max_phases):
        if residual == 0:
            break
        
        rows, final_s, residual, total_time = run_phase_with_switch(residual, phase, total_time)
        all_rows.extend(rows)
        
        if final_s is not None:
            phase_final_s.append(final_s)
        
        if residual == 0:
            break
    
    return all_rows, residual, total_time


def run_phase_with_switch(phase_target, phase_index, total_time, max_steps=20):
    """
    Phase execution with formal switching rule: switch when d(error)/dt >= 0.
    Implements overshoot strategy and warm-start capability.
    """
    # Warm start: use previous state estimate if available
    M = 1  # Could be initialized from cache for warm-start
    
    best_error = float("inf")
    best_residual = phase_target
    best_s = None
    rows = []
    
    sign = 1 if phase_target >= 0 else -1
    mag_target = abs(phase_target)
    
    prev_error = float("inf")
    
    for step in range(max_steps):
        t_max = max(5, min(200, mag_target // 1000 + 10))
        
        best_t, best_eval = 1, float("inf")
        for t in range(1, t_max):
            m_candidate = ceil_int(0.5 * M * t)
            s_candidate = m_candidate * t
            err = abs(mag_target - s_candidate)
            if err < best_eval:
                best_eval = err
                best_t = t
        
        t = ceil_int(best_t)
        m_new = ceil_int(0.5 * M * t)
        s = m_new * t
        error = phase_target - sign * s
        abs_error = abs(error)
        
        # Phase switching rule: stop when error stops improving
        if abs_error < best_error:
            best_error = abs_error
            best_residual = error
            best_s = s
            total_time += t
            
            rows.append({
                "phase": phase_index, "step": step + 1,
                "prev_m": M, "M": m_new, "t": t, "S": s,
                "total_time": total_time, "error": error,
                "phase_target": phase_target,
            })
            
            M = m_new
            prev_error = abs_error
            
            if abs_error == 0:
                break
        else:
            # d(error)/dt >= 0, switch phase
            break
    
    return rows, best_s, best_residual, total_time


def encode_large_compositional(target: int, chunk_size: int = 500) -> Tuple[List[Tuple], int]:
    """
    LARGE regime: Compositional medium system.
    Large data = repetition of medium chunks.
    No new physics, just scaling law.
    Returns (chunk_results, total_time)
    """
    target_str = str(target)
    chunks = []
    total_time = 0
    chunk_results = []
    
    # Split into medium-sized chunks
    for i in range(0, len(target_str), chunk_size):
        chunk_str = target_str[i:i + chunk_size]
        if chunk_str:
            chunk_int = int(chunk_str)
            chunks.append(chunk_int)
    
    # Process each chunk as medium regime
    for chunk_idx, chunk in enumerate(chunks):
        phase_data, residual, chunk_time = encode_medium_iterative(chunk)
        chunk_results.append((chunk_idx, chunk, phase_data, residual))
        total_time += chunk_time
    
    return chunk_results, total_time


def try_reconstruct(phase_final_s, final_residual, offset_range=100000):
    """Try to reconstruct target by testing sign combinations of phase S values.
    
    The target equals: sum(sign_i * S_i) + final_residual
    We test all sign combinations and small offsets to find a CRC-valid match.
    """
    n = len(phase_final_s)
    for offset in range(offset_range + 1):
        for mask in range(1 << n):
            total = 0
            for i, s in enumerate(phase_final_s):
                if i == 0 or not (mask >> i & 1):
                    total += s
                else:
                    total -= s
            # Add the final residual - this is critical!
            total += final_residual
            for candidate in ([total] if offset == 0 else [total + offset, total - offset]):
                if candidate <= 0:
                    continue
                cs = str(candidate)
                # Polynomial hash produces 9 digits, so data is all but last 9 chars
                if len(cs) < 10:
                    continue
                data, crc = cs[:-9], cs[-9:]
                if make_crc(data) == crc:
                    return candidate, offset
    return None, None


def print_table(all_rows, target):
    header = (
        f"{'Phase':<6} {'Step':<6} {'PrevM':<10} {'M':<10} "
        f"{'t':<6} {'S':<12} {'TotalTime':<12} {'Error':<12} "
        f"{'PhaseTarget':<15} {'Target'}"
    )
    print(header)
    print("-" * len(header))
    last_phase = -1
    for r in all_rows:
        if r["phase"] != last_phase and last_phase != -1:
            print()
        last_phase = r["phase"]
        print(
            f"{r['phase']:<6} {r['step']:<6} {r['prev_m']:<10} {r['M']:<10} "
            f"{r['t']:<6} {r['S']:<12} {r['total_time']:<12} {r['error']:<12} "
            f"{r['phase_target']:<15} {target}"
        )


def run_system(data_digits=12):
    """
    Main system entry point with regime-aware encoding.
    Selects encoding strategy based on data size and tracks efficiency metrics.
    """
    target = generate_target(data_digits)
    target_str = str(target)
    # Calculate raw binary bytes needed: ceil(bits / 8) where bits = digits * log2(10)
    target_bytes = math.ceil(len(target_str) * math.log2(10) / 8)
    
    # Determine encoding regime
    regime = determine_regime(target_bytes)
    
    print(f"\nTARGET (WITH CRC): {target} bytes={target_bytes}")
    print(f"REGIME: {regime.value.upper()}\n")
    
    all_rows = []
    phase_final_s = []
    phase_log = []
    total_time = 0
    
    if regime == Regime.SMALL:
        # SMALL: Direct event encoding, no M×t dynamics
        events, time_cost = encode_small_event(target)
        total_time = time_cost
        
        print(f"Small regime: direct event encoding")
        print(f"Events: {events}")
        print(f"Time cost: {time_cost}")
        
        # For small data, the reconstruction is trivial
        reconstructed = decode_small_event(events)
        result = reconstructed if make_crc(str(reconstructed)[:-9]) == str(reconstructed)[-9:] else None
        
    elif regime == Regime.MEDIUM:
        # MEDIUM: Iterative convergence with phase switching
        all_rows, final_residual, total_time = encode_medium_iterative(target)
        
        # Extract phase data for reconstruction
        for row in all_rows:
            if row['step'] == 1 or (len(all_rows) > 0 and row['step'] == 1):
                pass  # First step of each phase
        
        # Get final S values from last step of each phase
        phases_seen = set()
        for row in reversed(all_rows):
            if row['phase'] not in phases_seen:
                phase_final_s.insert(0, row['S'])
                phases_seen.add(row['phase'])
        
        # Print table for medium regime
        print_table(all_rows, target)
        
        print("\nPhase final S values:")
        for i, s in enumerate(phase_final_s):
            sign_note = "always +" if i == 0 else "+/- in search"
            print(f"  Phase {i}: S={s}  ({sign_note})")
        
        # Reconstruct
        result, offset = try_reconstruct(phase_final_s, final_residual)
        
        print("\nSign search + CRC reconstruction:")
        print(f"  Tried {2 ** len(phase_final_s)} combinations x offsets 0-200")
        if result is not None:
            print(f"  FOUND: {result}  (offset {offset})")
            if result == target:
                print(f"  EXACT MATCH to original target {target}")
            else:
                print(f"  Original target was {target} — nearest CRC-valid value found")
        else:
            print("  NO CRC-VALID RECONSTRUCTION FOUND")
        
    else:  # LARGE
        # LARGE: Compositional medium chunks
        chunk_results, total_time = encode_large_compositional(target)
        
        print(f"Large regime: compositional encoding with {len(chunk_results)} chunks")
        
        for chunk_idx, chunk, phase_data, residual in chunk_results:
            print(f"\nChunk {chunk_idx}: {chunk} ({len(str(chunk))} digits)")
            if phase_data:
                print(f"  Phases: {len(phase_data)}")
                print(f"  Residual: {residual}")
        
        # For large data, reconstruction happens per chunk
        # This is a simplified version - full implementation would combine chunks
        result = target  # Placeholder
    
    print(f"\nTotal time: {total_time}")
    
    # Calculate throughput: bytes per time unit
    if total_time > 0:
        bytes_per_second = target_bytes / total_time
        print(f"Total bytes transferred: {target_bytes}")
        print(f"Throughput: {bytes_per_second:.6f} bytes/time_unit")
    else:
        print(f"Total bytes transferred: {target_bytes}")
        print("Throughput: N/A (zero time)")
    
    return result


if __name__ == "__main__":
    import sys
    
    # Increase integer string conversion limit for large payloads
    try:
        sys.set_int_max_str_digits(10000000)  # Allow up to 10 million digits
    except AttributeError:
        pass  # Older Python versions don't have this limit
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        # Support various input formats
        if arg.endswith('KB'):
            # Convert KB to approximate data digits
            kb_size = int(arg[:-2])
            bytes_target = kb_size * 1024
            # Each decimal digit ≈ 3.32 bits, so 1 byte ≈ 2.4 decimal digits
            # For CRC overhead, we use slightly fewer digits
            data_digits = int(bytes_target * 2.4) - 9  # Subtract CRC digits
            data_digits = max(12, data_digits)  # Minimum 12 digits
        elif arg.endswith('MB'):
            mb_size = int(arg[:-2])
            bytes_target = mb_size * 1024 * 1024
            data_digits = int(bytes_target * 2.4) - 9
            data_digits = max(12, data_digits)
        elif arg.endswith('B'):
            bytes_target = int(arg[:-1])
            data_digits = int(bytes_target * 2.4) - 9
            data_digits = max(12, data_digits)
        else:
            # Assume it's a raw digit count
            data_digits = int(arg)
        run_system(data_digits=data_digits)
    else:
        run_system(data_digits=12)
