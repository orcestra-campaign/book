---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.7.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
  orphan: true
---

# Making a Flight Plan for HALO

HALO flight planning involves several steps  Here we cover the technical aspects and the timeline associated with them. 

## Flight planning on Cape Verde

1. a flight plan has to be filed with DRL-FX three working days before the flight.  So a flightplan for a Monday needs to be filed by the previous Wednesday.
2. fine tuning can be submitted to DLR-FX one working day before the planned flight.  At this time the crew should also be fixed and communicated.
3. discuss the flight plan with the pilots (usually at 14hr) on the day before the flight (assuming this is not a day off), paying attention to any potential challenges or non-standard elements.
4. provide detailed description of the flight plan to DLR-FX to be forwarded to the pilots the day before the flight.

# The elmenets of the flight plan#

* A flight plan is usually composed of standardized elements, such a legs, circles, or mayer pirouettes.  The essential elment of a flight plan is a waypoint in the form of coordinates as this is the basis of communication with ATC.  Waypoints can be discarded during a flight, but they are difficult to add.  Adding more waypoints builds in flexibility, but adding too many can be a source of confusiong.

  - We use `ec_north` to refer to a waypoint that is along the EarthCARE track north of the perimeter of `c_north` 
  - likewise `ec_south` refers to a waypoint that is along the EarthCARE track south of the perimeter of `c_south`
  - in some cases a waypiont can be the center point of a circle, or it could be calculated in c_south_in if it joins the circle on a perimeter.

* Coordinates are preferred in the format N23 15.3' for 23deg 15.2 minutes north.  Likewise W012 48.1' would correspond to 12deg 48.1 min west.
* An example of a detailed description of a flight plan is provided as below.  Note that it makes use of standard definitions for different waypoints, and these should be checked to ensure that they don't differ from waypoints in the flightplan filed with Air Traffic Control (ATC)

### Example of a "detailed description for pilots"

**Sequence and Transitions:**
1. 10:30 UTC (LT+1) Take off from SAL
2. Turn toward SW onto ec_track(around 11:45 UTC)
3. Drop sonde (WP2: 007 7.14N, -33 50.48W)
4. Drop sonde (WP3: 001 30.00N, 033 14.15W, around 13:15 UTC)
5. 270 deg enter c_south for CCW circle from the south FL430 (around 13:20 UTC)
6. 090 deg exit to EC Track (around (14:20 UTC)
7. 090 deg enter c_mid for CW circle from the south (around 14:50 UTC)
8. 090 deg exit to ec_track (around 15:50 UTC) ascend to FL450 (to be level no later than 1600 UTC)
9. EarthCARE overflight (around 16:15 at about 008 24.86N, 031 54.98W)
10. 090 deg enter c_north for CW circle from the north (around 16:46)
11. 090 deg exit c_north and ferry toward c_atr (around 17:46)
12. Gradually turn onto c_atr for CCW circle FL350 (around 19:00)
13. Fade off circle and return to SAL (around 19:40)

**Some coordinates:**

c_south:  003 13.96N, 032 53.18W
c_north:  011  0.27N, 031 25.48W
c_mid:    007  7.14N, 032  9.52W
c_atr:    017 26.00N, 023 30.00W

ec_north: 012 17.96N, 031 10.49W
ec_south:  001 30.00N, 033 14.15W
ec_under:  around 008 24.86N, 031 54.98W

**Possible Contingencies:**

- fly onto `c_south` from north to save time.
- perform `mayer_pirouettes` in `c_south` if congestus clouds can be identified.


