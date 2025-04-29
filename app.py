from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'Hpau'  # can be any random string

# Database connection settings
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Harini@14',  # Your actual MySQL password
    'database': 'clinic'  # Your actual database
}


@app.route('/')
def home():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("home.html", appointments=appointments)


@app.route('/add', methods=['GET', 'POST'])
def add_appointments():
    if request.method == 'POST':
        # Get form data
        patient_name = request.form['patient_name']
        doctor_name = request.form['doctor_name']
        appointment_date = request.form['appointment_date']
        slot_time = request.form['slot_time']
        status = request.form['status']
        symptoms = request.form['symptoms']
        phone_number = request.form['phone_number']

        # Connect and insert into database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        sql = """
            INSERT INTO appointments 
            (patient_name, doctor_name, appointment_date, slot_time, status, symptoms, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (patient_name, doctor_name, appointment_date, slot_time, status, symptoms, phone_number)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        flash('Appointment added successfully!')
        return redirect(url_for('home'))

    return render_template('add_appointments.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_appointment(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Get updated data from form
        patient_name = request.form['patient_name']
        doctor_name = request.form['doctor_name']
        appointment_date = request.form['appointment_date']
        slot_time = request.form['slot_time']
        status = request.form['status']
        symptoms = request.form['symptoms']
        phone_number = request.form['phone_number']

        sql = """
            UPDATE appointments SET
                patient_name=%s,
                doctor_name=%s,
                appointment_date=%s,
                slot_time=%s,
                status=%s,
                symptoms=%s,
                phone_number=%s
            WHERE id=%s
        """
        values = (patient_name, doctor_name, appointment_date, slot_time, status, symptoms, phone_number, id)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        flash('Appointment updated successfully!')
        return redirect(url_for('home'))

    # GET: show the existing values in the form
    cursor.execute("SELECT * FROM appointments WHERE id = %s", (id,))
    appointment = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_appointments.html', appointment=appointment)


@app.route('/delete/<int:id>')
def delete_appointment(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Appointment deleted successfully!')
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
