import os
from . import course
from .. import app, db
from ..models import Course, File, Order
from flask_login import login_required, current_user
from flask import send_file, render_template, flash, redirect, url_for


@course.route('/file/<path:filename>')
@login_required
def file(filename: str):

    # return coursesite logo png if no thumbnail
    if 'thumbnail/no-thumbnail.png' in filename:
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnail/no-thumbnail.svg'))
    
    # return thumbnail (no special permission needed)
    if 'thumbnail' in filename.split('/')[4]:
        return send_file(filename)

    # get course link
    link = filename.split('/')[2]
    course = Course.query.filter_by(link=link).first()

    # check if current user have acess to the course
    is_creator = course in current_user.courses
    has_ordered = False

    # check if user ordered this course
    user_orders = current_user.orders
    for order in user_orders:
        if order in course.orders and order.accepted:
            has_ordered = True

    # check if file is not restricted
    unrestricted = False
    sections = course.sections
    for section in sections:
        _files = section.files
        for file in _files:
            if file.path == filename:
                if not file.restrict_access:
                    unrestricted = True

    # user have access to course
    # return requested file
    if is_creator or has_ordered or unrestricted:
        return send_file(filename)
    
    else:
        # TODO: return a file telling user to order course if user does not have access to file
        return redirect(url_for('dashboard.error_page', msg='You can`t access this file.'))


@course.route('get_file_info/<int:file_id>')
@login_required
def get_file_info(file_id: int) -> str:

    # get file from db by file id
    file = File.query.get(file_id)

    # return file path if file exist
    if file:
        return dict(filepath=file.path, filetype=file.filetype, description=file.description), 200
    
    # return error if not 
    return 'File does not exist', 404


@course.route('view/<string:link>')
@login_required
def view(link):

    # get course by link
    course = Course.query.filter_by(link=link).first()

    # check if course does not exist
    if not course:
        # return page does not exist error
        return 'This page does not exist.', 404 

    
    # check if user created course
    created_course = False
    if current_user == course.user:
        created_course = True

    # get user order info

    # check if user placed an order
    placed_order = False
    users = [order.user for order in course.orders]
    for user in users:
        if current_user == user:
            placed_order = True
            break

    # check if order has been accept
    accepted = False
    if placed_order: # check if user place order
        for order in user.orders:
            if order.course == course:
                accepted = order.accepted
    
    order_data = dict(placed_order=placed_order, accepted=accepted, place_order=place_order, 
                      created_course=created_course)
                
    return render_template('view.html', course=course, order_data=order_data)


@course.route('place_order/<string:link>')
@login_required
def place_order(link:str):

    course = Course.query.filter_by(link=link).first()

    # if link exist create order request
    if course:
        order = Order() # create instance of Order
        current_user.orders.append(order) # add order to user's orders
        course.orders.append(order) # add order to course
        db.session.commit() # save change

        flash('Order placed! Wait for order request to be accepted.')

        return redirect(url_for('course.view', link=link))
    
    return 'Invalid URL', 404