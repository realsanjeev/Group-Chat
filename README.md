# Group-Chat
DBMS project to create a chat group web-application

# DATABASE
| user     |  	 	
|----------|		
| userid   | 		
| username | 		
| password | 		


| group      |
|------------|
| groupid(p) |
| groupname  |
| userid     |
## Automatically Generating Documentation

To automate the process of generating documentation, follow these steps:

1. Install Sphinx using pip:

   ```bash
   pip install Sphinx
   ```

2. Initialize Sphinx in your project directory:

   ```bash
   sphinx-quickstart
   ```

3. In the `config.py` file generated by Sphinx, add the following lines to ensure that your project's modules are properly imported:

   ```python
   import os
   import sys
   sys.path.insert(0, os.path.abspath('.'))
   ```

4. Use `sphinx-apidoc` to automatically generate documentation for your Python modules. This command should be run in the same directory as your Python files:

   ```bash
   sphinx-apidoc -o docs .
   ```

   This will create `.rst` files in the `docs` directory.

5. Finally, generate the HTML documentation by running:

   ```bash
   make html
   ```

   The generated HTML files can be found in the `docs/_build/html` directory.

These steps automate the process of generating documentation for your Python project using Sphinx.
## Contributing

Contributions are welcome! If you find any issues or want to add new features, feel free to submit a pull request.

## Contact Me

<table>
  <tr>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/instagram.png" alt="Instagram" width="50" height="50"></td>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/twitter.png" alt="Twitter" width="50" height="50"></td>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/github.png" alt="GitHub" width="50" height="50"></td>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/linkedin-logo.png" alt="LinkedIn" width="50" height="50"></td>
  </tr>
</table>