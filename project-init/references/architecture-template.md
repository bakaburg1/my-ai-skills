# `ARCHITECTURE.md` Scaffold

Use `ARCHITECTURE.md` for implemented reality. It must stay aligned with `PLAN.md`, but it must never pretend planned work already exists.

## Recommended Structure

Use nested numeric lists so backlog items can reference exact sections.

1. Project Overview
   1. State what exists today.
   2. Keep this anchored in implemented reality.
2. Repository Structure
   1. List the meaningful top-level directories, packages, services, or modules that already exist.
   2. Add subsection numbers for major subsystems if the project is large.
3. Implemented Functionality
   1. Group features by subsystem or capability.
   2. Use nested numeric items for important entry points and behaviors.
   3. Note current limitations only when they matter for future work.
4. Dependency and Tooling Shape
   1. Runtime dependencies
   2. Tooling
   3. Build system
   4. Testing approach
   5. Deployment or runtime environment if already established
5. Active Technical Decisions
   1. Record only decisions that are already true in the implementation.
   2. Do not include hypothetical future designs here.
6. Current Milestone Status
   1. Optionally summarize which milestones are complete, in progress, pending, or blocked.
   2. Keep milestone references aligned with `BACKLOG.md`.

## Quality Bar

If someone reads only `ARCHITECTURE.md`, they should understand what exists today and where to find it.
