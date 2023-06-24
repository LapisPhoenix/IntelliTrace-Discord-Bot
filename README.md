# IntelliTrace Discord Bot


IntelliTrace is an OSINT (Open-Source Intelligence) bot for Discord, built using Discord.py. It allows you to legally collect information and perform various operations. Please make sure to read and agree to the Terms of Service and Privacy Policy before using the bot. You can find the Terms of Service [here](https://raw.githubusercontent.com/LapisPhoenix/IntelliTrace-Discord-Bot/main/TERMS%20OF%20SERVICE) and the Privacy Policy [here](https://raw.githubusercontent.com/LapisPhoenix/IntelliTrace-Discord-Bot/main/PRIVACY%20POLICY).

## Add To Your Server
Link can be found [here](https://discord.com/api/oauth2/authorize?client_id=1121685167128453151&permissions=826781518912&scope=bot).

## Installation

1. Rename the file `.env.example` to `.env`.
2. Fill in the following values in the `.env` file:
   - `TOKEN`: Your Discord bot token.
   - `VERIPHONE`: Your Veriphone API key.
   - `PASTEE`: Your Pastee API key.
3. Install the required dependencies by running the following command:
   ```bash
   pip install -r requirements.txt
   ```
4. Run `main.py` to start the bot.

## Commands

The bot currently supports the following commands:
1. `phonenumber`: Verify a phone number and retrieve general information about it.
2. `exif_data_extraction`: Extract Exif data from a direct image URL.
3. `ping`: Check the bot's latency.
4. `legal`: View the legal terms of the bot.

## License

IntelliTrace is licensed under the Apache License 2.0. Please review the license terms for more information.

## Disclaimer
Please note that the usage of this bot is subject to legal and ethical guidelines. Ensure that you comply with all applicable laws and regulations while using this bot. The bot developers do not take responsibility for any misuse or illegal activities conducted using this bot.

## Contributions

Contributions to IntelliTrace are welcome! If you find any issues or have suggestions for improvements, please create a GitHub issue or submit a pull request.

## Support

If you need any assistance or have any questions regarding IntelliTrace, please join our support Discord server: [Link to support server](https://discord.gg/544vjfxAwf).

Thank you for using IntelliTrace! We hope you find it helpful for your OSINT needs.
