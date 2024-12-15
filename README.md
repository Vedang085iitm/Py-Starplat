# Python For Starplat

A Python translator for the Starplat DSL.

## Running the Translators

To run the translators, follow these steps:

 **Clone the Repo**
 ```sh
 git clone https://github.com/Vedang085iitm/Py-Starplat
 ```

## Make sure you have Python3 or Python installed. If not, download and install it.

### For Mac:

#### Option 1: Install Python Using the Python Installer

1. **Download the installer:**
    - Go to the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
    - Click the “Download Python 3.x.x” button (the latest version).
    - Once the download is complete, open the `.pkg` file.
2. **Install Python:**
    - Run the installer and follow the on-screen instructions.
    - Make sure to check the option “Add Python to PATH” (though this is usually handled by the installer automatically on macOS).
3. **Verify Installation:**
    - Open the Terminal (you can find it using Spotlight Search).
    - Type the following command to check the Python version:
      ```sh
      python3 --version
      ```
    - You should see the installed Python version printed in the terminal.

#### Option 2: Install Python Using Homebrew

1. **Install Homebrew** (if not already installed):
    - Open the Terminal and run the following command:
      ```sh
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      ```
2. **Install Python:**
    - Run the following command in the Terminal:
      ```sh
      brew install python
      ```
3. **Verify Installation:**
    - Type the following command to check the Python version:
      ```sh
      python3 --version
      ```
    - You should see the installed Python version printed in the terminal.

### For Windows:

1. **Download the installer:**
    - Go to the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
    - Click the “Download Python 3.x.x” button (the latest version).
    - Once the download is complete, open the `.exe` file.
2. **Install Python:**
    - In the installer window, check the box that says “Add Python 3.x to PATH” at the bottom.
    - Click “Install Now” and follow the on-screen instructions.
3. **Verify Installation:**
    - Open Command Prompt (you can find it by searching for `cmd` in the Start menu).
    - Type the following command to check the Python version:
      ```sh
      python --version
      ```
    - You should see the installed Python version printed in the Command Prompt.

### For Linux:

1. **Update the package list:**
    - Open the Terminal and run the following command:
    for Debian
      ```sh
      sudo apt update
      ```
      for Arch
      ```sh
      sudo pacman -Syu
      ```
2. **Install Python:**
    - Run the following command in the Terminal:
    for Debian 
      ```sh
      sudo apt install python3
      ```
       for Arch
      ```sh
      sudo pacman -S python3
      ```
3. **Verify Installation:**
    - Type the following command to check the Python version:
    for Debian And Arch
      ```sh
      python3 --version
      ```
    - You should see the installed Python version printed in the terminal.




## Now to use script directly 

 - Open terminal.
 - ```sh
    chmod +x script.sh
    ```
 - ```sh
    ./script.sh
    ```

## To use each Translator Separately

    python3 translator.py <path_to_python_code or input_file.py>



> ## NOTE: If u have python, change python3 to python in the script. 
