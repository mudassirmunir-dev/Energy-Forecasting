
# Daylight Saving Time Anomaly Investigation

## Objective
Investigate the unusually high electricity reading recorded at
02:00 on November 5, 2017, for Hog_lodging_Shonda.

## Observations

The following readings were observed:

| Year | 01:00 | 02:00 | 03:00 |
|---|---:|---:|---:|
| 2016 | 99 | 184 | 89 |
| 2017 | 110 | 212 | 95 |

Both years show a sharp increase at 02:00 followed by
a sharp decrease at 03:00.

## Findings

- November 5, 2017 contains 24 hourly records.
- November 5, 2016 also contains 24 hourly records.
- The same unusual pattern appears in both years.
- The pattern may be related to daylight saving time
  or recurring meter-recording behavior.

## Limitations

The available timestamps do not establish whether readings
are stored in local time or standardized time.

Therefore, daylight saving time cannot be confirmed as
the cause of the unusual readings.

## Decision

Retain the readings in the dataset.

Do not remove or modify them without additional evidence.

Investigate timestamp conventions and meter documentation
if further information becomes available.
