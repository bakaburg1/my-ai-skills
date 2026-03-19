# Object Systems and Class Design

Read this file when creating new classes or evaluating class systems.

## Decision Rules

- Use `vctrs` for vector-like classes that must integrate cleanly with
  data frames and type-stable operations.
- Use S7 for new non-vector class hierarchies that need formal structure,
  validation, and clear method dispatch.
- Use S3 for simple classes, existing S3 ecosystems, or lightweight
  internal structures.
- Use S4 mainly when the surrounding ecosystem already depends on it,
  especially Bioconductor.

## Decision Guide

- For vector-like objects, start with `vctrs` if you need data-frame
  integration, predictable coercion, and size stability.
- For general objects, prefer S7 for new projects that need formal
  property validation, safer access, and clearer inheritance.
- Choose S3 when simplicity, compatibility, or minimal overhead matters
  more than strict structure.
- Choose S4 when you are working in an existing S4 ecosystem or need the
  features that ecosystem already expects.

## Read Next

- For vector classes and coercion behavior:
  [s7-vctrs.md](s7-vctrs.md)
