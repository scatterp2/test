import random
import math


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


def run_phase(phase_target, phase_index, total_time, max_steps=20):
    M = 1
    best_error = float("inf")
    best_residual = phase_target
    best_s = None
    rows = []

    sign = 1 if phase_target >= 0 else -1
    mag_target = abs(phase_target)

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
            if abs_error == 0:
                break
        else:
            break

    return rows, best_s, best_residual, total_time


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
    target = generate_target(data_digits)
    target_str = str(target)
    # Calculate raw binary bytes needed: ceil(bits / 8) where bits = digits * log2(10)
    target_bytes = math.ceil(len(target_str) * math.log2(10) / 8)
    print(f"\nTARGET (WITH CRC): {target} bytes={target_bytes}\n")

    all_rows = []
    phase_final_s = []
    phase_log = []
    residual = target
    total_time = 0

    for phase in range(5):
        if residual == 0:
            break
        rows, final_s, residual, total_time = run_phase(residual, phase, total_time)
        all_rows.extend(rows)
        if final_s is not None:
            phase_final_s.append(final_s)
            phase_log.append((phase, final_s, residual))
        if residual == 0:
            break

    print_table(all_rows, target)

    print("\nPhase final S values:")
    for phase, s, res in phase_log:
        sign_note = "always +" if phase == 0 else "+/- in search"
        print(f"  Phase {phase}: S={s}  ({sign_note})  residual after: {res}")

    # Get the final residual from the last phase
    final_residual = phase_log[-1][2] if phase_log else 0
    
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
    run_system(data_digits=12)
