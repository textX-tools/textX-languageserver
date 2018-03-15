"""
This module is responsible for linting document file.
"""
from textx_langserv.utils import _utils
from textx_langserv.infrastructure.lsp import Diagnostic

__author__ = "Daniel Elero"
__copyright__ = "textX-tools"
__license__ = "MIT"


LINT_DEBOUNCE_S = 0.5


@_utils.debounce(LINT_DEBOUNCE_S)
def lint(doc_uri, workspace):
    """
    Create and return diagnostic object which contains all parsing errors
    """
    if doc_uri in workspace.documents:
        diagnostic = Diagnostic()
        txdoc = workspace.get_document(doc_uri)
        errors = txdoc.all_errors
        for e in errors:
            try:
                msg = e.args[0].decode("utf-8")
                msg = msg.split(' at')[0]
                diagnostic.error(txdoc.lines, e.line, e.col, msg)
            except:
                diagnostic.error(txdoc.lines, e.line, e.col, str(e))

        workspace.publish_diagnostics(doc_uri, diagnostic.get_diagnostics())
