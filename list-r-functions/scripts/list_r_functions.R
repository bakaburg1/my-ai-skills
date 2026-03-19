list_r_functions <- function(file_regex = "R/utils.*\\.R$") {
  # Validate file_regex input.
  if (!is.character(file_regex) || length(file_regex) < 1) {
    stop("file_regex must be a character vector with at least one regex.")
  }

  # Collect files from the working directory that match any regex.
  all_files <- list.files(".", recursive = TRUE, full.names = TRUE)
  matches_any <- function(path) {
    any(vapply(file_regex, function(rx) grepl(rx, path), logical(1)))
  }
  target_files <- sort(all_files[vapply(all_files, matches_any, logical(1))])

  # Exit early if no files matched.
  if (length(target_files) == 0) {
    message("No files matched file_regex.")
    return(list())
  }

  # Parse files and extract top-level function assignments.
  parsed <- lapply(target_files, function(path) parse(path, keep.source = TRUE))
  extract_defs <- function(exprs) {
    defs <- list()
    for (expr in exprs) {
      # Capture name <- function(...) or name = function(...) at top level.
      if (is.call(expr) &&
          (identical(expr[[1]], as.name("<-")) || identical(expr[[1]], as.name("="))) &&
          is.symbol(expr[[2]]) &&
          is.call(expr[[3]]) &&
          identical(expr[[3]][[1]], as.name("function"))) {
        defs[[as.character(expr[[2]])]] <- expr[[3]]
      }
    }
    defs
  }
  defs_list <- lapply(parsed, extract_defs)
  defs <- do.call(c, defs_list)

  # Exit early if no functions were found.
  if (length(defs) == 0) {
    message("No function definitions found.")
    return(list())
  }

  # Deduplicate functions while preserving the first occurrence.
  func_names <- names(defs)
  keep <- !duplicated(func_names)
  func_names <- func_names[keep]
  defs <- defs[keep]

  # Build and print signatures without evaluating function bodies.
  build_signature <- function(name, fn_call) {
    # Materialize the function object without executing the body.
    fn_obj <- eval(fn_call, envir = baseenv())
    # Render arguments with defaults while skipping empty defaults.
    arg_list <- formals(fn_obj)
    arg_names <- names(arg_list)
    arg_text <- mapply(function(arg_name, arg_value) {
      if (is.symbol(arg_value) && identical(as.character(arg_value), "")) {
        return(arg_name)
      }
      default_text <- paste(deparse(arg_value), collapse = " ")
      paste0(arg_name, " = ", default_text)
    }, arg_names, arg_list, USE.NAMES = FALSE)
    paste0(name, "(", paste(arg_text, collapse = ", "), ")")
  }
  sigs <- mapply(build_signature, func_names, defs, USE.NAMES = FALSE)
  cat(paste0(sigs, collapse = "\n"), "\n")

  # Read Rd files into a named list, with a fallback message if missing.
  rd_texts <- lapply(func_names, function(name) {
    rd_path <- file.path("man", paste0(name, ".Rd"))
    # Prefer dot- prefixed Rd files for internal helpers (e.g. .foo -> dot-foo.Rd).
    if (startsWith(name, ".")) {
      dot_path <- file.path("man", paste0("dot-", substring(name, 2), ".Rd"))
      if (file.exists(dot_path)) {
        rd_path <- dot_path
      }
    }
    if (!file.exists(rd_path)) {
      return("function documentation not found")
    }
    paste(readLines(rd_path, warn = FALSE), collapse = "\n")
  })
  names(rd_texts) <- func_names

  # Return the named list of Rd contents.
  rd_texts
}
