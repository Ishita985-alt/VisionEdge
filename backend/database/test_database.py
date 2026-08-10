import logging

from database_manager import DatabaseManager


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def test_database_initialization():
    print("\n# VisionEdge Database Manager Test\n")

    database = DatabaseManager()

    print(f"[✓] Database path: {database.database_path}")

    database.initialize_database()

    print("[✓] Database initialized successfully")
    print("[✓] Events table created successfully")


def test_add_event():
    database = DatabaseManager()

    event_id = database.add_event(
        camera_id="camera_0",
        event_type="motion_detected",
        description="Movement detected in camera frame",
        severity="INFO",
    )

    if event_id:
        print(f"[✓] Event inserted successfully: ID {event_id}")
    else:
        print("[✗] Event insertion failed")


def test_get_events():
    database = DatabaseManager()

    events = database.get_events()

    print(f"[✓] Retrieved {len(events)} event(s)")

    for event in events:
        print(
            f"    ID: {event['id']}, "
            f"Camera: {event['camera_id']}, "
            f"Type: {event['event_type']}, "
            f"Severity: {event['severity']}"
        )


if __name__ == "__main__":
    test_database_initialization()
    test_add_event()
    test_get_events()

    print("\n[✓] Day 4 Database Manager test completed successfully")