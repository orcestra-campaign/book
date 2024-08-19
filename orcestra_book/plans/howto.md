---
orphan: true
---

# Making a Flight Plan for HALO

HALO flight planning involves several steps:

1. deciding on the flight plan using the online flight planning tools.  Good to start this 4-5 working days before the flight.
2. Filing of the flight by providing coordinates and elements to FX
3. Briefing the pilots.

# Creating a flight plan

Once you know what you want to do in principle it needs to be made precise.  This is usually done using standardized elements, such a legs, circles, or *Mayer Pirouettes*.  The essential elment of a flight plan is a waypoint in the form of coordinates (see below) as this is the basis of communication with ATC.  Waypoints can be discarded during a flight, but they are difficult to add.  Adding more waypoints builds in flexibility, but adding too many can be a source of confusiong.

  - Be mindful of the standard elements (ec_under, c_north, c_mid, c_south)
  - Double check `ec_north`, `ec_south`, `ec_under` with Flo
  - Be mindful of the general rule of flying the circles after the transect, this can be important to ensure we have enough time to get ATC permission for the circle and drops.
  - We use `ec_north` to refer to a waypoint that is along the EarthCARE track north of the perimeter of `c_north` 
  - Likewise `ec_south` refers to a waypoint that is along the EarthCARE track south of the perimeter of `c_south`
  - In some cases a waypiont can be the center point of a circle, or it could be calculated in c_south_in if it joins the circle on a perimeter.
  - For timing `c_mid`, `c_north`, `c_south` are an hour, flying through them takes 30 min, `c_atr` is 40 min.

Preferred coordinates have the form 1644N02257W  for 16deg 44min N and 22 deg 57min W

## Filing of the flight plan (presently for Cape Verde)

1. a flight plan has to be filed with DRL-FX before 10am local time, three working days before the flight, e.g., a flightplan for a Monday needs to be communicated to FX the previous Wednesday (before 10am).
2. before 10am one working day before the flight communicate any desired changes, or confirm the absence of changes with FX.  At this time the crew should also be fixed and communicated.

## Briefing the pilots
1. discuss the flight plan with the pilots (usually at 14hr) on the day before the flight (assuming this is not a day off), paying attention to any potential challenges or non-standard elements.
2. provide a detailed description of the flight plan (see below) to DLR-FX to be forwarded to the pilots the day before the flight. Note that this can makes use of standard definitions for different waypoints, but these must be checked to ensure that they don't differ from waypoints in the flightplan filed with Air Traffic Control (ATC). Ask the ground scientist to verify these before submitting.

## Example of a "detailed description for pilots"

**Sequence and Transitions:**
1. 10:30 UTC (LT+1) Take off from SAL
2. Turn toward SW onto ec_track (around 11:45 UTC)
3. Drop sonde (WP2: N07 07.14, W033 50.48)
4. Drop sonde (WP3: N01 30.00, W033 14.15, around 13:15 UTC)
5. 270 deg enter c_south for CCW circle from the south FL430 (around 13:20 UTC)
6. 090 deg exit to EC Track (around 14:20 UTC)
7. 090 deg enter c_mid for CW circle from the south (around 14:50 UTC)
8. 090 deg exit to ec_track (around 15:50 UTC) ascend to FL450 (to be level no later than 1600 UTC)
9. EarthCARE overflight (around 16:15 at about 008 24.86N, 031 54.98W)
10. 090 deg enter c_north for CW circle from the north (around 16:46)
11. 090 deg exit c_north and ferry toward c_atr (around 17:46)
12. Gradually turn onto c_atr for CCW circle FL350 (around 19:00)
13. Fade off circle and return to SAL (around 19:40)

**Some coordinates:**

c_south: N03 13.96, W032 53.18
c_north: N11  0.27, W031 25.48
c_mid:   N07  7.14, W032  9.52
c_atr:   N17 26.00, W023 30.00

ec_north: N12 17.96, W031 10.49
ec_south: N01 30.00, W033 14.15
ec_under:  around N08 24.86, W031 54.98

**Possible Contingencies:**

- we could fly onto `c_south` from north to save time.
- perform `mayer_pirouettes` in `c_south` if congestus clouds can be identified.

*Note:* For the detailed description the coordinates are preferred in the format N23 15.3' for 23deg 15.2 minutes north.  Likewise W012 48.1' would correspond to 12deg 48.1 min west.

