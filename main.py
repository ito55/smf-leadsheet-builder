import argparse
import sys
from pathlib import Path
from music21 import converter, stream, harmony, note, meter, key

# ==============================================================================
# Builder Logic (formerly builder.py)
# ==============================================================================

def _parse_xf_sysex_chords(midi_stream: stream.Stream) -> list[harmony.ChordSymbol]:
    """
    Parses Yamaha XF-style SysEx messages from a music21 stream to extract chord symbols.
    """
    chords = []
    # XF chord SysEx messages look like: F0 43 7E 7F 04 01 <root> <type> F7
    xf_header = (0xF0, 0x43, 0x7E, 0x7F)
    chord_data_type = 0x04

    # Mapping from XF chord root value to pitch name
    root_map = {
        0x41: 'C#', 0x42: 'D', 0x43: 'D#', 0x44: 'E', 0x45: 'F',
        0x46: 'F#', 0x47: 'G', 0x48: 'G#', 0x49: 'A', 0x4A: 'A#',
        0x4B: 'B', 0x60: 'C'
    }
    # Mapping from XF chord type value to music21 kind string
    kind_map = {
        0x01: 'major', 0x02: 'minor', 0x03: 'augmented', 0x04: 'diminished',
        0x05: 'dominant-seventh', 0x06: 'minor-seventh', 0x07: 'major-seventh',
        0x08: 'major-sixth', 0x09: 'minor-sixth', 0x0A: 'suspended-fourth',
        # Add more mappings as needed
    }

    # Use .flatten() to get a flat stream of all elements, then filter for SysEx
    for element in midi_stream.flatten().getElementsByClass('Sysex'):
        data = element.getData()
        # Check if the SysEx message matches the XF chord format
        if len(data) == 9 and data[:4] == xf_header and data[4] == chord_data_type:
            root_val = data[6]
            kind_val = data[7]

            root_str = root_map.get(root_val)
            kind_str = kind_map.get(kind_val, 'major') # Default to major if unknown

            if root_str:
                try:
                    cs = harmony.ChordSymbol(root=root_str, kind=kind_str)
                    cs.offset = element.offset
                    chords.append(cs)
                except Exception as e:
                    print(f"Warning: Could not create chord for {root_str}{kind_str} at offset {element.offset}. Details: {e}")
    return chords

def create_lead_sheet(chord_midi_path: Path, melody_midi_path: Path, output_xml_path: Path):
    """
    Generates a MusicXML lead sheet by merging chords and melody from two MIDI files.
    """
    # 1. Extract chords from the XF MIDI file
    print("  - Parsing chord file for XF SysEx messages...")
    chord_midi_stream = converter.parse(str(chord_midi_path), forceSource=True)
    extracted_chords = _parse_xf_sysex_chords(chord_midi_stream)
    if not extracted_chords:
        print("Warning: No XF chord symbols were found in the chord file.")

    # 2. Extract melody from the melody MIDI file
    print("  - Parsing melody file...")
    melody_score = converter.parse(str(melody_midi_path))

    # Assume the melody is in the first part of the score
    if not melody_score.parts:
        raise ValueError("Melody file contains no parts.")
    melody_part = melody_score.parts[0]
    melody_part.id = 'melody'

    # 3. Get metadata from the melody score (Time Signature, Key Signature)
    # Use the first found time signature and key signature
    ts = melody_part.getElementsByClass(meter.TimeSignature).first()
    ks = melody_part.getElementsByClass(key.KeySignature).first()

    # 4. Create the new lead sheet structure
    lead_sheet = stream.Score()
    output_part = stream.Part()
    output_part.id = 'lead_sheet_part'

    # Insert metadata if found
    if ts:
        output_part.insert(0, ts)
    if ks:
        output_part.insert(0, ks)

    # 5. Insert chords into the output part
    print(f"  - Merging {len(extracted_chords)} chords...")
    for cs in extracted_chords:
        output_part.insert(cs.offset, cs)

    # 6. Insert notes and rests from the melody part
    print("  - Merging melody notes...")
    for el in melody_part.notesAndRests:
        output_part.insert(el.offset, el)

    # 7. Add the completed part to the score and write to file
    lead_sheet.insert(0, output_part)
    print(f"  - Writing to MusicXML file: {output_xml_path}")
    output_xml_path.parent.mkdir(parents=True, exist_ok=True)
    lead_sheet.write('musicxml', fp=str(output_xml_path))


# ==============================================================================
# Command-line execution logic
# ==============================================================================
def main():
    """
    Main function to parse command-line arguments and run the lead sheet generation process.
    """
    parser = argparse.ArgumentParser(
        description="Generate a MusicXML lead sheet by merging chords and melody from two MIDI files.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""\
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
        # Call the integrated function directly
        create_lead_sheet(
            chord_midi_path=args.chord_file,
            melody_midi_path=args.melody_file,
            output_xml_path=args.output
        )
        print(f"\n✅ Successfully created lead sheet: {args.output.resolve()}")

    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()