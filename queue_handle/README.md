- **psub**  

Submits .pbs suffixed job file(s) on the queue specified in the .pbs file on cx1/cx2; logs
new entry/entries in the log file with status of "Q"; creates a new README file if does not
exist, adds new submission entry/entries to README.

Argument following "-f" flag indicates submission of one particular file.

"-a" flag submits all .pbs type file in all child directories to where the script is called. This is particularly handy for umbrella sampling type of simulations.

"-z" flag also searches for all .pbs type file in all child directories to where the script is called. Then, all .pbs files found are cross-referenced with entries in the log file. Only jobs that have
not been run (either jobs not seen in log file or jobs that have been cancelled) are submitted to queue. This is particularly handy for submitting intermediate windows for umbrella
sampling and avoids unnecessary re-runs.


---

- **pdel**  

Deletes specified entry/entries that are running/waiting in the queue; changes the status of referenced entry/entries in the log file to cancelled (X symbol); adds update entry to README.

Argument following "-f" flag are file unique identifiers assigned by the cluster (e.g. "4142404.cx1b") to be deleted.

Argument following "i" flag are numbers. These numbers are interpreted as indices in the log file. Jobs with these indices are cancelled.

Argument following "-n" flag are numbers. These numbers are interpreted as job ordering when "qstat -u userid" is called. Counting start with 0.
"-a" flag cancels all jobs that are running/waiting.

---


- **pupdate**

Monitors jobs displayed when "qstat -u userid" is called. It changes job status from "Q" to "R" when jobs start running. It changes job status from "R" to "F" when jobs are done. In both cases, an update is written to the README file in the associated project directory.

This has been embedded in a bash script (*auto_check.sh*) that automatically re-submit itself after every 56 hours. Inside this script, pupdate is being called every 15 minutes (or any customary time separation). After 56 hrs, a new bash script is submitted, then the old one is terminated. This ensures the jobs are continuously, regularly monitored.

---

- **auto_check.sh**

Submitted to the job queue with the minmial amount of resources. Allows continuous monitoring of the queue and updating log file.
