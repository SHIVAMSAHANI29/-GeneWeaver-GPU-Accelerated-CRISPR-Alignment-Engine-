from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, DataTable

class GeneWeaverDashboard(App):
    TITLE = "GeneWeaver | Week 1 CPU Baseline"
    CSS = """
    Screen { padding: 1; }
    #summary { height: auto; border: round green; padding: 1; margin-bottom: 1; }
    DataTable { height: 1fr; }
    """

    def __init__(self, report, **kwargs):
        super().__init__(**kwargs)
        self.report = report

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("", id="summary")
        yield DataTable(id="hits")
        yield Footer()

    def on_mount(self) -> None:
        summary = self.query_one("#summary", Static)
        table = self.query_one("#hits", DataTable)
        report = self.report
        summary.update(
            f"CPU baseline complete | Bases: {report['bases_scanned']:,} | "
            f"Hits: {len(report['hits']):,} | "
            f"Time: {report['elapsed_seconds']:.6f} s | "
            f"Throughput: {report['bases_per_second']:,.0f} bases/s"
        )
        table.add_columns("Record", "Start", "End", "Strand", "Mismatches", "Matched DNA")
        for hit in report["hits"][:500]:
            table.add_row(hit.record_id, str(hit.start), str(hit.end),
                          hit.strand, str(hit.mismatches), hit.matched_sequence)
        if not report["hits"]:
            table.add_row("-", "-", "-", "-", "-", "No hits found")
