# Station Metadata Contract

This document defines the minimal station metadata contract. The registry allows the platform to distinguish known demo/simulated stations from unknown or misconfigured station IDs.

## Metadata Fields

* `station_id` (string): Unique identifier for the station.
* `station_name` (string): Human-readable name.
* `status` (string): Operational status (`demo`, `planned`, `active`, `inactive`, `retired`).
* `latitude` (float): Location latitude.
* `longitude` (float): Location longitude.
* `location_description` (string): Text description of the physical location.
* `waterbody` (string): Name of the waterbody (e.g., Clear Lake).
* `county` (string): County name (e.g., Lake County).
* `state` (string): State abbreviation (e.g., CA).
* `operator` (string): Entity responsible for the station.
* `deployment_type` (string): Nature of deployment (`simulated`, `bench_test`, `field_trial`, `production`).
* `allowed_parameters` (array of strings): List of environmental parameters the station is authorized to report.
* `notes` (string): Optional context.

## Important Distinctions

* **Simulated/Demo Stations**: `demo` and `simulated` stations are **not** real field deployments. They are used for testing the ingestion pipeline.
* **Registry Inclusion vs Publication**: A known station does not automatically make its readings publishable. Station metadata supports provenance checks and human review, not automatic public display.
* **Unknown Stations**: Unknown station IDs must require review or quarantine depending on pipeline policy.
