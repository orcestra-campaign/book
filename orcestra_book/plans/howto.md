---
orphan: true
---

# The HALO PI and their role

The job of the PI on HALO is to:

1. coordinate with DLR-FX to make a Flight Plan for HALO that is aligned with the campaign objectives.
2. identify the scientific crew, including ground support scientist
3. communicate the flight plan to the scientific crew and other campaign members
4. execute the flight plan during the flight, addressing contingencies in coordination with ground support and the pilots as they arise.
5. ensure the timely provision of the flight report.

## HALO flight planning 

1. deciding on the flight plan using the online flight planning tools.  Good to start this 4-5 working days before the flight.
2. Filing of the flight by providing coordinates and elements to FX
3. Briefing the pilots and the crew.
4. Ensure that the ground scientist is aware of the plan and can edit it if it changes during or just before the flight.

### Creating a flight plan

Once you know what you want to do in principle it needs to be made precise.  This is usually done using standardized elements, such a legs, circles, etc..  The essential element of a flight plan is a waypoint in the form a LatLon object as this is the basis of communication with ATC.  Waypoints can be discarded during a flight, but they are difficult to add on the fly.  Adding more waypoints ahead of time builds in flexibility, but adding too many can be a source of confusion.

  - Be mindful of the standard elements (ec_under, ec_track, c_north, c_mid, c_south)
  - Be mindful of the general rule of flying the circles after the transect, this can be important to ensure we have enough time to get ATC permission for the circle and drops.
  - We use `ec_north` to refer to a waypoint that is along the EarthCARE track north of the perimeter of `c_north` 
  - Likewise `ec_south` refers to a waypoint that is along the EarthCARE track south of the perimeter of `c_south`
  - In some cases a waypiont can be the center point of a circle, or it could be calculated in c_south_in if it joins the circle on a perimeter.
  - For timing `c_mid`, `c_north`, `c_south` are an hour, flying through them takes 20 min.  The `c_atr` is smaller and takes 40 min. to circuit.
  - Ask the ground scientist to check the plan, paying particular attentino to points of coordinatino, ie., `ec_under` or the `ec_track`. 


### Filing of the flight plan (presently for Cape Verde)

1. a flight plan has to be filed with DRL-FX before 10am local time, three working days before the flight, e.g., a flightplan for a Monday needs to be communicated to FX the previous Wednesday (before 10am).
2. before 10am one working day before the flight communicate any desired changes, or confirm the absence of changes with FX.  At this time the crew should also be fixed and communicated.

### Briefing the pilots
 - discuss the flight plan with the pilots (usually at 14hr) on the day before the flight (assuming this is not a day off), paying attention to any potential challenges or non-standard elements.
 - provide a detailed description of the flight plan (see below) to DLR-FX to be forwarded to the pilots the day before the flight. Note that this can makes use of standard definitions for different waypoints, but these must be checked to ensure that they don't differ from waypoints in the flightplan filed with Air Traffic Control (ATC). Ask the ground scientist to verify these before submitting.


### Before, during and immediately after the flight
 - meet with the crew and pilots shortly before the flight to brief everyone on the plan and review contingencies
 - assign seats that account for the various functions and needs of the crew, i.e., docu-scientist needs a good window.
 - answer questions from the pilots to deal with contingencies. 
 - communicate with the ground scientist to upload flight plan changes in the event of contingencies (delete and add new kml files to planet)
 - keep the crew briefed of events, including those they should be aware of.  For instance communicating a reminder "planned flight level change to FL450 is coming up in about 10 min" 
 - document the flight and remain aware of instrument issues.
 - debrief with FX and the crew upon landing.
 - remind the crew to keep their headphones on, and ensure that there is always someone who can address or respond to queries from the pilots.
