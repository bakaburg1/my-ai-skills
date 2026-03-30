#!/usr/bin/env python3
"""Spawn multiple noninteractive Codex runs with concurrency limits and timeouts."""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Optional


@dataclasses.dataclass
class Task:
    task_id: int
    text: str


@dataclasses.dataclass
class TaskState:
    task: Task
    command: List[str]
    process: subprocess.Popen
    start_time: float
    stdout_path: Optional[Path]
    stderr_path: Optional[Path]
    stdout_file: Optional[object]
    stderr_file: Optional[object]


@dataclasses.dataclass
class TaskResult:
    task_id: int
    text: str
    status: str
    returncode: Optional[int]
    duration_seconds: float
    stdout_path: Optional[str]
    stderr_path: Optional[str]
    stdout: Optional[str]
    stderr: Optional[str]


def parse_args() -> argparse.Namespace:
    # Build argument parser for concurrency and execution controls.
    parser = argparse.ArgumentParser(description="Spawn parallel codex exec tasks.")
    parser.add_argument(
        "--tasks-file",
        type=str,
        help="Path to a file with one task per line (blank lines ignored).",
    )
    parser.add_argument(
        "tasks",
        nargs="*",
        help="Tasks provided as positional arguments (in addition to --tasks-file).",
    )
    parser.add_argument(
        "--runner",
        type=str,
        default="opencode run",
        help="Base command to run (default: 'opencode run').",
    )
    parser.add_argument(
        "--runner-args",
        type=str,
        default="",
        help="Extra args appended to the runner command.",
    )
    parser.add_argument(
        "--task-placeholder",
        type=str,
        default="{task}",
        help="Placeholder token to replace with task text (default: {task}).",
    )
    parser.add_argument(
        "--prepend",
        type=str,
        default="",
        help="Text to prepend to every task before substitution.",
    )
    parser.add_argument(
        "--max-parallel",
        type=int,
        default=3,
        help="Maximum number of parallel tasks.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=600,
        help="Per-task timeout in seconds (0 disables).",
    )
    parser.add_argument(
        "--poll-seconds",
        type=float,
        default=5.0,
        help="Polling interval in seconds.",
    )
    parser.add_argument(
        "--max-loops",
        type=int,
        default=120,
        help="Maximum polling loops before aborting and asking to continue.",
    )
    parser.add_argument(
        "--confirm-large",
        action="store_true",
        help="Allow running more than 5 tasks.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="",
        help="Directory to write per-task stdout/stderr logs.",
    )
    parser.add_argument(
        "--print-output",
        action="store_true",
        help="Print per-task stdout/stderr after completion (enabled by default).",
        default=True,
    )
    parser.add_argument(
        "--no-print-output",
        action="store_false",
        dest="print_output",
        help="Disable printing per-task stdout/stderr.",
    )
    parser.add_argument(
        "--capture-output",
        action="store_true",
        help="Capture stdout/stderr in the JSON summary when no output dir is set.",
    )
    parser.add_argument(
        "--json-summary",
        type=str,
        default="",
        help="Write a JSON summary of results to this path.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without executing.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="opencode/mimo-v2-pro-free",
        help="Model to use in opencode (default: opencode/mimo-v2-pro-free).",
    )
    parser.add_argument(
        "--reasoning",
        type=str,
        default="high",
        help="Reasoning level variant in opencode (e.g. high, max, minimal). Default is high.",
    )
    return parser.parse_args()


def read_tasks(tasks_file: Optional[str], inline_tasks: List[str]) -> List[Task]:
    # Collect tasks from file and positional args, skipping blanks and comments.
    tasks: List[str] = []
    if tasks_file:
        path = Path(tasks_file)
        if not path.exists():
            raise FileNotFoundError(f"Tasks file not found: {tasks_file}")
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                continue
            tasks.append(stripped)
    for task in inline_tasks:
        if task.strip():
            tasks.append(task.strip())
    if not tasks:
        raise ValueError("No tasks provided. Use --tasks-file or positional tasks.")
    return [Task(task_id=i + 1, text=t) for i, t in enumerate(tasks)]


def build_command(
    runner: str,
    runner_args: str,
    task_placeholder: str,
    task_text: str,
    prepend_text: str,
) -> List[str]:
    # Build the command list with optional placeholder replacement.
    base = shlex.split(runner)
    extra = shlex.split(runner_args) if runner_args else []
    args = base + extra
    if prepend_text:
        task_text = f"{prepend_text}\n{task_text}"
    replaced = False
    for i, value in enumerate(args):
        if task_placeholder in value:
            args[i] = value.replace(task_placeholder, task_text)
            replaced = True
    if not replaced:
        args.append(task_text)
    return args


def ensure_output_dir(output_dir: str) -> Optional[Path]:
    # Create output directory if requested.
    if not output_dir:
        return None
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def start_task(task: Task, command: List[str], output_dir: Optional[Path]) -> TaskState:
    # Launch a subprocess for the task with optional log files.
    stdout_path = None
    stderr_path = None
    stdout_file = None
    stderr_file = None
    if output_dir:
        stdout_path = output_dir / f"task-{task.task_id:03d}.stdout"
        stderr_path = output_dir / f"task-{task.task_id:03d}.stderr"
        stdout_file = stdout_path.open("w", encoding="utf-8", errors="replace")
        stderr_file = stderr_path.open("w", encoding="utf-8", errors="replace")
        proc = subprocess.Popen(
            command,
            stdout=stdout_file,
            stderr=stderr_file,
        )
    else:
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    return TaskState(
        task=task,
        command=command,
        process=proc,
        start_time=time.time(),
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        stdout_file=stdout_file,
        stderr_file=stderr_file,
    )


def finish_task(state: TaskState, timeout_seconds: int) -> TaskResult:
    # Finalize the task, capturing output and status.
    stdout_text = None
    stderr_text = None
    if state.stdout_file:
        state.stdout_file.close()
    if state.stderr_file:
        state.stderr_file.close()
    if state.process.stdout or state.process.stderr:
        stdout_text, stderr_text = state.process.communicate()
    duration = time.time() - state.start_time
    status = "completed"
    if timeout_seconds > 0 and duration >= timeout_seconds and state.process.returncode is None:
        status = "timeout"
    return TaskResult(
        task_id=state.task.task_id,
        text=state.task.text,
        status=status,
        returncode=state.process.returncode,
        duration_seconds=round(duration, 2),
        stdout_path=str(state.stdout_path) if state.stdout_path else None,
        stderr_path=str(state.stderr_path) if state.stderr_path else None,
        stdout=stdout_text,
        stderr=stderr_text,
    )


def terminate_process(proc: subprocess.Popen) -> None:
    # Terminate a process and force kill if it does not exit quickly.
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def main() -> int:
    # Parse args and load tasks.
    args = parse_args()
    try:
        tasks = read_tasks(args.tasks_file, args.tasks)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    # Opencode specific validation and argument injection
    if "opencode run" in args.runner:
        if args.model == "opencode/mimo-v2-pro-free" or args.model == "mimo-v2-pro-free":
            # Check availability using opencode models
            try:
                models_output = subprocess.check_output(
                    ["opencode", "models"], text=True, stderr=subprocess.STDOUT
                )
                if "mimo-v2-pro-free" not in models_output:
                    print(
                        "ERROR: Free model 'mimo-v2-pro-free' is no longer available "
                        "and no custom model was specified. Please update the spawn-sub-agents skill.",
                        file=sys.stderr,
                    )
                    return 2
            except subprocess.CalledProcessError as e:
                pass # Ignore if opencode models command fails for some other reason

        # Inject opencode-specific arguments
        extra_args = [f"--model={args.model}", f"--variant={args.reasoning}"]
        if Path("AGENTS.md").exists():
            extra_args.extend(["-f", "AGENTS.md"])

        if args.runner_args:
            args.runner_args += " " + " ".join(shlex.quote(x) for x in extra_args)
        else:
            args.runner_args = " ".join(shlex.quote(x) for x in extra_args)

    # Enforce confirmation for large batches.
    if len(tasks) > 5 and not args.confirm_large:
        print(
            "ERROR: More than 5 tasks requested. Ask the user to confirm or rerun "
            "with --confirm-large.",
            file=sys.stderr,
        )
        return 2

    # Prepare output handling and command construction settings.
    output_dir = ensure_output_dir(args.output_dir)
    max_parallel = max(1, args.max_parallel)
    timeout_seconds = max(0, args.timeout_seconds)
    poll_seconds = max(0.1, args.poll_seconds)
    max_loops = max(1, args.max_loops)

    # Build and optionally print commands for dry runs.
    task_queue = tasks[:]
    running: List[TaskState] = []
    results: List[TaskResult] = []

    # Run tasks with concurrency and polling.
    loops = 0
    while task_queue or running:
        while task_queue and len(running) < max_parallel:
            task = task_queue.pop(0)
            command = build_command(
                args.runner,
                args.runner_args,
                args.task_placeholder,
                task.text,
                args.prepend,
            )
            if args.dry_run:
                print("DRY-RUN:", " ".join(shlex.quote(x) for x in command))
                results.append(
                    TaskResult(
                        task_id=task.task_id,
                        text=task.text,
                        status="dry_run",
                        returncode=None,
                        duration_seconds=0.0,
                        stdout_path=None,
                        stderr_path=None,
                        stdout=None,
                        stderr=None,
                    )
                )
                continue
            running.append(start_task(task, command, output_dir))

        if not running:
            continue

        time.sleep(poll_seconds)
        loops += 1

        # Abort if the max loop count is reached while tasks are still running.
        if loops >= max_loops and running:
            for state in running:
                terminate_process(state.process)
                results.append(
                    TaskResult(
                        task_id=state.task.task_id,
                        text=state.task.text,
                        status="aborted_max_loops",
                        returncode=state.process.returncode,
                        duration_seconds=round(time.time() - state.start_time, 2),
                        stdout_path=str(state.stdout_path) if state.stdout_path else None,
                        stderr_path=str(state.stderr_path) if state.stderr_path else None,
                        stdout=None,
                        stderr=None,
                    )
                )
            print(
                "ERROR: Max loop count reached. Ask the user whether to continue.",
                file=sys.stderr,
            )
            running = []
            break

        # Check running processes for completion or timeout.
        next_running: List[TaskState] = []
        for state in running:
            elapsed = time.time() - state.start_time
            if timeout_seconds > 0 and elapsed >= timeout_seconds:
                terminate_process(state.process)
                result = finish_task(state, timeout_seconds)
                result.status = "timeout"
                results.append(result)
                continue
            if state.process.poll() is not None:
                results.append(finish_task(state, timeout_seconds))
                continue
            next_running.append(state)
        running = next_running

    # Print outputs if requested.
    if args.print_output:
        for result in results:
            if result.stdout is not None:
                print(f"--- task-{result.task_id:03d} stdout ---")
                print(result.stdout.rstrip())
            if result.stderr is not None:
                print(f"--- task-{result.task_id:03d} stderr ---")
                print(result.stderr.rstrip())

    # Write JSON summary if requested.
    if args.json_summary:
        summary_path = Path(args.json_summary)
        summary = [dataclasses.asdict(r) for r in results]
        if not args.capture_output:
            for entry in summary:
                entry.pop("stdout", None)
                entry.pop("stderr", None)
        summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Print a concise status summary.
    completed = sum(1 for r in results if r.status == "completed")
    print(f"Completed: {completed}/{len(results)}")

    # Return non-zero if any task failed or timed out.
    if any(r.status in {"timeout", "aborted_max_loops"} for r in results):
        return 2
    if any(r.returncode not in (0, None) for r in results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
