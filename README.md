# Explain Gravity in *n* Characters

> [!NOTE]  
> This is an experiment!

This project is an interactive web application that dynamically explains the theory of gravity in varying lengths, depending on the size of a resizable text box. As you adjust the box, the application estimates the number of characters that can fit and displays an explanation of gravity tailored to that character count.

## Demo

[Live Demo Link](https://matthiasheim3d.github.io/gravity-explained-in-n-characters/)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Set Up the Backend**

   - Ensure you have Python 3 installed.
   - Install required Python packages:

     ```bash
     pip install openai
     ```

3. **Obtain OpenAI API Key**

   - Sign up on [OpenAI](https://openai.com/) to get an API key.
   - Save your API key in a file named `api_key.txt` in the project root directory.

4. **Generate the Lookup Table**

   Run the `WordGenerator.py` script to generate explanations:

   ```bash
   python WordGenerator.py
   ```

   Then, convert the lookup table to JavaScript format:

   ```bash
   python dump_list_to_javascript.py
   ```

5. **Change prompt**

   To create your own version, change the generation prompt in WordGenerator.py 

## Usage

1. **Open the Application**

   Open `index.html` in your web browser.

2. **Interact**

   - Resize the text box using the handles.
   - The explanation updates to fit the new size.
   - The character count is displayed in the header.
