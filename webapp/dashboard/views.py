
import os, shutil, gc
from . import dashboard
from .. import app, db, app_path
from ..string_generator import string_gen
from werkzeug.utils import secure_filename
from ..models import Course, Section, File, Order
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, session, request, flash
from .forms import CourseForm, EditTitleForm, EditThumbnailForm, EditDescriptionForm, \
    CreateSectionForm, EditSectionForm, UploadFileForm, ConfirmationForm, EditFileForm, ChangeUploadForm


def random_pad_filename(filename: str) -> str:
    '''
        return a new filename with a random string attached to the filename end.
    '''

    splits = filename.split('.') 
    return'.'.join([*splits[:-1], string_gen.random_string(4, True), splits[-1]]) 


@dashboard.route('/')
@login_required
def index():
    return render_template('dashboard.html', page='index', username=current_user.username, 
                           email=current_user.email)


@dashboard.route('/subscriptions')
@login_required
def subscriptions():

    # get user subscriptions
    subscriptions = []
    orders = current_user.orders
    for order in orders:
        course = order.course
        course_dict = dict(title=course.title, link=course.link, creator=course.user.username, 
                           thumbnail=course.thumbnail)
        subscriptions.append(course_dict)

    # reverse list
    subscriptions = subscriptions[::-1]

    return render_template('subscriptions.html', page='subscriptions', courses=subscriptions)


@dashboard.route('/mycourses')
@login_required
def hosted():

    # get uploaded courses
    hosted_courses = []
    courses = current_user.courses

    # reverse list
    courses = courses[::-1]

    return render_template('mycourses.html', page='mycourses', courses=courses)


@login_required
@dashboard.route('/upload_course', methods=['GET', 'POST'])
def upload_course():

    form = CourseForm()

    if form.validate_on_submit():

        # add course to database
        course = Course()
        course.title = form.title.data
        course.description = form.description.data
        # course.details = form.details.data

        #  create and save link
        # create link that is not used
        _link = string_gen.random_string(15, alpha_numeric=True)
        while Course.query.filter_by(link=_link).first():
            _link = string_gen.random_string(15, alpha_numeric=True)

        course.link = _link # add link

        thumbnail = form.thumbnail.data

        # create save directory
        _course_dir = os.path.join(current_user.username, course.link)
        thumbnail_dir = os.path.join(app_path, app.config['UPLOAD_FOLDER'], _course_dir, 'thumbnail')
        os.makedirs(thumbnail_dir) # create directory

        # save thumbnail file if any
        if thumbnail.content_type != 'application/octet-stream':
            filename = secure_filename(thumbnail.filename)
            thumbnail_path = os.path.join(thumbnail_dir, filename)  # create thumbnail path
            
            thumbnail.save(thumbnail_path) # save thumbnail to path
            course.thumbnail = os.path.join(app.config['UPLOAD_FOLDER'], _course_dir, \
                                            'thumbnail', filename) # add filename to database

            db.session.commit()
        
        # add course to database
        current_user.courses.append(course)
        db.session.commit()

        return redirect(url_for('.edit', link=_link))

    return render_template('upload-course.html', page='uploadcourse', form=form)


@dashboard.route('/section_to_edit_id/<int:section_id>', methods=['POST'])
@login_required
def section_id_to_session(section_id):
    session['section_id'] = section_id
    return ''

@dashboard.route('/delete_section/<int:section_id>', methods=['POST'])
@login_required
def delete_section(section_id):
    session['del_section'] = section_id
    return ''

@dashboard.route('/delete_file/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    session['del_file'] = file_id
    return ''

@dashboard.route('/delete_course/<string:data>', methods=['POST'])
@login_required
def delete_course(data: str):
    session['del_course'] = data
    return ''
    

@dashboard.route('/get_file_data/<int:file_id>', methods=['GET', 'POST'])
@login_required
def file_data(file_id: int) -> dict:
    file = File.query.filter_by(id=file_id).first()
    course = file.section.course
    if file:
        session['edit_file_id'] = file_id 
        return dict(title=file.title, number=file.index, description=file.description, 
                    restrict_access=file.restrict_access, status='success', link=course.link)
    else:
        return {'status': 'failed'}, 404


@dashboard.route('/edit/<string:link>', methods=['GET', 'POST'])
@login_required
def edit(link):

    # get course of the link
    course = Course.query.filter_by(link=link).first()
    if course is None:
        return redirect(url_for('.error_page', msg='Course not found.'))

    # check if current user is the creator of course in link
    elif course in current_user.courses:

        # Forms
        forms = {
            'title_form': EditTitleForm(),
            'tn_form': EditThumbnailForm(),
            'description': EditDescriptionForm(),
            'section': CreateSectionForm(),
            'edit_sect': EditSectionForm(),
            'edit_file': EditFileForm(),
            'confirmation': ConfirmationForm()
        }

        _course_dir = os.path.join(current_user.username, course.link) # course directory

        # EDIT FORMS

        # save title edits if valid
        title_form = forms['title_form']
        if title_form.save_title.data and title_form.validate():
            course.title = title_form.title.data
            db.session.commit()            
            return redirect(url_for('.edit', link=link)) # reload without resubmission

        # save thumbnail edits if valid
        tn_form = forms['tn_form']
        if tn_form.upload_tn.data and tn_form.validate():

            thumbnail = tn_form.thumbnail.data

            # save thumbnail file if any
            if thumbnail.content_type != 'application/octet-stream':
                filename = secure_filename(thumbnail.filename)
                thumbnail_path = os.path.join(app_path, app.config['UPLOAD_FOLDER'], _course_dir, \
                                              'thumbnail', filename) # create thumbnail path
                
                thumbnail.save(thumbnail_path) # save thumbnail to path
                course.thumbnail = os.path.join(app.config['UPLOAD_FOLDER'], _course_dir, \
                                                'thumbnail', filename) # add filename to database

                db.session.commit()

            # make None if no thumbnail file was upload
            else:
                course.thumbnail = 'thumbnail/no-thumbnail.png'
                db.session.commit()  # save changes to database

        # save description edit if valid
        desc_form = forms['description']
        if desc_form.save_description.data and desc_form.validate():
            course.description = desc_form.description.data
            db.session.commit()

        # save section edits if valid
        sect_form = forms['edit_sect']
        if sect_form.save_sect.data and sect_form.validate():
            # get section to edit
            section_to_edit = Section.query.filter_by(id=session.get('section_id')).first()
            section_to_edit.title = sect_form.title.data
            section_to_edit.index = sect_form.number.data
            db.session.commit()


        # save section edits if valid
        file_form = forms['edit_file']
        if file_form.save_file_edit.data and file_form.validate():

            file_id = session.get('edit_file_id')
            if file_id: # check if session has id of file to edit
                
                file = File.query.filter_by(id=file_id).first() # get file to edit

                # save edits to database
                file.title = file_form.title.data
                file.index = file_form.number.data
                file.description = file_form.description.data
                file.restrict_access = file_form.restrict_access.data
                db.session.commit()

                del file_id, file # delete varibles


        # save detail edits
        if request.method == 'POST':
            data = request.form.get('ckeditor')
            if data:
                course.details = data
                db.session.commit()
        

        # Create Section
        sect_form = forms['section']
        if sect_form.create_sect.data and sect_form.validate():
            # create instance of section model
            section = Section(title=sect_form.title.data,
                              index=sect_form.number.data)
            course.sections.append(section)
            db.session.commit()

            return redirect(url_for('.edit', link=link)) # reload to prevent resubmission
        
        # DELETE
        
        # delete section
        if session.get('del_section'):
            delete_sec = forms['confirmation']
            if delete_sec.confirm.data and delete_sec.validate():

                section_id = session.get('del_section') # get id of section to delete
                section = Section.query.filter_by(id=section_id).first()

                # delete section folder
                dir_path = os.path.join(app_path, app.config['UPLOAD_FOLDER'], _course_dir, \
                                   str(section_id)) # create file dir
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path)

                # delete from db
                db.session.delete(section)
                db.session.commit()

                session['del_section'] = None # clear session

                return redirect(url_for('.edit', link=link)) # reload to prevent resubmission

        # delete file
        if session.get('del_file'):
            delete_file = forms['confirmation']
            if delete_file.confirm.data and delete_file.validate():

                file_id = session.get('del_file') # get id of file to delete
                file = File.query.filter_by(id=file_id).first()

                # delete file
                file_path = os.path.join(app_path, file.path)
                if os.path.exists(file_path):
                    os.remove(file_path)

                # delete from db
                db.session.delete(file)
                db.session.commit()

                session['del_file'] = None # clear session

                return redirect(url_for('.edit', link=link)) # reload to prevent resubmission
            
        # delete course
        if session.get('del_course'):
            delete_course = forms['confirmation']
            if delete_course.confirm.data and delete_course.validate():

                # delete course folder
                course_path = os.path.join(app_path, app.config['UPLOAD_FOLDER'], course.user.username, link)
                print(course_path)
                if os.path.exists(course_path):
                    shutil.rmtree(course_path)

                # delete from db
                db.session.delete(course)
                db.session.commit()

                session['del_course'] = None # clear session

                return redirect(url_for('.hosted')) # take user to my course list


        # get sections and order sections by index
        sections = course.sections
        sections = sorted(sections, key=lambda x: x.index)

        return render_template('edit.html', page='edit', course=course, forms=forms, sections=sections)

    return redirect(url_for('.error_page', msg='You can`t edit this course!'))


@dashboard.route('upload_file/<string:link>/<int:section_id>', methods = ['GET', 'POST'])
@login_required
def upload_file(link, section_id):

    course = Course.query.filter_by(link=link).first() # course db entry
    _course_dir = os.path.join(current_user.username, course.link) # course directory

    form = UploadFileForm()

    if course is None:
        return redirect(url_for('.error_page', msg='Course not found.'))


    # check if current user is the creator of course in link
    elif course in current_user.courses:

        if form.validate_on_submit():

            # upload file
            file = form.file.data # get uploaded file
            filename = file.filename # get filename
            file_dir = os.path.join(app_path, app.config['UPLOAD_FOLDER'], _course_dir, str(section_id)) # file dir
            os.makedirs(file_dir, exist_ok=True) # create dir if it exist
            
            file_path = os.path.join(file_dir, secure_filename(filename)) # file path

            # check if filename is already used
            if os.path.exists(file_path):
                # create new filename to save file with
                while os.path.exists(file_path): # create new filenames till unique one is found
                    filename = random_pad_filename(file.filename) # change filename varible to padded filename 
                    file_path = os.path.join(file_dir, secure_filename(filename))

            file.save(file_path) # save file to path
            
            # create file entry
            file_entry = File(title=form.title.data, filetype=form.filetype.data, \
                index = form.number.data, description = form.description.data, \
                    restrict_access=form.restrict_access.data)
            
            # add path to file entry
            file_entry.path = os.path.join(app.config['UPLOAD_FOLDER'], _course_dir, str(section_id), secure_filename(filename))

            # add file entry to database
            upload_to_section = Section.query.filter_by(id=section_id).first()

            # if section does not exist show error msg
            if not upload_to_section:
                return redirect(url_for('.error_page', msg='Invaild request.'))
            
            upload_to_section.files.append(file_entry)
            db.session.commit()

            flash('File Uploaded!') # send message to user if file was saved

        return render_template('upload-file.html', course=course, section_id=section_id, form=form)
    
    else:
        return redirect(url_for('.error_page', msg='You can`t edit this course.'))


@dashboard.route('change_upload/<string:link>/<int:file_id>', methods = ['GET', 'POST'])
@login_required
def change_upload(link: str, file_id: int):

    course = Course.query.filter_by(link=link).first() # get course form database
    _course_dir = os.path.join(current_user.username, course.link) # course directory

    if course:

        # check if current user owns course
        if course in current_user.courses:
            
            file = File.query.filter_by(id=file_id).first() # get file form database
            section_id = file.section.id # get section id

            if file:
                form = ChangeUploadForm()
                if form.validate_on_submit():

                    # upload file
                    form_file_data = form.file.data # get uploaded file
                    filename = form_file_data.filename # get filename
                    file_dir = os.path.join(app_path, app.config['UPLOAD_FOLDER'], _course_dir, str(section_id)) # file dir
                    
                    file_path = os.path.join(file_dir, secure_filename(filename)) # file path

                    # check if filename is already used
                    if os.path.exists(file_path):
                        # create new filename to save file with
                        while os.path.exists(file_path): # create new filenames till unique one is found
                            filename = random_pad_filename(form_file_data.filename) # change filename varible to padded filename 
                            file_path = os.path.join(file_dir, secure_filename(filename))

                    form_file_data.save(file_path) # save file to path

                    # save changes to database
                    file.path = os.path.join(app.config['UPLOAD_FOLDER'], _course_dir, str(section_id), 
                                            secure_filename(filename))
                    file.filetype = form.filetype.data
                    db.session.commit()

                    flash('File Uploaded!')
                    return render_template('change-upload.html', course=course, form=form, file_id=file_id)

                return render_template('change-upload.html', course=course, form=form, file_id=file_id)

            else: 
                return redirect(url_for('.error_page', msg='File not found.'))
            
        else:
            return redirect(url_for('.error_page', msg='You can`t edit this course.'))

    else:
        return redirect(url_for('.error_page', msg='Course not found.'))




@dashboard.route('orders/<string:link>', methods=['GET', 'POST'])
@login_required
def orders(link:str):
    
    course = Course.query.filter_by(link=link).first()

    # restrict access to only creator of this course
    if course in current_user.courses:
        orders = course.orders
        return render_template('orders.html', orders=orders, title=course.title)
    
    return redirect(url_for('.error_page', msg='You don`t have access to course`s orders.'))



@dashboard.route('accept_order/<int:order_id>')
@login_required
def accept_order(order_id: int):

    order = Order.query.filter_by(id=order_id).first()
    if order:
        # check if current user can accept this course order
        if order.course in current_user.courses:
            # accept order and save to database
            order.accepted = True
            db.session.commit()
            return redirect(url_for('dashboard.orders', link=order.course.link))
        
        else:
            return redirect(url_for('.error_page', msg='You don`t have access to accept/decline order.'))

    return redirect(url_for('.error_page', msg='Order does not exist.'))


@dashboard.route('decline_order/<int:order_id>')
@login_required
def decline_order(order_id: int):

    order = Order.query.filter_by(id=order_id).first()
    if order:
        # check if current user can accept this course order
        if order.course in current_user.courses:
            # accept order and save to database
            order.accepted = False
            db.session.commit()
            return redirect(url_for('dashboard.orders', link=order.course.link))
        
        else:
            return redirect(url_for('.error_page', msg='You don`t have access to accept/decline order.'))

    return redirect(url_for('.error_page', msg='Order not found.'))


@dashboard.route('error_page/<string:msg>')
def error_page(msg: str):

    return render_template('error_page.html', msg=msg)