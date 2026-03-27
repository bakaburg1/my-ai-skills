# S7 and vctrs Guidance

Read this file when implementing class systems rather than just choosing
one.

## S7

- Prefer S7 for new projects that need explicit properties, validators,
  safer property access, and formal method dispatch.
- S7 is usually a strong replacement for ad hoc S3 classes when the code
  has outgrown informal structure.

## vctrs

- Prefer `vctrs` for custom vector classes, explicit casting, common type
  resolution, and predictable size/type behavior.
- Use `new_vctr()`, `vec_cast()`, and `vec_ptype_common()` when designing
  reusable vector APIs.
`scores <- vctrs::new_vctr(c(1, 2, 3))`

## Migration Guidance

- S3 to S7 is usually reasonable when you want better structure while
  keeping broad compatibility.
- Base types to `vctrs` are worth the cost when consistent coercion and
  data-frame integration matter.
- Do not migrate class systems just to look modern; the extra machinery
  should solve a real design problem.
