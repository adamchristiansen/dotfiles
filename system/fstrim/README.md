# fstrim

On systems with SSDs, `fstrim` is used to trim blocks not used by the
filesystem. To see if disks have TRIM support, run:

```sh
lsblk --discard
```

and look at the `DISC-GRAN` column, which will be non-zero for disks with TRIM.

The install script in this directory installs a script which runs
`fstrim` weekly as a cron job.
