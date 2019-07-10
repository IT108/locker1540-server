from flask import Flask, request, render_template, jsonify
from telemetry_processing import process_status, select_status
import telemetry_serial
app = Flask(__name__)


@app.route('/locker/api/monitor/status', methods=['GET'])
def get_status():
    return render_template('status.html', sysstatus=select_status())


@app.route('/locker/api/monitor/status', methods=['POST'])
def update_status():
    return jsonify({'data': render_template('status_table.html', sysstatus=select_status())})


@app.route('/locker/api/telemetry/status', methods=['POST'])
def set_status():
    print(request.form['status'])
    process_status(request.form['status'])
    return ''


@app.route('/locker/api/telemetry/request_status', methods=['POST'])
def request_status():
    telemetry_serial.request_status()
    return ''


if __name__ == '__main__':
    if not telemetry_serial.start_serial():
        exit(1)
    app.run()
