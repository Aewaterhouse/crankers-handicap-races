"""
Crankers Handicap Series — Race Prediction Engine

Reads rider profiles from riders.json and a course definition,
predicts finish times using physics model, outputs handicap start times.

Usage:
    python predict.py                  # predict with default course
    python predict.py --riders Waterhouse,Heslop,Einoder,Barton  # subset
"""

import json
import argparse
import math

# ── Physics constants ───────────────────────────────────────────────────────

RHO = 1.225            # air density (kg/m^3)
G = 9.81               # gravity (m/s^2)
DRIVETRAIN_LOSS = 0.025 # 2.5% loss

# ── Course definitions ──────────────────────────────────────────────────────

COURSES = {
    'glasgow_crit_six': {
        'name': 'Glasgow Crit Six',
        'world': 'Scotland',
        'laps': 6,
        'lead_in': [(200, 0.00)],
        # Per-lap segments: (distance_m, gradient as fraction)
        # Clyde Kicker: 301m at 3.64% avg, punch-flat-punch, max 7-9%
        'lap': [
            (100, 0.07),    # Clyde Kicker punch 1
            (101, 0.01),    # Clyde Kicker flat middle
            (100, 0.07),    # Clyde Kicker punch 2
            (150, -0.04),   # descent part 1
            (151, -0.03),   # descent part 2
            (2898, 0.00),   # flat sections
        ],
        'total_km': 18.2,
        'total_elevation_m': 204,
    },

    'times_square_x6': {
        'name': 'Times Square Circuit x6',
        'world': 'New York',
        'laps': 6,
        'lead_in': [(800, 0.00)],
        'lap': [
            (700, 0.023),   # climb
            (700, -0.023),  # descent
            (2100, 0.00),   # flat
        ],
        'total_km': 21.8,
        'total_elevation_m': 120,
    },

    'beach_island_x2': {
        'name': 'Beach Island Loop x2',
        'world': 'Watopia',
        'laps': 2,
        'lead_in': [(500, 0.00)],
        'lap': [
            (12600, 0.003),  # basically flat with tiny undulations
        ],
        'total_km': 26.2,
        'total_elevation_m': 88,
    },
}


# ── Physics model ───────────────────────────────────────────────────────────

def solve_speed(power_w, weight_kg, gradient, cda, crr):
    """
    Solve for steady-state speed given power and conditions.

    P_effective = (F_aero + F_roll + F_gravity) * v
    where:
        F_aero = 0.5 * CdA * rho * v^2
        F_roll = Crr * m * g * cos(theta)  (≈ Crr * m * g for small grades)
        F_gravity = m * g * sin(theta)      (≈ m * g * gradient for small grades)

    Uses Newton-Raphson iteration.
    """
    p_eff = power_w * (1.0 - DRIVETRAIN_LOSS)
    if p_eff <= 0:
        return 1.0

    v = 10.0  # initial guess (m/s)
    for _ in range(50):
        f_aero = 0.5 * cda * RHO * v * v
        f_roll = crr * weight_kg * G
        f_grav = weight_kg * G * gradient
        f_total = f_aero + f_roll + f_grav

        p_at_v = f_total * v
        # dP/dv = 3 * F_aero/v * v + F_roll + F_grav = 1.5*CdA*rho*v^2 + F_roll + F_grav
        dp_dv = 1.5 * cda * RHO * v * v + f_roll + f_grav

        if abs(dp_dv) < 1e-10:
            break

        v_new = v - (p_at_v - p_eff) / dp_dv
        v_new = max(v_new, 0.5)

        if abs(v_new - v) < 0.0001:
            break
        v = v_new

    # On steep descents, gravity alone can exceed rolling+aero resistance
    # Cap at a reasonable Zwift max (~70 kph descent)
    return min(max(v, 0.5), 19.4)


def predict_time(rider, course):
    """Predict finish time in seconds for a rider on a course."""
    weight = rider['weight_kg']
    base_power = rider['race_avg_power']
    cda = rider['cda']
    crr = rider['crr']
    fade = rider['power_fade_pct']
    laps = course['laps']

    total_time = 0.0

    # Lead-in (no fade yet)
    for dist_m, grad in course['lead_in']:
        speed = solve_speed(base_power, weight, grad, cda, crr)
        total_time += dist_m / speed

    # Laps with progressive fade
    for lap in range(laps):
        # Linear fade: power drops from 100% to (100% - fade%) over the race
        lap_progress = lap / max(laps - 1, 1)
        power = base_power * (1.0 - fade * lap_progress)

        for dist_m, grad in course['lap']:
            speed = solve_speed(power, weight, grad, cda, crr)
            total_time += dist_m / speed

    return total_time


# ── Output formatting ───────────────────────────────────────────────────────

def fmt_time(seconds):
    """Format seconds as M:SS or MM:SS."""
    m, s = divmod(int(round(seconds)), 60)
    return f"{m}:{s:02d}"


def print_predictions(riders, course_key):
    """Run predictions and print handicap table."""
    course = COURSES[course_key]

    print()
    print("=" * 65)
    print(f"  CRANKERS HANDICAP SERIES")
    print(f"  {course['name']} — {course['world']}")
    print(f"  {course['total_km']}km, {course['total_elevation_m']}m elevation, {course['laps']} laps")
    print("=" * 65)

    # Predict each rider
    predictions = {}
    print(f"\n{'Rider':<14} {'Weight':>6} {'Power':>6} {'W/kg':>6} {'CdA':>6} {'Fade':>6} {'Predicted':>10}")
    print("-" * 62)

    for name, profile in sorted(riders.items(), key=lambda x: x[1]['race_avg_power'] / x[1]['weight_kg'], reverse=True):
        time_s = predict_time(profile, course)
        predictions[name] = time_s
        wkg = profile['race_avg_power'] / profile['weight_kg']
        print(f"  {name:<12} {profile['weight_kg']:>5}kg {profile['race_avg_power']:>5}W "
              f"{wkg:>5.2f} {profile['cda']:>5.3f} {profile['power_fade_pct']*100:>4.1f}% "
              f"{fmt_time(time_s):>9}")

    # Handicap start times
    slowest = max(predictions.values())
    start_order = sorted(predictions.items(), key=lambda x: x[1], reverse=True)

    print(f"\n{'':─<65}")
    print(f"  HANDICAP START TIMES")
    print(f"{'':─<65}")
    print(f"\n  {'#':<4} {'Rider':<14} {'Delay':>8} {'Start':>8} {'Est. Finish':>12}")
    print(f"  {'':-<50}")

    for i, (name, time_s) in enumerate(start_order):
        delay = slowest - time_s
        est_finish = delay + time_s  # should all be ~equal = slowest
        print(f"  {i+1:<4} {name:<14} +{fmt_time(delay):>6} {fmt_time(delay):>8} {fmt_time(est_finish):>11}")

    # Spread analysis
    fastest_name, fastest_time = start_order[-1]
    slowest_name, slowest_time = start_order[0]
    spread = slowest_time - fastest_time

    print(f"\n  Total spread: {fmt_time(spread)} ({slowest_name} → {fastest_name})")
    print(f"  If perfect, all riders finish at: ~{fmt_time(slowest_time)}")

    return predictions


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Crankers Handicap Predictor')
    parser.add_argument('--course', default='glasgow_crit_six',
                        choices=list(COURSES.keys()),
                        help='Course to predict')
    parser.add_argument('--riders', default=None,
                        help='Comma-separated rider names (default: all)')
    parser.add_argument('--profiles', default='riders.json',
                        help='Path to rider profiles JSON')
    args = parser.parse_args()

    with open(args.profiles) as f:
        all_profiles = json.load(f)

    # Remove metadata keys
    riders = {k: v for k, v in all_profiles.items() if not k.startswith('_')}

    if args.riders:
        selected = [r.strip() for r in args.riders.split(',')]
        riders = {k: v for k, v in riders.items() if k in selected}

    predictions = print_predictions(riders, args.course)

    # Print rider notes
    print(f"\n{'':─<65}")
    print(f"  NOTES")
    print(f"{'':─<65}")
    for name in riders:
        note = riders[name].get('notes', '')
        if note:
            print(f"  {name}: {note}")
    print()


if __name__ == '__main__':
    main()
