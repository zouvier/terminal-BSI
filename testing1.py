from flask import Flask
from flask import render_template, request, flash, redirect
import re

global start_voltage
global start_A_Power
global start_A_Energy
global start_SOC
app = Flask(__name__)
app.config['SECRET_KEY'] = 'any_secret_key'

ALLOWED_EXTENSIONS = {'txt'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # important: the below is a working code to find battery state info.
        # TODO:[DONE] work on a code to find all instances of the above line
        # TODO:[DONE] Recreate the template above using the extracted data from the text file
        # TODO:[DONE] Find a way to extract the data from the text output
        '''*POSSIBLE SOLUTION 1: [1hr to complete]
        #       ~Using regex find the location of the specific word and using the finditer function
        #       ~ i should be able to find the location of the text and then calculate the distance away from the number
        #       ~ use this number to find the full value up to 2 decimal places.
        #       *POSSIBLE SOLUTION 2:[4hr to complete]
        #           ~ Create a data frame using pandas and divide the words with numbers before each new line
        #           ~ placing the data into a list will allow for a easier extraction from a dataframe'''
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            test_log = str(file.stream.read())

            # with open(file, "r") as org_file:
            #     test_log = org_file.read()

            full_string = []
            count = 1

            # finds all instances of BSI output within the text file
            # i want this to be on the page and allow the user to select which BSI (battery state info) that they want
            for x in re.finditer('Battery State Info:', test_log):
                start1 = x.start()
                end1 = test_log.find('HVOnCount: ', start1)
                full_string.append(test_log[start1:end1])

            # print('Type in the following information')
            name = request.form.get('name')
            car = request.form.get('car')
            b_Odo = request.form.get('b_odo')
            e_Odo = request.form.get('e_odo')
            outsideTemp = request.form.get('temp')
            b_dashBoard = request.form.get('b_dashboard')
            e_dashBoard = request.form.get('e_dashboard')
            cup = ''
            i = 0
            holder2 = []
            while i < len(full_string):
                holder = '[' + str(i + 1) + '] '
                cup2 = full_string[i]
                for z in re.finditer('HVoltage:', cup2):
                    volts = z.start()
                    holder += 'Voltage: ' + str(cup2[(volts + 9):volts + 16]) + '--'  # [49+9:49+16]
                for z in re.finditer('A-Power:', cup2):
                    apower = z.start()
                    holder += 'A-Power' + str(cup2[(apower + 9):apower + 16]) + '--'  # [453+9:453+16]
                for z in re.finditer('A-Energy:', cup2):
                    aenergy = z.start()
                    holder += 'A-Energy' + str(cup2[aenergy + 10:aenergy + 16]) + '--'  # [502+10:518]
                for z in re.finditer('SOC:', cup2):
                    soc = z.start()
                    holder += 'SOC' + str(cup2[soc + 5:soc + 11]) + '\n'  # [409+5:420]
                holder2.append(holder)
                i += 1

            user_input_one = 0
            user_input_two = (count - 2)

            # Finds location of the words within the text file that was taken out of the BSI
            def location_position(user_input):
                global start_voltage
                global start_A_Power
                global start_A_Energy
                global start_SOC
                for t in re.finditer('HVoltage:', full_string[user_input]):
                    start_voltage = t.start()  # [49+9:49+16]
                    # print('voltage position' + str(start_voltage))

                '''for t in re.finditer('Current:', full_string[user_input]):
                    start_current = t.start() # [98+9:112]
                    print('Current position: ' + str(start_current))

                for t in re.finditer('AvgTemp:', full_string[user_input]):
                    start_AvgTemp = t.start() # [145:
                    print('AvgTemp position: ' + str(start_AvgTemp))

                for t in re.finditer('MaxTemp:', full_string[user_input]):
                    start_MaxTemp = t.start() # [193:
                    print('MaxTemp position: '+ str(start_MaxTemp))'''

                for t in re.finditer('A-Power:', full_string[user_input]):
                    start_A_Power = t.start()  # [453+9:469]
                    # print('A-Power position: ' + str(start_A_Power))

                for t in re.finditer('A-Energy:', full_string[user_input]):
                    start_A_Energy = t.start()  # [502+10:518]
                    # print('A-Energy position: ' + str(start_A_Energy))

                '''for t in re.finditer('C-Power:', full_string[user_input]):
                    start_C_Power = t.start() # [ 551:
                    print('C-Power position: ' + str(start_C_Power))

                for t in re.finditer('C-Current:', full_string[user_input]):
                    start_C_Current = t.start() # [599+11:616]
                    print('C-Current position: ' + str(start_C_Current))'''

                for t in re.finditer('SOC:', full_string[user_input]):
                    start_SOC = t.start()  # [409+5:420+10]
                    # print('SOC position: ' + str(start_SOC))
                return start_voltage, start_A_Power, start_A_Energy, start_SOC

            SV1, SA1, SAE1, S_SOC1 = location_position(user_input_one)
            SV2, SA2, SAE2, S_SOC2 = location_position(user_input_two)

            choice_one = full_string[user_input_one]
            choice_two = full_string[user_input_two]
            dict1 = {
                'name': name,
                'car': (car + ' BMs'),
                'distance': (str((int(e_Odo) - int(b_Odo)))),
                'odometer': (str(b_Odo) + ' -> ' + str(e_Odo) + ' Miles'),
                'outside_Temp': (outsideTemp + ' F'),
                'dashBoard_range': (b_dashBoard + ' -> ' + e_dashBoard + ' Miles'),
                'voltage': (str(choice_one[(SV1 + 9):(SV1 + 16)]) + ' -> ' + str(
                    choice_two[(SV2 + 9):(SV2 + 16)]) + ' V'),
                'SOC': (str(choice_one[(S_SOC1 + 5):(S_SOC1 + 10)]) + '% -> ' + str(
                    choice_two[(S_SOC2 + 5):(S_SOC2 + 10)]) + '%'),
                'available_energy': (str(choice_one[(SAE1 + 10):(SAE1 + 16)]) + ' -> ' + str(
                    choice_two[(SAE2 + 10):(SAE2 + 16)])),
                'BSI': holder2
            }
            return render_template("data.html", data=dict1)


if __name__ == '__main__':
    app.run(debug=False)
