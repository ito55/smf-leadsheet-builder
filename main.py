import argparse
import sys
from pathlib import Path

# This allows the script to find the 'src' directory and import the builder module
# It makes the script runnable from the project's root directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from src.smf_leadsheet_builder import builder
except ImportError as e:
    print(f"Error: Could not import the builder module. Make sure 'src/smf_leadsheet_builder/builder.py' exists. Details: {e}")
    sys.exit(1)


def main():
    """
    Main function to parse command-line arguments and run the lead sheet generation process.
    """
    parser = argparse.ArgumentParser(
        description="Generate a MusicXML lead sheet by merging chords and melody from two MIDI files.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Example:
  python main.py --chord-file input/raw_example.mid --melody-file input/processed_example.mid --output output/lead_sheet.musicxml
"""
    )

    parser.add_argument(
        "--chord-file",
        type=Path,
        required=True,
        help="Path to the original XF-formatted MIDI file containing the chord data."
    )
    parser.add_argument(
        "--melody-file",
        type=Path,
        required=True,
        help="Path to the MIDI file containing the cleaned-up melody."
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path for the generated MusicXML file."
    )

    args = parser.parse_args()

    print("Starting lead sheet generation...")
    print(f"  - Chord source:  {args.chord_file}")
    print(f"  - Melody source: {args.melody_file}")
    print(f"  - Output file:   {args.output}")

    try:
        # Call the core logic from the builder module
        builder.create_lead_sheet(
            chord_midi_path=args.chord_file,
            melody_midi_path=args.melody_file,
            output_xml_path=args.output
        )
        print(f"\n✅ Successfully created lead sheet: {args.output}")

    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()