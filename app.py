from flask import Flask, render_template, request, send_file
from scraper import scrape_case_data, CASE_TYPES
from database import init_database, get_query_history, get_query_stats
import os

app = Flask(__name__)

# Initialize database on startup
init_database()

@app.route('/')
def index():
    return render_template('index.html', case_types=CASE_TYPES)

@app.route('/fetch', methods=['POST'])
def fetch():
    case_type = request.form['case_type']
    case_number = request.form['case_number']
    filing_year = request.form['filing_year']
    
    try:
        # Scrape data
        result = scrape_case_data(case_type, case_number, filing_year)
        if not result:
            return render_template('results.html', error="Invalid case number or site fucked up.")
        
        return render_template('results.html', data=result)
    except Exception as e:
        return render_template('results.html', error=f"Shit hit the fan: {str(e)}")

@app.route('/download/<filename>')
def download_pdf(filename):
    path = os.path.join('static/downloads', filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return"File got fucked, not found.", 404

@app.route('/history')
def history():
    """Show query history"""
    history_data = get_query_history(20)
    return render_template('history.html', history=history_data)

@app.route('/stats')
def stats():
    """Show query statistics"""
    stats_data = get_query_stats()
    return render_template('stats.html', stats=stats_data)

@app.route('/health')
def health_check():
    """Health check endpoint for deployment platforms"""
    return {
        'status': 'healthy',
        'service': 'Court Data Fetcher',
        'version': '1.0.0'
    }

if __name__ == '__main__':
    # Production configuration
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host=host, port=port, debug=debug)