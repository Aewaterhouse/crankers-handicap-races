# Crankers Handicap Race Series

## What This Is

A Zwift handicap race series between 6 friends (+ 1 baby) with wildly different abilities. Results are published as a single-page static site (`index.html`) hosted on GitHub Pages. The tone is irreverent, mocking, and affectionate — like a group chat that got turned into race commentary.

## The Riders

Canonical rider profiles are in `handicap/riders.json` — that's the source of truth for weights, power, CdA, fade, and notes. Update it after every race.

| Rider | Weight | Race Avg W | W/kg | Nickname | Key Notes |
|-------|--------|-----------|------|----------|-----------|
| A. Waterhouse (you) | 74kg | 268W | 3.62 | "The Sandbagging Dog" | Strongest rider. DNF'd R2, won R3 at 278W/3.8wkg. CdA 0.256. |
| S. Heslop | 80kg | 235W | 2.94 | "The Diesel" | Boringly consistent. 3 podiums in 3 races. Series leader. CdA 0.267, 5% fade. |
| A. Einoder | 64kg | 152W | 2.38 | "Small Bark, Big Bite" | Lightest rider, low absolute power. Won R2. CdA 0.240, 7% fade. |
| A. Barton | 135kg | 205W | 1.52 | "The Fridge" | Heaviest by far. Vendetta against Claude. Climbs are brutal. CdA 0.400, 6% fade. |
| M. Baum | 76kg | 260W | 3.42 | "The Piss Gargler" | Only raced R2. DNS R1, R3. CdA 0.244, 0% fade. Limited data. |
| L. Bone | 85kg | 210W | 2.47 | "Big Glands" | ZERO race data. Self-reported FTP 215W. 0 starts in 3 rounds. All values are guesses. |
| C. Bone | ~5kg | 0W | N/A | "The Prodigy" | Luke's 9-week-old son. Joke entry. |

## Series Standings After Race 3

| Rider | R1 | R2 | R3 | Total |
|-------|----|----|-----|-------|
| S. Heslop | 4 | 4 | 3 | 11 |
| A. Waterhouse | 3 | 1 | 4 | 8 |
| A. Einoder | 1 | 5 | 2 | 8 |
| A. Barton | 2 | 2 | 1 | 5 |
| M. Baum | 0 | 3 | 0 | 3 |
| L. Bone | 0 | 0 | 0 | 0 |

**Scoring:** N points for 1st in an N-rider field (starters only). DNF scores last-place points. DNS scores 0.

## Handicap Prediction System

### How it works

Physics-based power-to-speed model using Newton-Raphson solver:
```
P_effective = (F_aero + F_roll + F_gravity) * v
F_aero = 0.5 * CdA * rho * v^2
F_roll = Crr * m * g
F_gravity = m * g * gradient
```

Each rider has a profile in `handicap/riders.json` with: weight, height, CdA, Crr, race_avg_power, power_fade_pct. The prediction script (`handicap/predict.py`) reads profiles + a course definition, predicts finish times, and outputs handicap start times.

### Key files

- `handicap/riders.json` — rider profiles (the main thing to tweak between races)
- `handicap/predict.py` — prediction engine with course definitions and physics model
- `fit/R2/`, `fit/R3/` — .fit files from Zwift for all riders who started

### Running predictions

```bash
# Activate venv first
source venv/bin/activate

# Predict Race 4 (default course: glasgow_crit_six)
python handicap/predict.py

# Predict on a specific course
python handicap/predict.py --course times_square_x6

# Predict for a subset of riders
python handicap/predict.py --riders Waterhouse,Heslop,Einoder,Barton

# Available courses: glasgow_crit_six, times_square_x6, beach_island_x2
```

### Calibration approach

1. .fit files from past races were analyzed to extract per-rider power, speed-vs-gradient profiles, CdA, and fade rates
2. These values were loaded into `riders.json` as starting points
3. Alex manually tunes profiles based on gut feel and race context (e.g. tech issues, good/bad days)
4. Backtest against R3 actuals showed ~30-100s accuracy across all riders
5. After each race: compare predictions to actuals, update `riders.json`, add new .fit files to `fit/R{n}/`

### Known model limitations

- Barton's steep climb speed (>6% gradient) is physics-extrapolated — no real data from R2/R3 courses
- Bone has zero race data — everything is a guess
- Baum has one race only (R2) — limited confidence
- Model assumes no drafting — chase groups benefit from sitting in
- Power fade is modelled as linear across laps — reality is more complex

## Race History

- **R1:** Unknown route. Heslop 1st, Waterhouse 2nd, Barton 3rd, Einoder 4th. Baum & Bone DNS.
- **R2:** Beach Island Loop x2, Watopia (26.2km, 88m, flat). Einoder 1st, Heslop 2nd, Baum 3rd, Barton 4th, Waterhouse DNF, Bone DNS.
- **R3:** Times Square Circuit x6, New York (21.8km, 120m). Waterhouse 1st, Heslop 2nd, Einoder 3rd, Barton 4th, Baum DNS, Bone DNS.
- **R4 (upcoming):** Glasgow Crit Six, Scotland (18.2km, 204m, 6 laps). Sunday 13 April 2026, 6:30 AM AEST.

## How the Site Works

- Single `index.html` — HTML, CSS, no build step, no JS frameworks
- Dark theme: bg #0a0a0a, accent orange #ff5722, gold/silver/bronze for podiums
- Fonts: Racing Sans One (hero), Oswald (headings/data), Bitter (body text) — all from Google Fonts
- Animated gradient hero header with shimmer effect
- Stats strip, winner spotlight with crown, colour-coded callout boxes
- Collapsible race history sections (vanilla JS onclick toggles)
- Course profile visualisation bar (flexbox segments)
- Responsive: grid collapses on mobile
- Writing style: mocking sports journalism — nobody is spared, especially Barton and Bone

## Workflow

1. **Before race:** Tweak `handicap/riders.json` if needed, run `python handicap/predict.py` to get start times
2. **Race day:** Race on Zwift with staggered starts per handicap
3. **After race:** Collect .fit files, drop into `fit/R{n}/`, record results
4. **Update site:** Update `index.html` with results table, standings, race report prose, and next race preview
5. **Update model:** Compare predictions to actuals, adjust `riders.json`, add new course to `predict.py` if needed
6. **Push:** `git push` to deploy via GitHub Pages

## Adding a New Course

Add a new entry to the `COURSES` dict in `handicap/predict.py`:
```python
'course_key': {
    'name': 'Display Name',
    'world': 'Zwift World',
    'laps': N,
    'lead_in': [(distance_m, gradient_fraction), ...],
    'lap': [(distance_m, gradient_fraction), ...],
    'total_km': X,
    'total_elevation_m': Y,
}
```
