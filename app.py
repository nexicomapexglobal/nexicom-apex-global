from pathlib import Path
import os, re, uuid
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from models import db, AdminUser, SiteSetting, NavItem, Service, TeamMember, Review, Job, JobApplication, Page, ContactMessage
from dotenv import load_dotenv

BASE=Path(__file__).resolve().parent; load_dotenv(BASE/'.env')
app=Flask(__name__)
database_url = os.getenv('DATABASE_URL')
if not database_url:
    database_path = (BASE / 'instance' / 'nexicom.db').resolve()
    database_url = f"sqlite:///{database_path.as_posix()}"

app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'change-this-before-launch'),
    SQLALCHEMY_DATABASE_URI=database_url,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    UPLOAD_FOLDER=str(BASE / 'static' / 'uploads'),
    MAX_CONTENT_LENGTH=12 * 1024 * 1024,
)
db.init_app(app); login_manager=LoginManager(app); login_manager.login_view='admin_login'; login_manager.login_message_category='warning'
ALLOWED={'png','jpg','jpeg','webp','pdf','doc','docx'}
DEFAULT={
'site_name':'Nexicom Apex Global','tagline':'CONNECT • GROW • ENGAGE','address':'BPC, Third Floor, No.25, Bore Bank Road, Benson Town, Bangalore - 560 046.','phone':'+91 00000 00000','email':'hello@nexicomapexglobal.com','whatsapp':'910000000000','logo':'images/nexicom-logo-transparent.png','hero_eyebrow':'Recruitment • BPO • Consulting','hero_title':'People, process and performance built for business growth.','hero_text':'Nexicom Apex Global helps businesses hire better, engage customers and scale operations with accountable teams and practical consulting.','hero_primary_label':'Hire Talent','hero_primary_url':'/contact','hero_secondary_label':'Explore Services','hero_secondary_url':'#services','about_title':'A growth partner built around people','about_text':'We combine recruitment expertise, business process support and consulting discipline to help organizations build high-performing teams and better customer experiences.','why_title':'Why Nexicom Apex Global','why_text':'Clear ownership, measurable execution and people-first partnerships.','careers_title':'Build your career with Nexicom','careers_text':'Join a team that values communication, ownership, learning and consistent performance.','contact_title':'Let’s build something stronger','contact_text':'Tell us about your hiring, outsourcing or consulting requirement.','footer_text':'Nexicom Apex Global. Connect • Grow • Engage.','primary_color':'#078C96','deep_color':'#00616B','dark_color':'#004E59','bright_color':'#19B7C2','light_color':'#73D5DC','background_color':'#031419','text_color':'#EDFDFE','font_family':'Inter, Arial, sans-serif','border_radius':'22','custom_css':'','stat_candidates':'500+','stat_clients':'40+','stat_projects':'75+','stat_recruiters':'12+','show_services':'1','show_team':'1','show_reviews':'1','show_about':'1','show_careers':'1','show_contact':'1','animation_style':'fade-up','animation_speed':'700','popup_style':'zoom','meta_title':'Nexicom Apex Global | Recruitment, BPO & Business Consulting','meta_description':'Nexicom Apex Global provides recruitment, staffing, BPO, HR consulting, lead generation and business growth solutions in Bangalore.'}

@login_manager.user_loader
def load_user(i): return db.session.get(AdminUser,int(i))
def get_settings():
    d=DEFAULT.copy(); d.update({x.key:x.value for x in SiteSetting.query.all()}); return d
def save_setting(k,v):
    x=SiteSetting.query.filter_by(key=k).first()
    if x:x.value=v
    else:db.session.add(SiteSetting(key=k,value=v))
def slugify(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-') or uuid.uuid4().hex[:8]
def upload(file, folder='media'):
    if not file or not file.filename:return ''
    ext=file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else ''
    if ext not in ALLOWED:return ''
    name=f'{uuid.uuid4().hex}.{ext}'; p=Path(app.config['UPLOAD_FOLDER'])/folder; p.mkdir(parents=True,exist_ok=True); file.save(p/name); return f'uploads/{folder}/{name}'
def boolf(name): return request.form.get(name)=='on'

@app.context_processor
def inject():
    return {
        'site': get_settings(),
        'nav_items': NavItem.query.filter_by(is_active=True).order_by(NavItem.sort_order).all(),
        # Required by the footer on every public page, including service detail pages.
        'services': Service.query.filter_by(is_active=True).order_by(Service.sort_order).all(),
    }

def seed():
    email=os.getenv('ADMIN_EMAIL','admin@nexicomapexglobal.com').lower()
    if not AdminUser.query.filter_by(email=email).first():
        u=AdminUser(name=os.getenv('ADMIN_NAME','Nexicom Admin'),email=email); u.set_password(os.getenv('ADMIN_PASSWORD','Admin@123')); db.session.add(u)
    for k,v in DEFAULT.items():
        if not SiteSetting.query.filter_by(key=k).first():db.session.add(SiteSetting(key=k,value=v))
    if not NavItem.query.count():
        for a,b,c in [('Home','/',1),('About','/about',2),('Services','/#services',3),('Team','/#team',4),('Careers','/careers',5),('Contact','/contact',6)]:db.session.add(NavItem(label=a,url=b,sort_order=c))
    if not Service.query.count():
        data=[('Recruitment & Staffing','Talent acquisition, bulk hiring and workforce solutions.','👥'),('BPO Solutions','Voice, non-voice and customer operations built for scale.','🎧'),('HR Consulting','Practical HR systems, compliance and performance support.','⚙'),('Sales & Lead Generation','Qualified opportunities and structured customer outreach.','↗'),('Customer Support','Responsive customer care across channels.','◎'),('Corporate Training','Communication, sales and leadership capability building.','✦'),('Business Consulting','Process improvement, growth strategy and execution support.','◆'),('Workforce Management','Contract staffing and accountable workforce operations.','▦')]
        for i,(t,d,ic) in enumerate(data,1):db.session.add(Service(title=t,slug=slugify(t),short_description=d,description=d,icon=ic,sort_order=i))
    for slug,title,eye,body in [('about','About Nexicom Apex Global','Who we are','Nexicom Apex Global is a people-first business growth company serving recruitment, BPO, HR consulting and business operations.\n\nOur mission is to connect capable people with meaningful opportunities and help businesses grow through disciplined execution.'),('contact','Contact Nexicom Apex Global','Let’s connect','Reach our team for recruitment, outsourcing, consulting, partnerships or career enquiries.')]:
        if not Page.query.filter_by(slug=slug).first():db.session.add(Page(slug=slug,title=title,eyebrow=eye,body=body))
    if not Review.query.count():
        db.session.add(Review(client_name='Business Partner',company='Confidential Client',service_used='Recruitment Support',rating=5,review_text='The Nexicom team brought structure, speed and accountability to our hiring process.',is_featured=True))
    db.session.commit()

with app.app_context():
    (BASE/'instance').mkdir(exist_ok=True); (BASE/'static'/'uploads').mkdir(parents=True,exist_ok=True); db.create_all(); seed()

@app.route('/')
def home(): return render_template('index.html',services=Service.query.filter_by(is_active=True).order_by(Service.sort_order).all(),team=TeamMember.query.filter_by(is_active=True).order_by(TeamMember.sort_order).all(),reviews=Review.query.filter_by(is_active=True).order_by(Review.sort_order).all(),jobs=Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).limit(3).all())
@app.route('/about')
def about(): return render_template('page.html',page=Page.query.filter_by(slug='about').first_or_404())
@app.route('/service/<slug>')
def service_detail(slug): return render_template('service.html',service=Service.query.filter_by(slug=slug,is_active=True).first_or_404())
@app.route('/careers')
def careers(): return render_template('careers.html',jobs=Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).all())
@app.route('/apply/<int:job_id>',methods=['GET','POST'])
def apply(job_id):
    job=db.get_or_404(Job,job_id)
    if request.method=='POST':
        if not all(request.form.get(x,'').strip() for x in ['name','email','phone']):flash('Please complete your name, email and phone.','warning')
        else:
            db.session.add(JobApplication(job_id=job.id,name=request.form['name'].strip(),email=request.form['email'].strip(),phone=request.form['phone'].strip(),experience=request.form.get('experience',''),message=request.form.get('message',''),resume=upload(request.files.get('resume'),'resumes'))); db.session.commit(); flash('Application submitted successfully.','success'); return redirect(url_for('careers'))
    return render_template('apply.html',job=job)
@app.route('/contact',methods=['GET','POST'])
def contact():
    page=Page.query.filter_by(slug='contact').first_or_404()
    if request.method=='POST':
        if not all(request.form.get(x,'').strip() for x in ['name','email','message']):flash('Please complete all required fields.','warning')
        else:db.session.add(ContactMessage(name=request.form['name'],email=request.form['email'],phone=request.form.get('phone',''),subject=request.form.get('subject',''),message=request.form['message']));db.session.commit();flash('Thank you. We will contact you soon.','success');return redirect(url_for('contact'))
    return render_template('contact.html',page=page)
@app.route('/robots.txt')
def robots(): return app.response_class('User-agent: *\nAllow: /\nSitemap: '+request.url_root.rstrip('/')+'/sitemap.xml\n',mimetype='text/plain')
@app.route('/sitemap.xml')
def sitemap():
    urls=[url_for('home',_external=True),url_for('about',_external=True),url_for('careers',_external=True),url_for('contact',_external=True)]+[url_for('service_detail',slug=s.slug,_external=True) for s in Service.query.filter_by(is_active=True)]
    return app.response_class('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{u}</loc></url>' for u in urls)+'</urlset>',mimetype='application/xml')

@app.route('/admin/login',methods=['GET','POST'])
def admin_login():
    if current_user.is_authenticated:return redirect(url_for('admin_dashboard'))
    if request.method=='POST':
        u=AdminUser.query.filter_by(email=request.form.get('email','').lower().strip()).first()
        if u and u.check_password(request.form.get('password','')):login_user(u);return redirect(url_for('admin_dashboard'))
        flash('Invalid email or password.','danger')
    return render_template('admin/login.html')
@app.route('/admin/logout')
@login_required
def admin_logout(): logout_user();return redirect(url_for('admin_login'))
@app.route('/admin')
@login_required
def admin_dashboard(): return render_template('admin/dashboard.html',service_count=Service.query.count(),team_count=TeamMember.query.count(),review_count=Review.query.count(),job_count=Job.query.count(),application_count=JobApplication.query.count(),message_count=ContactMessage.query.count(),recent_messages=ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all())

@app.route('/admin/design',methods=['GET','POST'])
@login_required
def admin_design():
    if request.method=='POST':
        for k in DEFAULT:
            if k.startswith('show_'):save_setting(k,'1' if request.form.get(k)=='on' else '0')
            elif k in request.form:save_setting(k,request.form.get(k,''))
        logo=upload(request.files.get('logo'),'branding')
        if logo:save_setting('logo',logo)
        db.session.commit();flash('Website settings updated.','success');return redirect(url_for('admin_design'))
    return render_template('admin/design.html')

def crud_model(model,template,kind,fields):
    obj_id=request.args.get('edit',type=int); obj=db.session.get(model,obj_id) if obj_id else None
    if request.method=='POST':
        oid=request.form.get('id',type=int); obj=db.session.get(model,oid) if oid else model()
        for f in fields:
            if f in ['is_active','is_featured']:setattr(obj,f,boolf(f))
            elif f in request.form:setattr(obj,f,request.form.get(f,''))
        if hasattr(obj,'sort_order'):obj.sort_order=request.form.get('sort_order',0,type=int)
        if model is Service:
            obj.slug=slugify(request.form.get('slug') or obj.title); img=upload(request.files.get('image'),'services'); obj.image=img or obj.image
        if model is TeamMember:
            img=upload(request.files.get('photo'),'team'); obj.photo=img or obj.photo
        if model is Review:
            obj.rating=max(1,min(5,request.form.get('rating',5,type=int))); img=upload(request.files.get('photo'),'reviews'); obj.photo=img or obj.photo
        db.session.add(obj);db.session.commit();flash(f'{kind} saved.','success');return redirect(request.path)
    return render_template(template,items=model.query.order_by(getattr(model,'sort_order',model.id),model.id).all(),edit_item=obj)

@app.route('/admin/services',methods=['GET','POST'])
@login_required
def admin_services():return crud_model(Service,'admin/services.html','Service',['title','slug','short_description','description','icon','sort_order','is_active'])
@app.route('/admin/team',methods=['GET','POST'])
@login_required
def admin_team():return crud_model(TeamMember,'admin/team.html','Team member',['name','role','department','short_bio','bio','experience','skills','achievements','email','linkedin','sort_order','is_featured','is_active'])
@app.route('/admin/reviews',methods=['GET','POST'])
@login_required
def admin_reviews():return crud_model(Review,'admin/reviews.html','Review',['client_name','company','service_used','review_text','sort_order','is_featured','is_active'])
@app.route('/admin/jobs',methods=['GET','POST'])
@login_required
def admin_jobs():return crud_model(Job,'admin/jobs.html','Job',['title','department','location','employment_type','experience','salary','description','requirements','is_active'])
@app.route('/admin/applications')
@login_required
def admin_applications():return render_template('admin/applications.html',items=JobApplication.query.order_by(JobApplication.created_at.desc()).all())
@app.route('/admin/application/<int:i>/status',methods=['POST'])
@login_required
def application_status(i): x=db.get_or_404(JobApplication,i);x.status=request.form.get('status','New');db.session.commit();return redirect(url_for('admin_applications'))
@app.route('/admin/messages')
@login_required
def admin_messages():return render_template('admin/messages.html',messages=ContactMessage.query.order_by(ContactMessage.created_at.desc()).all())
@app.route('/admin/delete/<kind>/<int:i>',methods=['POST'])
@login_required
def admin_delete(kind,i):
    m={'service':Service,'team':TeamMember,'review':Review,'job':Job}.get(kind)
    if m:
        x=db.get_or_404(m,i);db.session.delete(x);db.session.commit();flash('Deleted.','success')
    return redirect(request.referrer or url_for('admin_dashboard'))
@app.route('/admin/account',methods=['GET','POST'])
@login_required
def admin_account():
    if request.method=='POST':
        current_user.name=request.form.get('name',current_user.name); current_user.email=request.form.get('email',current_user.email).lower(); p=request.form.get('password');
        if p:current_user.set_password(p)
        db.session.commit();flash('Account updated.','success')
    return render_template('admin/account.html')

if __name__=='__main__': app.run(debug=os.getenv('FLASK_DEBUG','0')=='1')
