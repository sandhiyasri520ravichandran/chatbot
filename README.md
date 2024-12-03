                                                            Chatbot with Graph Generation

Overview:
This project is an interactive chatbot application that incorporates a visually appealing user interface and functionality to generate graphs from uploaded CSV files. It leverages Dash for web-based visualization, Plotly for creating graphs, and Google Generative AI for intelligent chatbot responses.

Features:
Chatbot Functionality:
Responsive chatbot capable of handling user queries.
Integrated with Google Generative AI for generating text-based responses.

Graph Generation:
Allows users to upload CSV files to generate graphs dynamically.
Supports line graphs with customizable datasets.

Intuitive Design:
Aesthetic interface built using Dash and Bootstrap components.
Gradient background and custom-styled elements for a modern look.

Dynamic File Parsing:
Automatic detection and parsing of CSV files with error handling.
Supports UTF-8 and Latin-1 encodings.

Technologies Used
*Python 3.9+
*Dash (for web app development)
*Dash Bootstrap Components (for UI design)
*Plotly (for graph generation)
*Google Generative AI (for chatbot responses)
*Pandas (for data processing)

Installation Instructions:
Clone the repository:

git clone https:/sandhiyasri520ravichandran/chatbot.git
cd chatbot

Install the required dependencies:
pip install -r requirements.txt

Set up the Google Generative AI API key:
Obtain an API key from the Google Cloud Console.

Add the API key to your environment variables:
export GEMINI_API_KEY=your_api_key

Run the application:
python app.py

