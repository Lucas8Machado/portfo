from flask import Flask, render_template, url_for, request, redirect
import csv

app = Flask(__name__)  # Create an instance of the Flask application
print(__name__)  # Print the name of the current module (script)


@app.route('/')
def my_home():
    # Render and return the 'index.html' template
    return render_template('index.html')


@app.route("/<string:page_name>")
def html_page(page_name=None):
    # Render and return the specified HTML template
    return render_template(page_name)


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        # Write form data to 'database.txt' file
        file = database.write(f'\n{email}, {subject}, {message}')


def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database2:
        email = data['email']
        subject = data['subject']
        message = data['message']

        if database2.tell() == 0:  # Check if the file is empty
            csv_writer = csv.writer(
                database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # Write the column headers
            csv_writer.writerow(['email', 'subject', 'message'])

        csv_writer = csv.writer(database2, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Write the data to the CSV file
        csv_writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':  # If the request method is POST
        try:
            data = request.form.to_dict()  # Convert form data to a dictionary
            write_to_csv(data)  # Write form data to file
            # Redirect to the 'thankyou.html' page
            return redirect('/thankyou.html')
        except:
            return 'did not save to database'
    else:
        # If request method is not POST, display an error message
        return 'something went wrong try again'


# Turning the debug mode on
app.debug = True  # Enable debug mode for the Flask application
# app.debug = False

if __name__ == '__main__':
    app.run()  # Run the Flask application if the script is executed directly
