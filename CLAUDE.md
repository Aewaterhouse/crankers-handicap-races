# Crankers Handicap Race Series

## What This Is

A Zwift handicap race series between 6 friends with wildly different abilities. Results are published as a single-page static site (`index.html`) hosted on GitHub Pages. The tone is irreverent, mocking, and affectionate — like a group chat that got turned into race commentary.

## The Riders

| Rider | Weight | Approx W/kg | Notes |
|-------|--------|-------------|-------|
| A. Waterhouse (you) | 74kg | 3.6-3.8 | Strongest rider. DNF'd R2, won R3. "The sandbagging dog" |
| S. Heslop | 80kg | ~3.0 | "The Diesel." Boringly consistent. Series leader after R3 (11pts) |
| A. Einoder | 64kg | ~2.3-2.4 | Lightest rider. Won R2 off handicap. Punches above weight |
| A. Barton | 135kg | ~1.5 | "The Fridge." Heaviest rider by far. Has a vendetta against Claude |
| M. Baum | 76kg | ~3.3 | "The Piss Gargler." Only raced R2 (250W). DNS R1, R3 |
| L. Bone | 85kg | ~2.5 (stated) | "Big Glands." Has never raced. 0 starts across 3 rounds. FTP unverified |

## Series Standings After Race 3

| Rider | R1 | R2 | R3 | Total |
|-------|----|----|-----|-------|
| S. Heslop | 4 | 4 | 3 | 11 |
| A. Waterhouse | 3 | 1 | 4 | 8 |
| A. Einoder | 1 | 5 | 2 | 8 |
| A. Barton | 2 | 2 | 1 | 5 |
| M. Baum | 0 | 3 | 0 | 3 |
| L. Bone | 0 | 0 | 0 | 0 |

**Scoring:** N points for 1st in an N-rider field. DNF/DNS gets last-place points (1 for DNF, 0 for DNS).

## Handicap System

- Physics-based power-to-speed model: `P = 1/2 * CdA * rho * v^3 + Crr * m * g * v + m * g * G * v`
- CdA scales with rider weight
- Predicted finish times calculated per rider, then staggered so slowest rider starts first
- Recent race data weighted more heavily (same-course data weighted double)
- Actual race W/kg used where available; L. Bone's remains self-reported

## Race History

- **R1:** Unknown route. Heslop 1st, Waterhouse 2nd, Barton 3rd, Einoder 4th. Baum & Bone DNS.
- **R2:** Beach Island Loop x2, Watopia (26.2km, 88m, flat). Einoder 1st, Heslop 2nd, Baum 3rd, Barton 4th, Waterhouse DNF, Bone DNS.
- **R3:** Times Square Circuit x6, New York (21.8km, 120m). Waterhouse 1st, Heslop 2nd, Einoder 3rd, Barton 4th, Baum DNS, Bone DNS.

## How the Site Works

- Everything is in a single `index.html` — HTML, CSS, inline styles, no build step
- Dark theme with orange accent (#ff5722), Oswald + Bitter fonts from Google Fonts
- Sections: header, results table, series standings scorecard, prose race report, next race teaser, footer
- The writing style is mocking sports journalism — nobody is spared, especially Barton

## Workflow

1. Choose a route and calculate handicap start times using the physics model
2. Race on Zwift
3. Collect results (finish times, avg watts, w/kg)
4. Update `index.html` with results, updated standings, a race report, and the next race preview
5. Push to GitHub Pages
