# Football Arber

Football Arber is a Python-based arbitrage betting tool for soccer matches. It collects odds from various bookmakers and analyzes them to find potential arbitrage opportunities.

## Features

- Collects odds from multiple bookmakers (currently Winamax and Zebet)
- Supports multiple soccer leagues and competitions
- Calculates arbitrage opportunities
- Updates league data in JSON format

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/football-arber.git
   cd football-arber
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file in the root directory and add your Odds API key:
   ```
   ODDS_API=your_api_key_here
   ```

## Usage

Run the main script:

```
python main.py
```

This will process the configured competitions, fetch odds from supported bookmakers, and update the league data files.

## Project Structure

- `arb_calculator.py`: Contains the main logic for calculating arbitrage opportunities
- `file_grabber.py`: Fetches odds data from the Odds API
- `main.py`: The main script that orchestrates the odds collection and analysis process
- `bookmakers/`: Contains modules for each supported bookmaker
  - `winamax/`: Winamax odds fetcher
  - `zebet/`: Zebet odds fetcher
- `utils/`: Utility functions and configurations
  - `update_leagues.py`: Updates league JSON files with new odds data
  - `league_info.py`: Contains information about supported leagues
  - `config.py`: Configuration settings for the project

## Adding New Bookmakers

To add a new bookmaker:

1. Create a new module in the `bookmakers/` directory
2. Implement the `get_games()` function that returns a list of games with their odds
3. Update the `main.py` script to include the new bookmaker

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This tool is for educational purposes only. Be aware that arbitrage betting may be against the terms of service of some bookmakers. Use at your own risk.
