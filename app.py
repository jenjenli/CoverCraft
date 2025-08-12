from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from main import generate_ai_letter

app = Flask(__name__)

app.config['ARLIA_API_KEY'] = os.getenv('ARLIA_API_KEY')

dataset_path = 'cover_letter_data.csv'

def save_to_csv(data):
    file_exists = os.path.isfile(dataset_path)

    with open(dataset_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(['name', 'job_title', 'company', 'skills', 'experience'])

        writer.writerow([data['name'], data['job_title'], data['company'], data['skills'], data['experience']])

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    try:
        print("Generating cover letter...")
        # Get data from form
        name = request.form['name']
        job_title = request.form['job_title']
        company = request.form['company']
        skills = request.form['skills']
        experience = request.form.get('experience', '')  # Handle optional field
        print("Got data")

        form_data = {
            'name': name,
            'job_title': job_title,
            'company': company,
            'skills': skills,
            'experience': experience
        }

        # Save to dataset
        save_to_csv(form_data)
        
        # Generate AI letter
        letter = generate_ai_letter(name, job_title, company, skills, experience)
        
        # Modern HTML response with improved styling
        html_response = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Your Cover Letter - Ready!</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}

                body {{
                    min-height: 100vh;
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }}

                .header {{
                    text-align: center;
                    color: white;
                    margin-bottom: 30px;
                    animation: fadeInDown 0.8s ease-out;
                }}

                .header h1 {{
                    font-size: 2.5rem;
                    font-weight: 700;
                    margin-bottom: 8px;
                    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
                }}

                .header p {{
                    font-size: 1.2rem;
                    opacity: 0.9;
                }}

                .letter-container {{
                    background: rgba(255, 255, 255, 0.95);
                    backdrop-filter: blur(20px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 24px;
                    padding: 40px;
                    max-width: 800px;
                    width: 100%;
                    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
                    animation: slideInUp 1s ease-out;
                    margin-bottom: 30px;
                }}

                .letter-content {{
                    white-space: pre-wrap;
                    word-wrap: break-word;
                    line-height: 1.7;
                    font-size: 16px;
                    color: #374151;
                    font-family: 'Georgia', serif;
                }}

                .actions {{
                    display: flex;
                    gap: 15px;
                    justify-content: center;
                    flex-wrap: wrap;
                    animation: fadeInUp 1s ease-out 0.5s both;
                }}

                .btn {{
                    padding: 14px 28px;
                    border: none;
                    border-radius: 12px;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    position: relative;
                    overflow: hidden;
                }}

                .btn-primary {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
                }}

                .btn-secondary {{
                    background: rgba(255, 255, 255, 0.9);
                    color: #667eea;
                    border: 2px solid #667eea;
                }}

                .btn:hover {{
                    transform: translateY(-3px);
                }}

                .btn-primary:hover {{
                    box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
                }}

                .btn-secondary:hover {{
                    background: rgba(102, 126, 234, 0.1);
                    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
                }}

                .stats {{
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 16px;
                    padding: 20px;
                    margin-top: 20px;
                    color: white;
                    text-align: center;
                    animation: fadeInUp 1s ease-out 0.7s both;
                }}

                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                    gap: 20px;
                    margin-top: 15px;
                }}

                .stat-item {{
                    text-align: center;
                }}

                .stat-number {{
                    font-size: 1.5rem;
                    font-weight: 700;
                    display: block;
                }}

                .stat-label {{
                    font-size: 0.9rem;
                    opacity: 0.8;
                }}

                @keyframes fadeInDown {{
                    from {{ opacity: 0; transform: translateY(-30px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}

                @keyframes slideInUp {{
                    from {{ opacity: 0; transform: translateY(50px) scale(0.95); }}
                    to {{ opacity: 1; transform: translateY(0) scale(1); }}
                }}

                @keyframes fadeInUp {{
                    from {{ opacity: 0; transform: translateY(30px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}

                @media (max-width: 600px) {{
                    body {{ padding: 15px; }}
                    .letter-container {{ padding: 25px; }}
                    .header h1 {{ font-size: 2rem; }}
                    .actions {{ flex-direction: column; align-items: center; }}
                    .btn {{ width: 100%; max-width: 280px; }}
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎉 Your Cover Letter is Ready!</h1>
                <p>AI-generated and personalized for {company}</p>
            </div>

            <div class="letter-container">
                <div class="letter-content">{letter}</div>
            </div>

            <div class="actions">
                <a href="/" class="btn btn-primary">Generate Another Letter</a>
                <button onclick="copyToClipboard()" class="btn btn-secondary">📋 Copy to Clipboard</button>
                <button onclick="downloadPDF()" class="btn btn-secondary">📄 Download PDF</button>
            </div>

            <div class="stats">
                <h3>✨ Letter Statistics</h3>
                <div class="stats-grid">
                    <div class="stat-item">
                        <span class="stat-number" id="wordCount">-</span>
                        <span class="stat-label">Words</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number" id="charCount">-</span>
                        <span class="stat-label">Characters</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">⚡</span>
                        <span class="stat-label">AI-Powered</span>
                    </div>
                </div>
            </div>

            <script>
                const letterText = document.querySelector('.letter-content').textContent;
                const wordCount = letterText.trim().split(/\\s+/).length;
                const charCount = letterText.length;
                
                document.getElementById('wordCount').textContent = wordCount;
                document.getElementById('charCount').textContent = charCount;

                async function copyToClipboard() {{
                    try {{
                        await navigator.clipboard.writeText(letterText);
                        
                        const btn = event.target;
                        const originalText = btn.textContent;
                        btn.textContent = '✅ Copied!';
                        btn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                        
                        setTimeout(() => {{
                            btn.textContent = originalText;
                            btn.style.background = '';
                        }}, 2000);
                    }} catch (err) {{
                        alert('Failed to copy to clipboard');
                    }}
                }}

                function downloadPDF() {{
                    const element = document.querySelector('.letter-content');
                    const opt = {{
                        margin: 1,
                        filename: 'cover-letter-{name.lower().replace(" ", "-")}.pdf',
                        image: {{ type: 'jpeg', quality: 0.98 }},
                        html2canvas: {{ scale: 2 }},
                        jsPDF: {{ unit: 'in', format: 'letter', orientation: 'portrait' }}
                    }};
                    
                    alert('PDF download feature requires additional setup. Copy the text for now!');
                }}

                window.addEventListener('scroll', () => {{
                    const scrolled = window.pageYOffset;
                    const parallax = document.querySelector('body');
                    const speed = scrolled * 0.1;
                    parallax.style.backgroundPosition = `center ${{speed}}px`;
                }});
            </script>
        </body>
        </html>
        """
        return html_response
    
    except Exception as e:
        # Error handling with styled error page
        error_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Oops! Something went wrong</title>
            <style>
                body {{
                    font-family: 'Inter', sans-serif;
                    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    text-align: center;
                    padding: 20px;
                }}
                .error-container {{
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(20px);
                    border-radius: 24px;
                    padding: 40px;
                    max-width: 500px;
                }}
                .error-icon {{ font-size: 4rem; margin-bottom: 20px; }}
                h1 {{ font-size: 2rem; margin-bottom: 15px; }}
                p {{ font-size: 1.1rem; margin-bottom: 30px; opacity: 0.9; }}
                .btn {{
                    background: rgba(255, 255, 255, 0.2);
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 12px;
                    text-decoration: none;
                    display: inline-block;
                    transition: all 0.3s;
                }}
                .btn:hover {{ background: rgba(255, 255, 255, 0.3); }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <div class="error-icon">😞</div>
                <h1>Oops! Something went wrong</h1>
                <p>We couldn't generate your cover letter right now. Please try again.</p>
                <a href="/" class="btn">← Back to Form</a>
            </div>
        </body>
        </html>
        """
        return error_html, 500

if __name__ == '__main__':
    app.run(debug=True)