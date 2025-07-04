import os
import json
import logging
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from forms import WorkerRegistrationForm, ContactForm

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_workers():
    """Load workers from JSON file"""
    try:
        with open('data/workers.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_workers(workers):
    """Save workers to JSON file"""
    os.makedirs('data', exist_ok=True)
    with open('data/workers.json', 'w') as f:
        json.dump(workers, f, indent=2)

@app.route('/')
def index():
    """Homepage with hero section and service categories"""
    workers = load_workers()
    featured_workers = workers[:6]  # Show first 6 workers as featured
    
    # Service categories with icons
    services = [
        {
            'name': 'Plumbing',
            'icon': 'fas fa-wrench',
            'description': 'Professional plumbing services for all your needs',
            'image': 'https://pixabay.com/get/g1ea02cf2c4e9cfeafe49de82b2767b23eaf31220af6f11963bbd51c82f90558e3d353be9c659a28a8ded0700dce28cba9af85195ab50a3be4f4df43555e1f12c_1280.jpg'
        },
        {
            'name': 'Electrical',
            'icon': 'fas fa-bolt',
            'description': 'Certified electricians for safe electrical work',
            'image': 'https://pixabay.com/get/g000c59090e47f5f683bb2f331bafa7cc9d877d23ee7fc321bb64bc0ce5af6590deb18d3c9000059d77200da4659185d9b23c85cd43a6fe23657064f17f188844_1280.jpg'
        },
        {
            'name': 'Carpentry',
            'icon': 'fas fa-hammer',
            'description': 'Skilled carpenters for construction and repairs',
            'image': 'https://pixabay.com/get/g2b2bf796ada76e289830baeb30d026982abc92ebcbae4283e7af2ae643e31140b4c2a934a828a74a4e20faabb78c730f49dcdde38700587ddd3eafd55d5a65e2_1280.jpg'
        },
        {
            'name': 'Cleaning',
            'icon': 'fas fa-broom',
            'description': 'Professional cleaning services for homes and offices',
            'image': 'https://pixabay.com/get/g7325fa06d11860894b9072dbdb17569de6d7c7e6373701d5cebd22f08e1042d71541c375fda79e6abb951e2cee2d189be9cd7a05eab1c293328d07c05d6faaee_1280.jpg'
        }
    ]
    
    # Testimonials
    testimonials = [
        {
            'name': 'Sarah Johnson',
            'rating': 5,
            'comment': 'Found an excellent plumber through this platform. Quick, professional, and affordable!',
            'image': 'https://pixabay.com/get/g99523402a6c818ca7d1b9b05e13a7ab13a17200495def5cbffbfd7c865a7a6ac6c55b0feac61fbc66aa5e8318db522aafb32304fcc7497dde9f4ee2b78cfca62_1280.jpg'
        },
        {
            'name': 'Michael Chen',
            'rating': 5,
            'comment': 'Great experience! The electrician was knowledgeable and fixed the issue quickly.',
            'image': 'https://pixabay.com/get/ga653e0f7c04253d58d4e7238089ae02ccbcfc8e93d778ff9701ec5248e9ebb10a4dd11801c1bf674ba7134a680d6de465e5135f607f87fae98f21138d53e04e3_1280.jpg'
        },
        {
            'name': 'Emma Davis',
            'rating': 5,
            'comment': 'Highly recommend! Found a reliable cleaning service that exceeded expectations.',
            'image': 'https://pixabay.com/get/ga0139820ef7008bab6d24ccf1ce45be5d26cabaaeca1741dccf171cf0eb2e664ad5ebd28864333fb56d1526d5fb620f5eabd7ff4e98fe014ed18cc7078e2e825_1280.jpg'
        }
    ]
    
    return render_template('index.html', services=services, featured_workers=featured_workers, testimonials=testimonials)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Worker registration form"""
    form = WorkerRegistrationForm()
    
    if form.validate_on_submit():
        workers = load_workers()
        
        # Handle file upload
        profile_image = None
        if form.profile_image.data:
            file = form.profile_image.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename to avoid conflicts
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_image = filename
        
        # Create new worker
        new_worker = {
            'id': len(workers) + 1,
            'name': form.name.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'service': form.service.data,
            'location': form.location.data,
            'experience': form.experience.data,
            'description': form.description.data,
            'rate': form.rate.data,
            'availability': form.availability.data,
            'profile_image': profile_image,
            'created_at': datetime.now().isoformat(),
            'rating': 0,
            'reviews': []
        }
        
        workers.append(new_worker)
        save_workers(workers)
        
        flash('Registration successful! Your profile has been created.', 'success')
        return redirect(url_for('workers'))
    
    return render_template('register.html', form=form)

@app.route('/workers')
def workers():
    """Searchable and filterable worker directory"""
    workers = load_workers()
    
    # Get filter parameters
    service_filter = request.args.get('service', '')
    location_filter = request.args.get('location', '')
    search_query = request.args.get('search', '')
    
    # Apply filters
    filtered_workers = workers
    
    if service_filter:
        filtered_workers = [w for w in filtered_workers if w['service'].lower() == service_filter.lower()]
    
    if location_filter:
        filtered_workers = [w for w in filtered_workers if location_filter.lower() in w['location'].lower()]
    
    if search_query:
        filtered_workers = [w for w in filtered_workers if 
                          search_query.lower() in w['name'].lower() or 
                          search_query.lower() in w['description'].lower()]
    
    # Get unique services and locations for filter dropdowns
    services = list(set(w['service'] for w in workers))
    locations = list(set(w['location'] for w in workers))
    
    return render_template('workers.html', 
                         workers=filtered_workers,
                         services=services,
                         locations=locations,
                         current_service=service_filter,
                         current_location=location_filter,
                         current_search=search_query)

@app.route('/worker/<int:worker_id>')
def worker_profile(worker_id):
    """Individual worker profile page"""
    workers = load_workers()
    worker = next((w for w in workers if w['id'] == worker_id), None)
    
    if not worker:
        flash('Worker not found.', 'error')
        return redirect(url_for('workers'))
    
    return render_template('worker_profile.html', worker=worker)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form"""
    form = ContactForm()
    
    if form.validate_on_submit():
        # In a real application, you would send an email or save to database
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', form=form)

@app.route('/api/workers')
def api_workers():
    """API endpoint for workers (for AJAX requests)"""
    workers = load_workers()
    return jsonify(workers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
