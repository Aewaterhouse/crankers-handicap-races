# Zwift Handicap Race Series

## Series Standings

| Rider          | R1 | R2 | R3 | Total |
|----------------|----|----|-----|-------|
| S. Heslop      | 4  | 4  | 3   | 11    |
| A. Waterhouse  | 3  | 1  | 4   | 8     |
| A. Einoder     | 1  | 5  | 2   | 8     |
| A. Barton      | 2  | 2  | 1   | 5     |
| M. Baum        | 0  | 3  | 0   | 3     |
| L. Bone        | 0  | 0  | 0   | 0     |

Scoring: N points for 1st in N-rider field. DNF gets last place points.

---

## Race 3 Summary — Times Square Circuit x6 (New York), 21.8km, 120m elevation

Waterhouse, the sandbagging dog, took the win in the third round of the handicap series, overhauling the field despite giving up a 9-minute-19-second head start to first-starter Barton. Riding at 270W and 3.8 w/kg — the highest output of the day and suspiciously close to his stated FTP of 280W — Waterhouse carved through the field to cross the line in 42:05, more than a minute clear of Heslop. So much for those "technical difficulties" that plagued his earlier races.

Heslop and Einoder produced a tight battle for second, finishing just 4 seconds apart on corrected time. Heslop's 237W effort was enough to hold off Einoder, who continued to punch well above his weight with a 156W average on a course that doesn't favour lighter riders.

Barton's vendetta against the handicap algorithm took an unexpected turn — rather than the handicap being too harsh, his 9:19 head start proved insufficient as he faded to 200W average (down from his 217W race average in prior rounds), finishing nearly 4 minutes behind the predicted time. Whether this was tactical conservatism or the inevitable toll of hauling 135kg around Times Square six times remains a matter of debate.

Notably absent were Baum, Bone, and any semblance of their "technical infrastructure." Baum's tech issues continue into a second consecutive race, while Bone remains a DNS for the third straight round — his self-reported 215W FTP continuing to exist purely in the theoretical realm.

### R3 Results (with handicap start times baked in)

| Pos | Rider          | Finish Time | Avg W | W/kg |
|-----|----------------|-------------|-------|------|
| 1   | A. Waterhouse  | 42:05       | 270W  | 3.8  |
| 2   | S. Heslop      | 43:06       | 237W  | 3.0  |
| 3   | A. Einoder     | 43:10       | 156W  | 2.4  |
| 4   | A. Barton      | 47:08       | 200W  | 1.5  |
| DNS | M. Baum        | —           | —     | —    |
| DNS | L. Bone        | —           | —     | —    |

### R3 Actual Ride Times (handicap removed)

| Rider          | Start Delay | Finish Time | Actual Ride Time |
|----------------|-------------|-------------|------------------|
| A. Barton      | 0:00        | 47:08       | 47:08            |
| A. Einoder     | 1:58        | 43:10       | 41:12            |
| S. Heslop      | 7:31        | 43:06       | 35:35            |
| A. Waterhouse  | 9:19        | 42:05       | 32:46            |

### R3 Model Accuracy

| Rider          | Predicted | Actual | Difference |
|----------------|-----------|--------|------------|
| A. Waterhouse  | 33:57     | 32:46  | 1:11 fast  |
| S. Heslop      | 35:45     | 35:35  | 0:10 fast  |
| A. Einoder     | 41:18     | 41:12  | 0:06 fast  |
| A. Barton      | 43:17     | 47:08  | 3:51 slow  |

---

## Race 4 Handicaps — Times Square Circuit x6

**Course:** Times Square Circuit, New York  
**Distance:** 6 laps × 3.5km = 21km (+0.8km lead-in)  
**Elevation:** ~120m total  

### Start Order

| Start | Rider          | Delay   | Start Time |
|-------|----------------|---------|------------|
| 1st   | A. Barton      | —       | 0:00       |
| 2nd   | A. Einoder     | +3:24   | 3:24       |
| 3rd   | L. Bone        | +6:24   | 6:24       |
| 4th   | S. Heslop      | +8:30   | 8:30       |
| 5th   | M. Baum        | +9:41   | 9:41       |
| 6th   | A. Waterhouse  | +10:54  | 10:54      |

### Basis

Handicaps calculated using physics-based power-to-speed model (P = ½CdAρv³ + Crrmgv + mgGv). Race average w/kg weighted with R3 counted double (same course). Course modelled as 700m at 2.3% climb, 700m at 2.3% descent, 2100m flat per lap.

| Rider          | Weight | Race avg W | Race avg w/kg | CdA   | Flat speed | Est. 6-lap time |
|----------------|--------|------------|---------------|-------|------------|-----------------|
| A. Waterhouse  | 74kg   | 266W       | 3.59          | 0.261 | 40.6 kph   | 33:09           |
| M. Baum        | 76kg   | 250W       | 3.29          | 0.268 | 39.3 kph   | 34:23           |
| S. Heslop      | 80kg   | 237W       | 2.96          | 0.274 | 38.2 kph   | 35:34           |
| L. Bone        | 85kg   | 215W       | 2.53 (stated) | 0.281 | 36.4 kph   | 37:40           |
| A. Einoder     | 64kg   | 148W       | 2.32          | 0.239 | 33.8 kph   | 40:40           |
| A. Barton      | 135kg  | 210W       | 1.55          | 0.351 | 32.6 kph   | 44:04           |

### Speed Breakdown

| Rider          | Flat     | Climb    | Descent  | Avg lap  |
|----------------|----------|----------|----------|----------|
| A. Waterhouse  | 40.6 kph | 29.5 kph | 52.2 kph | 39.4 kph |
| M. Baum        | 39.3 kph | 28.0 kph | 51.2 kph | 38.0 kph |
| S. Heslop      | 38.2 kph | 26.4 kph | 50.7 kph | 36.7 kph |
| L. Bone        | 36.4 kph | 24.0 kph | 49.7 kph | 34.7 kph |
| A. Einoder     | 33.8 kph | 21.8 kph | 46.8 kph | 32.1 kph |
| A. Barton      | 32.6 kph | 17.6 kph | 50.2 kph | 29.6 kph |

### Notes

- R3 w/kg weighted double in averages since R4 is the same course
- Waterhouse's handicap increases by 1:35 from R3 — the sandbagging dog tax
- Barton's predicted time blows out by 47s reflecting his R3 fade to 1.5 w/kg
- L. Bone's FTP remains self-reported and unverified — no race data after 3 rounds
- M. Baum still has only one race data point (R2) — two consecutive DNS
- Physics model was excellent for Heslop (10s off) and Einoder (6s off) in R3
- Model assumes no drafting — chase groups will benefit from sitting in
