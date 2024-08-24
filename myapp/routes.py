from flask import render_template, redirect, url_for, request
from .models import  User, check_password_hash, Locations, Checkins, Events
from .forms import RegistrationForm,LoginForm, LocationForm, CheckinForm
from . import app, db
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime

@app.route('/')
def home():
    #recipes = Recipe.query.all()
    return render_template('home.html')#, recipes = recipes)

@app.route('/checkin', methods =['GET','POST'])
@login_required 
def new_checkin():
    locations=Locations.query.all()
    form = CheckinForm()
    users = User.query.order_by(User.checkin_score.desc()).all()
    #eventstabledata=Events.get_tablejson()
    userstabledata = User.get_json()
    eventtableheaders=Events.get_tableheaders()
    eventtableheaders1=Events.get_tableheaders1()
   
    for user in users:
        user.update_scores(user.id)
    db.session.commit()
    user = current_user

    if form.validate_on_submit():
        checkin = Checkins(
            location_name = form.location_name.data,
            user_id = current_user.id
        )
        multiplier=Checkins.get_todays_events(checkin)
        print(multiplier)
        checkin.multiplier=multiplier
        db.session.add(checkin)
        db.session.commit()
        user.update_scores(user.id)
        db.session.commit()

        
        return redirect(url_for('new_checkin'))
    return render_template('checkin.html',eventtableheaders1=eventtableheaders1, form=form, eventtableheaders=eventtableheaders, userstabledata=userstabledata, users = users, locations=locations, user=current_user.username)


@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data)
        user.set_password(form.password.data)
        user.update_scores(user.id)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('new_checkin'))
    
    return render_template('register.html', title="Register", form=form)

@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('new_checkin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('new_checkin'))
    error="Invalid username or password"
    return render_template('login.html', form=form, error=error)
    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



###old routes
###@app.route('/new_recipe', methods=['GET','POST'])
###def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title = form.title.data, 
            description=form.description.data)
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('new_recipe.html', title="New Recipe", form=form)

###@app.route('/share_recipe/<int:recipe_id>', methods =['GET','POST'])
###@login_required
###def share_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    users = User.query.filter(User.id!= current_user.id).all()
    if request.method == "POST":
        selected_user_id = request.form.get('sharee')
        sharee = User.query.get(selected_user_id)
        if sharee:
            shared_recipe = SharedRecipe(recipe_id = recipe.id, sharer_id= current_user.id, sharee_id =sharee.id)
            db.session.add(shared_recipe)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('share_recipe.html', recipe=recipe, users=users)


#@app.route('/recipes/shared')
#@login_required
#def shared_recipes():
    shared = SharedRecipe.query.filter_by(sharee_id = current_user.id).all()
    return render_template('shared_recipes.html', shared=shared)



#@app.route('/admin', methods=['GET','POST'])
#def admin():
#    form = LocationForm()
#    locations=Locations.query.all()
#    users = User.query.all()
#    if form.validate_on_submit():
#        location = Locations(
#            location_name = form.location_name.data)
#        db.session.add(location)
#        db.session.commit()
#        return redirect(url_for('admin'))
#    return render_template('admin.html', title="Admin Page", users=users,form=form, locations=locations)
