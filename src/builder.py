from pathlib import Path
from music21 import converter, stream, chord, note, metadata

def create_lead_sheet(chord_midi_path: Path, melody_midi_path: Path, output_xml_path: Path):
    """
    Extracts chords and melody from two separate MIDI files and merges them into a single MusicXML lead sheet.

    :param chord_midi_path: Path to the MIDI file containing XF chord data.
    :param melody_midi_path: Path to the MIDI file with the cleaned melody.
    :param output_xml_path: Path to save the final MusicXML file.
    """
    # --- 1. Extract Chords from the Raw MIDI File ---
    print("\n[1/4] Parsing chord data...")
    try:
        raw_score = converter.parse(chord_midi_path)
        # music21 often parses XF chords as ChordSymbol objects automatically.
        chords = raw_score.flat.getElementsByClass('ChordSymbol')

        if not chords:
            print("      Warning: No ChordSymbol objects found directly. This might happen if the XF format isn't standard.")
            # As a fallback, you might need to parse text events if you know the format.
        else:
            print(f"      Found {len(chords)} chord symbols.")

    except Exception as e:
        raise RuntimeError(f"Failed to parse chord file '{chord_midi_path}': {e}")

    # --- 2. Extract Melody from the Processed MIDI File ---
    print("[2/4] Parsing melody data...")
    try:
        melody_score = converter.parse(melody_midi_path)
        # We assume the first part in the processed file is the desired melody.
        if not melody_score.parts:
            raise ValueError("No instrument parts found in the melody file.")
        
        melody_part = melody_score.parts[0]
        melody_part.id = 'Melody'
        print("      Extracted melody part.")

    except Exception as e:
        raise RuntimeError(f"Failed to parse melody file '{melody_midi_path}': {e}")

    # --- 3. Merge Melody and Chords ---
    print("[3/4] Merging melody and chords...")
    # We will insert the chords directly into the melody part we extracted.
    if chords:
        for ch in chords:
            # insert() places the chord at the correct beat offset.
            melody_part.insert(ch.offset, ch)
    print("      Merge complete.")

    # --- 4. Write to MusicXML File ---
    print(f"[4/4] Writing to output file: {output_xml_path}")
    # The melody_part is now a complete lead sheet with both notes and chords.
    # We ensure the output directory exists.
    output_xml_path.parent.mkdir(parents=True, exist_ok=True)
    melody_part.write('musicxml', fp=output_xml_path)