Merge the header_corrector GUI code implemented in header_corrector.py into the modal dialog flow of the zAppcontroller tinter application found in Z-UltimateTournamet.py to allow the user to adjust the column headers in the registration data.   

The purpose of the header_corrector.py code is to allow the user to select the proper column headers for the CSV file that contains registration data.   We have had problems with consistency in the column headers, so the header_corrector.py module was developed to provide a user friendly way to select the proper column headers.   It presents all the columns in the provided data file, and lets the user select new headers from a list of correct header names.   The code also has an auto map feature that uses regex patterns to try to match header names to the correct header names automatically.


Once merged into the Z-UltimateTournament code the new header corrector window should open as a modal at the end of the on_continue method in file_picker_controller.py

The integrated code will read the file from the data stored in AppController.input_Data_filename and it should store the file with the corrected headers in the output folder path stored in zAppController.tournament_output_folder_path

Relevant files provided for context are:
Z-UltimateTournament.py - this is the driver for the GUI application
header_corrector.py - this is the stand-alone application that allows a user to assign the correct column header to the data file.
file_picker_controller.py - this is the MVC controller module that allows a user to select the input data files.  The file_picker logic will precede the new header_corrector logic.
file_picker_view.py - this in the MVC view module for the GUI controls that allow a user to select the input data files.
data_validation_controller.py - this is the MVC controller module that will be called after the column headers have been fixed.  It will need to read the new file with the corrected header information.
data_validation_view.py - this is the MVC view module for the GUI controls that allow the user to validate errors in the data file.   It will be used logically after the column headers have been corrected.
