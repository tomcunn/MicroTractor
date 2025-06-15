+------------+--------------------------+--------------------------------------------------+
| Byte Index | Name                     | Description                                      |
+============+==========================+==================================================+
| 0          | Packet Identifier (0x4D) | Identifies the packet type as a control packet. |
+------------+--------------------------+--------------------------------------------------+
| 1          | Left Motor Command       | Controls the speed and direction of the left    |
|            |                          | motor. Value ranges from 0 (full reverse) to    |
|            |                          | 250 (full forward), with 125 as stop.           |
+------------+--------------------------+--------------------------------------------------+
| 2          | Right Motor Command      | Controls the speed and direction of the right   |
|            |                          | motor. Value ranges from 0 (full reverse) to    |
|            |                          | 250 (full forward), with 125 as stop.           |
+------------+--------------------------+--------------------------------------------------+
| 3          | Front Hitch Position     | Controls the angle of the front hitch. Value    |
|            |                          | ranges from 0 (minimum angle) to 180 (maximum   |
|            |                          | angle). 0xFF indicates no change.               |
+------------+--------------------------+--------------------------------------------------+
| 4          | A Button State           | Enables the drivetrain when set to 1.           |
+------------+--------------------------+--------------------------------------------------+
| 5          | Y Button State           | Disables the drivetrain when set to 1.          |
+------------+--------------------------+--------------------------------------------------+
