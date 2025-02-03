from flask import Flask, request, send_file
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import io

app = Flask(__name__)

@app.route('/rlocus', methods=['GET'])
def rlocus():
    poles = request.args.get("poles", "").split()
    zeros = request.args.get("zeros", "").split()
    
    try:
        poles = [complex(x) for x in poles]
        zeros = [complex(x) for x in zeros]

        system = ctrl.TransferFunction(np.poly(zeros), np.poly(poles))

        plt.figure()
        ctrl.rlocus(system, grid=True)
        plt.title("Lugar das Raízes")
        plt.xlabel("Parte Real")
        plt.ylabel("Parte Imaginária")

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        return send_file(img, mimetype='image/png')

    except Exception as e:
        return {"error": str(e)}, 400

if __name__ == '__main__':
    app.run(debug=True)
