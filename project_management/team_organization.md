# Team Organization

## Team Members
* **aqoraan**
* **atahtamo**

## Roles and Responsibilities
The project was divided to ensure equal workload and to play to the strengths of both team members:
* **aqoraan**: Responsible for the Pygame loop architecture, graphics rendering, Ghost AI/Pathfinding (BFS algorithms), and the maze generation wrapper.
* **atahtamo**: Responsible for the collision detection logic, `Config` parser and validation, Highscore JSON storage, and project management/documentation.

## Decision Making Process
* **Architecture**: All high-level architecture decisions were mapped out via UML class diagrams and System Context diagrams before coding began (see `pic/class_diagram.png` and `pic/system_context_diagram.png`).
* **Conflict Resolution**: Disagreements on code implementations were resolved via peer review. If a consensus could not be reached, the AI assistant was consulted for an objective best-practice standard (such as PEP-8 style and design patterns).

## Communication
* We held brief daily syncs to discuss blockers and progress.
* Code integration was handled through Git branches, with features being tested before being merged into the `alhareth` (or `main`) branch.
