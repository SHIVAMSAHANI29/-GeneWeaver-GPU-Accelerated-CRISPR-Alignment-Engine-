# GeneWeaver — Week 1

A CPU-baseline CRISPR-like guide-sequence scanner with a BioPython FASTA parser,
overlapping genome chunking, mismatch-tolerant fixed-length alignment, and an
optional Textual terminal dashboard.

> Educational prototype only. It is not clinically validated and must not be
> used to make experimental or medical decisions.

## Week 1 scope

- Parse FASTA records with BioPython.
- Normalize DNA sequence symbols (A/C/G/T/N).
- Split records into chunks while preserving cross-chunk matches.
- Scan each guide-length window and count mismatches (Hamming distance).
- Report zero-based genomic coordinates, strand, mismatch count and matched sequence.
- Measure CPU elapsed time and bases/second.
- Optionally show results in a Textual TUI.

Numba/CUDA and Dask are intentionally not used in Week 1. They are later
optimization/distribution stages; first establish a correct CPU reference.

## Setup (Windows PowerShell)

```powershell
cd GeneWeaver_Week1
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run the sample

```powershell
python -m src.main --fasta data/mock_genome.fasta --guide AGTCGATCGTACGATCGTAA --max-mismatches 2 --chunk-size 1000
```

Open the terminal dashboard:
```powershell
python -m src.main --fasta data/mock_genome.fasta --guide AGTCGATCGTACGATCGTAA --max-mismatches 2 --chunk-size 1000 --tui
```

Use your own FASTA:
```powershell
python -m src.main --fasta "D:\genomes\sample.fasta" --guide AGTCGATCGTACGATCGTAA --max-mismatches 2
```

The sample FASTA is synthetic and tiny. It is only for validating the pipeline,
not for performance claims about a human genome.

## Project layout

```text
GeneWeaver_Week1/
├── data/
│   └── mock_genome.fasta
├── src/
│   ├── __init__.py
│   ├── fasta_parser.py
│   ├── chunker.py
│   ├── cpu_aligner.py
│   ├── benchmark.py
│   ├── dashboard.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Algorithm and coordinate conventions

The baseline scans every window whose length equals the guide length and
computes Hamming distance (number of differing positions). A hit is reported
when mismatches <= `--max-mismatches`. Both forward and reverse-complement
strands are scanned by default. Coordinates are zero-based, half-open:
`[start, end)`, relative to each FASTA record.

Chunking uses a right overlap of `guide_length - 1` bases. Only windows whose
start belongs to a chunk's non-overlapping core are evaluated, so matches
crossing chunk boundaries are found once rather than missed or duplicated.

This is a simplified sequence-similarity baseline. It does not model PAM
requirements, bulges, thermodynamics, variant context, or biological activity.
A real CRISPR off-target workflow must incorporate nuclease-specific PAM rules
and validated alignment/scoring methods.

## Week 1 acceptance checklist

- [ ] Sample FASTA parses and reports record IDs and lengths.
- [ ] Chunker covers the entire sequence, including the final partial chunk.
- [ ] A guide inserted into the sample is found with 0 mismatches.
- [ ] A one-base variant is found with 1 mismatch when threshold is 1.
- [ ] Reverse-complement hits are reported on the minus strand.
- [ ] A match spanning a chunk boundary is found exactly once.
- [ ] CPU runtime and throughput are printed.
- [ ] TUI starts with `--tui`.

Run the unit tests:\n```powershell\npython -m unittest discover -s tests -v\n```\n\n## Benchmarking notes

Run the exact same FASTA, guide, mismatch threshold, and machine configuration
for future CPU/Numba/Dask comparisons. Record genome bases scanned, elapsed
seconds, throughput (bases/second), number of hits, Python version, CPU model,
and later GPU model. Do not compare runs with different input sizes.
