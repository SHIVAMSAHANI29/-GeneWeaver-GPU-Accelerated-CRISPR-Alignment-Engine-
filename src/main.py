import argparse
from .fasta_parser import load_fasta
from .benchmark import run_benchmark

def build_parser():
    parser = argparse.ArgumentParser(
        description="GeneWeaver Week 1 CPU DNA guide alignment baseline"
    )
    parser.add_argument("--fasta", required=True, help="Input FASTA file")
    parser.add_argument("--guide", required=True, help="Guide DNA sequence, e.g. ACGT...")
    parser.add_argument("--max-mismatches", type=int, default=0)
    parser.add_argument("--chunk-size", type=int, default=1_000_000)
    parser.add_argument("--forward-only", action="store_true",
                        help="Do not scan the reverse-complement strand")
    parser.add_argument("--tui", action="store_true",
                        help="Show results in the Textual terminal dashboard")
    return parser

def main():
    args = build_parser().parse_args()
    records = load_fasta(args.fasta)

    print("\nGENEWEAVER | WEEK 1 CPU BASELINE")
    print("-" * 55)
    for record in records:
        print(f"FASTA record: {record['id']} | {len(record['sequence']):,} bases")
    print(f"Guide: {args.guide.upper()}")
    print(f"Maximum mismatches: {args.max_mismatches}")
    print(f"Chunk size: {args.chunk_size:,}")

    report = run_benchmark(
        records=records,
        guide=args.guide,
        max_mismatches=args.max_mismatches,
        chunk_size=args.chunk_size,
        both_strands=not args.forward_only,
    )

    print("\nRESULTS")
    print("-" * 55)
    print(f"Bases scanned : {report['bases_scanned']:,}")
    print(f"Hits found    : {len(report['hits']):,}")
    print(f"Elapsed time  : {report['elapsed_seconds']:.6f} seconds")
    print(f"Throughput    : {report['bases_per_second']:,.0f} bases/second")
    print("\nFirst 20 hits:")
    for hit in report["hits"][:20]:
        print(f"{hit.record_id}\t{hit.start}\t{hit.end}\t"
              f"{hit.strand}\t{hit.mismatches}\t{hit.matched_sequence}")

    if args.tui:
        from .dashboard import GeneWeaverDashboard
        GeneWeaverDashboard(report).run()

if __name__ == "__main__":
    main()
