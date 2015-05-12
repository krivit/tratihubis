Tratihubis
==========

Tratihubis converts Trac tickets to Github issues by using the following steps:

1. The user manually exports the Trac tickets to convert to a CSV file.
2. Tratihubis reads the CSV file and uses the data to create Github issues and
   milestones.

For more information, visit <http://pypi.python.org/pypi/tratihubis/>.

-----
May, 2015

Edits for GENI-NSF use:

 - SQL edits for Trac 0.11 backed by PostgreSQL, and export keywords,
   priorities, and CC list.
 - Support labels from keywords and priorities.
 - Add option `--skipExisting`: If there are existing tickets or pull requests, skip importing
   those tickets.
 - Fix up translator from wiki to Markdown to properly convert links,
   and links to commit messages.
 - Try to support logging the name of the github user even when we
   don't have a Github key for them, and try to have the commenter and
   ticket reporter be the right person where possible.
 - Support repositories belonging to an organization, not the user.
 - Watch the Github API rate limit and sleep until the reset time.
 - Include Trac CC list in ticket comment (stripping email domain from
   the CC list).
 - Change print statements to log messages.

-----
Usage:
1) Export Tickets from Trac
For each `.sql` file included, create a new Trac report
View Tickets -> Available Queries -> Create New Report
Paste in the SQL from one of the files. Run the report, and at the
bottom click the link to save it as CSV.

2) Write a tratihubis config file
See sample-ticket-export.cfg

3) Practice ticket imports
Run your ticket import into a new / practice repository. Check that it
works and the new github issues look good. Then delete that repository.

4) Import tickets
Run command something like: python ./tratihubis.py ../my-ticket-export.cfg --skipExisting --really
