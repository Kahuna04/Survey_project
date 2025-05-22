#!/usr/bin/env python3
"""
Simple Web GUI for Survey and Matrix Operations
No external dependencies required - uses Python's built-in modules only!
"""

import http.server
import socketserver
import json
import urllib.parse
import webbrowser
import threading
import time
import math
import sys
from io import StringIO

class SurveyMatrixHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_main_page().encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            if self.path == '/calculate_survey':
                result = self.calculate_survey(data)
            elif self.path == '/calculate_matrix':
                result = self.calculate_matrix(data)
            else:
                result = {'error': 'Invalid endpoint'}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def calculate_survey(self, data):
        try:
            origin_easting = float(data['origin_easting'])
            origin_northing = float(data['origin_northing'])
            distances = [float(d) for d in data['distances']]
            bearings = [float(b) for b in data['bearings']]
            
            # Calculate boundary coordinates
            coordinates = [(origin_easting, origin_northing)]
            current_easting = origin_easting
            current_northing = origin_northing
            
            for i in range(len(distances)):
                bearing_rad = math.radians(bearings[i])
                delta_easting = distances[i] * math.sin(bearing_rad)
                delta_northing = distances[i] * math.cos(bearing_rad)
                current_easting += delta_easting
                current_northing += delta_northing
                coordinates.append((current_easting, current_northing))
            
            # Calculate area using cross coordinate method
            eastings = [coord[0] for coord in coordinates]
            northings = [coord[1] for coord in coordinates]
            
            if eastings[0] != eastings[-1] or northings[0] != northings[-1]:
                eastings.append(eastings[0])
                northings.append(northings[0])
            
            area_sum1 = sum(eastings[i] * northings[i+1] for i in range(len(eastings) - 1))
            area_sum2 = sum(northings[i] * eastings[i+1] for i in range(len(eastings) - 1))
            
            area_square_meters = abs(area_sum1 - area_sum2) / 2
            area_acres = area_square_meters * 0.000247105
            
            return {
                'coordinates': coordinates,
                'area_square_meters': area_square_meters,
                'area_acres': area_acres
            }
            
        except Exception as e:
            return {'error': f'Survey calculation error: {str(e)}'}
    
    def calculate_matrix(self, data):
        try:
            matrix_a = data['matrix_a']
            matrix_b = data['matrix_b']
            
            # Simple matrix operations without numpy
            def matrix_add(a, b):
                if len(a) != len(b) or len(a[0]) != len(b[0]):
                    return None, "Matrices must have same dimensions for addition"
                result = []
                for i in range(len(a)):
                    row = []
                    for j in range(len(a[0])):
                        row.append(a[i][j] + b[i][j])
                    result.append(row)
                return result, None
            
            def matrix_subtract(a, b):
                if len(a) != len(b) or len(a[0]) != len(b[0]):
                    return None, "Matrices must have same dimensions for subtraction"
                result = []
                for i in range(len(a)):
                    row = []
                    for j in range(len(a[0])):
                        row.append(a[i][j] - b[i][j])
                    result.append(row)
                return result, None
            
            def matrix_multiply(a, b):
                if len(a[0]) != len(b):
                    return None, "Number of columns in first matrix must equal number of rows in second matrix"
                result = []
                for i in range(len(a)):
                    row = []
                    for j in range(len(b[0])):
                        sum_val = 0
                        for k in range(len(b)):
                            sum_val += a[i][k] * b[k][j]
                        row.append(sum_val)
                    result.append(row)
                return result, None
            
            add_result, add_error = matrix_add(matrix_a, matrix_b)
            sub_result, sub_error = matrix_subtract(matrix_a, matrix_b)
            mul_result, mul_error = matrix_multiply(matrix_a, matrix_b)
            
            return {
                'matrix_a': matrix_a,
                'matrix_b': matrix_b,
                'addition': {'result': add_result, 'error': add_error},
                'subtraction': {'result': sub_result, 'error': sub_error},
                'multiplication': {'result': mul_result, 'error': mul_error}
            }
            
        except Exception as e:
            return {'error': f'Matrix calculation error: {str(e)}'}
    
    def get_main_page(self):
        return '''<!DOCTYPE html>
<html>
<head>
    <title>Survey and Matrix Operations Suite</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .tabs {
            display: flex;
            margin-bottom: 20px;
            border-bottom: 2px solid #ddd;
        }
        .tab {
            background-color: #f1f1f1;
            border: none;
            padding: 12px 24px;
            cursor: pointer;
            margin-right: 5px;
            border-radius: 5px 5px 0 0;
            font-size: 16px;
        }
        .tab.active {
            background-color: #007bff;
            color: white;
        }
        .tab-content {
            display: none;
            padding: 20px;
        }
        .tab-content.active {
            display: block;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        input, textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            box-sizing: border-box;
        }
        button {
            background-color: #007bff;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px 0;
        }
        button:hover {
            background-color: #0056b3;
        }
        .results {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 15px;
            margin-top: 20px;
            white-space: pre-wrap;
            font-family: monospace;
            max-height: 400px;
            overflow-y: auto;
        }
        .boundary-grid {
            display: grid;
            grid-template-columns: auto 1fr 1fr;
            gap: 10px;
            align-items: center;
            margin: 10px 0;
        }
        .boundary-grid label {
            margin: 0;
        }
        .matrix-input {
            display: inline-block;
            margin: 10px;
        }
        .matrix-grid {
            display: inline-grid;
            gap: 5px;
            margin: 10px 0;
        }
        .matrix-cell {
            width: 60px;
            padding: 5px;
            text-align: center;
        }
        .error {
            color: #dc3545;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Survey and Matrix Operations Suite</h1>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('survey')">Survey Calculator</button>
            <button class="tab" onclick="showTab('matrix')">Matrix Operations</button>
        </div>
        
        <div id="survey" class="tab-content active">
            <h2>Survey Boundary Calculator</h2>
            <form id="surveyForm">
                <div class="form-group">
                    <label>Origin Easting:</label>
                    <input type="number" id="originEasting" step="any" required>
                </div>
                <div class="form-group">
                    <label>Origin Northing:</label>
                    <input type="number" id="originNorthing" step="any" required>
                </div>
                <div class="form-group">
                    <label>Boundary Lines:</label>
                    <div id="boundaryLines">
                        <div class="boundary-grid">
                            <label>Line 1:</label>
                            <input type="number" placeholder="Distance (m)" class="distance" step="any">
                            <input type="number" placeholder="Bearing (°)" class="bearing" step="any">
                        </div>
                    </div>
                    <button type="button" onclick="addBoundaryLine()">Add Line</button>
                    <button type="button" onclick="removeBoundaryLine()">Remove Line</button>
                </div>
                <button type="submit">Calculate Survey</button>
            </form>
            <div id="surveyResults" class="results"></div>
        </div>
        
        <div id="matrix" class="tab-content">
            <h2>Matrix Operations Calculator</h2>
            <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                <div class="matrix-input">
                    <h3>Matrix A</h3>
                    <label>Rows: <input type="number" id="matrixARows" value="2" min="1" max="5" onchange="generateMatrixGrid('A')"></label>
                    <label>Cols: <input type="number" id="matrixACols" value="2" min="1" max="5" onchange="generateMatrixGrid('A')"></label>
                    <div id="matrixAGrid" class="matrix-grid"></div>
                </div>
                <div class="matrix-input">
                    <h3>Matrix B</h3>
                    <label>Rows: <input type="number" id="matrixBRows" value="2" min="1" max="5" onchange="generateMatrixGrid('B')"></label>
                    <label>Cols: <input type="number" id="matrixBCols" value="2" min="1" max="5" onchange="generateMatrixGrid('B')"></label>
                    <div id="matrixBGrid" class="matrix-grid"></div>
                </div>
            </div>
            <button onclick="calculateMatrix()">Calculate Matrix Operations</button>
            <div id="matrixResults" class="results"></div>
        </div>
    </div>

    <script>
        let boundaryLineCount = 1;
        
        function showTab(tabName) {
            // Hide all tab contents
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            // Remove active class from all tabs
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // Show selected tab content
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked tab
            event.target.classList.add('active');
        }
        
        function addBoundaryLine() {
            boundaryLineCount++;
            const container = document.getElementById('boundaryLines');
            const newLine = document.createElement('div');
            newLine.className = 'boundary-grid';
            newLine.innerHTML = `
                <label>Line ${boundaryLineCount}:</label>
                <input type="number" placeholder="Distance (m)" class="distance" step="any">
                <input type="number" placeholder="Bearing (°)" class="bearing" step="any">
            `;
            container.appendChild(newLine);
        }
        
        function removeBoundaryLine() {
            if (boundaryLineCount > 1) {
                const container = document.getElementById('boundaryLines');
                container.removeChild(container.lastElementChild);
                boundaryLineCount--;
            }
        }
        
        function generateMatrixGrid(matrix) {
            const rows = parseInt(document.getElementById(`matrix${matrix}Rows`).value);
            const cols = parseInt(document.getElementById(`matrix${matrix}Cols`).value);
            const grid = document.getElementById(`matrix${matrix}Grid`);
            
            grid.innerHTML = '';
            grid.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
            
            for (let i = 0; i < rows; i++) {
                for (let j = 0; j < cols; j++) {
                    const input = document.createElement('input');
                    input.type = 'number';
                    input.className = 'matrix-cell';
                    input.value = '0';
                    input.step = 'any';
                    grid.appendChild(input);
                }
            }
        }
        
        document.getElementById('surveyForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const originEasting = parseFloat(document.getElementById('originEasting').value);
            const originNorthing = parseFloat(document.getElementById('originNorthing').value);
            
            const distances = Array.from(document.querySelectorAll('.distance'))
                .map(input => input.value.trim())
                .filter(val => val !== '')
                .map(val => parseFloat(val));
            
            const bearings = Array.from(document.querySelectorAll('.bearing'))
                .map(input => input.value.trim())
                .filter(val => val !== '')
                .map(val => parseFloat(val));
            
            if (distances.length !== bearings.length || distances.length === 0) {
                document.getElementById('surveyResults').innerHTML = 
                    '<div class="error">Please enter matching distances and bearings for all boundary lines.</div>';
                return;
            }
            
            const data = {
                origin_easting: originEasting,
                origin_northing: originNorthing,
                distances: distances,
                bearings: bearings
            };
            
            fetch('/calculate_survey', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.error) {
                    document.getElementById('surveyResults').innerHTML = 
                        `<div class="error">${result.error}</div>`;
                } else {
                    let output = '=== BOUNDARY COORDINATES ===\\n';
                    output += 'Pillar\\tEasting\\t\\tNorthing\\n';
                    output += '----------------------------------------\\n';
                    
                    result.coordinates.forEach((coord, i) => {
                        output += `${i+1}\\t${coord[0].toFixed(3)}\\t\\t${coord[1].toFixed(3)}\\n`;
                    });
                    
                    output += '\\n=== LAND AREA ===\\n';
                    output += `Area: ${result.area_square_meters.toFixed(3)} square meters\\n`;
                    output += `Area: ${result.area_acres.toFixed(5)} acres`;
                    
                    document.getElementById('surveyResults').textContent = output;
                }
            })
            .catch(error => {
                document.getElementById('surveyResults').innerHTML = 
                    `<div class="error">Error: ${error.message}</div>`;
            });
        });
        
        function calculateMatrix() {
            const rowsA = parseInt(document.getElementById('matrixARows').value);
            const colsA = parseInt(document.getElementById('matrixACols').value);
            const rowsB = parseInt(document.getElementById('matrixBRows').value);
            const colsB = parseInt(document.getElementById('matrixBCols').value);
            
            const matrixA = [];
            const cellsA = document.querySelectorAll('#matrixAGrid .matrix-cell');
            for (let i = 0; i < rowsA; i++) {
                const row = [];
                for (let j = 0; j < colsA; j++) {
                    row.push(parseFloat(cellsA[i * colsA + j].value) || 0);
                }
                matrixA.push(row);
            }
            
            const matrixB = [];
            const cellsB = document.querySelectorAll('#matrixBGrid .matrix-cell');
            for (let i = 0; i < rowsB; i++) {
                const row = [];
                for (let j = 0; j < colsB; j++) {
                    row.push(parseFloat(cellsB[i * colsB + j].value) || 0);
                }
                matrixB.push(row);
            }
            
            const data = {
                matrix_a: matrixA,
                matrix_b: matrixB
            };
            
            fetch('/calculate_matrix', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.error) {
                    document.getElementById('matrixResults').innerHTML = 
                        `<div class="error">${result.error}</div>`;
                } else {
                    let output = '=== INPUT MATRICES ===\\n';
                    output += 'Matrix A:\\n';
                    result.matrix_a.forEach(row => {
                        output += '[' + row.map(val => val.toFixed(2)).join('\\t') + ']\\n';
                    });
                    output += '\\nMatrix B:\\n';
                    result.matrix_b.forEach(row => {
                        output += '[' + row.map(val => val.toFixed(2)).join('\\t') + ']\\n';
                    });
                    
                    output += '\\n=== OPERATIONS ===\\n';
                    
                    if (result.addition.result) {
                        output += 'Addition (A + B):\\n';
                        result.addition.result.forEach(row => {
                            output += '[' + row.map(val => val.toFixed(2)).join('\\t') + ']\\n';
                        });
                    } else {
                        output += 'Addition: ' + result.addition.error + '\\n';
                    }
                    output += '\\n';
                    
                    if (result.subtraction.result) {
                        output += 'Subtraction (A - B):\\n';
                        result.subtraction.result.forEach(row => {
                            output += '[' + row.map(val => val.toFixed(2)).join('\\t') + ']\\n';
                        });
                    } else {
                        output += 'Subtraction: ' + result.subtraction.error + '\\n';
                    }
                    output += '\\n';
                    
                    if (result.multiplication.result) {
                        output += 'Multiplication (A × B):\\n';
                        result.multiplication.result.forEach(row => {
                            output += '[' + row.map(val => val.toFixed(2)).join('\\t') + ']\\n';
                        });
                    } else {
                        output += 'Multiplication: ' + result.multiplication.error + '\\n';
                    }
                    
                    document.getElementById('matrixResults').textContent = output;
                }
            })
            .catch(error => {
                document.getElementById('matrixResults').innerHTML = 
                    `<div class="error">Error: ${error.message}</div>`;
            });
        }
        
        // Initialize matrix grids
        generateMatrixGrid('A');
        generateMatrixGrid('B');
    </script>
</body>
</html>'''

def start_server(port=8000):
    """Start the web server."""
    handler = SurveyMatrixHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"")
            print(f"🚀 Survey and Matrix Operations Suite")
            print(f"📊 Web interface running at: http://localhost:{port}")
            print(f"🌐 Open your browser and go to the URL above")
            print(f"")
            print(f"Press Ctrl+C to stop the server")
            print(f"=" * 50)
            
            # Try to open browser automatically
            def open_browser():
                time.sleep(1)
                try:
                    webbrowser.open(f'http://localhost:{port}')
                except:
                    pass
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"Port {port} is already in use. Trying port {port + 1}...")
            start_server(port + 1)
        else:
            raise

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print(f"\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)