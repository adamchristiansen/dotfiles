# Cronlet

A small, anacron-like periodic job runner.
Pure Python 3, standard library only.
Runs entirely as your user, with no daemon, no root, and no configuration file.
It is designed to be run from **your user crontab**, not the system cron.

Cronlet is meant to be called repeatedly by cron,
typically once per minute, from a single crontab entry.
Each time it runs,
it checks per-job stamp files and executes only those jobs whose interval has elapsed.
You manage jobs by dropping executable scripts into directories; Cronlet handles the rest.

## Why user cron, not system cron?

Cronlet is built for the user crontab (`crontab -e` as your own user).
Everything it touches (jobs, stamps, markers, logs)
lives under your home directory and runs with your ordinary privileges.
It never needs root,
never touches `/etc/cron.d`, `/etc/crontab`, or `/var/spool/cron`,
and should not be installed there.
System-level scheduling is a different world
(different environment, privilege separation, mail routing),
and Cronlet deliberately stays out of it.

## How it works

Cronlet keeps no process alive between invocations.
Every run:

1.  Discovers job scripts under the jobs root
    (`minutely`, `hourly/`, `daily/`, `weekly/`, `monthly/`).
2.  For each job, reads its stamp file (the UTC time of its last run attempt)
    and decides whether it is due.
3.  Runs each due job, guarded by a mutual-exclusion marker (see below), with a global timeout.
4.  Updates the stamp and the log, and exits.

Because due-ness is checked at invocation time,
Cronlet behaves like anacron: missed intervals collapse.
If the machine is suspended for a day,
the daily job runs once at the next invocation,
not once per missed interval.

## Installing

Open **your user crontab** with `crontab -e`
(as your regular user - not `sudo crontab`, not root's crontab), and add one entry:

```
* * * * * $HOME/path/to/cronlet
```

Cron provides a minimal environment.
If your job scripts need tools beyond `/usr/bin` and `/bin`,
set `PATH` at the top of the crontab,
or give each job script a shebang with an absolute interpreter path.
If you do not want cron mailing you Cronlet's stderr on every run,
set `MAILTO=""` in the crontab.
The log file is your history.

## Layout

Jobs are ordinary executable scripts which can use any interpreter and any language.
A job is simply a file with the execute bit set:

```
~/.config/cronlet/minutely/heartbeat
~/.config/cronlet/hourly/backup-cache
~/.config/cronlet/daily/rotate-logs
~/.config/cronlet/weekly/vacuum-db
~/.config/cronlet/monthly/report
```

Runtime state lives in the spool directory (created automatically):

| File                              | Purpose                                     |
|-----------------------------------|---------------------------------------------|
| `<period>.<name>.stamp`           | UTC time of the job's last run attempt      |
| `<period>.<name>.running`         | Exclusion marker while the job is in flight |
| `cronlet.log`                     | Log, capped at `--max-log-lines` lines      |

Default paths follow the XDG convention.
Both roots can be overridden on the command line (useful for testing):

    --spool DIR    state directory  (default: ~/.local/state/cronlet)
    --jobs DIR     jobs root        (default: ~/.config/cronlet)

## Behaviour

### Due-ness

`minutely` jobs run when the elapsed time since the stamp reaches one minute.
With a once-per-minute crontab,
a minutely job runs on essentially every invocation,
unless the previous run is still in flight.

`hourly`, `daily`, and `weekly` jobs run when the elapsed time
since the stamp reaches one hour, one day, or one week respectively.
The phase is set by the first run:
with a once-per-minute crontab, "hourly" really means "about every 60 minutes".

`monthly` jobs are due whenever the current calendar month
differs from the stamp's (anacron semantics), not a rolling 30-day window.

The stamp is updated on every run attempt, including failures and timeouts.
Like anacron, Cronlet does not retry a failing job within the same interval;
it just reports the failure.
A job with a missing, empty, or corrupt stamp is treated as due
and a botched manual edit can never permanently suppress a job.
Nothing is ever deleted; state files are replaced atomically.

### Mutual exclusion (no double runs)

At the start of a job, Cronlet writes a `.running` marker into the spool.
Any other invocation that finds a marker for a job skips that job
and logs `SKIP`, moving on to other jobs.
When the job finishes,
whether success, failure, or timeout,
the marker is removed and the job is marked done via its stamp.

The marker records three things from the kernel:
the job's PID, the kernel's per-process `starttime` counter, and the current boot's `boot_id`.
A later invocation only treats a job as blocked when all three still match the exact live process.
Otherwise the marker is recognised as stale and cleared, and the job becomes runnable again.
This covers:

- Cronlet killed mid-job (dead PID),
- the machine rebooted with a marker left on disk (boot_id differs),
- the rare PID-recycling edge case (starttime differs).

Two Cronlet invocations may therefore run *different* jobs concurrently.
A slow weekly job never holds up the hourly ones,
but the same job is never started twice.

### Timeouts

Every job gets the same timeout, `--timeout`, default 60 seconds.
Jobs run in their own process session,
so on timeout the entire process group (including children spawned by the job) receives SIGKILL.
A hung job occupies at most its timeout before being killed.
A timed-out job counts as failed and is stamped, so it is not re-launched within the same interval.

There is deliberately no per-job timeout configuration:
a job is just an executable file, and Cronlet has no configuration file.
With a once-per-minute crontab,
the 60 s default also means a hung job is cleaned up by the time the next invocation arrives.

## Command line

```
cronlet [--spool DIR] [--jobs DIR] [--timeout SECONDS]
        [--max-log-lines N] [--run-now JOB ...] [--list]
```

| Flag                 | Meaning                                                    |
|----------------------|------------------------------------------------------------|
| `--spool DIR`        | State directory (default `~/.local/state/cronlet`)         |
| `--jobs DIR`         | Jobs root (default `~/.config/cronlet/jobs`)               |
| `--timeout SEC`      | Kill jobs running longer than this (default: 60)           |
| `--max-log-lines N`  | Keep at most N log lines; 0 disables the log file entirely |
| `--run-now JOB...`   | Force-run jobs now, bypassing due-ness                     |
| `--list`             | Show each job and its state (`ok` / `due` / `running`)     |

`--run-now` accepts `all`, bare names, or qualified `period/name` forms.
A forced job that is already running is skipped like any other.

```sh
cronlet --run-now all
cronlet --run-now rotate-logs
cronlet --run-now daily/rotate-logs weekly/vacuum-db
```

## Logging

Every message goes to stderr (visible to cron's MAILTO) and,
unless logging is disabled, to `cronlet.log`.
Once per invocation,
if the log exceeds the cap, the oldest excess lines are discarded via an atomic rewrite.
Messages include `RUN`, `OUT` (job output, line by line),
`DONE`, `FAIL`, `TIME` (timeout), `SKIP` (already running), and `INFO`/`WARN` diagnostics.
The log converges to at most `--max-log-lines` lines between runs;
a very chatty job can briefly exceed the cap mid-run,
and the excess is trimmed on the next invocation.

## Exit status

| Code | Meaning                                                          |
|------|------------------------------------------------------------------|
| 0    | Success - includes "nothing was due" and "job already running"   |
| 1    | At least one job failed or timed out                             |
| 2    | Configuration error - jobs root or a period directory is missing |

Cronlet fails fast rather than fabricating directories:
all four period directories must exist under the jobs root, even if currently empty.

## Troubleshooting

A job shows `running` in `--list` but nothing seems to be going on?
`--list` also verifies markers,
so a stale marker is normally cleared and reported as such on the next invocation.
If a marker somehow persists
(for example on a system without `/proc`, where identity checks fall back to a weaker signal probe),
deleting that single `.running` file restores the job.

## Limitations

- **Platform.**
  Cronlet targets POSIX systems (Linux, the BSDs).
  The PID-identity checks rely on `/proc`, which is Linux-specific.
  On systems without it, marker verification falls back to a weaker signal-0 probe,
  which distinguishes a dead PID but not a recycled one.
  On Linux, full identity checking makes the recycled-PID window effectively vanish,
  since the kernel's starttime counter is monotonic per process.
- **Single user.** Cronlet assumes one user owns the spool and the jobs.
  There is no multi-user coordination, no privilege separation, and no locking across users.
  Two accounts pointing Cronlet at the same spool directory would confuse each other's markers.
- **Environment.**
  Cronlet inherits whatever cron gives it.
  It does not sanitise, extend, or document the environment beyond passing it through;
  job scripts that care must set it themselves.
- **Local only.**
  Jobs run sequentially on one machine, in the order they are discovered, within one invocation.
  There is no parallel execution, distributed awareness, or remote triggering.
- **Identity verification granularity.**
  The starttime counter has finite resolution (measured in clock ticks since boot);
  a PID recycled within the same tick is theoretically indistinguishable.
  In practice this has never been observed;
  it is the residual risk after the boot_id and starttime checks.
- **No catch-up replay.**
  An overdue job runs once, never once per missed interval.
  This is intentional (anacron semantics),
  but it means a job that should conceptually run "once per missed day" needs its own logic.
- **Failures are stamped, not retried.**
  A failing or timed-out job is stamped like a success and waits for the next interval.
  There is no retry count, backoff, or alerting - watch the log or wire `MAILTO` if you need that.
- **No per-job configuration, by design.**
  No timeouts, environments, priorities, or dependencies per job.
  A job that needs special treatment should wrap itself
  (e.g. a wrapper script exporting variables or using flock/nice).
  Cronlet deliberately stays a thin scheduler.
- **Overlap with the cron cadence.**
  With cron firing every minute and a minutely interval of 60 s,
  a `minutely/` job becomes due on every invocation, which is the point.
  The marker keeps it from doubling up if a run straddles a minute boundary:
  cron fires at 12:00:00, the job takes 75 s, the 12:01:00 invocation sees the live marker,
  logs SKIP, and the 12:02:00 run picks it up again.
  So expect a steady rhythm of RUN/DONE lines with occasional SKIPs interleaved for slower runs.
- **Minutely phase drift.**
  Like all the elapsed-time periods,
  "minutely" means "at least one minute apart," not "on the minute."
  The stamp sets the phase,
  so a job finishing at 12:00:43 next becomes due at 12:01:43
  and the clock hands have nothing to do with it.
- **Minutely requires cron to fire every minute.**
  A user who does not run Cronlet every minute (say from the old hourly cron entry)
  will find `minutely/` jobs behave like hourly ones,
  running once per invocation, at most.
- **The 60 s default timeout may bite.**
  A minutely job that hangs occupies exactly one timeout window before SIGKILL,
  then gets stamped and waits a full minute to retry.
  If you plan to keep anything meaningful in `minutely/`,
  that's the period most worth sanity-checking against the global `--timeout`,
  as a job that reliably takes 45 s leaves little margin.
