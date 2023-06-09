from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import DataRequired, ValidationError, Length, InputRequired
from wtforms import StringField, FileField, TextAreaField, SubmitField, IntegerField, SelectField, \
    BooleanField


class CourseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    thumbnail = FileField('Upload your thumbnail (optional)', 
                          validators=[FileAllowed(['png', 'jpg', 'jpeg'], 'Image "png, jpg, jpeg" file only!')])
    description = StringField('Description (optional)')
    submit = SubmitField('Create Course')


class EditTitleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    save_title = SubmitField('Save')


class EditDescriptionForm(FlaskForm):
    description = StringField('Description')
    save_description = SubmitField('Save')


class EditThumbnailForm(FlaskForm):
    thumbnail = FileField('Banner image')
    upload_tn = SubmitField('Upload')

    def validate_thumbnail(self, thumbnail):
        filetypes = ['png', 'jpg', 'jpeg']
        _type = thumbnail.data.filename.split('.')[-1] # filetype of file selected

        if _type: # continue if file was selected
            if _type not in filetypes: # raise error if file is not of preferred type
                raise ValidationError('Upload a png, jpeg, jpg file.')


class CreateSectionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    number = IntegerField('Section number', validators=[InputRequired()])    
    create_sect = SubmitField('Add Section')


class EditSectionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    number = IntegerField('Section number', validators=[InputRequired()])
    save_sect = SubmitField('Save')
    

class UploadFileForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    file = FileField('Upload file', validators=[FileRequired()])
    number = IntegerField('File number', validators=[InputRequired()])
    description = TextAreaField('Description (optional)')
    restrict_access = BooleanField('Restrict access')
    filetype = SelectField('File Type', choices=['video', 'audio', 'pdf'])
    upload_file = SubmitField('Upload File')


    def validate_file(self, file):
        # filetypes
        filetypes = {
            'video': ['mp4', 'avi', 'mkv'],
            'audio': ['mp3', 'wav', 'ogg'],
            'pdf': ['pdf']
        }

        selected_type = str(self.filetype.data) # filetype selected

        _type = file.data.filename.split('.')[-1] # type of file selected
        if _type not in filetypes[selected_type]: # raise error if ...
            raise ValidationError('The file you chose to upload does not \
                                  match the file type you selected.')
        
class EditFileForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    number = IntegerField('File number', validators=[InputRequired()])
    description = TextAreaField('Description')
    restrict_access = BooleanField('Restrict access')
    save_file_edit = SubmitField('Save')


class ChangeUploadForm(FlaskForm):
    filetype = SelectField('File Type', choices=['video', 'audio', 'pdf'])
    file = FileField('Upload file', validators=[FileRequired()])
    upload_file = SubmitField('Upload File')

    def validate_file(self, file):
        # filetypes
        filetypes = {
            'video': ['mp4', 'avi', 'mkv'],
            'audio': ['mp3', 'wav', 'ogg'],
            'pdf': ['pdf']
        }

        selected_type = str(self.filetype.data) # filetype selected

        _type = file.data.filename.split('.')[-1] # type of file selected
        if _type not in filetypes[selected_type]: # raise error if ...
            raise ValidationError('The file you chose to uploaded does not \
                                  match the file type you selected.')
        

class ConfirmationForm(FlaskForm):
    confirm = SubmitField('Yes')