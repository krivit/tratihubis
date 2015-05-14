''' Tratihubis converts Trac tickets to Github issues by using the
following steps:

1. The user manually exports the Trac tickets to convert to a CSV file.
2. Tratihubis reads the CSV file and uses the data to create Github issues and milestones.


Installation
============

To install tratihubis, use ``pip`` or ``easy_install``::

  $ pip install tratihubis

If necessary, this also installs the `PyGithub <http://pypi.python.org/pypi/PyGithub/>`_ package.
 * If it does not, do `sudo pip install PyGithub`

Usage
=====

Information about Trac tickets to convert has to be provided in several CSV files. To obtain these CSV files, create
new Trac queries using the SQL statements stored in
`query_tickets.sql <https://github.com/roskakori/tratihubis/blob/master/query_tickets.sql>`_ (or better, the current version from this repo) and
`query_comments.sql <https://github.com/roskakori/tratihubis/blob/master/query_comments.sql>`_.   Then
execute the queries and save the results by clicking "Download in other formats: Comma-delimited Text" and
choosing for example ``/Users/me/mytool/tickets.csv`` and ``/Users/me/mytool/comments.csv`` as output files. Do the same for `query_attachments.sql`.

Next create a config file to describe how to login to Github and what to convert. For an example, see `sample-ticket-export.cfg`. For example, you could
store the following in ``~/mytool/tratihubis.cfg``::

  [tratihubis]
  token = my_github_token
  repo = mytool
  tickets = /Users/me/mytool/tickets.csv
  comments = /Users/me/mytool/comments.csv

Then run::

  $ tratihubis ~/mytool/tratihubis.cfg

This tests that the input data and Github information is valid and writes a log to the console describing
which operations would be performed.

To actually create the Github issues, you need to enable to command line option ``--really``::

  $ tratihubis --really ~/mytool/tratihubis.cfg

Be aware that Github issues and milestones cannot be deleted in case you mess up. Your only remedy is to
remove the whole repository and start anew. So make sure that tratihubis does what you want before you
enable ``--really``. A good practice would be to do a practice import into a junk repository, check that you like the results, then delete that
repository and redo it using your real repository.

Mapping users
-------------

By default all tickets and comments are created by the user specified with the option `token`. For
a private Trac project with a single user this already gives the desired result in the Github project.

In case there are multiple Trac users, you can map them to different Github tokens using the option
`users`. For example::

   users = johndoe: johndoe_token, *: another_token, sally: *

This maps the Trac user ``ohndoe` using John Doe's Github token and everyone else to
`another_token`. Sally is mapped to default token as specified with the `token` option above,
which in this example is `my_github_token`.

The default value is::

  users = *:*

This maps every Trac user to the default token.

You may also use the config `userLogins` to map trac login names to github login names. This is used to capture more information in
the new comments. Be sure to use the correct GitHub login in order for tickets to be properly assigned.

Mapping labels
--------------

Github labels somewhat mimic the functionality Trac stores in the ``type`` and ``resolution`` field of
tickets. By default, Github supports the following labels:

* bug
* duplicate
* enhancement
* invalid
* question
* wontfix

Trac on the other hand has a ``type`` field which by default can be:

* bug
* enhancement
* task

Furthermore closed Trac tickets have a ``resolution`` which, among others, can be:

* duplicate
* invalid
* wontfix

The ``labels`` config option allows you to map Trac fields to Github labels. For example::

  labels = type=defect: bug, type=enhancement: enhancement, resolution=wontfix: wontfix

Here, ``labels`` is a comma separated list of mappings taking the form
``<trac-field>=<trac-value>:<github-label>``.

In case types or labels contain other characters than ASCII letters, digits and underscore (_), put them
between quotes::

  labels = type="software defect": bug

This script will also support labels of type `priority` and `keyword` matching the corresponding Trac field.

``IMPORTANT``: You must pre-create all the above labels in Github for the import to complete.

Note that components will also map to labels if you supply the config option `addComponentLabels=true`. In this case, the script will create the needed label if not present.

Attachments
-----------

You can find some notes on this in `issue #19 <https://github.com/roskakori/tratihubis/issues/19>`.

In short, Github doesn't directly support attachments. Instead, this script can create a comment that includes a link to a document elsewhere.
For example, you can create a Gist for the attachment, or create a repository. Run `query_attachments.sql` to get the paths / descriptions of attachments.
Then set `attachmentsPrefix` in the config. The script will create a comment referencing the URL <prefix>/<issue#>/<attachmentName>.

Converting Trac Wiki Markup to Github Markdown
----------------------------------------------

Tratihubis makes an attempt to convert Trac Wiki markup into
Github markdown with the use of a number of regular expression
substitutions. This is far from a perfect process so care should be
taken and the the regular expressions may need amending on a case by
case basis. This conversion process also tries to preserve links
between tickets with expressions such as `ticket:XX` converted to
`issue #YY`. Also links in Trac such as `rXXXX` when referring to
subversion changeset will link back to the original Trac repository if
required. Use::

  convert_text = true

in the `.cfg` file to attempt the markup conversion. Stipulate the
Trac repository with::

  trac_url = https://trac/url

Limitations
===========

The author of Github issues and comments always is the user specified in the config, even if a different
user opened the original Trac ticket or wrote the original Trac comment - except where the config file supplies a `user` and `userLogin` for 
this other user.

Github issues and comments have the current time as time stamp instead of the time from Trac.

The due date of Trac milestones is not migrated to Github milestones, so when the conversion is done, you
have to set it manually. Similarly, closed milestones will not be closed.

Trac milestones without any tickets are not converted to Github milestone.

Support
=======

In case of questions and problems, open an issue at <https://github.com/roskakori/tratihubis/issues>.

To obtain the source code or create your own fork to implement fixes or improvements, visit
<https://github.com/roskakori/tratihubis>.


License
=======

Copyright (c) 2012-2013, Thomas Aglassinger. All rights reserved. Distributed under the
`BSD License <http://www.opensource.org/licenses/bsd-license.php>`_.


Changes
=======

2015-05

(Contributed by Aaron Helsinger)

 * Fixes to translation of wiki markup
 * Revised SQL to match my environment (Trac 0.11 backed by PostgreSQL)
  * And export CC list, keywords, priority
 * Add support for labels from keywords, priorities
 * Add option `--skipExisting` to skip tickets whose # conflicts with a pre-existing issue / pull request.
 * Watch the Github rate limit and sleep until the reset time if needed.
 * Include the CC list (minus email domain) in comments
 * Work on including the proper Github user login and having the proper Github user be the reporter / assignee.
 * Cache all Github API objects, optionally calling update() if you specify --updateObjects
 * New config option `ticketToStartAt` to support resuming an import

Version 1.0, 2014-06-14

(Contributed by Daniel Wheeler)

* Changed user authentication from password to token.
* Added basic translation of Wiki markup.
* Added conversion of ticket:xx links.
* Added backlink to from Github issue to original Trac link.

Version 0.5, 2013-02-13

(Contributed by Steven Di Rocco)

* Added support for file attachments.
* Added work around for information lost due GitHub API limitations:
  * Added trac commenter and date at the top of each comment.
  * Added automatic comment to each isseu showing original author, date authored, and last modification date.
* Fixed API calls to work with PyGithub 1.8.

Version 0.4, 2012-05-04

* Added config option ``labels`` to map Trac status and resolution to  Github labels.

Version 0.3, 2012-05-03

* Added config option ``comments`` to convert Trac ticket comments.
* Added closing of issue for which the corresponding Trac ticket has been closed already.
* Added validation of users issues are assigned to. They must have an active Github user.

Version 0.2, 2012-05-02

* Added config option ``users`` to map Trac users to Github users.
* Added binary in order to run ``tratihubis`` instead of ``python -m tratihubis``.
* Changed supposed issue number in log to take existing issues in account.

Version 0.1, 2012-05-01

* Initial release.
'''
# Copyright (c) 2012-2013, Thomas Aglassinger
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of Thomas Aglassinger nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
import codecs
import collections
import ConfigParser
import csv
import github
import logging
import optparse
import os.path
import StringIO
import sys
import token
import tokenize
import datetime
import dateutil.parser

from translator import Translator, NullTranslator

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s: %(message)s',datefmt='%H:%M:%S')
_log = logging.getLogger('tratihubis')

__version__ = "1.0"

_SECTION = 'tratihubis'
_OPTION_LABELS = 'labels'
_OPTION_USERS = 'users'

_validatedGithubTokens = set()
_tokenToHubMap = {}

_FakeMilestone = collections.namedtuple('_FakeMilestone', ['number', 'title'])
_FakeIssue = collections.namedtuple('_FakeIssue', ['number', 'title', 'body', 'state'])

# For storing if we should call update() on github objects
_doUpdateVar = {}

def _setUpdate(doit=False):
    if doit:
        _doUpdateVar['val'] = True
    else:
        _doUpdateVar['val'] = False

def _doUpdate():
    return _doUpdateVar['val']

csv.field_size_limit(sys.maxsize)

class _ConfigError(Exception):
    def __init__(self, option, message):
        assert option is not None
        assert message is not None
        Exception.__init__(self, u'cannot process config option "%s" in section [%s]: %s'
                % (option, _SECTION, message))


class _CsvDataError(Exception):
    def __init__(self, csvPath, rowIndex, message):
        assert csvPath is not None
        assert rowIndex is not None
        assert rowIndex >= 0
        assert message is not None
        Exception.__init__(self, u'%s:%d: %s' % (os.path.basename(csvPath), rowIndex + 1, message))


class _UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):  # @ReservedAssignment
        result = self.reader.next().encode("utf-8")
        return result


class _UnicodeCsvReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = _UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):  # @ReservedAssignment
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


class _LabelTransformations(object):
    def __init__(self, repo, definition):
        assert repo is not None

        self._transformations = []
        self._labelMap = {}
        if definition:
            self._buildLabelMap(repo)
            self._buildTransformations(repo, definition)

    def _buildLabelMap(self, repo):
        assert repo is not None

        _log.info(u'analyze existing labels (read from repo)')
        self._labelMap = {}
        for label in repo.get_labels():
            _log.debug(u'  found label "%s"', label.name)
            self._labelMap[label.name] = label
        _log.info(u'  found %d labels', len(self._labelMap))

    def _buildTransformations(self, repo, definition):
        assert repo is not None
        assert definition is not None

        STATE_AT_TRAC_FIELD = 'f'
        STATE_AT_COMPARISON_OPERATOR = '='
        STATE_AT_TRAC_VALUE = 'v'
        STATE_AT_COLON = ':'
        STATE_AT_LABEL = 'l'
        STATE_AT_COMMA = ','

        self._transformations = []
        state = STATE_AT_TRAC_FIELD
        for tokenType, tokenText, _, _, _ in tokenize.generate_tokens(StringIO.StringIO(definition).readline):
            if tokenType == token.STRING:
                tokenText = tokenText[1:len(tokenText) - 1]
            if state == STATE_AT_TRAC_FIELD:
                tracField = tokenText
                tracValue = None
                labelValue = None
                state = STATE_AT_COMPARISON_OPERATOR
            elif state == STATE_AT_COMPARISON_OPERATOR:
                if tokenText != '=':
                    raise _ConfigError(_OPTION_LABELS,
                            u'Trac field "%s" must be followed by \'=\' instead of %r'
                            % (tracField, tokenText))
                state = STATE_AT_TRAC_VALUE
            elif state == STATE_AT_TRAC_VALUE:
                tracValue = tokenText
                state = STATE_AT_COLON
            elif state == STATE_AT_COLON:
                if tokenText != ':':
                    raise _ConfigError(_OPTION_LABELS,
                            u'value for comparison "%s" with Trac field "%s" must be followed by \':\' instead of %r'
                            % (tracValue, tracField, tokenText))
                state = STATE_AT_LABEL
            elif state == STATE_AT_LABEL:
                labelValue = tokenText
                if not labelValue in self._labelMap:
                    raise _ConfigError(_OPTION_LABELS,
                            u'unknown label "%s" must be replaced by one of: %s'
                            % (labelValue, sorted(self._labelMap.keys())))
                self._transformations.append((tracField, tracValue, labelValue))
                state = STATE_AT_COMMA
            elif state == STATE_AT_COMMA:
                if (tokenType != token.ENDMARKER) and (tokenText != ','):
                    raise _ConfigError(_OPTION_LABELS,
                            u'label transformation for Trac field "%s" must end with \',\' instead of %r'
                            % (tracField, tokenText))
                state = STATE_AT_TRAC_FIELD
            else:
                assert False, u'state=%r' % state

    def labelFor(self, tracField, tracValue):
        assert tracField
        assert tracValue is not None
        result = None
        transformationIndex = 0
        while (result is None) and (transformationIndex < len(self._transformations)):
            transformedField, transformedValueToCompareWith, transformedLabel = \
                    self._transformations[transformationIndex]
            if (transformedField == tracField) and (transformedValueToCompareWith == tracValue):
                assert transformedLabel in self._labelMap
                result = self._labelMap[transformedLabel]
            else:
                transformationIndex += 1
        return result

def _getConfigOption(config, name, required=True, defaultValue=None, boolean=False):
    try:
        if boolean:
            result = config.getboolean(_SECTION, name)
        else:
            result = config.get(_SECTION, name)
    except ConfigParser.NoOptionError:
        if required:
            raise _ConfigError(name, 'config must contain a value for this option')
        result = defaultValue
    except ConfigParser.NoSectionError:
        raise _ConfigError(name, u'config must contain this section')
    return result


def _shortened(text):
    assert text is not None
    THRESHOLD = 30
    if len(text) > THRESHOLD:
        result = text[:THRESHOLD] + '...'
    else:
        result = text
    return result


def _addNewLabel(label, repo):
    if label not in [l.name for l in repo.get_labels()]:
        repo.create_label(label, '5319e7')

def _tracTicketMaps(ticketsCsvPath):
    """
    Sequence of maps where each items describes the relevant fields of each row from the tickets CSV exported
    from Trac.
    """
    EXPECTED_COLUMN_COUNT = 15
    _log.info(u'read ticket details from "%s"', ticketsCsvPath)
    with open(ticketsCsvPath, "rb") as ticketCsvFile:
        csvReader = _UnicodeCsvReader(ticketCsvFile)
        hasReadHeader = False
        for rowIndex, row in enumerate(csvReader):
            columnCount = len(row)
            if columnCount != EXPECTED_COLUMN_COUNT:
                raise _CsvDataError(ticketsCsvPath, rowIndex,
                        u'ticket row must have %d columns but has %d: %r' %
                        (EXPECTED_COLUMN_COUNT, columnCount, row))
            if hasReadHeader:
                ticketMap = {
                    'id': long(row[0]),
                    'type': row[1],
                    'owner': row[2],
                    'reporter': row[3],
                    'milestone': row[4],
                    'status': row[5],
                    'resolution': row[6],
                    'summary': row[7],
                    'description': row[8],
#                    'createdtime': datetime.datetime.fromtimestamp(long(row[9])),
#                    'modifiedtime': datetime.datetime.fromtimestamp(long(row[10])),
                    'createdtime': dateutil.parser.parse(str(row[9])),
                    'modifiedtime': dateutil.parser.parse(str(row[10])),
                    'component': row[11],
                    'priority': row[12],
                    'keywords': row[13],
                    'cc': row[14]
                }
                if ticketMap['keywords'] and str(ticketMap['keywords']).strip() != "":
                    kws = str(ticketMap['keywords']).strip()
                    kwArray = []
                    for kw in ticketMap['keywords'].split():
                        kwArray.append(kw.strip())
                    ticketMap['keywords'] = kwArray
                yield ticketMap
            else:
                hasReadHeader = True


def _createMilestoneMap(repo):
    def addMilestones(targetMap, state):
        for milestone in repo.get_milestones(state=state):
            _log.debug(u'  %d: %s', milestone.number, milestone.title)
            targetMap[milestone.title] = milestone
    result = {}
    _log.info(u'analyze existing milestones (read milestones, both open and closed)')
    addMilestones(result, 'open')
    addMilestones(result, 'closed')
    _log.info(u'  found %d milestones', len(result))
    return result


def _createIssueMap(repo):
    def addIssues(targetMap, state):
        _log.debug("Looking up all issues that are %s", state)
        for issue in repo.get_issues(state=state):
            _log.debug(u'  %s: (%s) %s', issue.number, issue.state, issue.title)
            targetMap[issue.number] = issue
    result = {}
    _log.info(u'analyze existing issues')
    addIssues(result, 'open')
    addIssues(result, 'closed')
    _log.info(u'  found %d issues', len(result))
    return result


def _createTicketToCommentsMap(commentsCsvPath):
    EXPECTED_COLUMN_COUNT = 4
    result = {}
    if commentsCsvPath is not None:
        _log.info(u'read ticket comments from "%s"', commentsCsvPath)
        with open(commentsCsvPath, "rb") as commentsCsvFile:
            csvReader = _UnicodeCsvReader(commentsCsvFile)
            hasReadHeader = False
            for rowIndex, row in enumerate(csvReader):
                columnCount = len(row)
                if columnCount != EXPECTED_COLUMN_COUNT:
                    raise _CsvDataError(commentsCsvPath, rowIndex,
                            u'comment row must have %d columns but has %d: %r' %
                            (EXPECTED_COLUMN_COUNT, columnCount, row))
                if hasReadHeader:
                    commentMap = {
                        'id': long(row[0]),
#                        'date': datetime.datetime.fromtimestamp(long(row[1])),
                        'date': dateutil.parser.parse(str(row[1])),
                        'author': row[2],
                        'body': row[3],
                    }
                    ticketId = commentMap['id']
                    ticketComments = result.get(ticketId)
                    if ticketComments is None:
                        ticketComments = []
                        result[ticketId] = ticketComments
                    ticketComments.append(commentMap)
                else:
                    hasReadHeader = True
    return result

def is_int(s):
    try:
        long(s)
        return True
    except ValueError:
        return False

def _createTicketsToAttachmentsMap(attachmentsCsvPath, attachmentsPrefix):
    EXPECTED_COLUMN_COUNT = 4
    result = {}

    if attachmentsCsvPath is not None and attachmentsPrefix is None:
        _log.error(u'attachments csv path specified but attachmentsprefix is not\n')
        return result

    if attachmentsCsvPath is not None:
        _log.info(u'read attachments from "%s"', attachmentsCsvPath)
    else:
        return result

    with open(attachmentsCsvPath, "rb") as attachmentsCsvFile:
        attachmentsReader = _UnicodeCsvReader(attachmentsCsvFile)
        hasReadHeader = False
        for rowIndex, row in enumerate(attachmentsReader):
            columnCount = len(row)
            if columnCount != EXPECTED_COLUMN_COUNT:
                raise _CsvDataError(attachmentsCsvPath, rowIndex,
                    u'attachment row must have %d columns but has %d: %r' %
                    (EXPECTED_COLUMN_COUNT, columnCount, row))
            if hasReadHeader:
                id_string = row[0]
                if is_int(id_string):
                    attachmentMap = {
                    'id': long(id_string),
                    'author': row[3],
                    'filename': row[1],
#                    'date': datetime.datetime.fromtimestamp(long(row[2])),
                    'date': dateutil.parser.parse(str(row[2])),
                    'fullpath': u'%s/%s/%s' % (attachmentsPrefix, row[0], row[1]),
                    }
                    if not attachmentMap['id'] in result:
                        result[attachmentMap['id']] = [attachmentMap]
                    else:
                        result[attachmentMap['id']].append(attachmentMap)
            else:
                hasReadHeader = True

    return result

def createTicketsToIssuesMap(ticketsCsvPath, existingIssues, firstTicketIdToConvert, lastTicketIdToConvert, skipExisting):
    ticketsToIssuesMap = dict()
    fakeIssueId = 1 + len(existingIssues)
    # FIXME: This probably doesn't do the right thing if the issues to convert doesn't start with 1
    if skipExisting:
        _log.debug("Skipping existing tickets. The tickets to issues map will pretend there are no existing issues.")
        fakeIssueId = 1
    else:
        if len(existingIssues) > 0:
            _log.debug("Due to existing %d issues, 1st ticket %d will become issue %d", len(existingIssues), firstTicketIdToConvert, fakeIssueId)
        else:
            _log.debug("No existing issues. 1st ticket %d will be issue %d", firstTicketIdToConvert, fakeIssueId)
    for ticketMap in _tracTicketMaps(ticketsCsvPath):
        ticketId = ticketMap['id']
        if (ticketId >= firstTicketIdToConvert) \
          and ((ticketId <= lastTicketIdToConvert) or (lastTicketIdToConvert == 0)):
          ticketsToIssuesMap[int(ticketId)] = fakeIssueId
          fakeIssueId += 1

    return ticketsToIssuesMap

def migrateTickets(hub, repo, defaultToken, ticketsCsvPath,
                   commentsCsvPath=None, attachmentsCsvPath=None,
                   firstTicketIdToConvert=1, lastTicketIdToConvert=0,
                   labelMapping=None, userMapping="*:*",
                   attachmentsPrefix=None, pretend=True,
                   trac_url=None, convert_text=False, ticketsToRender=False, addComponentLabels=False, userLoginMapping="*:*", skipExisting=False):
    
    assert hub is not None
    assert repo is not None
    assert ticketsCsvPath is not None
    assert userMapping is not None
    _log.debug("Doing getuser")
    baseUserO = _getUserFromHub(hub)
    baseUser = baseUserO.login
    #baseUser = hub.get_user().login

    tracTicketToCommentsMap = _createTicketToCommentsMap(commentsCsvPath)
    tracTicketToAttachmentsMap = _createTicketsToAttachmentsMap(attachmentsCsvPath, attachmentsPrefix)
    existingIssues = _createIssueMap(repo)
    existingMilestones = _createMilestoneMap(repo)
    tracToGithubUserMap = _createTracToGithubUserMap(hub, userMapping, defaultToken)
    tracToGithubLoginMap = _createTracToGithubLoginMap(hub, userLoginMapping, baseUser)
    labelTransformations = _LabelTransformations(repo, labelMapping)
    ticketsToIssuesMap = createTicketsToIssuesMap(ticketsCsvPath, existingIssues, firstTicketIdToConvert, lastTicketIdToConvert, skipExisting)

    if convert_text:
        Translator_ = Translator
    else:
        Translator_ = NullTranslator

    translator = Translator_(repo, ticketsToIssuesMap, trac_url=trac_url, attachmentsPrefix=attachmentsPrefix)
        
    def possiblyAddLabel(labels, tracField, tracValue):
        label = labelTransformations.labelFor(tracField, tracValue)
        if label is not None:
            _log.info('  add label "%s"', label.name)
            if not pretend:
                labels.append(label.name)

    fakeIssueId = 1 + len(existingIssues)
    createdCount = 0
    for ticketMap in _tracTicketMaps(ticketsCsvPath):
        _log.debug("Rate limit status: %r resets at %r", hub.rate_limiting, datetime.datetime.fromtimestamp(hub.rate_limiting_resettime))
        # rate limit is 5000 per hour, after which you get an error: "403 Forbidden" with message "API rate limit exceeded...."
        if hub.rate_limiting[0] < 10:
            # This solution to the rate limit is fairly crude: when we're about to hit the limit, sleep until the reset time.
            # That could be nearly an hour (maybe). An alternative would be to (a) try to catch the error when you hit the limit and sleep then, and/or (b)
            # sleep 10 minutes and retry when we need to, or (c) sleep periodically if we are burning up our API calls quickly
            _log.warning("Rate limit nearly exceeded. Sleeping until reset time of %s", datetime.datetime.fromtimestamp(hub.rate_limiting_resettime))
            # FIXME: TZ handling
            now = datetime.datetime.now()
            sleeptime = datetime.datetime.fromtimestamp(hub.rate_limiting_resettime) - now
            _log.info("Will sleep for %d seconds. See you at %s! Zzz.....", int(sleeptime.total_seconds()), datetime.datetime.fromtimestamp(hub.rate_limiting_resettime))
            import time
            time.sleep(int(sleeptime.total_seconds()) + 1)
            _log.info(" ... And, we're back!")

        # FIXME: Parse hub.rate_limiting "(4990,5000)". If 1st # < somethign small, say 10, then at least warn, and maybe cleep until the reset time.
        ticketId = ticketMap['id']
        # FIXME: This probably doesn't do the right thing if the issues to convert doesn't start with 1
        if skipExisting and ticketId in existingIssues:
            iss = existingIssues.get(ticketId)
            _log.debug("Skipping Trac ticket %s because its ID overlaps an existing issue %s:%s", ticketId, iss.number, iss.title)
            continue
        _log.debug("Looking at ticket %s", ticketId)
        title = ticketMap['summary']
        renderTicket = True
        if ticketsToRender:
            if not ticketId in ticketsToRender:
                renderTicket = False
        if renderTicket and (ticketId >= firstTicketIdToConvert) \
                and ((ticketId <= lastTicketIdToConvert) or (lastTicketIdToConvert == 0)):
            body = ticketMap['description']
            tracReporter = ticketMap['reporter'].strip()
            tokenReporter = _tokenFor(hub, tracToGithubUserMap, tracReporter)
            _hub = _getHub(tokenReporter)
            tracOwner = ticketMap['owner'].strip()
            tokenOwner = _tokenFor(hub, tracToGithubUserMap, tracOwner)
            _hubOwner = _getHub(tokenOwner)
            _log.debug("Repo will be %s", '{0}/{1}'.format(repo.owner.login, repo.name))
            _repo = _getRepoNoUser(hub, '{0}/{1}'.format(repo.owner.login, repo.name))
            #_repo = _hub.get_repo('{0}/{1}'.format(repo.owner.login, repo.name))
            #_repo = _getRepo(hub, '{0}/{1}'.format(repo.owner.login, repo.name))
            githubAssignee = _getUserFromHub(_hubOwner)
            #githubAssignee = _hubOwner.get_user()
            ghAssigneeLogin = _loginFor(tracToGithubLoginMap, tracOwner)
            ghlRaw = tracToGithubLoginMap.get(tracOwner)
            ghlIsDefault = False
            if ghlRaw is None or ghlRaw == '*':
                ghlIsDefault = True
            _log.debug("For ticket %d got tracOwner %s, token %s, hub user's login: %s, ghAssigneeLogin from lookup on tracOwner: %s, ghlRaw: %s, isDefault: %s", ticketId, tracOwner, tokenOwner, githubAssignee.login, ghAssigneeLogin, ghlRaw, ghlIsDefault)
            milestoneTitle = ticketMap['milestone'].strip()
            if len(milestoneTitle) != 0:
                if milestoneTitle not in existingMilestones:
                    _log.info(u'add milestone: %s', milestoneTitle)
                    _log.info(u'Existing milestones: %s', existingMilestones)
                    if not pretend:
                        newMilestone = repo.create_milestone(milestoneTitle)
                    else:
                        newMilestone = _FakeMilestone(len(existingMilestones) + 1, milestoneTitle)
                    existingMilestones[milestoneTitle] = newMilestone
                milestone = existingMilestones[milestoneTitle]
                milestoneNumber = milestone.number
            else:
                milestone = None
                milestoneNumber = 0
            _log.info(u'convert ticket #%d: %s', ticketId, _shortened(title))

            title = translator.translate(title)
            origbody = body
            body = translator.translate(body, ticketId=ticketId)
            if body != origbody and pretend:
                _log.debug("Translated body from '%s' to '%s'", origbody, body)

            dateformat = "%m-%d-%Y at %H:%M"
            ticketString = '#{0}'.format(ticketId)
            if trac_url:
                ticket_url = '/'.join([trac_url, 'ticket', str(ticketId)])
                ticketString = '[{0}]({1})'.format(ticketString, ticket_url)
            legacyInfo = u"\n\n _Imported from trac ticket %s,  created by %s on %s, last modified: %s_\n" \
                         % (ticketString, ticketMap['reporter'], ticketMap['createdtime'].strftime(dateformat),
                         ticketMap['modifiedtime'].strftime(dateformat))
            if ticketMap['cc'] and str(ticketMap['cc']).strip() != "":
                # strip out email domains (privacy)
                import re
                ccList = ticketMap['cc']
                sub = re.compile(r"([^\@\s\,]+)(@[^\,\s]+)?", re.DOTALL)
                ccListNew = sub.sub(r"\1@...", ccList)
                if ccListNew != ccList:
                    _log.debug("Edited ccList from '%s' to '%s'", ccList, ccListNew)
                legacyInfo += u"   CCing: %s" % ccListNew

            body += legacyInfo

            if ticketsToRender:
                _log.info(u'body of ticket:\n%s', body)
            
            githubAssigneeLogin = None
            if ghAssigneeLogin:
                githubAssigneeLogin = ghAssigneeLogin
            elif githubAssignee:
                githubAssigneeLogin = githubAssignee.login
            _log.debug("Found ghAssignee login: %s", githubAssigneeLogin)

            # Argh and FIXME
            # After carefully setting things up to use just a login name for assigning tickets, that seems to fail
            # for a login that I think should have worked, I got:
#GithubException: 422 {u'documentation_url': u'https://developer.github.com/v3/issues/#create-an-issue', u'message': u'Validation Failed', u'errors': [{u'field': u'assignee', u'code': u'invalid', u'resource': u'Issue', u'value': u'tcmitchell'}]}
            # So for now, assign things to me or leave them unassigned.

            # Hmm. Nope, the assignee should be a login. That much is true. However, the _repo instance needs to have been created
            # with a token that matches the login.
            useLogin = None
            if githubAssignee and ((not ghlIsDefault) or githubAssignee.login != baseUser) and ghAssigneeLogin == githubAssignee.login:
                useLogin = githubAssignee.login
                _log.debug("Will use the token of the owner with login %s", useLogin)
            else:
                _log.debug("Either had no ghAssignee or it is assigned to me by default, so leave it unassigned")
            issue = None
            if not pretend:
                if milestone is None:
                    if useLogin:
                        issue = _repo.create_issue(title, body, assignee=useLogin)
                    else:
                        issue = _repo.create_issue(title, body)
                else:
                    if useLogin:
#                    if githubAssigneeLogin:
                        issue = _repo.create_issue(title, body, assignee=useLogin, milestone=milestone)
                    else:
                        issue = _repo.create_issue(title, body, milestone=milestone)
            else:
                issue = _FakeIssue(fakeIssueId, title, body, 'open')
                fakeIssueId += 1
            createdCount += 1
                
#            if githubAssigneeLogin:
            if useLogin:
                _log.info(u'  issue #%s: owner=%s-->%s; milestone=%s (%d)',
                          issue.number, tracOwner, useLogin, milestoneTitle, milestoneNumber)
            else:
                _log.info(u'  issue #%s: owner=%s--><unassigned>; milestone=%s (%d)',
                          issue.number, tracOwner, milestoneTitle, milestoneNumber)

            labels = []
            possiblyAddLabel(labels, 'type', ticketMap['type'])
            possiblyAddLabel(labels, 'resolution', ticketMap['resolution'])
            possiblyAddLabel(labels, 'priority', ticketMap['priority'])
            for kw in ticketMap['keywords']:
                possiblyAddLabel(labels, 'keyword', kw)
            
            if addComponentLabels and ticketMap['component'] != 'None':
                if not pretend:
                    labels.append(ticketMap['component'])
            if not pretend:
                for l in labels:
                    _addNewLabel(l, repo)
            if len(labels) > 0:
                _hub = _getHub(defaultToken)
                _repo = _getRepoNoUser(_hub, '{0}/{1}'.format(repo.owner.login, repo.name))
                #_repo = _hub.get_repo('{0}/{1}'.format(repo.owner.login, repo.name))
                _issue = _getIssueFromRepo(_repo,issue.number)
                #_issue = _repo.get_issue(issue.number)
                _log.debug("Setting labels on issue %d: %s", issue.number, labels)
                _issue.edit(labels=labels)
                
            attachmentsToAdd = tracTicketToAttachmentsMap.get(ticketId)
            if attachmentsToAdd is not None:
                for attachment in attachmentsToAdd:
                    token = _tokenFor(repo, tracToGithubUserMap, attachment['author'], False)
                    attachmentAuthor = _userFor(token)
                    _hub = _getHub(token)
                    _repo = _getRepoNoUser(_hub, '{0}/{1}'.format(repo.owner.login, repo.name))
                    #_repo = _hub.get_repo('{0}/{1}'.format(repo.owner.login, repo.name))
                    attachmentAuthorLogin = _loginFor(tracToGithubLoginMap, attachment['author'])
                    if attachmentAuthorLogin and attachmentAuthorLogin != baseUser:
                        legacyInfo = u"_%s (%s) attached [%s](%s) on %s_\n"  \
                                     % (attachment['author'], attachmentAuthorLogin, attachment['filename'], attachment['fullpath'], attachment['date'].strftime(dateformat))
                        _log.info(u'  added attachment from %s', attachmentAuthorLogin)
                    else:
                        legacyInfo = u"_%s attached [%s](%s) on %s_\n"  \
                                     % (attachment['author'], attachment['filename'], attachment['fullpath'], attachment['date'].strftime(dateformat))
                        _log.info(u'  added attachment from %s', attachmentAuthor.login)

                    if ticketsToRender:
                        _log.info(u'attachment legacy info:\n%s',legacyInfo)
                        
                    if not pretend:
                        _issue = _getIssueFromRepo(_repo,issue.number)
                        #_issue = _repo.get_issue(issue.number)
                        assert _issue is not None
                        _issue.create_comment(legacyInfo)

            commentsToAdd = tracTicketToCommentsMap.get(ticketId)
            if commentsToAdd is not None:
                for comment in commentsToAdd:
                    token = _tokenFor(repo, tracToGithubUserMap, comment['author'], False)
                    commentAuthor = _userFor(token)
                    commentAuthorLogin = _loginFor(tracToGithubLoginMap, comment['author'])
                    _hub = _getHub(token)
                    _repo = _getRepoNoUser(_hub, '{0}/{1}'.format(repo.owner.login, repo.name))
                    #_repo = _hub.get_repo('{0}/{1}'.format(repo.owner.login, repo.name))
                    
                    if commentAuthorLogin and commentAuthorLogin != baseUser:
                        commentBody = u"%s\n\n_Trac comment by %s (github user: %s) on %s_\n" % (comment['body'], comment['author'], commentAuthorLogin, comment['date'].strftime(dateformat))
                        
                        _log.info(u'  add comment by %s: %r', commentAuthorLogin, _shortened(commentBody))
                    else:
                        commentBody = u"%s\n\n_Trac comment by %s on %s_\n" % (comment['body'], comment['author'], comment['date'].strftime(dateformat))

                        _log.info(u'  add comment by %s: %r', commentAuthor.login, _shortened(commentBody))

                    commentBody = translator.translate(commentBody, ticketId=ticketId)

                    if ticketsToRender:
                        _log.info(u'commentBody:\n%s',commentBody)
                    
                    if not pretend:
                        # Here we use the token from the users map
                        # so the real github user creates teh comment if possible
                        _issue = _getIssueFromRepo(_repo,issue.number)
                        #_issue = _repo.get_issue(issue.number)
                        assert _issue is not None
                        _issue.create_comment(commentBody)

            if ticketMap['status'] == 'closed':
                _log.info(u'  close issue')
                if not pretend:
                    issue.edit(state='closed')
        else:
            _log.info(u'skip ticket #%d: %s', ticketId, title)
    if pretend:
        _log.info(u'Finished pretend creating %d issues from %d tickets', createdCount, len(ticketsToIssuesMap))
    else:
        _log.info(u'Finished really creating %d issues from %d tickets', createdCount, len(ticketsToIssuesMap))

def _parsedOptions(arguments):
    assert arguments is not None

    # Parse command line options.
    Usage = 'usage: %prog [options] CONFIGFILE\n\n  Convert Trac tickets to Github issues.'
    parser = optparse.OptionParser(
        usage=Usage,
        version="%prog " + __version__
    )
    parser.add_option("-R", "--really", action="store_true", dest="really",
                      help="really perform the conversion")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      help="log all actions performed in console")
    parser.add_option("-s", "--skipExisting", action="store_true", default=False, dest="skipExisting",
                      help="Skip tickets whose # overlaps an existing GitHub Issue (default %default)")
    parser.add_option("--updateObjects", action="store_true", default=False,
                      help="Update cached Github objects (each is a 5sec call that only counts against rate limit if the object changed; usually not needed)")
    (options, others) = parser.parse_args(arguments)
    if len(others) == 0:
        parser.error(u"CONFIGFILE must be specified")
    elif len(others) > 1:
        parser.error(u"unknown options must be removed: %s" % others[1:])
    if options.verbose:
        _log.setLevel(logging.DEBUG)

    configPath = others[0]

    return options, configPath

def _validateGithubUser(hub, tracUser, token):
    assert hub is not None
    assert tracUser is not None
    assert token is not None
    if token not in _validatedGithubTokens:
        try:
            _log.debug(u'  check for token "%s"', token)
            _hub = _getHub(token)
            githubUser = _getUserFromHub(_hub)
            _log.debug(u'  user is "%s"', githubUser.login)
        except Exception, e:
            import traceback
            _log.debug("Error from Github API: %s", traceback.format_exc())
            # FIXME: After PyGithub API raises a predictable error, use  "except WahteverException".
            raise _ConfigError(_OPTION_USERS,
                    u'Trac user "%s" must be mapped to an existing Github users token instead of "%s" = "%s"'
                    % (tracUser, githubUser, token))
        _validatedGithubTokens.add(token)


def _createTracToGithubUserMap(hub, definition, defaultToken):
    result = {}
    for mapping in definition.split(','):
        words = [word.strip() for word in mapping.split(':')]
        if words:
            if len(words) != 2:
                raise _ConfigError(_OPTION_USERS,
                        u'mapping must use syntax "trac-user: token" but is: "%s"' % mapping)
            tracUser, token = words
            if token == '*':
                token = defaultToken
            # if len(tracUser) == 0:
            #     raise _ConfigError(_OPTION_USERS, u'Trac user must not be empty: "%s"' % mapping)
            if len(token) == 0:
                raise _ConfigError(_OPTION_USERS, u'Token must not be empty: "%s"' % mapping)
            existingMappedGithubUser = result.get(tracUser)
            if existingMappedGithubUser is not None:
                raise _ConfigError(_OPTION_USERS,
                        u'Trac user "%s" must be mapped to only one token instead of "%s" and "%s"'
                         % (tracUser, existingMappedGithubUser, token))
            result[tracUser] = token
            if token != '*':
                _validateGithubUser(hub, tracUser, token)
    for user in result.keys():
        _log.debug("User token mapping found for: %s", user)
    return result

def _createTracToGithubLoginMap(hub, definition, defaultLogin):
    result = {}
    for mapping in definition.split(','):
        words = [word.strip() for word in mapping.split(':')]
        if words:
            if len(words) != 2:
                raise _ConfigError(_OPTION_USERS,
                        u'mapping must use syntax "trac-user: github-login" but is: "%s"' % mapping)
            tracUser, login = words
            if login == '*':
                login = defaultLogin
            # if len(tracUser) == 0:
            #     raise _ConfigError(_OPTION_USERS, u'Trac user must not be empty: "%s"' % mapping)
            if len(login) == 0:
                raise _ConfigError(_OPTION_USERS, u'Login must not be empty: "%s"' % mapping)
            existingMappedGithubUser = result.get(tracUser)
            if existingMappedGithubUser is not None:
                raise _ConfigError(_OPTION_USERS,
                        u'Trac user "%s" must be mapped to only one login instead of "%s" and "%s"'
                         % (tracUser, existingMappedGithubUser, login))
            result[tracUser] = login
    for user in result.keys():
        _log.debug("User login mapping found for: %s=%s", user, result.get(user))
    return result

def _loginFor(tracToGithubLoginMap, tracUser):
    assert tracToGithubLoginMap is not None
    assert tracUser is not None
    result = tracToGithubLoginMap.get(tracUser)
    if result is None:
        result = tracToGithubLoginMap.get('*')
        if result is None:
            raise _ConfigError(_OPTION_USERS, u'Trac user "%s" must be mapped to a Github user' % (tracUser,))
    return result

def _tokenFor(hub, tracToGithubUserMap, tracUser, validate=True):
    assert tracToGithubUserMap is not None
    assert tracUser is not None
    result = tracToGithubUserMap.get(tracUser)
    if result is None:
        result = tracToGithubUserMap.get('*')
        if result is None:
            raise _ConfigError(_OPTION_USERS, u'Trac user "%s" must be mapped to a Github user' % (tracUser,))
    if validate:
        _validateGithubUser(hub, tracUser, result)
    return result

def _getHub(token):
    if token in _tokenToHubMap:
        hub = _tokenToHubMap[token]
        return hub
    _log.debug("Getting hub object from token")
    _hub = github.Github(token)
    if _hub:
        _tokenToHubMap[token] = _hub
    return _hub

def _userFor(token):
    _hub = _getHub(token)
    return _getUserFromHub(_hub)

_orgsByHub = {} # key is hub object, value is hash by orgname of org objects
_reposByOrg = {} # key is org object, value is hash by reponame of repo objects
#_reposByHub = {} # key is hub object, value is hash by reponame of repo objects

def _getRepo(hub, repoName):
    # For initially getting the repo, split the repoName on / into org and repo
    if '/' in repoName:
        (orgname, repoName) = repoName.split('/')
        _log.info("Repo %s belongs to org %s", repoName, orgname)
        if hub in _orgsByHub:
            if orgname in _orgsByHub[hub]:
                org = _orgsByHub[hub][orgname]
                if _doUpdate():
                    _log.debug("Doing org.update for %s", orgname)
                    org.update()
                    _orgsByHub[hub][orgname] = org
            else:
                _log.debug("getting org %s object", orgname)
                org = hub.get_organization(orgname)
                _orgsByHub[hub][orgname] = org
        else:
            _orgsByHub[hub] = {}
            _log.debug("getting org %s object", orgname)
            org = hub.get_organization(orgname)
            _orgsByHub[hub][orgname] = org

        _log.debug("Org ID: %d, login: %s, name: %s, url: %s", org.id, org.login, org.name, org.url)
        if org in _reposByOrg:
            reposForOrg = _reposByOrg[org]
        else:
            reposForOrg = {}
        if repoName in reposForOrg:
            repo = reposForOrg[repoName]
            if _doUpdate():
                _log.debug("Doing repo.update for repo %s under org %s", repoName, orgname)
                repo.update()
        else:
            _log.debug("looking up repo %s on org", repoName)
            repo = org.get_repo(repoName)
        reposForOrg[repoName] = repo
        _reposByOrg[org] = reposForOrg
        _log.debug("Repo full_name %s, id: %d, name: %s, organization name: %s, owner %s, url: %s", repo.full_name, repo.id, repo.name, repo.organization.name, repo.owner.login, repo.url)
        _log.debug("So later get_repo will get %s/%s", repo.owner.login, repo.name)
        return repo
#    return hub.get_repo(repoName)
    _log.debug("Doing get_repo %s on a user", repoName)
    return _getUserFromHub(hub).get_repo(repoName)

_reposNoUserByHub = {} # key is hub, value is array by repo name of repo objects
def _getRepoNoUser(hub, repoName):
    if hub not in _reposNoUserByHub:
        _reposByName = {}
    else:
        _reposByName = _reposNoUserByHub[hub]

    if repoName not in _reposByName:
        # For some reason we fall in here relatively often. I suspect it is because
        # The hub instances are for different ticket reporters
        _log.debug("Looking up repo %s", repoName)
        repo = hub.get_repo(repoName)
        _reposByName[repoName] = repo
        _reposNoUserByHub[hub] = _reposByName
        return repo
    else:
        repo = _reposByName[repoName]
        # This takes 5 seconds each time and we do it a lot.
        if _doUpdate():
            _log.debug("Doing repo.update for %s", repoName)
            if repo.update():
                _reposByName[repoName] = repo
                _reposNoUserByHub[hub] = _reposByName
        return repo

_hubToUser = {} # key is hub object, value is user object
def _getUserFromHub(hub):
    if hub in _hubToUser:
        user = _hubToUser[hub]
        # Doing user.update takes 5-11 seconds, and we do this often
        if _doUpdate():
            _log.debug("Doing user.update from hub")
            user.update()
            _hubToUser[hub] = user
        return user
    else:
        _log.debug("Doing get user from hub")
        user = hub.get_user()
        _hubToUser[hub] = user
        return user

_repoToIssue = {} # key is repo object, value is array by issue # of issue objects
def _getIssueFromRepo(repo, issueNumber):
    if repo in _repoToIssue:
        issuesForRepo = _repoToIssue[repo]
    else:
        issuesForRepo = {}
    if issueNumber in issuesForRepo:
        issue = issuesForRepo[issueNumber]
        # Update calls are 5seconds each. Since we're creating the object, it shouldn't have changed on us
        if _doUpdate():
            _log.debug("Updating issue %d", issueNumber)
            if issue.update():
                issuesForRepo[issueNumber] = issue
                _repoToIssue[repo] = issuesForRepo
        return issue
    _log.debug("looking up issue %d", issueNumber)
    issue = repo.get_issue(issueNumber)
    issuesForRepo[issueNumber] = issue
    _repoToIssue[repo] = issuesForRepo
    return issue

def main(argv=None):
    if argv is None:
        argv = sys.argv

    exitCode = 1
    try:
        options, configPath = _parsedOptions(argv[1:])
        config = ConfigParser.SafeConfigParser()
        config.read(configPath)
        commentsCsvPath = _getConfigOption(config, 'comments', False)
        attachmentsCsvPath = _getConfigOption(config, 'attachments', False)
        attachmentsPrefix = _getConfigOption(config, 'attachmentsprefix', False)
        labelMapping = _getConfigOption(config, 'labels', False)
        repoName = _getConfigOption(config, 'repo')
        ticketsCsvPath = _getConfigOption(config, 'tickets', False, 'tickets.csv')
        token = _getConfigOption(config, 'token')
        userMapping = _getConfigOption(config, 'users', False, '*:{0}'.format(token))
        userLoginMapping = _getConfigOption(config, 'userLogins', False, '*:*')
        trac_url = _getConfigOption(config, 'trac_url', False)
        convert_text = _getConfigOption(config, 'convert_text',
                                        required=False,
                                        defaultValue=False,
                                        boolean=True)
        ticketsToRender = _getConfigOption(config,
                                           'ticketsToRender',
                                           required=False,
                                           defaultValue=False,
                                           boolean=False)
        ticketToStartAt = _getConfigOption(config,
                                           'ticketToStartAt',
                                           required=False,
                                           defaultValue=1,
                                           boolean=False)
        addComponentLabels = _getConfigOption(config, 'addComponentLabels',
                                              required=False,
                                              defaultValue=False,
                                              boolean=True)

        if ticketToStartAt:
            ticketToStartAt = long(ticketToStartAt)
            if ticketToStartAt < 1:
                ticketToStartAt = 1
            if ticketToStartAt > 1:
                _log.info("Starting import with ticket# %d", ticketToStartAt)
        else:
            ticketToStartAt = 1
        if ticketsToRender:
            ticketsToRender = [long(x) for x in ticketsToRender.split(',')]
            if ticketToStartAt and ticketToStartAt > 1:
                tkt2 = []
                for tkt in ticketsToRender:
                    if tkt >= ticketToStartAt:
                        tkt2.append(tkt)
                ticketsToRender = tkt2
            _log.info("Only rendering tickets %s", ticketsToRender)

        if not options.really:
            _log.warning(u'no actions are performed unless command line option --really is specified')
        else:
            _log.warning(u'Really doing the ticket import!')

        if options.skipExisting:
            _log.warning(u'Tickets whose #s overlap with existing issues will not be copied over.')

        if options.updateObjects:
            _log.info("Will update Github objects as needed - adds time")
            _setUpdate(True)
        else:
            _setUpdate(False)

        hub = _getHub(token)
        _log.info(u'log on to github as user "%s"', _getUserFromHub(hub).login)
        repo = _getRepo(hub, repoName)
        _log.info(u'connect to github repo "%s"', repoName)

        migrateTickets(hub, repo, token, ticketsCsvPath,
                       commentsCsvPath, attachmentsCsvPath, firstTicketIdToConvert=ticketToStartAt,
                       userMapping=userMapping,
                       labelMapping=labelMapping,
                       attachmentsPrefix=attachmentsPrefix, 
                      pretend=not options.really,
                       trac_url=trac_url, convert_text=convert_text, ticketsToRender=ticketsToRender, addComponentLabels=addComponentLabels, userLoginMapping=userLoginMapping,
                       skipExisting=options.skipExisting)
        
        exitCode = 0
    except (EnvironmentError, OSError, _ConfigError, _CsvDataError), error:
        _log.error(error)
    except KeyboardInterrupt:
        _log.warning(u"interrupted by user")
    except Exception, error:
        _log.exception(error)
    return exitCode


def _mainEntryPoint():
#    logging.basicConfig(level=logging.INFO)
    sys.exit(main())


if __name__ == "__main__":
    _mainEntryPoint()
