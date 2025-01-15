from flask import Flask, request, Response, redirect, send_file, render_template, send_from_directory, abort
import json
from haversine import haversine, Unit


class Nef:
    
    def __init__(self):
        try:
            with open('gnode_db.json') as f_in:
                self.db_gnodeb = json.load(f_in)
        except:
            self.db_gnodeb = { 'error_message':'empty db' }
    
    def get_closest_gnodeB(self, lat_mobile, lon_mobile)->dict:
        min_dist_km = 360000
        min_gn = {}
        for gn in self.db_gnodeb['db']:
            d = haversine((lat_mobile, lon_mobile), (gn['antenna_lat'],gn['antenna_lon']))
            if d < min_dist_km:
                min_gn = gn
        return gn

app = Flask(__name__)

@app.route("/api/elo/v1/nef_translate_mobile_ip_to_cell_id", methods=['GET'])
def nef_translate_mobile_ip_to_cell_id():
    
    ########################### REQUEST EXAMPLE ################################
    ## http://{{SERVER_vm}}:{{NEF_PORT}}/api/elo/v1/nef_translate_mobile_ip_to_cell_id?lat_mobile=45.119&lon_mobile=9.18
    ############################################################################

    ############################ RESPONSE EXAMPLE ############################################
    # {
    # "gnodeb_code": "NAB0001",
    # "tracking_area": "4300",
    # "antenna_lat": 0.0,
    # "antenna_lon": 0.0
    # }
    ##########################################################################################

    lat_mobile:float = None
    lon_mobile:float = None
    try:
         lat_mobile = float(request.args.get('lat_mobile'))
         lon_mobile = float(request.args.get('lon_mobile'))
    except:
        return json.dumps({ 'error_message':'wrong request parameters' }), 200
    gndb = Nef()
    
    return json.dumps(gndb.get_closest_gnodeB(lat_mobile, lon_mobile)), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9001) 