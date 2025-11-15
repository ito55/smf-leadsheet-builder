# smf-leadsheet-builder
A tool to generate a lead sheet (MusicXML) by merging chord data from an XF-formatted SMF and a melody from another SMF.

This script is designed to solve a specific problem: creating a lead sheet when the chord information and the final melody are in separate MIDI files. It extracts chord progressions from a raw XF-formatted Standard MIDI File and merges them with a cleaned-up melody track from a processed MIDI file, outputting a single MusicXML file ready for use in notation software like Dorico, Sibelius, or MuseScore.

## Features

-   **Chord Extraction**: Parses chord information from XF-formatted MIDI files.
-   **Melody Extraction**: Isolates the melody track from a standard MIDI file.
-   **Merge Logic**: Intelligently combines chords and melody into a single musical structure.
-   **MusicXML Output**: Generates a standard MusicXML file for easy import into notation software.

## Requirements

-   Python 3.8+
-   `music21` library

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ito55/smf-leadsheet-builder.git
    cd smf-leadsheet-builder
    ```

2.  **Set up a virtual environment (recommended):**
    This creates an isolated environment for the project's dependencies.
    
    ```bash
    # Create a virtual environment named 'venv'
    python -m venv venv
    
    # Activate the virtual environment
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install the required Python library:**
    ```bash
    pip install music21
    ```

## Usage

Run the main script from your terminal, providing the paths to the two input MIDI files and the desired output path.

```bash
# Example with placeholder files in the 'input' directory
python main.py --chord-file input/raw_example.mid --melody-file input/processed_example.mid --output output/lead_sheet.musicxml
```

-   `--chord-file`: The path to the original XF-formatted MIDI file containing the chord data.
-   `--melody-file`: The path to the MIDI file containing the cleaned-up melody (e.g., on Channel 1).
-   `--output`: The path for the generated MusicXML file.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
