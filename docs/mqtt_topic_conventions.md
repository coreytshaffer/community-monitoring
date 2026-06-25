# MQTT Topic Conventions

This document outlines the proposed topic hierarchy for field sensor telemetry. It is designed to be logical, easily filterable, and strictly segmented.

## Topic Structure

The base pattern for all sensor-related topics follows:

```text
clearlakewatch/sensors/{station_id}/{sensor_id}/{message_type}
```

### Defined Message Types

- `observations`: Used for structured data payloads conforming to the Sensor Data Contract.
- `status`: Used for hardware health, battery levels, connectivity metrics, or heartbeat messages.
- `deadletter`: Used by the broker or ingestion layer to route malformed or unrecognizable payloads away from the main processing pipeline.

## Examples

### North Shore Station
- `clearlakewatch/sensors/station_north_shore/temp_probe_a1/observations`
- `clearlakewatch/sensors/station_north_shore/temp_probe_a1/status`

### East Bay Station
- `clearlakewatch/sensors/station_east_bay/ph_sensor_b2/observations`
- `clearlakewatch/sensors/station_east_bay/ph_sensor_b2/status`
- `clearlakewatch/sensors/station_east_bay/ph_sensor_b2/deadletter`

## Subscribing Strategies

- **Firehose (All Data):** `clearlakewatch/sensors/#`
- **All Observations:** `clearlakewatch/sensors/+/+/observations`
- **Specific Station (All Data):** `clearlakewatch/sensors/station_north_shore/#`
- **Specific Sensor Observations:** `clearlakewatch/sensors/station_north_shore/temp_probe_a1/observations`

This structure allows the ingestion layer to securely subscribe only to `observations` topics for processing, while maintenance services can monitor `status` topics, and logging systems can monitor `deadletter` queues.
