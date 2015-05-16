import re

class Translator(object):
    """
    Simple regular expression to convert Trac wiki to Github markdown.
    """
    def __init__(self, repo, ticketsToIssuesMap, trac_url=None, attachmentsPrefix=None):
        self.repo_url = r'https://github.com/{login}/{name}'.format(login=repo.owner.login, name=repo.name)
        self.trac_url = trac_url
        self.ticketsToIssuesMap = ticketsToIssuesMap
        self.subs = self.compile_subs()
        self.attachmentsPrefix = attachmentsPrefix

    def compile_subs(self):
        subs = [
            # This first handles things like #!xml
            [r"\{\{\{\s*?[\n\r]{1,2}#!([a-z\/]+)(.*?)\}\}\}", r"```\1\2```"],
            # Single line block quotes
            [r"\{\{\{([^\n]*?)\}\}\}",  r"`\1`"],
            # Multi line block quotes
            [r"\{\{\{(.*?)\}\}\}",  r"```\1```"],
            # These next are for headings
            [r"====\s([^\n]+?)\s====(\s*[\n\r]+)", r'#### \1\2'],
            [r"===\s([^\n]+?)\s===(\s*[\n\r]+)", r'### \1\2'],
            [r"==\s([^\n]+?)\s==(\s*[\n\r]+)", r'## \1\2'],
            [r"=\s([^\n]+?)\s=(\s*[\n\r]+)", r'# \1\2'],
            [r"\!(([A-Z][a-z0-9]+){2,})", r'\1'],
            # These next are italics, bold
            [r"'''(.+)'''", r'*\1*'],
            [r"''(.+)''", r'_\1_'],
            # These next 2 are various bulleted or numbered lists
            # Note though that they are only single space indents
            [r"^\s\*", r'*'],
            [r"^\s\d\.", r'#'],
            # This next looks like it tries to strip leading !
            [r"!(\w)", r"\1"],
            #            [r"(^|\n)[ ]{6,}", r"\1"], # AH: This stripped leading whitespace from lines, which messes up block quotes
            [r"\[([^\s\n\,\]\.\(\)]{6,}?)\s{1,}([^\n]+?)\]", r"[\2](\1)"],
            # This next line turns hashes into links. Require at least 15 chars to avoid mistaken links
            [r"(\s+|\()(changeset:|commit:|:)?([0-9a-f]{15,})([^0-9a-f\-])", r"\1[\3]({repo_url}/commit/\3)\4".format(repo_url=self.repo_url)],
            [r"source:branches/([\w\-]*)", r"[\1](../tree/\1)"],
            [r"source:fipy/([\w/\.]*)@([0-9a-f]{5,40})", r"[\1@\2](../tree/\2/\1)"],
            [r"source:([\w/\.\-\_\d\~]+)", r"[\1](../tree/master/\1)"],
            [r"blog:(\w*)", r"[blog:\1]({trac_url}/blog/\1)".format(trac_url=self.trac_url)],
            [r"(\b)([0-9a-f]{5,40})\.", r"\1\2"],
            [r" (\w*?)::", r"#### \1"],
            [r"\[([0-9]{1,4})\/(.+?)\]", r"[\1/\2]({trac_url}/changeset/\1/historical/\2)".format(trac_url=self.trac_url)],
            [r'\[changeset:"(\S*?)\/fipy"\]', r"\1"],          
            [r'\^([0-9]{1,5})\^', r"<sup>\1</sup>"],
            [r'diff:@([0-9]{1,5}):([0-9]{1,5})', r'[diff:@\1:\2]({trac_url}/changeset?new=\2&old=\1)'.format(trac_url=self.trac_url)],
            [r"\[([^\[\]\s\n\r\E\"\{][^\[\]\s\n\r\"\{]+)\s+([^\]]+)]", r"[\2](\1)"]
            ]

        # AH: Last one converts wiki links [URL text] to markdown links [text](URL)
        # piece at beginning excludes things that start with certain characters. Then it says rest of target may not
        # have certain characters
        regex = r"ticket:([0-9]{1,3})"
        sub = lambda m: r"issue #{0}".format(self.ticketsToIssuesMap[int(m.group(1))])
        subs.append([regex, sub])

        return [[re.compile(r, re.DOTALL), s] for r, s in subs]

    def no_compile_subs(self, ticketId):
        #print 'ticketId',ticketId
        subs = [[r"\[\[Image\((\S*?)\,\s{0,}\S*?\)\]\]", r"![\1]({attachmentsPrefix}/{ticketId}/\1)".format(attachmentsPrefix=self.attachmentsPrefix, ticketId=ticketId)],
                [r"\[\[Image\((\S*?)\)\]\]", r"![\1]({attachmentsPrefix}/{ticketId}/\1)".format(attachmentsPrefix=self.attachmentsPrefix, ticketId=ticketId)],
                [r"attachment:(\S*?)", r"{attachmentsPrefix}/{ticketId}/\1".format(attachmentsPrefix=self.attachmentsPrefix, ticketId=ticketId)]]

        return subs

    def translate(self, text, ticketId=''):
        subs = self.no_compile_subs(ticketId)
        for r, s in subs:
            p = re.compile(r, re.DOTALL)
            #ot = text
            text = p.sub(s, text)
            #if ot != text:
            #    print "regex '%s' changed \n'%s' to \n'%s'" % (r, ot, text)
        for p, s in self.subs:
            #ot = text
            text = p.sub(s, text)
            #if ot != text:
            #    print "regex '%s' changed \n'%s' to \n'%s'" % (p.pattern, ot, text)
        return text

class NullTranslator(Translator):
    def translate(self, text):
        return text
